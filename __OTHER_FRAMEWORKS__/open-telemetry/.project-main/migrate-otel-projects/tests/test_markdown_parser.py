"""Tests for the markdown parser."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_parser import ProjectMarkdownParser


def test_browser_project():
    """Test parsing the browser-phase-1.md project."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/browser-phase-1.md"
    
    if not project_path.exists():
        print(f"Warning: {project_path} not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    
    # Test project name extraction
    project_name = parser.get_project_name()
    print(f"Project Name: {project_name}")
    assert project_name == "Browser Instrumentation (Phase 1) Proposal"
    
    # Test section extraction
    timeline_content = parser.get_section_content("Timeline")
    print(f"\nTimeline Section Found: {bool(timeline_content)}")
    
    # Test labels extraction
    labels = parser.extract_labels()
    print(f"\nLabels: {labels}")
    assert 'spec-browser' in labels
    
    # Test project board extraction
    board_link = parser.extract_project_board_link()
    print(f"\nProject Board: {board_link}")
    assert board_link == "https://github.com/orgs/open-telemetry/projects/146"
    
    # Test status determination
    status = parser.get_directory_status()
    print(f"\nStatus: {status}")
    assert status == "Active"
    
    # Test staffing section
    staffing_section = parser.get_section("Staffing / Help Wanted")
    if staffing_section:
        print(f"\nStaffing Section Found: Yes")
        # Look for subsections
        required_staffing = staffing_section.get_subsection("Required Staffing")
        if required_staffing:
            print("Required Staffing Subsection: Found")


def test_gen_ai_project():
    """Test parsing the gen-ai.md project."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/gen-ai.md"
    
    if not project_path.exists():
        print(f"Warning: {project_path} not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    
    # Test project name
    project_name = parser.get_project_name()
    print(f"\n\nGen AI Project Name: {project_name}")
    
    # Test timeline with specific dates
    timeline_content = parser.get_section_content("Timeline")
    if timeline_content:
        print(f"\nTimeline Content Preview:\n{timeline_content[:200]}...")
    
    # Test labels
    labels = parser.extract_labels()
    print(f"\nLabels: {labels}")


if __name__ == "__main__":
    test_browser_project()
    test_gen_ai_project()