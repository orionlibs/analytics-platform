"""Markdown parser for OpenTelemetry project files."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MarkdownSection:
    """Represents a section in a markdown document."""
    
    def __init__(self, title: str, level: int, content: str):
        self.title = title
        self.level = level
        self.content = content
        self.subsections: List[MarkdownSection] = []
    
    def add_subsection(self, section: 'MarkdownSection'):
        """Add a subsection to this section."""
        self.subsections.append(section)
    
    def get_subsection(self, title: str) -> Optional['MarkdownSection']:
        """Get a subsection by title (case-insensitive)."""
        for subsection in self.subsections:
            if subsection.title.lower() == title.lower():
                return subsection
        return None
    
    def get_full_content(self) -> str:
        """Get the full content including subsections."""
        content = self.content
        for subsection in self.subsections:
            content += f"\n\n{'#' * (subsection.level)} {subsection.title}\n\n"
            content += subsection.get_full_content()
        return content


class ProjectMarkdownParser:
    """Parser for OpenTelemetry project markdown files."""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = file_path.read_text(encoding='utf-8')
        self.sections: Dict[str, MarkdownSection] = {}
        self._parse()
    
    def _parse(self):
        """Parse the markdown content into sections."""
        lines = self.content.split('\n')
        current_section = None
        current_content = []
        section_stack: List[MarkdownSection] = []
        
        for line in lines:
            # Check if this is a header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            
            if header_match:
                # Save the previous section's content
                if current_section:
                    current_section.content = '\n'.join(current_content).strip()
                    current_content = []
                
                # Create new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                new_section = MarkdownSection(title, level, '')
                
                # Find the parent section
                while section_stack and section_stack[-1].level >= level:
                    section_stack.pop()
                
                if section_stack:
                    # This is a subsection
                    section_stack[-1].add_subsection(new_section)
                else:
                    # This is a top-level section
                    self.sections[title] = new_section
                
                section_stack.append(new_section)
                current_section = new_section
            else:
                # Regular content line
                current_content.append(line)
        
        # Save the last section's content
        if current_section:
            current_section.content = '\n'.join(current_content).strip()
    
    def get_project_name(self) -> Optional[str]:
        """Extract the project name from the first H1 header."""
        for line in self.content.split('\n'):
            match = re.match(r'^#\s+(.+)$', line)
            if match:
                return match.group(1).strip()
        return None
    
    def get_section(self, title: str) -> Optional[MarkdownSection]:
        """Get a section by title (case-insensitive)."""
        # First check top-level sections
        for section_title, section in self.sections.items():
            if section_title.lower() == title.lower():
                return section
        
        # Then check subsections recursively
        def search_subsections(parent: MarkdownSection) -> Optional[MarkdownSection]:
            for subsection in parent.subsections:
                if subsection.title.lower() == title.lower():
                    return subsection
                # Recursive search
                result = search_subsections(subsection)
                if result:
                    return result
            return None
        
        for section in self.sections.values():
            result = search_subsections(section)
            if result:
                return result
        
        return None
    
    def get_section_content(self, title: str) -> Optional[str]:
        """Get the content of a section by title."""
        section = self.get_section(title)
        return section.get_full_content() if section else None
    
    def extract_labels(self) -> List[str]:
        """Extract labels from the Labels section."""
        labels = []
        labels_section = self.get_section("Labels")
        
        if labels_section:
            # Look for bullet points or inline code blocks
            content = labels_section.content
            
            # Match labels in bullet points (- `label`)
            bullet_matches = re.findall(r'^\s*[-*]\s*`([^`]+)`', content, re.MULTILINE)
            labels.extend(bullet_matches)
            
            # Match standalone labels in backticks (including on same line as section header)
            backtick_matches = re.findall(r'`([^`]+)`', content)
            labels.extend(backtick_matches)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_labels = []
            for label in labels:
                if label not in seen:
                    seen.add(label)
                    unique_labels.append(label)
            labels = unique_labels
        
        return labels
    
    def extract_project_board_link(self) -> Optional[str]:
        """Extract the GitHub project board link."""
        project_section = self.get_section("GitHub Project") or self.get_section("Project Board")
        
        if project_section:
            # Look for GitHub project URLs
            match = re.search(r'https://github\.com/orgs/open-telemetry/projects/\d+', 
                            project_section.get_full_content())
            if match:
                return match.group(0)
        
        return None
    
    def get_directory_status(self) -> str:
        """Determine project status based on directory location."""
        path_str = str(self.file_path)
        
        if 'completed-projects' in path_str:
            return 'Completed'
        elif 'currently-inactive' in path_str:
            return 'Inactive'
        else:
            return 'Active'