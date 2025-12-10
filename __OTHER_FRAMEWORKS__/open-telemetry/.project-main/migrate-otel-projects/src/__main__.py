"""Main CLI entry point for the migration tool."""

import click
import json
from pathlib import Path
from typing import List, Optional
import sys

from .markdown_parser import ProjectMarkdownParser
from .field_extractor import FieldExtractor
from .github_client import GitHubClient, GitHubMigrator
from .models import MigrationResult


@click.command()
@click.option(
    '--project', 
    help='Process a specific project file (e.g., browser-phase-1.md)'
)
@click.option(
    '--all', 
    'process_all',
    is_flag=True,
    help='Process all project files'
)
@click.option(
    '--dry-run/--no-dry-run',
    default=True,
    help='Perform a dry run without creating issues (default: True)'
)
@click.option(
    '--community-path',
    type=click.Path(exists=True, path_type=Path),
    default=Path('../community'),
    help='Path to the community repository'
)
@click.option(
    '--output-json',
    type=click.Path(path_type=Path),
    help='Save results to JSON file'
)
@click.option(
    '--github-token',
    envvar='GITHUB_TOKEN',
    help='GitHub token (can also use GITHUB_TOKEN env var)'
)
@click.option(
    '--project-id',
    type=int,
    default=155,
    help='GitHub project board ID (default: 155)'
)
@click.option(
    '--use-llm/--no-llm',
    default=True,
    help='Use LLM for enhanced extraction (default: True)'
)
def main(
    project: Optional[str],
    process_all: bool,
    dry_run: bool,
    community_path: Path,
    output_json: Optional[Path],
    github_token: Optional[str],
    project_id: int,
    use_llm: bool
):
    """Migrate OpenTelemetry projects to GitHub issues."""
    
    click.echo("🚀 OpenTelemetry Project Migration Tool")
    click.echo("=" * 50)
    
    # Validate input
    if not project and not process_all:
        click.echo("❌ Error: Specify either --project or --all")
        sys.exit(1)
    
    if project and process_all:
        click.echo("❌ Error: Cannot use both --project and --all")
        sys.exit(1)
    
    # Find project files
    projects_dir = community_path / "projects"
    if not projects_dir.exists():
        click.echo(f"❌ Error: Projects directory not found: {projects_dir}")
        sys.exit(1)
    
    # Collect files to process
    files_to_process: List[Path] = []
    
    if project:
        # Process specific file
        project_file = projects_dir / project
        if not project_file.exists():
            # Try with .md extension
            project_file = projects_dir / f"{project}.md"
        
        if not project_file.exists():
            click.echo(f"❌ Error: Project file not found: {project}")
            sys.exit(1)
        
        files_to_process = [project_file]
    else:
        # Process all markdown files
        files_to_process = list(projects_dir.rglob("*.md"))
        # Exclude README files
        files_to_process = [f for f in files_to_process if f.name.lower() != "readme.md"]
        click.echo(f"📁 Found {len(files_to_process)} project files")
    
    # Initialize GitHub client if not in dry-run mode or if token provided
    github_client = None
    migrator = None
    
    if dry_run:
        # For dry run, create a migrator without validating the token
        if github_token:
            try:
                github_client = GitHubClient(github_token)
                migrator = GitHubMigrator(github_client, project_id)
            except ValueError:
                # Token validation failed, but that's OK for dry run
                click.echo("ℹ️  Using dry-run mode (token validation skipped)")
        else:
            click.echo("ℹ️  Dry run mode - no GitHub token provided")
        
        # Create a dummy migrator for dry run if we don't have one
        if not migrator:
            # Create migrator with dummy client for dry run
            class DummyClient:
                def __init__(self):
                    pass
                def check_issue_exists(self, repo, title):
                    return None
                def get_or_create_milestone(self, **kwargs):
                    return None
                def create_issue(self, **kwargs):
                    return None
                def add_issue_to_project(self, **kwargs):
                    return True
            migrator = GitHubMigrator(DummyClient(), project_id)
    else:
        # Real mode - token required
        try:
            if not github_token:
                raise ValueError("GitHub token required for non-dry-run mode")
            github_client = GitHubClient(github_token)
            migrator = GitHubMigrator(github_client, project_id)
        except ValueError as e:
            click.echo(f"❌ Error: {e}")
            sys.exit(1)
    
    # Process files
    results: List[MigrationResult] = []
    
    for file_path in files_to_process:
        click.echo(f"\n📄 Processing: {file_path.name}")
        click.echo("-" * 40)
        
        try:
            # Parse and extract
            parser = ProjectMarkdownParser(file_path)
            extractor = FieldExtractor(parser, use_llm=use_llm, repo_path=community_path)
            project_data = extractor.extract_to_model()
            
            # Show extraction results
            click.echo(f"✅ Extracted: {project_data.project_name}")
            click.echo(f"   Status: {project_data.status}")
            click.echo(f"   Labels: {', '.join(project_data.labels) or 'None'}")
            
            if project_data.extraction_warnings:
                click.echo("   ⚠️  Warnings:")
                for warning in project_data.extraction_warnings:
                    click.echo(f"      - {warning}")
            
            # Migrate if we have a migrator
            if migrator:
                result = migrator.migrate_project(project_data, dry_run)
                results.append(result)
            else:
                # Create a dry-run result
                result = MigrationResult(
                    project_file=str(file_path),
                    dry_run=True,
                    project_data=project_data,
                    success=True
                )
                results.append(result)
                
        except Exception as e:
            click.echo(f"❌ Error processing {file_path.name}: {e}")
            result = MigrationResult(
                project_file=str(file_path),
                dry_run=dry_run,
                success=False,
                error=str(e)
            )
            results.append(result)
    
    # Summary
    click.echo("\n" + "=" * 50)
    click.echo("📊 Summary")
    click.echo(f"   Total projects: {len(results)}")
    click.echo(f"   Successful: {sum(1 for r in results if r.success)}")
    click.echo(f"   Failed: {sum(1 for r in results if not r.success)}")
    
    if dry_run:
        click.echo("\n✅ Dry run complete - no issues were created")
    
    # Save to JSON if requested
    if output_json:
        output_data = []
        for result in results:
            data = {
                "file": result.project_file,
                "success": result.success,
                "dry_run": result.dry_run,
                "issue_url": result.issue_url,
                "error": result.error
            }
            if result.project_data:
                data["project_data"] = result.project_data.model_dump()
            output_data.append(data)
        
        with open(output_json, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        click.echo(f"\n💾 Results saved to: {output_json}")


if __name__ == "__main__":
    main()