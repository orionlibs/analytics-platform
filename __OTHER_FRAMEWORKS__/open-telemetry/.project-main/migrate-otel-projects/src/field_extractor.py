"""Field extraction combining regex patterns and LLM fallback."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dateutil import parser as date_parser

from .markdown_parser import ProjectMarkdownParser
from .llm_extractor import LLMExtractor
from .git_history import GitHistoryExtractor
from .models import ProjectData, ProjectStatus, SponsorshipLevel, TimelineMilestone


class FieldExtractor:
    """Extract all fields needed for GitHub issues and project board."""
    
    def __init__(self, parser: ProjectMarkdownParser, use_llm: bool = True, repo_path: Optional[Path] = None):
        """Initialize with a markdown parser instance."""
        self.parser = parser
        self.llm = LLMExtractor() if use_llm else None
        self.git = GitHistoryExtractor(repo_path or Path.cwd()) if repo_path else None
    
    def extract_all_fields(self) -> Dict[str, Any]:
        """Extract all fields from the project markdown."""
        # Extract basic labels from markdown
        labels = self.parser.extract_labels()
        
        # Add area labels based on content
        area_labels = self._determine_area_labels()
        labels.extend(area_labels)
        
        # Add manual review label if needed
        if self.parser.get_directory_status() == ProjectStatus.ACTIVE:
            # We'll add this later based on extraction warnings
            pass
        
        fields = {
            "project_name": self.parser.get_project_name(),
            "markdown_url": self._get_github_url(),
            "labels": list(set(labels)),  # Remove duplicates
            "status": self.parser.get_directory_status(),
            "project_board_url": self.parser.extract_project_board_link(),
        }
        
        # Extract git history first
        git_dates = self._extract_git_history()
        fields.update(git_dates)
        
        # Extract timeline dates with git context
        timeline_data = self._extract_timeline_dates(git_dates)
        fields.update(timeline_data)
        
        # Extract staffing information
        staffing_data = self._extract_staffing()
        fields.update(staffing_data)
        
        # Extract deliverables summary if LLM is available
        if self.llm:
            deliverables_section = self.parser.get_section("Deliverables")
            if deliverables_section:
                fields["deliverables_summary"] = self.llm.extract_deliverables_summary(
                    deliverables_section.get_full_content()
                )
        
        # Extract meeting info
        fields["meeting_info"] = self._extract_meeting_info()
        
        return fields
    
    def extract_to_model(self) -> ProjectData:
        """Extract fields and return as validated ProjectData model."""
        fields = self.extract_all_fields()
        
        # Track extraction warnings
        warnings = []
        
        # Check for missing critical fields
        if not fields.get("project_name"):
            warnings.append("No project name found")
            fields["project_name"] = self.parser.file_path.stem  # Use filename as fallback
        
        if not fields.get("project_lead") and not fields.get("gc_sponsors") and not fields.get("tc_sponsors"):
            warnings.append("No project sponsors found")
        
        if fields.get("timeline_confidence") == "low":
            warnings.append("Timeline dates are uncertain")
        
        # Check sponsorship level
        sponsorship_level = fields.get("sponsorship_level")
        if sponsorship_level == "NeedReview":
            warnings.append("Sponsorship level could not be determined")
        elif sponsorship_level in ["None", "Escalating", "Guiding", "Leading"]:
            warnings.append("Sponsorship level requires manual verification")
        
        # Add warnings to fields
        fields["extraction_warnings"] = warnings
        fields["needs_manual_review"] = len(warnings) > 0
        
        # Add needs-manual-review label if necessary
        if fields["needs_manual_review"] and "needs-manual-review" not in fields["labels"]:
            fields["labels"].append("needs-manual-review")
        
        # Create and return the model
        return ProjectData(**fields)
    
    def _get_github_url(self) -> str:
        """Construct the GitHub URL for this markdown file."""
        # Find the community directory in the path
        path_parts = self.parser.file_path.parts
        
        # Find where 'community' appears in the path
        try:
            community_idx = path_parts.index('community')
            # Get everything after 'community'
            relative_parts = path_parts[community_idx + 1:]
            relative_path = '/'.join(relative_parts)
            return f"https://github.com/open-telemetry/community/blob/main/{relative_path}"
        except ValueError:
            # Fallback if 'community' not in path
            return f"https://github.com/open-telemetry/community/blob/main/{self.parser.file_path.name}"
    
    def _extract_git_history(self) -> Dict[str, Any]:
        """Extract git history dates for the project file."""
        if not self.git:
            return {"git_start_date": None, "git_end_date": None}
        
        git_summary = self.git.get_file_history_summary(self.parser.file_path)
        
        # Determine git end date based on directory moves
        git_end_date = None
        if git_summary.get('moved_to_completed'):
            git_end_date = git_summary['moved_to_completed']
        elif git_summary.get('moved_to_inactive'):
            git_end_date = git_summary['moved_to_inactive']
        
        return {
            "git_start_date": git_summary.get('created'),
            "git_end_date": git_end_date
        }
    
    def _extract_timeline_dates(self, git_dates: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Extract start and end dates from timeline section."""
        result = {
            "start_date": None, 
            "end_date": None, 
            "timeline_confidence": "low",
            "timeline_milestones": [],
            "timeline_reasoning": None
        }
        
        # Use comprehensive LLM extraction if available
        if self.llm:
            llm_timeline = self.llm.extract_project_timeline(
                self.parser.content,  # Pass full markdown
                git_dates
            )
            
            # Convert milestones to model objects
            milestones = []
            for m in llm_timeline.get("milestones", []):
                if isinstance(m, dict) and m.get("date") and m.get("description"):
                    try:
                        # Handle empty date strings
                        if m["date"] and m["date"].strip():
                            from dateutil import parser
                            milestone_date = parser.parse(m["date"]).date()
                            milestones.append(TimelineMilestone(
                                date=milestone_date,
                                description=m["description"]
                            ))
                    except Exception as e:
                        pass
            
            result.update({
                "start_date": llm_timeline.get("start_date"),
                "end_date": llm_timeline.get("end_date"),
                "timeline_confidence": llm_timeline.get("confidence", "low"),
                "timeline_milestones": milestones,
                "timeline_reasoning": llm_timeline.get("reasoning")
            })
        
        # Fall back to regex extraction if no LLM or LLM failed
        if not result["start_date"] or not result["end_date"]:
            timeline_section = self.parser.get_section("Timeline")
            if timeline_section:
                regex_dates = self._extract_dates_with_regex(timeline_section.get_full_content())
                if not result["start_date"]:
                    result["start_date"] = regex_dates.get("start_date")
                if not result["end_date"]:
                    result["end_date"] = regex_dates.get("end_date")
                if regex_dates.get("timeline_confidence") == "high":
                    result["timeline_confidence"] = "medium"
        
        # Apply business rules based on git history and project status
        result = self._apply_timeline_rules(result, git_dates)
        
        return result
    
    def _apply_timeline_rules(self, timeline: Dict[str, Any], git_dates: Dict[str, Any]) -> Dict[str, Any]:
        """Apply business rules for timeline based on git history and project status."""
        # Rule 1: Always use git history for start date if available
        if git_dates.get("git_start_date") and not timeline.get("start_date"):
            timeline["start_date"] = git_dates["git_start_date"].strftime("%Y-%m-%d")
            if not timeline.get("timeline_reasoning"):
                timeline["timeline_reasoning"] = "Start date derived from git history"
        
        # Rule 2: For completed/inactive projects, use git move date as end date
        status = self.parser.get_directory_status()
        if status in [ProjectStatus.COMPLETED, ProjectStatus.INACTIVE]:
            if git_dates.get("git_end_date"):
                timeline["end_date"] = git_dates["git_end_date"].strftime("%Y-%m-%d")
                timeline["timeline_confidence"] = "high"
                if not timeline.get("timeline_reasoning"):
                    timeline["timeline_reasoning"] = f"End date derived from when project was moved to {status.value.lower()} status"
        
        # Rule 3: For active projects without end date, default to Dec 31, 2025
        if status == ProjectStatus.ACTIVE and not timeline.get("end_date"):
            timeline["end_date"] = "2025-12-31"
            timeline["timeline_confidence"] = "low"
            if not timeline.get("timeline_reasoning"):
                timeline["timeline_reasoning"] = "End date defaulted to 2025-12-31 for active project without clear timeline"
        
        return timeline
    
    def _determine_area_labels(self) -> List[str]:
        """Determine area labels based on project content."""
        area_labels = []
        content_lower = self.parser.content.lower()
        title_lower = self.parser.get_project_name().lower() if self.parser.get_project_name() else ""
        
        # Check for semantic conventions
        if "semantic convention" in content_lower or "semconv" in content_lower:
            area_labels.append("area:semantic-conventions")
        
        # Check for specification
        if "specification" in content_lower or "spec:" in content_lower:
            area_labels.append("area:specification")
        
        # Check for collector
        if "collector" in content_lower and "collector" in title_lower:
            area_labels.append("area:collector")
        
        # Check for SDK/instrumentation
        if "sdk" in content_lower or "instrumentation" in content_lower:
            area_labels.append("area:instrumentation")
        
        # Check for documentation
        if "documentation" in content_lower or "docs" in title_lower:
            area_labels.append("area:documentation")
        
        # Check for CI/CD
        if "ci/cd" in content_lower or "ci-cd" in content_lower:
            area_labels.append("area:ci-cd")
        
        # Check for security
        if "security" in content_lower:
            area_labels.append("area:security")
        
        # Check for configuration
        if "configuration" in content_lower or "config" in title_lower:
            area_labels.append("area:configuration")
        
        return area_labels
    
    def _extract_dates_with_regex(self, text: str) -> Dict[str, Optional[str]]:
        """Extract dates using regex patterns."""
        dates = {"start_date": None, "end_date": None, "timeline_confidence": "medium"}
        
        # Patterns to match various date formats
        date_patterns = [
            r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
            r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4})\b',  # Month Year
            r'\b((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})\b',
            r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b',  # Month DD, YYYY
        ]
        
        found_dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    parsed_date = date_parser.parse(match)
                    found_dates.append(parsed_date)
                except:
                    pass
        
        if found_dates:
            found_dates.sort()
            dates["start_date"] = found_dates[0].strftime("%Y-%m-%d")
            if len(found_dates) > 1:
                dates["end_date"] = found_dates[-1].strftime("%Y-%m-%d")
            dates["timeline_confidence"] = "high"
        
        return dates
    
    def _extract_staffing(self) -> Dict[str, Any]:
        """Extract staffing information."""
        staffing_section = self.parser.get_section("Staffing / Help Wanted")
        if not staffing_section:
            return {
                "gc_sponsors": [],
                "tc_sponsors": [],
                "project_lead": None,
                "sponsorship_level": "Community"
            }
        
        content = staffing_section.get_full_content()
        
        # Try regex extraction first
        sponsors = self._extract_sponsors_with_regex(content)
        
        # Use LLM if available for better extraction
        if self.llm:
            llm_sponsors = self.llm.extract_sponsors(content)
            # Merge results
            if not sponsors["gc_sponsors"] and llm_sponsors.get("gc_sponsors"):
                sponsors["gc_sponsors"] = llm_sponsors["gc_sponsors"]
            if not sponsors["tc_sponsors"] and llm_sponsors.get("tc_sponsors"):
                sponsors["tc_sponsors"] = llm_sponsors["tc_sponsors"]
            if not sponsors["project_lead"] and llm_sponsors.get("project_lead"):
                sponsors["project_lead"] = llm_sponsors["project_lead"]
        
        # Determine sponsorship level
        if self.llm:
            sponsors["sponsorship_level"] = self.llm.determine_sponsorship_level(
                sponsors, self.parser.content
            )
        else:
            sponsors["sponsorship_level"] = self._simple_sponsorship_level(sponsors)
        
        return sponsors
    
    def _extract_sponsors_with_regex(self, text: str) -> Dict[str, List[str]]:
        """Extract sponsors using regex patterns."""
        result = {"gc_sponsors": [], "tc_sponsors": [], "project_lead": None}
        
        # Project lead patterns
        lead_match = re.search(r'\*\*Project Lead[:\s]*\*\*\s*([^(\n]+)(?:\(([^)]+)\))?', text)
        if lead_match:
            name = lead_match.group(1).strip()
            company = lead_match.group(2)
            if company:
                result["project_lead"] = f"{name} ({company})"
            else:
                result["project_lead"] = name
        
        # GC sponsor patterns
        gc_patterns = [
            r'\*\*GC (?:Liaison|Sponsor)[:\s]*\*\*\s*([^(\n]+)(?:\(([^)]+)\))?',
            r'GC (?:Liaison|Sponsor):\s*([^(\n]+)(?:\(([^)]+)\))?'
        ]
        for pattern in gc_patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                company = match.group(2)
                sponsor = f"{name} ({company})" if company else name
                result["gc_sponsors"].append(sponsor)
                break
        
        # TC sponsor patterns
        tc_section = re.search(r'\*\*(?:TC )?Sponsor[s]?[:\s]*\*\*(.*?)(?=\*\*|\n\n|$)', text, re.DOTALL)
        if tc_section:
            # Extract individual sponsors from bullet points
            sponsor_text = tc_section.group(1)
            sponsor_lines = re.findall(r'^\s*[-*]\s*(.+)$', sponsor_text, re.MULTILINE)
            for line in sponsor_lines:
                # Clean up the line and extract name/company
                clean_line = re.sub(r'[@\-–—]', '', line).strip()
                if clean_line and not clean_line.lower().startswith(('spec', 'tc ', 'maintainer')):
                    result["tc_sponsors"].append(clean_line)
        
        return result
    
    def _simple_sponsorship_level(self, sponsors: Dict[str, List[str]]) -> str:
        """Simple heuristic for sponsorship level without LLM."""
        has_gc = len(sponsors.get("gc_sponsors", [])) > 0
        has_tc = len(sponsors.get("tc_sponsors", [])) > 0
        
        if has_tc and has_gc:
            return "Leading"
        elif has_tc:
            return "Guiding"
        elif has_gc:
            return "Escalating"
        else:
            return "None"
    
    def _extract_meeting_info(self) -> Optional[str]:
        """Extract meeting schedule information."""
        meeting_section = self.parser.get_section("SIG Meetings and Other Info")
        if not meeting_section:
            return None
        
        content = meeting_section.content
        
        # Look for meeting time patterns
        time_pattern = r'(?:meeting|meets?).*?(?:weekly|biweekly|monthly|every).*?(?:\d{1,2}:\d{2}|morning|afternoon)'
        match = re.search(time_pattern, content, re.IGNORECASE)
        
        if match:
            return match.group(0)
        
        # Fallback: return first non-empty line
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        return lines[0] if lines else None