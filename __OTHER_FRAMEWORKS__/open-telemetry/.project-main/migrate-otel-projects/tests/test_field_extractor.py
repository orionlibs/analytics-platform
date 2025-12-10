"""Tests for the field extractor."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_parser import ProjectMarkdownParser
from src.field_extractor import FieldExtractor
import json


def test_browser_project_extraction():
    """Test extracting all fields from browser-phase-1.md."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/browser-phase-1.md"
    
    if not project_path.exists():
        print(f"Warning: {project_path} not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    # Test without LLM first
    extractor = FieldExtractor(parser, use_llm=False)
    fields = extractor.extract_all_fields()
    
    print("Browser Project Fields (without LLM):")
    print(json.dumps(fields, indent=2))
    
    # Verify basic fields
    assert fields["project_name"] == "Browser Instrumentation (Phase 1) Proposal"
    assert fields["labels"] == ["spec-browser"]
    assert fields["status"] == "Active"
    assert "open-telemetry/community/blob/main/projects/browser-phase-1.md" in fields["markdown_url"]
    
    # Check if we found sponsors (regex-based)
    print(f"\nProject Lead: {fields.get('project_lead')}")
    print(f"GC Sponsors: {fields.get('gc_sponsors')}")
    print(f"TC Sponsors: {fields.get('tc_sponsors')}")


def test_gen_ai_project_extraction():
    """Test extracting fields from gen-ai.md."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/gen-ai.md"
    
    if not project_path.exists():
        print(f"Warning: {project_path} not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    extractor = FieldExtractor(parser, use_llm=False)
    fields = extractor.extract_all_fields()
    
    print("\n\nGen AI Project Fields (without LLM):")
    print(json.dumps(fields, indent=2))
    
    # Check timeline extraction
    print(f"\nTimeline dates found:")
    print(f"  Start: {fields.get('start_date')}")
    print(f"  End: {fields.get('end_date')}")
    print(f"  Confidence: {fields.get('timeline_confidence')}")


def test_completed_project():
    """Test a completed project."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/completed-projects/database-client-semconv.md"
    
    if not project_path.exists():
        print(f"\n\nWarning: completed project not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    extractor = FieldExtractor(parser, use_llm=False)
    fields = extractor.extract_all_fields()
    
    print("\n\nCompleted Project Status:", fields.get("status"))
    assert fields["status"] == "Completed"


if __name__ == "__main__":
    test_browser_project_extraction()
    test_gen_ai_project_extraction()
    test_completed_project()