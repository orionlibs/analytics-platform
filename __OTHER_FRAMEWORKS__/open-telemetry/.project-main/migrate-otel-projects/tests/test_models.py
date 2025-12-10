"""Tests for Pydantic models and full extraction pipeline."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.markdown_parser import ProjectMarkdownParser
from src.field_extractor import FieldExtractor
from src.models import ProjectData
import json


def test_browser_project_model():
    """Test creating ProjectData model from browser project."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/browser-phase-1.md"
    
    if not project_path.exists():
        print(f"Warning: {project_path} not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    extractor = FieldExtractor(parser, use_llm=False)
    
    # Extract to model
    project_data = extractor.extract_to_model()
    
    print("Browser Project Model:")
    print(project_data.model_dump_json(indent=2))
    
    # Test GitHub issue format
    issue_dict = project_data.to_github_issue()
    print("\n\nGitHub Issue Format:")
    print(f"Title: {issue_dict['title']}")
    print(f"Labels: {issue_dict['labels']}")
    print(f"\nBody:\n{issue_dict['body']}")
    
    # Test project board fields
    board_fields = project_data.to_project_fields()
    print("\n\nProject Board Fields:")
    for field, value in board_fields.items():
        print(f"  {field}: {value}")


def test_gen_ai_project_model():
    """Test creating ProjectData model from gen-ai project."""
    project_path = Path(__file__).parent.parent.parent / "community/projects/gen-ai.md"
    
    if not project_path.exists():
        print(f"Warning: {project_path} not found, skipping test")
        return
    
    parser = ProjectMarkdownParser(project_path)
    extractor = FieldExtractor(parser, use_llm=False)
    
    project_data = extractor.extract_to_model()
    
    print("\n\nGen AI Project Summary:")
    print(f"  Name: {project_data.project_name}")
    print(f"  Status: {project_data.status}")
    print(f"  Start Date: {project_data.start_date}")
    print(f"  End Date: {project_data.end_date}")
    print(f"  Warnings: {project_data.extraction_warnings}")
    print(f"  Needs Review: {project_data.needs_manual_review}")


def test_json_export():
    """Test exporting multiple projects to JSON."""
    projects_dir = Path(__file__).parent.parent.parent / "community/projects"
    
    if not projects_dir.exists():
        print(f"Warning: {projects_dir} not found, skipping test")
        return
    
    results = []
    
    # Process first 3 markdown files
    for i, md_file in enumerate(projects_dir.glob("*.md")):
        if i >= 3:
            break
        
        print(f"\nProcessing: {md_file.name}")
        try:
            parser = ProjectMarkdownParser(md_file)
            extractor = FieldExtractor(parser, use_llm=False)
            project_data = extractor.extract_to_model()
            
            results.append({
                "file": str(md_file.name),
                "data": project_data.model_dump()
            })
        except Exception as e:
            print(f"  Error: {e}")
            results.append({
                "file": str(md_file.name),
                "error": str(e)
            })
    
    # Save to JSON file
    output_file = Path(__file__).parent.parent / "test_output.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n\nExported {len(results)} projects to {output_file}")


if __name__ == "__main__":
    test_browser_project_model()
    test_gen_ai_project_model()
    test_json_export()