#!/usr/bin/env python3
"""
Security Scanner for Marbily E-commerce System
Comprehensive credential leak detection before GitHub operations
"""

import os
import re
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SecurityIssue:
    """Represents a security issue found in code"""
    file_path: str
    line_number: int
    issue_type: str
    matched_text: str
    severity: str
    description: str

class SecurityScanner:
    """Advanced security scanner for credential leak detection"""

    def __init__(self):
        self.issues = []
        self.scan_stats = {
            'files_scanned': 0,
            'issues_found': 0,
            'critical_issues': 0,
            'high_issues': 0,
            'medium_issues': 0,
            'low_issues': 0
        }

        # Comprehensive credential patterns
        self.credential_patterns = {
            # API Keys and Tokens
            'openai_api_key': {
                'pattern': r'sk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}',
                'severity': 'CRITICAL',
                'description': 'OpenAI API Key detected'
            },
            'anthropic_api_key': {
                'pattern': r'sk-ant-api03-[A-Za-z0-9_-]{95}',
                'severity': 'CRITICAL',
                'description': 'Anthropic Claude API Key detected'
            },
            'shopify_token': {
                'pattern': r'shpat_[a-fA-F0-9]{32}',
                'severity': 'CRITICAL',
                'description': 'Shopify Access Token detected'
            },
            'github_token': {
                'pattern': r'ghp_[A-Za-z0-9]{36}',
                'severity': 'CRITICAL',
                'description': 'GitHub Personal Access Token detected'
            },
            'github_token_classic': {
                'pattern': r'[a-fA-F0-9]{40}',
                'severity': 'HIGH',
                'description': 'Potential GitHub Classic Token detected'
            },
            'replicate_token': {
                'pattern': r'r8_[A-Za-z0-9]{40}',
                'severity': 'HIGH',
                'description': 'Replicate API Token detected'
            },
            'openrouter_key': {
                'pattern': r'sk-or-[A-Za-z0-9_-]{43}',
                'severity': 'HIGH',
                'description': 'OpenRouter API Key detected'
            },
            'cloudinary_key': {
                'pattern': r'[0-9]{15}:[A-Za-z0-9_-]{27}',
                'severity': 'HIGH',
                'description': 'Cloudinary API Key detected'
            },

            # Google Services
            'google_oauth_client_id': {
                'pattern': r'[0-9]+-[a-zA-Z0-9_]{32}\.apps\.googleusercontent\.com',
                'severity': 'HIGH',
                'description': 'Google OAuth Client ID detected'
            },
            'google_oauth_secret': {
                'pattern': r'GOCSPX-[A-Za-z0-9_-]{28}',
                'severity': 'CRITICAL',
                'description': 'Google OAuth Client Secret detected'
            },
            'google_api_key': {
                'pattern': r'AIza[0-9A-Za-z_-]{35}',
                'severity': 'HIGH',
                'description': 'Google API Key detected'
            },

            # Database Credentials
            'mysql_connection': {
                'pattern': r'mysql://[^:]+:[^@]+@[^/]+/[^?\s]+',
                'severity': 'CRITICAL',
                'description': 'MySQL connection string with credentials detected'
            },
            'postgres_connection': {
                'pattern': r'postgres://[^:]+:[^@]+@[^/]+/[^?\s]+',
                'severity': 'CRITICAL',
                'description': 'PostgreSQL connection string with credentials detected'
            },
            'supabase_key': {
                'pattern': r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
                'severity': 'HIGH',
                'description': 'Potential Supabase/JWT Token detected'
            },

            # Email and SMTP
            'email_password': {
                'pattern': r'(?i)(smtp|email|mail).*password.*["\']([^"\']{8,})["\']',
                'severity': 'HIGH',
                'description': 'Email/SMTP password detected'
            },

            # Generic Patterns
            'private_key': {
                'pattern': r'-----BEGIN[A-Z ]+PRIVATE KEY-----',
                'severity': 'CRITICAL',
                'description': 'Private key detected'
            },
            'api_key_generic': {
                'pattern': r'(?i)(api[_-]?key|apikey|secret[_-]?key|secretkey)["\'\s]*[:=]["\'\s]*([A-Za-z0-9_-]{20,})',
                'severity': 'MEDIUM',
                'description': 'Generic API key pattern detected'
            },
            'password_generic': {
                'pattern': r'(?i)(password|passwd|pwd)["\'\s]*[:=]["\'\s]*([^"\'\s]{8,})',
                'severity': 'MEDIUM',
                'description': 'Generic password pattern detected'
            },
            'token_generic': {
                'pattern': r'(?i)(token|secret)["\'\s]*[:=]["\'\s]*([A-Za-z0-9_-]{20,})',
                'severity': 'MEDIUM',
                'description': 'Generic token pattern detected'
            }
        }

        # Files to exclude from scanning
        self.exclude_patterns = [
            r'\.git/',
            r'__pycache__/',
            r'\.pytest_cache/',
            r'node_modules/',
            r'venv/',
            r'env/',
            r'\.env',
            r'\.jpg$',
            r'\.png$',
            r'\.gif$',
            r'\.pdf$',
            r'\.xlsx?$',
            r'\.docx?$',
            r'\.zip$',
            r'\.tar\.gz$',
            r'\.log$',
            r'\.sqlite$',
            r'\.db$',
            r'\.pickle$',
            r'\.pkl$',
            r'security_scanner\.py$',  # Don't scan this file itself
            r'UNIVERSAL_CREDENTIALS_TEMPLATE\.py$',  # Template file is safe
        ]

        # File extensions to scan
        self.scan_extensions = [
            '.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.yaml', '.yml',
            '.md', '.txt', '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat',
            '.html', '.css', '.scss', '.sass', '.php', '.rb', '.go', '.rs',
            '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.swift', '.kt',
            '.sql', '.xml', '.toml', '.ini', '.cfg', '.conf'
        ]

    def should_exclude_file(self, file_path: str) -> bool:
        """Check if file should be excluded from scanning"""
        file_path_str = str(file_path)

        for pattern in self.exclude_patterns:
            if re.search(pattern, file_path_str):
                return True

        # Check if file has scannable extension
        file_ext = Path(file_path).suffix.lower()
        if file_ext and file_ext not in self.scan_extensions:
            return True

        return False

    def scan_file(self, file_path: Path) -> List[SecurityIssue]:
        """Scan a single file for security issues"""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            for line_num, line in enumerate(lines, 1):
                # Skip empty lines and comments (basic)
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('#'):
                    continue

                # Check each credential pattern
                for pattern_name, pattern_info in self.credential_patterns.items():
                    matches = re.finditer(pattern_info['pattern'], line, re.IGNORECASE)

                    for match in matches:
                        # Additional validation to reduce false positives
                        if self._is_valid_match(pattern_name, match.group(), line):
                            issue = SecurityIssue(
                                file_path=str(file_path),
                                line_number=line_num,
                                issue_type=pattern_name,
                                matched_text=match.group(),
                                severity=pattern_info['severity'],
                                description=pattern_info['description']
                            )
                            issues.append(issue)

        except Exception as e:
            logger.warning(f"Could not scan file {file_path}: {e}")

        return issues

    def _is_valid_match(self, pattern_name: str, match_text: str, line: str) -> bool:
        """Additional validation to reduce false positives"""

        # Skip obvious placeholders and templates
        placeholder_patterns = [
            r'YOUR_.*_HERE',
            r'REPLACE_.*',
            r'INSERT_.*',
            r'PLACEHOLDER',
            r'EXAMPLE',
            r'TEST',
            r'DEMO',
            r'FAKE',
            r'SAMPLE'
        ]

        for placeholder in placeholder_patterns:
            if re.search(placeholder, match_text, re.IGNORECASE):
                return False

        # Skip comments that mention these patterns as examples
        if re.search(r'#.*' + re.escape(match_text), line):
            return False

        # Skip documentation strings
        if '"""' in line or "'''" in line:
            return False

        # Skip URL examples
        if 'http' in line and 'example' in line.lower():
            return False

        return True

    def scan_directory(self, directory: Path) -> Dict:
        """Scan entire directory for security issues"""
        logger.info(f"🔍 Starting security scan of {directory}")

        self.issues = []
        self.scan_stats = {key: 0 for key in self.scan_stats.keys()}

        # Get all files to scan
        all_files = []
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(re.search(pattern, os.path.join(root, d))
                                                 for pattern in self.exclude_patterns)]

            for file in files:
                file_path = Path(os.path.join(root, file))
                if not self.should_exclude_file(file_path):
                    all_files.append(file_path)

        # Scan each file
        for file_path in all_files:
            self.scan_stats['files_scanned'] += 1
            file_issues = self.scan_file(file_path)
            self.issues.extend(file_issues)

            # Update severity stats
            for issue in file_issues:
                self.scan_stats['issues_found'] += 1
                if issue.severity == 'CRITICAL':
                    self.scan_stats['critical_issues'] += 1
                elif issue.severity == 'HIGH':
                    self.scan_stats['high_issues'] += 1
                elif issue.severity == 'MEDIUM':
                    self.scan_stats['medium_issues'] += 1
                else:
                    self.scan_stats['low_issues'] += 1

        return self._generate_report()

    def _generate_report(self) -> Dict:
        """Generate comprehensive security scan report"""
        # Group issues by file
        issues_by_file = {}
        for issue in self.issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)

        # Determine overall security status
        if self.scan_stats['critical_issues'] > 0:
            status = 'CRITICAL'
            recommendation = 'STOP: Critical security issues found. Do not proceed with GitHub upload.'
        elif self.scan_stats['high_issues'] > 0:
            status = 'HIGH_RISK'
            recommendation = 'WARNING: High-risk security issues found. Review before proceeding.'
        elif self.scan_stats['medium_issues'] > 0:
            status = 'MEDIUM_RISK'
            recommendation = 'CAUTION: Medium-risk security issues found. Consider review.'
        else:
            status = 'SECURE'
            recommendation = 'OK: No significant security issues detected. Safe to proceed.'

        return {
            'status': status,
            'recommendation': recommendation,
            'statistics': self.scan_stats,
            'issues_by_file': issues_by_file,
            'issues_summary': self._create_issues_summary(),
            'safe_to_upload': status in ['SECURE', 'MEDIUM_RISK']
        }

    def _create_issues_summary(self) -> List[Dict]:
        """Create summary of all issues for quick review"""
        summary = []
        for issue in self.issues:
            summary.append({
                'file': issue.file_path,
                'line': issue.line_number,
                'type': issue.issue_type,
                'severity': issue.severity,
                'description': issue.description,
                'preview': issue.matched_text[:50] + '...' if len(issue.matched_text) > 50 else issue.matched_text
            })
        return summary

    def print_report(self, report: Dict) -> None:
        """Print formatted security scan report"""
        print("\n" + "="*60)
        print("🔒 SECURITY SCAN REPORT")
        print("="*60)

        # Status
        status_emoji = {
            'SECURE': '✅',
            'MEDIUM_RISK': '⚠️',
            'HIGH_RISK': '🚨',
            'CRITICAL': '🔥'
        }

        print(f"{status_emoji.get(report['status'], '❓')} Status: {report['status']}")
        print(f"📋 {report['recommendation']}")
        print()

        # Statistics
        stats = report['statistics']
        print(f"📊 Scan Statistics:")
        print(f"   Files scanned: {stats['files_scanned']}")
        print(f"   Issues found: {stats['issues_found']}")
        print(f"   🔥 Critical: {stats['critical_issues']}")
        print(f"   🚨 High: {stats['high_issues']}")
        print(f"   ⚠️  Medium: {stats['medium_issues']}")
        print(f"   ℹ️  Low: {stats['low_issues']}")
        print()

        # Issues summary
        if report['issues_summary']:
            print("🚨 Security Issues Found:")
            print("-" * 40)

            for issue in report['issues_summary']:
                severity_emoji = {
                    'CRITICAL': '🔥',
                    'HIGH': '🚨',
                    'MEDIUM': '⚠️',
                    'LOW': 'ℹ️'
                }

                print(f"{severity_emoji.get(issue['severity'], '❓')} {issue['severity']}")
                print(f"   📁 File: {issue['file']}")
                print(f"   📍 Line: {issue['line']}")
                print(f"   🏷️  Type: {issue['type']}")
                print(f"   📝 Description: {issue['description']}")
                print(f"   👁️  Preview: {issue['preview']}")
                print()

        # Final recommendation
        print("="*60)
        if report['safe_to_upload']:
            print("✅ SAFE TO UPLOAD TO GITHUB")
        else:
            print("❌ NOT SAFE - RESOLVE SECURITY ISSUES FIRST")
        print("="*60)

def scan_before_github_upload(directory: str = None) -> bool:
    """
    Main function to scan for credentials before GitHub upload
    Returns True if safe to upload, False if security issues found
    """
    if directory is None:
        # Auto-detect project root
        current_dir = Path.cwd()
        if current_dir.name == 'ecommerce-ceo-system':
            directory = current_dir.parent
        else:
            directory = current_dir

    scanner = SecurityScanner()
    report = scanner.scan_directory(Path(directory))
    scanner.print_report(report)

    return report['safe_to_upload']

if __name__ == '__main__':
    """Run security scan from command line"""
    import argparse

    parser = argparse.ArgumentParser(description='Security scanner for credential leak detection')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current)')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')

    args = parser.parse_args()

    scanner = SecurityScanner()
    report = scanner.scan_directory(Path(args.directory))

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        scanner.print_report(report)

    # Exit with error code if security issues found
    sys.exit(0 if report['safe_to_upload'] else 1)