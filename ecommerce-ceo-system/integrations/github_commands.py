#!/usr/bin/env python3
"""
GitHub Command Integration for Marbily E-commerce System
Natural language command processing for GitHub operations
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from UNIVERSAL_CREDENTIALS import credentials

# Import GitHub manager from same directory
sys.path.append(str(Path(__file__).parent))
from github_manager import GitHubManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubCommandProcessor:
    """Process natural language GitHub commands"""

    def __init__(self):
        self.github = GitHubManager()
        self.command_mappings = {
            # Sync commands
            'sync to github': self.sync_to_github,
            'sync github': self.sync_to_github,
            'push to github': self.sync_to_github,
            'commit and push': self.sync_to_github,
            'save to github': self.sync_to_github,

            # Status commands
            'check status': self.check_git_status,
            'git status': self.check_git_status,
            'github status': self.check_git_status,
            'check git': self.check_git_status,
            'repo status': self.check_git_status,

            # Repository management
            'list repos': self.list_repositories,
            'list repositories': self.list_repositories,
            'show repos': self.list_repositories,
            'my repos': self.list_repositories,

            # Clone operations
            'clone project': self.clone_repository,
            'clone repo': self.clone_repository,
            'clone repository': self.clone_repository,

            # Create operations
            'create repo': self.create_repository,
            'create repository': self.create_repository,
            'new repo': self.create_repository,
            'new repository': self.create_repository,

            # Pull operations
            'pull latest': self.pull_latest,
            'pull changes': self.pull_latest,
            'update from github': self.pull_latest,
            'sync from github': self.pull_latest,

            # Info operations
            'repo info': self.get_repository_info,
            'repository info': self.get_repository_info,
            'project info': self.get_repository_info,

            # History operations
            'commit history': self.get_commit_history,
            'git history': self.get_commit_history,
            'git log': self.get_commit_history,
            'recent commits': self.get_commit_history,
        }

        logger.info(f"🐙 GitHub Command Processor initialized with {len(self.command_mappings)} commands")

    def process_command(self, command: str, **kwargs) -> Dict:
        """Process a natural language GitHub command"""
        try:
            command_lower = command.lower().strip()

            # Find matching command
            for pattern, handler in self.command_mappings.items():
                if pattern in command_lower:
                    logger.info(f"🎯 Processing GitHub command: '{command}' → {handler.__name__}")
                    return handler(**kwargs)

            # If no exact match, try partial matching
            for pattern, handler in self.command_mappings.items():
                pattern_words = set(pattern.split())
                command_words = set(command_lower.split())

                if pattern_words.intersection(command_words):
                    logger.info(f"🎯 Partial match for command: '{command}' → {handler.__name__}")
                    return handler(**kwargs)

            return {
                'status': 'error',
                'error': f'Unknown GitHub command: {command}',
                'available_commands': list(self.command_mappings.keys())
            }

        except Exception as e:
            logger.error(f"Error processing GitHub command: {e}")
            return {'status': 'error', 'error': str(e)}

    def sync_to_github(self, message: Optional[str] = None, **kwargs) -> Dict:
        """Sync all changes to GitHub"""
        try:
            logger.info("🔄 Executing: Sync to GitHub")
            result = self.github.sync_to_github(message=message)

            if result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': '✅ Successfully synced all changes to GitHub',
                    'details': result,
                    'command': 'sync_to_github'
                }
            elif result['status'] == 'no_changes':
                return {
                    'status': 'info',
                    'message': 'ℹ️ No changes to sync - repository is clean',
                    'command': 'sync_to_github'
                }
            else:
                return {
                    'status': 'error',
                    'message': f"❌ GitHub sync failed: {result.get('error', 'Unknown error')}",
                    'details': result,
                    'command': 'sync_to_github'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'sync_to_github'}

    def check_git_status(self, **kwargs) -> Dict:
        """Check Git repository status"""
        try:
            logger.info("🔍 Executing: Check Git status")
            status_result = self.github.get_repository_status()
            repo_info = self.github.get_repository_info()

            if status_result['status'] == 'success':
                clean = status_result.get('clean', False)
                changes = status_result.get('changes', 0)

                status_message = f"📊 Repository Status:\n"
                status_message += f"   Branch: {status_result.get('branch', 'unknown')}\n"
                status_message += f"   Changes: {changes} files\n"
                status_message += f"   Status: {'✅ Clean' if clean else '⚠️ Has changes'}"

                return {
                    'status': 'success',
                    'message': status_message,
                    'repository_status': status_result,
                    'repository_info': repo_info,
                    'command': 'check_git_status'
                }
            else:
                return {
                    'status': 'error',
                    'message': f"❌ Could not check Git status: {status_result.get('error', 'Unknown error')}",
                    'command': 'check_git_status'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'check_git_status'}

    def list_repositories(self, limit: int = 10, **kwargs) -> Dict:
        """List GitHub repositories"""
        try:
            logger.info("📚 Executing: List repositories")
            repos = self.github.list_repositories(limit=limit)

            if repos:
                repo_list = f"📚 Your GitHub Repositories ({len(repos)}):\n"
                for i, repo in enumerate(repos, 1):
                    repo_list += f"   {i}. {repo['name']} ({repo['visibility']}) - {repo.get('updated', 'unknown')}\n"

                return {
                    'status': 'success',
                    'message': repo_list,
                    'repositories': repos,
                    'count': len(repos),
                    'username': self.github.username,
                    'command': 'list_repositories'
                }
            else:
                return {
                    'status': 'info',
                    'message': 'ℹ️ No repositories found or unable to access GitHub',
                    'command': 'list_repositories'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'list_repositories'}

    def clone_repository(self, repo: str, target_dir: Optional[str] = None,
                        owner: Optional[str] = None, **kwargs) -> Dict:
        """Clone a GitHub repository"""
        try:
            if not repo:
                return {
                    'status': 'error',
                    'error': 'Repository name required for cloning',
                    'command': 'clone_repository'
                }

            logger.info(f"⬇️ Executing: Clone repository '{repo}'")
            result = self.github.clone_repository(repo, target_dir, owner)

            if result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': f"✅ Successfully cloned repository '{result['repo']}' to {result['path']}",
                    'details': result,
                    'command': 'clone_repository'
                }
            else:
                return {
                    'status': 'error',
                    'message': f"❌ Failed to clone repository: {result.get('error', 'Unknown error')}",
                    'details': result,
                    'command': 'clone_repository'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'clone_repository'}

    def create_repository(self, name: str, description: str = "",
                         private: bool = False, **kwargs) -> Dict:
        """Create a new GitHub repository"""
        try:
            if not name:
                return {
                    'status': 'error',
                    'error': 'Repository name required for creation',
                    'command': 'create_repository'
                }

            logger.info(f"🆕 Executing: Create repository '{name}'")
            result = self.github.create_repository(name, description, private)

            if result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': f"✅ Successfully created repository '{name}' at {result['url']}",
                    'details': result,
                    'command': 'create_repository'
                }
            else:
                return {
                    'status': 'error',
                    'message': f"❌ Failed to create repository: {result.get('error', 'Unknown error')}",
                    'details': result,
                    'command': 'create_repository'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'create_repository'}

    def pull_latest(self, branch: Optional[str] = None, **kwargs) -> Dict:
        """Pull latest changes from GitHub"""
        try:
            logger.info("⬇️ Executing: Pull latest changes")
            result = self.github.pull_latest(branch=branch)

            if result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': f"✅ Successfully pulled latest changes",
                    'details': result,
                    'command': 'pull_latest'
                }
            else:
                return {
                    'status': 'error',
                    'message': f"❌ Failed to pull changes: {result.get('error', 'Unknown error')}",
                    'details': result,
                    'command': 'pull_latest'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'pull_latest'}

    def get_repository_info(self, repo: Optional[str] = None,
                           owner: Optional[str] = None, **kwargs) -> Dict:
        """Get repository information"""
        try:
            logger.info("ℹ️ Executing: Get repository info")
            result = self.github.get_repository_info(repo, owner)

            if 'status' in result and result['status'] == 'error':
                return {
                    'status': 'error',
                    'message': f"❌ Could not get repository info: {result.get('error', 'Unknown error')}",
                    'command': 'get_repository_info'
                }
            else:
                info_text = f"ℹ️ Repository Information:\n"
                info_text += f"   Name: {result.get('name', 'unknown')}\n"
                info_text += f"   Description: {result.get('description', 'No description')}\n"
                info_text += f"   URL: {result.get('url', 'unknown')}\n"
                info_text += f"   Visibility: {result.get('visibility', 'unknown')}\n"
                info_text += f"   Stars: {result.get('stargazerCount', 0)}\n"
                info_text += f"   Updated: {result.get('updatedAt', 'unknown')}"

                return {
                    'status': 'success',
                    'message': info_text,
                    'repository_info': result,
                    'command': 'get_repository_info'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'get_repository_info'}

    def get_commit_history(self, limit: int = 10, **kwargs) -> Dict:
        """Get commit history"""
        try:
            logger.info("📜 Executing: Get commit history")
            commits = self.github.get_commit_history(limit=limit)

            if commits:
                history_text = f"📜 Recent Commits ({len(commits)}):\n"
                for i, commit in enumerate(commits, 1):
                    history_text += f"   {i}. {commit['short_hash']} - {commit['message']}\n"

                return {
                    'status': 'success',
                    'message': history_text,
                    'commits': commits,
                    'count': len(commits),
                    'command': 'get_commit_history'
                }
            else:
                return {
                    'status': 'info',
                    'message': 'ℹ️ No commit history found or not a Git repository',
                    'command': 'get_commit_history'
                }

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'command': 'get_commit_history'}

    def get_available_commands(self) -> List[str]:
        """Get list of available GitHub commands"""
        return list(self.command_mappings.keys())

    def get_command_help(self) -> str:
        """Get help text for GitHub commands"""
        help_text = "🐙 GitHub Commands Available:\n\n"

        categories = {
            "Sync Operations": [
                "sync to github", "push to github", "commit and push", "save to github"
            ],
            "Status & Info": [
                "check status", "git status", "repo status", "repo info"
            ],
            "Repository Management": [
                "list repos", "create repo", "clone repo"
            ],
            "Pull Operations": [
                "pull latest", "pull changes", "update from github"
            ],
            "History": [
                "commit history", "git log", "recent commits"
            ]
        }

        for category, commands in categories.items():
            help_text += f"**{category}:**\n"
            for cmd in commands:
                help_text += f"  • {cmd}\n"
            help_text += "\n"

        help_text += "**Usage Examples:**\n"
        help_text += "  • 'sync to github' - Commit and push all changes\n"
        help_text += "  • 'check status' - Show Git repository status\n"
        help_text += "  • 'list repos' - Show your GitHub repositories\n"
        help_text += "  • 'create repo MyProject' - Create new repository\n"
        help_text += "  • 'clone repo ProjectName' - Clone repository locally\n"

        return help_text

def main():
    """Test GitHub command processor"""
    print("🧪 Testing GitHub Command Processor")

    processor = GitHubCommandProcessor()

    # Test commands
    test_commands = [
        "check status",
        "list repos",
        "sync to github",
        "commit history"
    ]

    for command in test_commands:
        print(f"\n🎯 Testing: '{command}'")
        result = processor.process_command(command)
        print(f"Result: {result.get('status', 'unknown')} - {result.get('message', 'No message')}")

if __name__ == '__main__':
    main()