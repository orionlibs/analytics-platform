"""GitHub API client for creating issues and updating project boards."""

import os
from typing import Dict, Optional, List, Any
from github import Github, GithubException
from github.Issue import Issue
from github.Milestone import Milestone
from dotenv import load_dotenv
import json
from datetime import datetime, date, timedelta
from typing import Union


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialize GitHub client with token."""
        # Load .env file if it exists
        load_dotenv()
        
        # Get token from parameter, env, or error
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError(
                "GitHub token required. Either:\n"
                "1. Add GITHUB_TOKEN to .env file\n"
                "2. Set GITHUB_TOKEN environment variable\n"
                "3. Pass token parameter"
            )
        
        self.github = Github(self.token)
        self._validate_token()
    
    def _validate_token(self):
        """Validate that the token works."""
        try:
            # Try to get the authenticated user
            user = self.github.get_user()
            self.username = user.login
            print(f"✅ Authenticated as {self.username}")
        except GithubException as e:
            raise ValueError(f"Invalid GitHub token: {e}")
    
    def check_issue_exists(self, repo_name: str, title: str) -> Optional[Issue]:
        """Check if an issue with this title already exists."""
        try:
            repo = self.github.get_repo(repo_name)
            # Search for issues with matching title
            issues = repo.get_issues(state='all')
            for issue in issues:
                if issue.title == title:
                    return issue
            return None
        except GithubException as e:
            print(f"Error checking existing issues: {e}")
            return None
    
    def get_or_create_milestone(self, repo_name: str, title: str, 
                               description: Optional[str] = None,
                               due_date: Optional[Union[date, datetime]] = None) -> Optional[Milestone]:
        """Get existing milestone or create a new one."""
        try:
            repo = self.github.get_repo(repo_name)
            
            # Check if milestone already exists
            milestones = repo.get_milestones(state='all')
            for milestone in milestones:
                if milestone.title == title:
                    print(f"✅ Found existing milestone: {milestone.title}")
                    return milestone
            
            # Create new milestone
            milestone = repo.create_milestone(
                title=title,
                state='open',
                description=description or f"Milestone: {title}",
                due_on=due_date
            )
            
            print(f"✅ Created milestone: {milestone.title}")
            return milestone
            
        except GithubException as e:
            print(f"❌ Error with milestone '{title}': {e}")
            return None
    
    def create_issue(self, repo_name: str, title: str, body: str, labels: List[str], 
                    milestone: Optional[Milestone] = None) -> Optional[Issue]:
        """Create a new issue in the specified repository."""
        try:
            repo = self.github.get_repo(repo_name)
            
            # Create the issue
            create_params = {
                "title": title,
                "body": body,
                "labels": labels
            }
            
            if milestone:
                create_params["milestone"] = milestone
            
            issue = repo.create_issue(**create_params)
            
            print(f"✅ Created issue #{issue.number}: {issue.title}")
            print(f"   URL: {issue.html_url}")
            return issue
            
        except GithubException as e:
            print(f"❌ Error creating issue: {e}")
            return None
    
    def update_project_item(self, project_id: int, item_id: str, fields: Dict[str, Any]) -> bool:
        """Update fields on a project board item using GraphQL API."""
        import requests
        from datetime import date, datetime
        
        # GraphQL endpoint
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # First get the project and field IDs
        field_ids = self.get_project_field_ids(project_id)
        
        print(f"\n📋 Updating project item fields...")
        
        # Update each field
        for field_name, field_value in fields.items():
            if field_name not in field_ids:
                print(f"   ⚠️  Unknown field: {field_name}")
                continue
                
            field_id = field_ids[field_name]
            
            # Format the value based on field type
            if isinstance(field_value, (date, datetime)):
                value = field_value.strftime("%Y-%m-%d")
            else:
                value = str(field_value)
            
            # GraphQL mutation to update field
            mutation = """
            mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
              updateProjectV2ItemFieldValue(input: {
                projectId: $projectId
                itemId: $itemId
                fieldId: $fieldId
                value: $value
              }) {
                projectV2Item {
                  id
                }
              }
            }
            """
            
            # Determine the value format based on field type
            if field_name in ["Start Date", "Estimate Target Date"]:
                field_value_obj = {"date": value}
            elif field_name in ["Status", "Sponsorship Level"] and hasattr(self, '_field_options'):
                # For single select fields, we need the option ID
                options = self._field_options.get(field_name, {})
                option_id = options.get(value)
                if option_id:
                    field_value_obj = {"singleSelectOptionId": option_id}
                else:
                    print(f"   ⚠️  Unknown option '{value}' for field {field_name}")
                    continue
            elif field_name in ["Project File", "Project Board"]:
                field_value_obj = {"text": value}
            else:
                field_value_obj = {"text": value}
            
            try:
                # Get the project node ID first
                if not hasattr(self, '_project_node_id_cache'):
                    self._project_node_id_cache = {}
                
                if project_id not in self._project_node_id_cache:
                    # Get project node ID
                    project_query = """
                    query($org: String!, $number: Int!) {
                      organization(login: $org) {
                        projectV2(number: $number) {
                          id
                        }
                      }
                    }
                    """
                    
                    resp = requests.post(
                        url,
                        json={
                            "query": project_query,
                            "variables": {"org": "open-telemetry", "number": project_id}
                        },
                        headers=headers
                    )
                    resp_data = resp.json()
                    self._project_node_id_cache[project_id] = resp_data["data"]["organization"]["projectV2"]["id"]
                
                project_node_id = self._project_node_id_cache[project_id]
                
                response = requests.post(
                    url,
                    json={
                        "query": mutation,
                        "variables": {
                            "projectId": project_node_id,
                            "itemId": item_id,
                            "fieldId": field_id,
                            "value": field_value_obj
                        }
                    },
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                if "errors" in data:
                    print(f"   ❌ Error updating {field_name}: {data['errors']}")
                else:
                    print(f"   ✅ Updated {field_name}: {value}")
                    
            except Exception as e:
                print(f"   ❌ Error updating {field_name}: {e}")
        
        return True
    
    def check_issue_in_project(self, issue: Issue, project_id: int) -> Optional[str]:
        """Check if an issue is already in a project board and return the item ID if found."""
        import requests
        
        # GraphQL endpoint
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Query to check if issue is in project and get item ID
        query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              items(first: 100) {
                nodes {
                  id
                  content {
                    ... on Issue {
                      id
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                url,
                json={
                    "query": query,
                    "variables": {
                        "org": "open-telemetry",
                        "number": project_id
                    }
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"❌ Error checking project items: {data['errors']}")
                return None
            
            # Check if issue is in the project items and return item ID
            items = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("items", {}).get("nodes", [])
            for item in items:
                content = item.get("content", {})
                if content and content.get("id") == issue.node_id:
                    return item.get("id")  # Return the item ID
            
            return None
                
        except Exception as e:
            print(f"❌ Error checking if issue is in project: {e}")
            return None
    
    def add_issue_to_project(self, issue: Issue, project_id: int) -> Optional[str]:
        """Add an issue to a project board using GraphQL API and return the item ID."""
        import requests
        
        # GraphQL endpoint
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # First, get the project's node ID
        project_query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              id
            }
          }
        }
        """
        
        try:
            # Get project node ID
            response = requests.post(
                url,
                json={
                    "query": project_query, 
                    "variables": {"org": "open-telemetry", "number": project_id}
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"❌ Error getting project: {data['errors']}")
                return None
            
            if not data.get("data", {}).get("organization", {}).get("projectV2"):
                print(f"❌ Project {project_id} not found in open-telemetry org")
                return None
                
            project_node_id = data["data"]["organization"]["projectV2"]["id"]
            
            # Now add the issue to the project
            add_mutation = """
            mutation($projectId: ID!, $contentId: ID!) {
              addProjectV2ItemById(input: {
                projectId: $projectId
                contentId: $contentId
              }) {
                item {
                  id
                }
              }
            }
            """
            
            response = requests.post(
                url,
                json={
                    "query": add_mutation,
                    "variables": {
                        "projectId": project_node_id,
                        "contentId": issue.node_id
                    }
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"❌ Error adding issue to project: {data['errors']}")
                return None
            
            item_data = data.get("data", {}).get("addProjectV2ItemById", {}).get("item")
            if item_data:
                item_id = item_data["id"]
                print(f"✅ Added issue #{issue.number} to project {project_id}")
                return item_id
            else:
                print(f"❌ Failed to add issue to project")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error adding issue to project: {e}")
            return None
    
    def get_project_field_ids(self, project_id: int) -> Dict[str, str]:
        """Get the field IDs for a project board."""
        import requests
        
        # GraphQL endpoint
        url = "https://api.github.com/graphql"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Query to get project fields
        query = """
        query($org: String!, $number: Int!) {
          organization(login: $org) {
            projectV2(number: $number) {
              fields(first: 100) {
                nodes {
                  ... on ProjectV2Field {
                    id
                    name
                  }
                  ... on ProjectV2SingleSelectField {
                    id
                    name
                    options {
                      id
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """
        
        try:
            response = requests.post(
                url,
                json={
                    "query": query,
                    "variables": {"org": "open-telemetry", "number": project_id}
                },
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                print(f"❌ Error getting project fields: {data['errors']}")
                return {}
            
            fields = data.get("data", {}).get("organization", {}).get("projectV2", {}).get("fields", {}).get("nodes", [])
            field_map = {}
            
            # Store field IDs and option IDs for single select fields
            self._field_options = {}
            
            for field in fields:
                field_name = field.get("name")
                field_id = field.get("id")
                if field_name and field_id:
                    field_map[field_name] = field_id
                    
                    # Store options for single select fields
                    if "options" in field:
                        self._field_options[field_name] = {
                            opt["name"]: opt["id"] for opt in field.get("options", [])
                        }
            
            return field_map
            
        except Exception as e:
            print(f"❌ Error getting project field IDs: {e}")
            # Return empty dict to force dynamic lookup
            return {}


class GitHubMigrator:
    """Handles the migration of projects to GitHub."""
    
    def __init__(self, github_client: GitHubClient, project_id: int = 155):
        """Initialize with GitHub client and project board ID."""
        self.client = github_client
        self.project_id = project_id
        self.target_repo = "open-telemetry/.project"
        self._milestone_cache = {}  # Cache for milestones
    
    def _get_monthly_milestone(self, target_date: date, dry_run: bool = True) -> Optional[Milestone]:
        """Get or create a monthly milestone for the given date."""
        # Create key for the month
        month_key = f"{target_date.year}-{target_date.month:02d}"
        month_name = target_date.strftime("%B %Y")
        
        # Check cache
        if month_key in self._milestone_cache:
            return self._milestone_cache[month_key]
        
        # Calculate month end date
        if target_date.month == 12:
            month_end = date(target_date.year, 12, 31)
        else:
            next_month = date(target_date.year, target_date.month + 1, 1)
            month_end = next_month - timedelta(days=1)
        
        if dry_run:
            print(f"   Would use monthly milestone: {month_name}")
            return None
        
        # Create or get milestone
        milestone = self.client.get_or_create_milestone(
            repo_name=self.target_repo,
            title=f"OpenTelemetry Projects - {month_name}",
            description=f"Projects and milestones for {month_name}",
            due_date=month_end
        )
        
        if milestone:
            self._milestone_cache[month_key] = milestone
        
        return milestone
    
    def _create_milestones_for_project(self, project_data: 'ProjectData', dry_run: bool = True) -> List[Milestone]:
        """Create or get milestones for project timeline milestones."""
        milestones = []
        
        if not project_data.timeline_milestones:
            return milestones
        
        print(f"\n📅 Processing {len(project_data.timeline_milestones)} milestones...")
        
        for milestone_data in project_data.timeline_milestones:
            # Create milestone title from project name and date
            milestone_title = f"{project_data.project_name} - {milestone_data.date.strftime('%Y-%m')}"
            
            if dry_run:
                print(f"   Would create milestone: {milestone_title}")
                print(f"   Description: {milestone_data.description}")
                print(f"   Due date: {milestone_data.date}")
            else:
                milestone = self.client.get_or_create_milestone(
                    repo_name=self.target_repo,
                    title=milestone_title,
                    description=milestone_data.description,
                    due_date=milestone_data.date
                )
                if milestone:
                    milestones.append(milestone)
        
        return milestones
    
    def migrate_project(self, project_data: 'ProjectData', dry_run: bool = True) -> 'MigrationResult':
        """Migrate a single project to GitHub."""
        from .models import MigrationResult
        
        result = MigrationResult(
            project_file=str(project_data.markdown_url),
            dry_run=dry_run,
            project_data=project_data,
            success=False
        )
        
        try:
            # Check if issue already exists
            existing = self.client.check_issue_exists(
                self.target_repo, 
                project_data.project_name
            )
            
            if existing:
                result.issue_url = existing.html_url
                print(f"⚠️  Issue already exists: {existing.html_url}")
                
                # Check if we should add it to the project board
                if not dry_run:
                    # Process milestones for existing issue
                    milestones = self._create_milestones_for_project(project_data, dry_run)
                    
                    # Find the appropriate milestone for the issue
                    issue_milestone = None
                    if milestones:
                        today = date.today()
                        future_milestones = [m for m in milestones if m.due_on and m.due_on.date() >= today]
                        issue_milestone = future_milestones[0] if future_milestones else milestones[-1]
                    elif project_data.end_date:
                        issue_milestone = self._get_monthly_milestone(project_data.end_date, dry_run)
                    
                    # Update the issue's milestone if needed
                    if issue_milestone and existing.milestone != issue_milestone:
                        print(f"   📅 Updating issue milestone to: {issue_milestone.title}")
                        existing.edit(milestone=issue_milestone)
                    
                    print(f"   Checking if issue #{existing.number} is already on project board...")
                    item_id = self.client.check_issue_in_project(existing, self.project_id)
                    if item_id:
                        print(f"   ✅ Issue is already on project board, updating fields...")
                        # Update project fields for existing issue on board
                        board_fields = project_data.to_project_fields()
                        self.client.update_project_item(self.project_id, item_id, board_fields)
                        result.success = True
                        result.error = f"Issue already exists and fields were updated on project board"
                    else:
                        print(f"   📋 Issue not on project board, adding it...")
                        item_id = self.client.add_issue_to_project(existing, self.project_id)
                        if item_id:
                            # Update project fields for existing issue
                            board_fields = project_data.to_project_fields()
                            self.client.update_project_item(self.project_id, item_id, board_fields)
                            result.success = True
                            result.error = f"Issue existed but was newly added to project board with fields updated"
                        else:
                            result.error = f"Issue exists but failed to add to project board"
                else:
                    print(f"   DRY RUN - Would check if issue needs to be added to project board")
                    result.success = True
                    result.error = "Issue already exists (dry run)"
                
                return result
            
            # Get issue content
            issue_dict = project_data.to_github_issue()
            
            # Process milestones
            milestones = self._create_milestones_for_project(project_data, dry_run)
            
            # Find the appropriate milestone for the issue
            issue_milestone = None
            
            if not dry_run:
                # If project has specific milestones, use the nearest one
                if milestones:
                    today = date.today()
                    future_milestones = [m for m in milestones if m.due_on and m.due_on.date() >= today]
                    issue_milestone = future_milestones[0] if future_milestones else milestones[-1]
                
                # Otherwise, use monthly milestone based on project end date
                elif project_data.end_date:
                    issue_milestone = self._get_monthly_milestone(project_data.end_date, dry_run)
            
            if dry_run:
                print(f"\n🔍 DRY RUN - Would create issue:")
                print(f"   Title: {issue_dict['title']}")
                print(f"   Labels: {issue_dict['labels']}")
                
                # Show milestone assignment
                if milestones:
                    print(f"   Milestone: Would assign to project-specific milestone")
                elif project_data.end_date:
                    month_name = project_data.end_date.strftime("%B %Y")
                    print(f"   Milestone: Would assign to {month_name}")
                else:
                    print(f"   Milestone: None (no timeline data)")
                    
                print(f"   Body preview: {issue_dict['body'][:200]}...")
                
                # Show project board updates
                board_fields = project_data.to_project_fields()
                print(f"\n   Project board fields:")
                for field, value in board_fields.items():
                    print(f"     {field}: {value}")
                
                result.success = True
                result.issue_url = "DRY_RUN"
            else:
                # Create the issue
                issue = self.client.create_issue(
                    self.target_repo,
                    issue_dict['title'],
                    issue_dict['body'],
                    issue_dict['labels'],
                    milestone=issue_milestone
                )
                
                if issue:
                    result.issue_url = issue.html_url
                    
                    # Add to project board and update fields
                    item_id = self.client.add_issue_to_project(issue, self.project_id)
                    
                    if item_id:
                        # Update project fields
                        board_fields = project_data.to_project_fields()
                        self.client.update_project_item(self.project_id, item_id, board_fields)
                        result.success = True
                    else:
                        result.error = "Issue created but failed to add to project board"
                        result.success = True  # Partial success
                else:
                    result.error = "Failed to create issue"
            
        except Exception as e:
            result.error = str(e)
            print(f"❌ Error migrating project: {e}")
        
        return result