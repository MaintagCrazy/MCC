#!/usr/bin/env python3
"""
GitHub Repository Manager for Marbily E-commerce System
Comprehensive GitHub integration with workflow automation
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from UNIVERSAL_CREDENTIALS import credentials

# Import security scanner
sys.path.append(str(Path(__file__).parent))
from security_scanner import SecurityScanner

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GitHubManager:
    """Comprehensive GitHub repository and workflow manager"""

    def __init__(self):
        self.token = credentials.GITHUB_PERSONAL_ACCESS_TOKEN
        self.username = self.get_authenticated_user()
        self.project_root = Path(__file__).parent.parent.parent

        logger.info(f"🐙 GitHub Manager initialized for user: {self.username}")

    def get_authenticated_user(self) -> str:
        """Get the currently authenticated GitHub user"""
        try:
            result = subprocess.run(
                ['gh', 'api', 'user', '--jq', '.login'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Failed to get user info: {result.stderr}")
                return "unknown"
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return "unknown"

    def list_repositories(self, limit: int = 10, include_private: bool = True) -> List[Dict]:
        """List user repositories"""
        try:
            cmd = ['gh', 'repo', 'list', '--limit', str(limit)]
            if include_private:
                cmd.append('--source')

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                repos = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            repos.append({
                                'name': parts[0],
                                'visibility': parts[1],
                                'updated': parts[2] if len(parts) > 2 else 'unknown'
                            })
                return repos
            else:
                logger.error(f"Failed to list repositories: {result.stderr}")
                return []

        except Exception as e:
            logger.error(f"Error listing repositories: {e}")
            return []

    def create_repository(self, name: str, description: str = "", private: bool = False,
                         initialize: bool = True) -> Dict:
        """Create a new GitHub repository"""
        try:
            cmd = ['gh', 'repo', 'create', name]

            if description:
                cmd.extend(['--description', description])

            if private:
                cmd.append('--private')
            else:
                cmd.append('--public')

            if initialize:
                cmd.append('--readme')

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            if result.returncode == 0:
                logger.info(f"✅ Repository '{name}' created successfully")
                return {
                    'status': 'success',
                    'name': name,
                    'url': f"https://github.com/{self.username}/{name}",
                    'message': result.stdout.strip()
                }
            else:
                logger.error(f"Failed to create repository: {result.stderr}")
                return {
                    'status': 'error',
                    'error': result.stderr.strip()
                }

        except Exception as e:
            logger.error(f"Error creating repository: {e}")
            return {'status': 'error', 'error': str(e)}

    def clone_repository(self, repo_name: str, target_dir: Optional[str] = None,
                        owner: Optional[str] = None) -> Dict:
        """Clone a repository"""
        try:
            full_repo_name = f"{owner or self.username}/{repo_name}"

            cmd = ['gh', 'repo', 'clone', full_repo_name]
            if target_dir:
                cmd.append(target_dir)

            # Change to target directory if specified, otherwise use current
            cwd = Path(target_dir).parent if target_dir else self.project_root

            result = subprocess.run(cmd, capture_output=True, text=True,
                                  timeout=300, cwd=str(cwd))

            if result.returncode == 0:
                clone_path = Path(cwd) / (target_dir or repo_name)
                logger.info(f"✅ Repository '{full_repo_name}' cloned to {clone_path}")
                return {
                    'status': 'success',
                    'repo': full_repo_name,
                    'path': str(clone_path),
                    'message': result.stdout.strip()
                }
            else:
                logger.error(f"Failed to clone repository: {result.stderr}")
                return {
                    'status': 'error',
                    'error': result.stderr.strip()
                }

        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            return {'status': 'error', 'error': str(e)}

    def get_repository_status(self, repo_path: Optional[str] = None) -> Dict:
        """Get git status for a repository"""
        try:
            repo_path = repo_path or str(self.project_root)

            # Check if it's a git repository
            if not (Path(repo_path) / '.git').exists():
                return {
                    'status': 'not_a_repo',
                    'path': repo_path,
                    'message': 'Not a git repository'
                }

            # Get git status
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, cwd=repo_path, timeout=10
            )

            if result.returncode == 0:
                changes = result.stdout.strip().split('\n') if result.stdout.strip() else []

                # Get branch info
                branch_result = subprocess.run(
                    ['git', 'branch', '--show-current'],
                    capture_output=True, text=True, cwd=repo_path, timeout=5
                )

                current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'

                # Get remote status
                remote_result = subprocess.run(
                    ['git', 'status', '--porcelain=v1', '--branch'],
                    capture_output=True, text=True, cwd=repo_path, timeout=5
                )

                return {
                    'status': 'success',
                    'path': repo_path,
                    'branch': current_branch,
                    'changes': len(changes),
                    'files': changes,
                    'clean': len(changes) == 0,
                    'remote_status': remote_result.stdout.strip() if remote_result.returncode == 0 else 'unknown'
                }
            else:
                return {
                    'status': 'error',
                    'error': result.stderr.strip()
                }

        except Exception as e:
            logger.error(f"Error getting repository status: {e}")
            return {'status': 'error', 'error': str(e)}

    def commit_and_push(self, repo_path: Optional[str] = None, message: Optional[str] = None,
                       add_all: bool = True, push: bool = True) -> Dict:
        """Commit changes and optionally push to remote"""
        try:
            repo_path = repo_path or str(self.project_root)

            if not (Path(repo_path) / '.git').exists():
                return {
                    'status': 'error',
                    'error': 'Not a git repository'
                }

            # Generate commit message if not provided
            if not message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = f"Automated commit - {timestamp}\n\n🤖 Generated with Marbily Command Center\n\nCo-Authored-By: Claude <noreply@anthropic.com>"

            results = {'steps': []}

            # Add files
            if add_all:
                add_result = subprocess.run(
                    ['git', 'add', '.'],
                    capture_output=True, text=True, cwd=repo_path, timeout=30
                )
                results['steps'].append({
                    'step': 'add',
                    'success': add_result.returncode == 0,
                    'output': add_result.stdout if add_result.returncode == 0 else add_result.stderr
                })

            # Commit changes
            commit_result = subprocess.run(
                ['git', 'commit', '-m', message],
                capture_output=True, text=True, cwd=repo_path, timeout=30
            )

            results['steps'].append({
                'step': 'commit',
                'success': commit_result.returncode == 0,
                'output': commit_result.stdout if commit_result.returncode == 0 else commit_result.stderr
            })

            if commit_result.returncode != 0:
                # Check if there's nothing to commit
                if 'nothing to commit' in commit_result.stdout:
                    return {
                        'status': 'no_changes',
                        'message': 'No changes to commit',
                        'steps': results['steps']
                    }
                else:
                    return {
                        'status': 'error',
                        'error': commit_result.stderr.strip(),
                        'steps': results['steps']
                    }

            # Push changes if requested
            if push:
                push_result = subprocess.run(
                    ['git', 'push'],
                    capture_output=True, text=True, cwd=repo_path, timeout=60
                )

                results['steps'].append({
                    'step': 'push',
                    'success': push_result.returncode == 0,
                    'output': push_result.stdout if push_result.returncode == 0 else push_result.stderr
                })

                if push_result.returncode != 0:
                    return {
                        'status': 'error',
                        'error': f"Push failed: {push_result.stderr.strip()}",
                        'steps': results['steps']
                    }

            logger.info(f"✅ Successfully committed and {'pushed' if push else 'staged'} changes")
            return {
                'status': 'success',
                'message': f"Successfully committed and {'pushed' if push else 'staged'} changes",
                'steps': results['steps']
            }

        except Exception as e:
            logger.error(f"Error committing and pushing: {e}")
            return {'status': 'error', 'error': str(e)}

    def pull_latest(self, repo_path: Optional[str] = None, branch: Optional[str] = None) -> Dict:
        """Pull latest changes from remote repository"""
        try:
            repo_path = repo_path or str(self.project_root)

            if not (Path(repo_path) / '.git').exists():
                return {
                    'status': 'error',
                    'error': 'Not a git repository'
                }

            cmd = ['git', 'pull']
            if branch:
                cmd.extend(['origin', branch])

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=repo_path, timeout=60
            )

            if result.returncode == 0:
                logger.info(f"✅ Successfully pulled latest changes")
                return {
                    'status': 'success',
                    'message': 'Successfully pulled latest changes',
                    'output': result.stdout.strip()
                }
            else:
                return {
                    'status': 'error',
                    'error': result.stderr.strip()
                }

        except Exception as e:
            logger.error(f"Error pulling latest changes: {e}")
            return {'status': 'error', 'error': str(e)}

    def create_pull_request(self, title: str, body: str = "", base: str = "main",
                           head: Optional[str] = None, repo_path: Optional[str] = None) -> Dict:
        """Create a pull request"""
        try:
            repo_path = repo_path or str(self.project_root)

            cmd = ['gh', 'pr', 'create', '--title', title, '--body', body]
            if base:
                cmd.extend(['--base', base])
            if head:
                cmd.extend(['--head', head])

            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=repo_path, timeout=30
            )

            if result.returncode == 0:
                pr_url = result.stdout.strip()
                logger.info(f"✅ Pull request created: {pr_url}")
                return {
                    'status': 'success',
                    'url': pr_url,
                    'message': 'Pull request created successfully'
                }
            else:
                return {
                    'status': 'error',
                    'error': result.stderr.strip()
                }

        except Exception as e:
            logger.error(f"Error creating pull request: {e}")
            return {'status': 'error', 'error': str(e)}

    def manage_files(self, action: str, files: List[str], repo_path: Optional[str] = None) -> Dict:
        """Manage files in repository (add, remove, move)"""
        try:
            repo_path = repo_path or str(self.project_root)

            if not (Path(repo_path) / '.git').exists():
                return {
                    'status': 'error',
                    'error': 'Not a git repository'
                }

            results = []

            for file_path in files:
                if action == 'add':
                    cmd = ['git', 'add', file_path]
                elif action == 'remove':
                    cmd = ['git', 'rm', file_path]
                elif action == 'unstage':
                    cmd = ['git', 'reset', 'HEAD', file_path]
                else:
                    return {'status': 'error', 'error': f'Unknown action: {action}'}

                result = subprocess.run(
                    cmd, capture_output=True, text=True, cwd=repo_path, timeout=10
                )

                results.append({
                    'file': file_path,
                    'action': action,
                    'success': result.returncode == 0,
                    'output': result.stdout if result.returncode == 0 else result.stderr
                })

            successful_operations = sum(1 for r in results if r['success'])

            return {
                'status': 'success' if successful_operations == len(files) else 'partial',
                'results': results,
                'successful': successful_operations,
                'total': len(files)
            }

        except Exception as e:
            logger.error(f"Error managing files: {e}")
            return {'status': 'error', 'error': str(e)}

    def get_commit_history(self, repo_path: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get commit history for repository"""
        try:
            repo_path = repo_path or str(self.project_root)

            if not (Path(repo_path) / '.git').exists():
                return []

            cmd = ['git', 'log', '--oneline', '--decorate', f'-{limit}']
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=repo_path, timeout=10
            )

            if result.returncode == 0:
                commits = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = line.split(' ', 1)
                        if len(parts) >= 2:
                            commits.append({
                                'hash': parts[0],
                                'message': parts[1],
                                'short_hash': parts[0][:7]
                            })
                return commits
            else:
                logger.error(f"Error getting commit history: {result.stderr}")
                return []

        except Exception as e:
            logger.error(f"Error getting commit history: {e}")
            return []

    def sync_to_github(self, repo_path: Optional[str] = None, message: Optional[str] = None, force_upload: bool = False) -> Dict:
        """Complete sync to GitHub: security scan, add, commit, and push all changes"""
        try:
            logger.info("🔄 Starting complete GitHub sync...")

            # Determine repository path
            if repo_path:
                scan_directory = Path(repo_path)
            else:
                scan_directory = self.project_root

            # SECURITY SCAN BEFORE ANY UPLOAD
            logger.info("🔍 Running security scan before GitHub upload...")
            scanner = SecurityScanner()
            security_report = scanner.scan_directory(scan_directory)

            # Check if upload is safe
            if not security_report['safe_to_upload'] and not force_upload:
                logger.error("🔒 SECURITY BLOCK: Credential leaks detected!")
                scanner.print_report(security_report)

                return {
                    'status': 'security_block',
                    'error': 'Security scan detected potential credential leaks. Upload blocked for safety.',
                    'security_report': security_report,
                    'recommendation': 'Fix security issues or use force_upload=True to override (not recommended)',
                    'critical_issues': security_report['statistics']['critical_issues'],
                    'high_issues': security_report['statistics']['high_issues']
                }

            elif not security_report['safe_to_upload'] and force_upload:
                logger.warning("⚠️ FORCE UPLOAD: Security issues detected but upload forced!")
                print("🚨 WARNING: Uploading despite security issues!")
                scanner.print_report(security_report)

            else:
                logger.info("✅ Security scan passed - safe to upload")

            # Get current status
            status = self.get_repository_status(repo_path)
            if status['status'] == 'not_a_repo':
                return {
                    'status': 'error',
                    'error': 'Directory is not a git repository'
                }

            # Check if there are changes
            if status.get('clean', True):
                return {
                    'status': 'no_changes',
                    'message': 'No changes to sync - repository is clean'
                }

            # Pull latest changes first
            pull_result = self.pull_latest(repo_path)
            if pull_result['status'] == 'error':
                logger.warning(f"Pull failed, continuing anyway: {pull_result['error']}")

            # Commit and push changes
            sync_result = self.commit_and_push(
                repo_path=repo_path,
                message=message,
                add_all=True,
                push=True
            )

            if sync_result['status'] == 'success':
                logger.info("✅ Complete GitHub sync successful")
                return {
                    'status': 'success',
                    'message': 'Successfully synced all changes to GitHub',
                    'details': sync_result,
                    'files_synced': status.get('changes', 0),
                    'security_scan': {
                        'status': security_report['status'],
                        'files_scanned': security_report['statistics']['files_scanned'],
                        'issues_found': security_report['statistics']['issues_found']
                    }
                }
            else:
                return sync_result

        except Exception as e:
            logger.error(f"Error during GitHub sync: {e}")
            return {'status': 'error', 'error': str(e)}

    def get_repository_info(self, repo_name: Optional[str] = None, owner: Optional[str] = None) -> Dict:
        """Get detailed information about a repository"""
        try:
            if repo_name:
                full_name = f"{owner or self.username}/{repo_name}"
                cmd = ['gh', 'repo', 'view', full_name, '--json',
                      'name,description,url,visibility,defaultBranch,updatedAt,stargazerCount']
            else:
                # Get info for current directory
                cmd = ['gh', 'repo', 'view', '--json',
                      'name,description,url,visibility,defaultBranch,updatedAt,stargazerCount']

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {
                    'status': 'error',
                    'error': result.stderr.strip()
                }

        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return {'status': 'error', 'error': str(e)}

    def initialize_repo(self, path: str, remote_url: Optional[str] = None) -> Dict:
        """Initialize a new git repository"""
        try:
            repo_path = Path(path)
            repo_path.mkdir(parents=True, exist_ok=True)

            # Initialize git repo
            result = subprocess.run(
                ['git', 'init'],
                capture_output=True, text=True, cwd=str(repo_path), timeout=10
            )

            if result.returncode != 0:
                return {
                    'status': 'error',
                    'error': f"Failed to initialize git repo: {result.stderr}"
                }

            # Add remote if provided
            if remote_url:
                remote_result = subprocess.run(
                    ['git', 'remote', 'add', 'origin', remote_url],
                    capture_output=True, text=True, cwd=str(repo_path), timeout=10
                )

                if remote_result.returncode != 0:
                    logger.warning(f"Failed to add remote: {remote_result.stderr}")

            logger.info(f"✅ Repository initialized at {repo_path}")
            return {
                'status': 'success',
                'path': str(repo_path),
                'message': 'Repository initialized successfully'
            }

        except Exception as e:
            logger.error(f"Error initializing repository: {e}")
            return {'status': 'error', 'error': str(e)}

def main():
    """Test GitHub manager functionality"""
    print("🧪 Testing GitHub Manager")

    github = GitHubManager()

    # Test basic operations
    print(f"\n👤 Authenticated user: {github.username}")

    # List repositories
    repos = github.list_repositories(limit=5)
    print(f"\n📚 Repositories ({len(repos)}):")
    for repo in repos:
        print(f"  - {repo['name']} ({repo['visibility']})")

    # Get current repository status
    status = github.get_repository_status()
    print(f"\n📊 Current repository status:")
    print(f"  - Path: {status.get('path', 'unknown')}")
    print(f"  - Branch: {status.get('branch', 'unknown')}")
    print(f"  - Changes: {status.get('changes', 0)}")
    print(f"  - Clean: {status.get('clean', False)}")

if __name__ == '__main__':
    main()