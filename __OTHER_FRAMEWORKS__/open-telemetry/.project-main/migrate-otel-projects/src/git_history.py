"""Git history extraction for project files."""

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import re


class GitHistoryExtractor:
    """Extract git history information for project files."""
    
    def __init__(self, repo_path: Path):
        """Initialize with repository path."""
        self.repo_path = repo_path
        
    def _run_git_command(self, cmd: List[str], cwd: Optional[Path] = None) -> Optional[str]:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ['git'] + cmd,
                cwd=cwd or self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Git command failed: {' '.join(cmd)}")
            print(f"Error: {e.stderr}")
            return None
    
    def get_file_creation_date(self, file_path: Path) -> Optional[datetime]:
        """Get the date when a file was first added to the repository."""
        # Convert to relative path from repo root
        try:
            relative_path = file_path.relative_to(self.repo_path)
        except ValueError:
            # If file is not in repo, try to find it
            relative_path = file_path.name
            
        # Get the first commit that added this file
        output = self._run_git_command([
            'log', '--follow', '--format=%aI', '--reverse', '--', str(relative_path)
        ])
        
        if output:
            # Get the first line (oldest commit)
            first_commit_date = output.split('\n')[0]
            try:
                return datetime.fromisoformat(first_commit_date.replace('+00:00', '+0000'))
            except ValueError:
                # Try parsing without timezone
                return datetime.fromisoformat(first_commit_date.split('+')[0])
        return None
    
    def get_file_move_date(self, file_path: Path, to_directory: str) -> Optional[datetime]:
        """Get the date when a file was moved to a specific directory."""
        try:
            relative_path = file_path.relative_to(self.repo_path)
        except ValueError:
            relative_path = file_path.name
            
        # Look for commits that moved the file to the target directory
        output = self._run_git_command([
            'log', '--follow', '--format=%aI %s', '--', str(relative_path)
        ])
        
        if not output:
            return None
            
        # Parse commits looking for moves to the target directory
        for line in output.split('\n'):
            if not line:
                continue
                
            # Extract date and commit message
            parts = line.split(' ', 1)
            if len(parts) < 2:
                continue
                
            date_str, message = parts
            
            # Check if this commit moved the file to the target directory
            if to_directory.lower() in message.lower() and ('move' in message.lower() or 'mv' in message.lower()):
                try:
                    return datetime.fromisoformat(date_str.replace('+00:00', '+0000'))
                except ValueError:
                    return datetime.fromisoformat(date_str.split('+')[0])
        
        # Alternative: check if file is currently in target directory
        if to_directory in str(relative_path):
            # Get the first commit where file appears in this directory
            parent_dir = relative_path.parent
            if to_directory in str(parent_dir):
                # Try to find when it was moved here by checking rename detection
                output = self._run_git_command([
                    'log', '--follow', '--name-status', '--format=%aI', '--', str(relative_path)
                ])
                
                if output:
                    lines = output.split('\n')
                    for i, line in enumerate(lines):
                        if line.startswith('R') and i > 0:  # Rename detected
                            # Previous line should be the date
                            date_line = lines[i-1].strip()
                            if date_line:  # Check if not empty
                                try:
                                    return datetime.fromisoformat(date_line.replace('+00:00', '+0000'))
                                except ValueError:
                                    try:
                                        return datetime.fromisoformat(date_line.split('+')[0])
                                    except ValueError:
                                        pass  # Continue looking
        
        return None
    
    def get_last_commit_date(self, file_path: Path) -> Optional[datetime]:
        """Get the date of the last commit that modified this file."""
        try:
            relative_path = file_path.relative_to(self.repo_path)
        except ValueError:
            relative_path = file_path.name
            
        output = self._run_git_command([
            'log', '-1', '--format=%aI', '--', str(relative_path)
        ])
        
        if output:
            try:
                return datetime.fromisoformat(output.replace('+00:00', '+0000'))
            except ValueError:
                return datetime.fromisoformat(output.split('+')[0])
        return None
    
    def get_file_history_summary(self, file_path: Path) -> Dict[str, Optional[datetime]]:
        """Get a summary of key dates for a file."""
        return {
            'created': self.get_file_creation_date(file_path),
            'last_modified': self.get_last_commit_date(file_path),
            'moved_to_completed': self.get_file_move_date(file_path, 'completed'),
            'moved_to_inactive': self.get_file_move_date(file_path, 'inactive'),
        }