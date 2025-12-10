"""Pydantic models for project data."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import date, datetime
from enum import Enum


class ProjectStatus(str, Enum):
    """Valid project statuses."""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"


class SponsorshipLevel(str, Enum):
    """Valid sponsorship levels."""
    LEADING = "Leading"
    GUIDING = "Guiding"
    ESCALATING = "Escalating"
    NONE = "None"  # For projects without sponsors
    NEEDREVIEW = "NeedReview"  # When we can't determine the level


class TimelineMilestone(BaseModel):
    """Represents a project milestone with date."""
    date: date
    description: str


class ProjectData(BaseModel):
    """Represents extracted project data ready for GitHub."""
    
    # Required fields
    project_name: str = Field(..., min_length=1, description="Project name from H1 header")
    markdown_url: str = Field(..., description="GitHub URL to the markdown file")
    status: ProjectStatus = Field(..., description="Project status based on directory")
    
    # Optional fields
    labels: List[str] = Field(default_factory=list, description="Labels for the issue")
    project_board_url: Optional[str] = Field(None, description="URL to project's own board")
    
    # Date fields
    start_date: Optional[date] = Field(None, description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end/target date")
    timeline_confidence: str = Field("low", description="Confidence in extracted dates")
    
    # Git history fields
    git_start_date: Optional[datetime] = Field(None, description="When file was added to git")
    git_end_date: Optional[datetime] = Field(None, description="When file was moved to completed/inactive")
    timeline_milestones: List[TimelineMilestone] = Field(default_factory=list, description="Project milestones")
    timeline_reasoning: Optional[str] = Field(None, description="Reasoning for timeline extraction")
    
    # Staffing fields
    project_lead: Optional[str] = Field(None, description="Project lead name and affiliation")
    gc_sponsors: List[str] = Field(default_factory=list, description="GC sponsors/liaisons")
    tc_sponsors: List[str] = Field(default_factory=list, description="TC sponsors")
    sponsorship_level: SponsorshipLevel = Field(SponsorshipLevel.NONE, description="Sponsorship level")
    
    # Additional fields
    deliverables_summary: Optional[str] = Field(None, description="Brief summary of deliverables")
    meeting_info: Optional[str] = Field(None, description="Meeting schedule info")
    
    # Extraction metadata
    extraction_warnings: List[str] = Field(default_factory=list, description="Warnings during extraction")
    needs_manual_review: bool = Field(False, description="Flag for manual review needed")
    
    @field_validator('start_date', 'end_date', mode='before')
    def parse_dates(cls, v):
        """Parse date strings to date objects."""
        if v is None or v == "":
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            from dateutil import parser
            try:
                return parser.parse(v).date()
            except:
                return None
        return None
    
    @field_validator('git_start_date', 'git_end_date', mode='before')
    def parse_datetimes(cls, v):
        """Parse datetime objects."""
        if v is None or v == "":
            return None
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            from dateutil import parser
            try:
                return parser.parse(v)
            except:
                return None
        return None
    
    @field_validator('sponsorship_level', mode='before')
    def validate_sponsorship_level(cls, v):
        """Convert old sponsorship levels to valid ones."""
        if v is None:
            return SponsorshipLevel.NONE
        
        # Map old values to new ones
        old_to_new = {
            "Community": SponsorshipLevel.NONE,
            "Technical": SponsorshipLevel.GUIDING,
            "Governance": SponsorshipLevel.ESCALATING,
            "Full": SponsorshipLevel.LEADING,
        }
        
        if isinstance(v, str):
            # Check if it's already a valid value
            if v in [level.value for level in SponsorshipLevel]:
                return v
            # Convert old values
            if v in old_to_new:
                return old_to_new[v]
            # Unknown value
            return SponsorshipLevel.NEEDREVIEW
            
        return v
    
    def to_github_issue(self) -> dict:
        """Convert to format for GitHub issue creation."""
        # Build issue body in consistent format
        body_lines = [
            f"# {self.project_name}",
            "",
            "## Deliverables",
        ]
        
        if self.deliverables_summary:
            body_lines.append(self.deliverables_summary)
        else:
            body_lines.append("*No deliverables summary available - see project file for details*")
        
        body_lines.extend([
            "",
            "## Links",
            f"- **Project File**: {self.markdown_url}",
            f"- **Project Board**: {self.project_board_url or 'None specified'}",
        ])
        
        # Add validation/review section if there are warnings
        if self.extraction_warnings or self.needs_manual_review:
            body_lines.extend([
                "",
                "## ⚠️ Manual Review Required",
                "",
                "The following items need manual verification:",
            ])
            
            # Add specific warnings
            for warning in self.extraction_warnings:
                body_lines.append(f"- {warning}")
            
            # Add field-specific validations
            if self.sponsorship_level in [SponsorshipLevel.NEEDREVIEW, SponsorshipLevel.NONE]:
                body_lines.append("- Sponsorship level could not be determined from project file")
            
            if not self.project_lead and not self.gc_sponsors and not self.tc_sponsors:
                body_lines.append("- No project sponsors identified")
            
            if self.timeline_confidence == "low":
                body_lines.append("- Timeline dates are uncertain and should be verified")
            
            if not self.project_board_url:
                body_lines.append("- No project board URL found in markdown file")
            
            body_lines.extend([
                "",
                "Please review the project file and update this issue with the correct information."
            ])
        
        return {
            "title": self.project_name,
            "body": "\n".join(body_lines),
            "labels": self.labels
        }
    
    def to_project_fields(self) -> dict:
        """Convert to format for GitHub project board fields."""
        # Map our status values to project board values
        status_mapping = {
            ProjectStatus.ACTIVE: "In Progress",
            ProjectStatus.IN_PROGRESS: "In Progress",
            ProjectStatus.INACTIVE: "Backlog",
            ProjectStatus.COMPLETED: "Complete"
        }
        
        fields = {
            "Status": status_mapping.get(self.status, "Backlog"),
            "Sponsorship Level": self.sponsorship_level.value,
        }
        
        if self.gc_sponsors:
            fields["GC Sponsor"] = ", ".join(self.gc_sponsors)
        
        if self.tc_sponsors:
            fields["TC Sponsors"] = ", ".join(self.tc_sponsors)
        
        if self.start_date:
            fields["Start Date"] = self.start_date.isoformat()
        
        if self.end_date:
            fields["Estimate Target Date"] = self.end_date.isoformat()
        
        # Add new fields for project file and board
        fields["Project File"] = self.markdown_url
        
        if self.project_board_url:
            fields["Project Board"] = self.project_board_url
        
        return fields


class MigrationResult(BaseModel):
    """Result of attempting to migrate a project."""
    
    project_file: str = Field(..., description="Path to the project markdown file")
    success: bool = Field(..., description="Whether migration succeeded")
    project_data: Optional[ProjectData] = Field(None, description="Extracted project data")
    issue_url: Optional[str] = Field(None, description="Created issue URL")
    error: Optional[str] = Field(None, description="Error message if failed")
    dry_run: bool = Field(True, description="Whether this was a dry run")