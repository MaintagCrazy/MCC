#!/usr/bin/env python3
"""
Test GitHub Integration for Marbily Command Center
Comprehensive test suite for GitHub functionality
"""

import sys
import requests
import time
import threading
from pathlib import Path

# Import command center
sys.path.append(str(Path(__file__).parent))
from COMMAND_CENTER import RailwayCommandCenter

def test_github_integration():
    """Test GitHub integration functionality"""
    print("🧪 Testing GitHub Integration")
    print("=" * 50)

    # Initialize command center
    print("1. Initializing Command Center...")
    try:
        command_center = RailwayCommandCenter()
        print(f"   ✅ Command Center initialized")
        print(f"   🐙 GitHub integration: {'✅ Ready' if command_center.github else '❌ Failed'}")

        if not command_center.github:
            print("❌ GitHub integration not available, skipping tests")
            return

    except Exception as e:
        print(f"   ❌ Failed to initialize: {e}")
        return

    # Test GitHub manager directly
    print("\n2. Testing GitHub Manager...")
    try:
        github = command_center.github

        # Test basic functionality
        print(f"   👤 Authenticated user: {github.username}")

        # Test repository listing
        repos = github.list_repositories(limit=5)
        print(f"   📚 Found {len(repos)} repositories")

        # Test repository status
        status = github.get_repository_status()
        print(f"   📊 Repository status: {status.get('status', 'unknown')}")
        print(f"   📝 Changes: {status.get('changes', 0)} files")

        print("   ✅ GitHub Manager tests passed")

    except Exception as e:
        print(f"   ❌ GitHub Manager test failed: {e}")

    # Test workflow methods
    print("\n3. Testing Workflow Methods...")
    try:
        # Test GitHub status check
        status_result = command_center.run_github_status_check()
        print(f"   📊 Status check: {status_result.get('status', 'unknown')}")

        # Test repository listing
        list_result = command_center.run_list_repositories()
        print(f"   📚 List repos: {list_result.get('status', 'unknown')}")
        print(f"   📚 Found {list_result.get('count', 0)} repositories")

        print("   ✅ Workflow method tests passed")

    except Exception as e:
        print(f"   ❌ Workflow method test failed: {e}")

    # Start web server for API tests
    print("\n4. Testing API Endpoints...")
    try:
        # Start server in background thread
        def run_server():
            command_center.app.run(host='localhost', port=8001, debug=False, threaded=True)

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait for server to start
        time.sleep(2)

        base_url = "http://localhost:8001"

        # Test basic health endpoint
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Basic health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {response.status_code}")

        # Test GitHub status endpoint
        response = requests.get(f"{base_url}/execute/check-github-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ GitHub status endpoint: {data.get('status', 'unknown')}")
        else:
            print(f"   ❌ GitHub status endpoint failed: {response.status_code}")

        # Test list repositories endpoint
        response = requests.get(f"{base_url}/execute/list-repositories", timeout=10)
        if response.status_code == 200:
            data = response.json()
            count = data.get('results', {}).get('count', 0)
            print(f"   ✅ List repositories endpoint: found {count} repos")
        else:
            print(f"   ❌ List repositories endpoint failed: {response.status_code}")

        # Test GitHub action endpoint
        response = requests.get(f"{base_url}/github/repo-info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ GitHub action endpoint: {data.get('status', 'unknown')}")
        else:
            print(f"   ❌ GitHub action endpoint failed: {response.status_code}")

        print("   ✅ API endpoint tests completed")

    except Exception as e:
        print(f"   ❌ API endpoint test failed: {e}")

    # Test GitHub commands
    print("\n5. Testing GitHub Commands...")
    try:
        from ecommerce_ceo_system.integrations.github_commands import GitHubCommandProcessor

        processor = GitHubCommandProcessor()
        print(f"   🎯 Command processor initialized with {len(processor.get_available_commands())} commands")

        # Test various commands
        test_commands = [
            "check status",
            "list repos",
            "repo info"
        ]

        for command in test_commands:
            result = processor.process_command(command)
            status = result.get('status', 'unknown')
            print(f"   🎯 '{command}': {status}")

        print("   ✅ GitHub command tests passed")

    except Exception as e:
        print(f"   ❌ GitHub command test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 GitHub Integration Test Complete!")
    print("\n📋 Available GitHub Commands:")
    print("  • sync to github     - Commit and push all changes")
    print("  • check status       - Show Git repository status")
    print("  • list repos         - Show your GitHub repositories")
    print("  • create repo <name> - Create new repository")
    print("  • clone repo <name>  - Clone repository locally")
    print("  • pull latest        - Pull latest changes")
    print("  • repo info          - Show repository information")
    print("  • commit history     - Show recent commits")

    print("\n🌐 Available API Endpoints:")
    print("  • GET /execute/sync-to-github")
    print("  • GET /execute/check-github-status")
    print("  • GET /execute/list-repositories")
    print("  • GET /execute/pull-latest")
    print("  • GET /github/create-repo?repo=<name>")
    print("  • GET /github/clone-repo?repo=<name>")
    print("  • GET /github/repo-info")

if __name__ == '__main__':
    test_github_integration()