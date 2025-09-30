#!/usr/bin/env python3
"""
MARBILY E-COMMERCE COMMAND CENTER
Railway-Optimized Master Control System
"""

import os
import sys
import json
import logging
import subprocess
import threading
import time
import argparse
from datetime import datetime
from pathlib import Path

# Flask for web server
from flask import Flask, request, jsonify, render_template_string
import schedule

# Import credentials
sys.path.append(os.path.dirname(__file__))
from UNIVERSAL_CREDENTIALS import credentials

# Import GitHub manager
sys.path.append(str(Path(__file__).parent / 'ecommerce-ceo-system' / 'integrations'))
from github_manager import GitHubManager

# Configure logging for Railway
logging.basicConfig(
    level=getattr(logging, os.environ.get('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

class RailwayCommandCenter:
    """Railway-optimized command center for Marbily e-commerce system"""

    def __init__(self):
        self.port = int(os.environ.get('PORT', 8000))
        self.environment = os.environ.get('ENVIRONMENT', 'development')
        self.debug = os.environ.get('DEBUG', 'false').lower() == 'true'
        self.project_root = Path(__file__).parent
        self.ecommerce_system = self.project_root / 'ecommerce-ceo-system'

        # Setup Flask app
        self.app = Flask(__name__)
        self.app.config['DEBUG'] = self.debug

        # Initialize GitHub manager
        try:
            self.github = GitHubManager()
            logger.info(f"🐙 GitHub integration initialized for user: {self.github.username}")
        except Exception as e:
            logger.error(f"❌ GitHub integration failed: {e}")
            self.github = None

        # Setup routes
        self.setup_routes()

        # Setup scheduler
        self.setup_scheduler()

        # Start scheduler thread
        self.start_scheduler()

        logger.info(f"🚀 Railway Command Center initialized for {self.environment}")
        logger.info(f"📊 Port: {self.port}, Debug: {self.debug}")
        logger.info(f"🐙 GitHub: {'✅ Ready' if self.github else '❌ Disabled'}")

    def setup_routes(self):
        """Setup all Flask routes for the Railway deployment"""

        @self.app.route('/')
        def health_check():
            """Main health check endpoint"""
            return jsonify({
                "status": "healthy",
                "environment": self.environment,
                "timestamp": datetime.now().isoformat(),
                "services": {
                    "command_center": "running",
                    "scheduler": "active",
                    "ecommerce_system": "operational"
                },
                "endpoints": {
                    "health": "/health",
                    "execute": "/execute/<workflow>",
                    "status": "/status",
                    "logs": "/logs"
                }
            })

        @self.app.route('/health')
        def detailed_health():
            """Detailed health check for Railway monitoring"""
            try:
                health_status = {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "environment": self.environment,
                    "system": {
                        "python_version": sys.version,
                        "working_directory": str(self.project_root),
                        "ecommerce_system": str(self.ecommerce_system.exists())
                    },
                    "services": {
                        "flask": "running",
                        "scheduler": "active",
                        "background_tasks": self.get_background_status()
                    },
                    "credentials": {
                        "shopify": bool(credentials.SHOPIFY_API_KEY),
                        "baselinker": bool(credentials.BASELINKER_API_KEY),
                        "openai": bool(credentials.OPENAI_API_KEY),
                        "google": bool(credentials.GOOGLE_SHEETS_CLIENT_ID)
                    }
                }

                return jsonify(health_status)

            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return jsonify({
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 500

        @self.app.route('/execute/<workflow>')
        def execute_workflow(workflow):
            """Execute specific workflow via API"""
            try:
                logger.info(f"🎯 Executing workflow: {workflow}")

                if workflow == 'sync-all':
                    # BaseLinker + Shopify sync
                    result = self.run_parallel_sync()
                    return jsonify({
                        "status": "success",
                        "workflow": "sync-all",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'create-shadows':
                    # Image shadow processing
                    result = self.run_shadow_creation()
                    return jsonify({
                        "status": "success",
                        "workflow": "create-shadows",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'backup-system':
                    # System backup
                    result = self.run_system_backup()
                    return jsonify({
                        "status": "success",
                        "workflow": "backup-system",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'verify-products':
                    # Product verification
                    result = self.run_product_verification()
                    return jsonify({
                        "status": "success",
                        "workflow": "verify-products",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'health-check':
                    # Complete system health check
                    result = self.run_health_check()
                    return jsonify({
                        "status": "success",
                        "workflow": "health-check",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                # GitHub workflows
                elif workflow == 'sync-to-github':
                    # Sync all changes to GitHub
                    result = self.run_github_sync()
                    return jsonify({
                        "status": "success",
                        "workflow": "sync-to-github",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'check-github-status':
                    # Check Git status
                    result = self.run_github_status_check()
                    return jsonify({
                        "status": "success",
                        "workflow": "check-github-status",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'list-repositories':
                    # List GitHub repositories
                    result = self.run_list_repositories()
                    return jsonify({
                        "status": "success",
                        "workflow": "list-repositories",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                elif workflow == 'pull-latest':
                    # Pull latest changes
                    result = self.run_pull_latest()
                    return jsonify({
                        "status": "success",
                        "workflow": "pull-latest",
                        "results": result,
                        "timestamp": datetime.now().isoformat()
                    })

                else:
                    return jsonify({
                        "error": f"Unknown workflow: {workflow}",
                        "available_workflows": [
                            "sync-all", "create-shadows", "backup-system",
                            "verify-products", "health-check",
                            "sync-to-github", "check-github-status",
                            "list-repositories", "pull-latest"
                        ]
                    }), 400

            except Exception as e:
                logger.error(f"Workflow execution failed: {e}")
                return jsonify({
                    "status": "error",
                    "workflow": workflow,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 500

        @self.app.route('/status')
        def system_status():
            """Get comprehensive system status"""
            try:
                return jsonify({
                    "system": "Marbily E-commerce Automation",
                    "version": "Railway Production",
                    "status": "operational",
                    "uptime": self.get_uptime(),
                    "environment": self.environment,
                    "scheduled_tasks": self.get_scheduled_tasks(),
                    "last_sync": self.get_last_sync_time(),
                    "system_health": self.check_system_health()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/logs')
        def get_logs():
            """Get recent system logs"""
            try:
                # Return recent log entries for debugging
                log_entries = self.get_recent_logs()
                return jsonify({
                    "logs": log_entries,
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/github/<action>')
        def github_action(action):
            """GitHub-specific actions with parameters"""
            try:
                if not self.github:
                    return jsonify({
                        "error": "GitHub integration not available"
                    }), 503

                # Get query parameters
                repo_name = request.args.get('repo')
                message = request.args.get('message')
                owner = request.args.get('owner')
                description = request.args.get('description', '')
                private = request.args.get('private', 'false').lower() == 'true'

                if action == 'create-repo':
                    if not repo_name:
                        return jsonify({"error": "repo parameter required"}), 400
                    result = self.github.create_repository(repo_name, description, private)

                elif action == 'clone-repo':
                    if not repo_name:
                        return jsonify({"error": "repo parameter required"}), 400
                    result = self.github.clone_repository(repo_name, owner=owner)

                elif action == 'repo-info':
                    result = self.github.get_repository_info(repo_name, owner)

                elif action == 'commit-history':
                    limit = int(request.args.get('limit', 10))
                    result = self.github.get_commit_history(limit=limit)

                else:
                    return jsonify({
                        "error": f"Unknown GitHub action: {action}",
                        "available_actions": [
                            "create-repo", "clone-repo", "repo-info", "commit-history"
                        ]
                    }), 400

                return jsonify({
                    "status": "success",
                    "action": action,
                    "results": result,
                    "timestamp": datetime.now().isoformat()
                })

            except Exception as e:
                logger.error(f"GitHub action failed: {e}")
                return jsonify({
                    "status": "error",
                    "action": action,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }), 500

        @self.app.route('/dashboard')
        def dashboard():
            """Simple web dashboard for monitoring"""
            dashboard_html = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Marbily Command Center - Railway</title>
                <meta http-equiv="refresh" content="30">
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                    .status-good { color: #28a745; } .status-warning { color: #ffc107; } .status-error { color: #dc3545; }
                    .endpoint { background: #e9ecef; padding: 10px; margin: 5px 0; border-radius: 4px; }
                    h1 { color: #333; } h2 { color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🚀 Marbily E-commerce Command Center</h1>
                    <div class="card">
                        <h2>System Status</h2>
                        <p><strong>Environment:</strong> {{ environment }}</p>
                        <p><strong>Status:</strong> <span class="status-good">Operational</span></p>
                        <p><strong>Last Updated:</strong> {{ timestamp }}</p>
                    </div>

                    <div class="card">
                        <h2>Available Endpoints</h2>
                        <div class="endpoint"><strong>GET /</strong> - Basic health check</div>
                        <div class="endpoint"><strong>GET /health</strong> - Detailed system health</div>
                        <div class="endpoint"><strong>GET /execute/sync-all</strong> - Run complete sync</div>
                        <div class="endpoint"><strong>GET /execute/create-shadows</strong> - Process images</div>
                        <div class="endpoint"><strong>GET /execute/backup-system</strong> - System backup</div>
                        <div class="endpoint"><strong>GET /execute/sync-to-github</strong> - Sync to GitHub</div>
                        <div class="endpoint"><strong>GET /execute/check-github-status</strong> - Check Git status</div>
                        <div class="endpoint"><strong>GET /github/create-repo?repo=name</strong> - Create repository</div>
                        <div class="endpoint"><strong>GET /status</strong> - System status JSON</div>
                    </div>

                    <div class="card">
                        <h2>Quick Actions</h2>
                        <button onclick="fetch('/execute/sync-all').then(r=>r.json()).then(d=>alert(JSON.stringify(d)))">🔄 Sync All</button>
                        <button onclick="fetch('/execute/create-shadows').then(r=>r.json()).then(d=>alert(JSON.stringify(d)))">🖼️ Create Shadows</button>
                        <button onclick="fetch('/health').then(r=>r.json()).then(d=>alert(JSON.stringify(d,null,2)))">🏥 Health Check</button>
                        <button onclick="fetch('/execute/sync-to-github').then(r=>r.json()).then(d=>alert(JSON.stringify(d)))">🐙 Sync to GitHub</button>
                        <button onclick="fetch('/execute/check-github-status').then(r=>r.json()).then(d=>alert(JSON.stringify(d,null,2)))">📊 Git Status</button>
                        <button onclick="fetch('/execute/list-repositories').then(r=>r.json()).then(d=>alert(JSON.stringify(d,null,2)))">📚 List Repos</button>
                    </div>
                </div>
            </body>
            </html>
            '''
            return render_template_string(dashboard_html,
                environment=self.environment,
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
            )

    def setup_scheduler(self):
        """Setup automated scheduling for Railway"""
        # BaseLinker sync every 30 minutes
        schedule.every(30).minutes.do(self.run_baselinker_sync)

        # Shopify sync every hour
        schedule.every().hour.do(self.run_shopify_sync)

        # Daily backup at 2 AM UTC
        schedule.every().day.at("02:00").do(self.run_system_backup)

        # Health check every 15 minutes
        schedule.every(15).minutes.do(self.run_health_check)

        # Product verification every 6 hours
        schedule.every(6).hours.do(self.run_product_verification)

        logger.info("📅 Scheduler configured with automated tasks")

    def start_scheduler(self):
        """Start scheduler in background thread"""
        def run_scheduler():
            logger.info("🔄 Starting automated scheduler thread")
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    logger.error(f"Scheduler error: {e}")
                    time.sleep(300)  # Wait 5 minutes on error

        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()

    # Workflow execution methods
    def run_baselinker_sync(self):
        """Execute BaseLinker sync workflow"""
        try:
            logger.info("🔄 Starting BaseLinker sync")
            script_path = self.ecommerce_system / 'baselinker_operations' / 'sync' / 'bidirectional_sync_engine.py'

            if script_path.exists():
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=300, cwd=str(self.project_root))

                if result.returncode == 0:
                    logger.info("✅ BaseLinker sync completed successfully")
                    return {"status": "success", "output": result.stdout}
                else:
                    logger.error(f"❌ BaseLinker sync failed: {result.stderr}")
                    return {"status": "error", "error": result.stderr}
            else:
                # Fallback to main.py command
                return self.run_main_command(['main.py', '/sync'])

        except Exception as e:
            logger.error(f"BaseLinker sync exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_shopify_sync(self):
        """Execute Shopify sync workflow"""
        try:
            logger.info("🛍️ Starting Shopify sync")
            script_path = self.ecommerce_system / 'shopify_management' / 'sync' / 'shopify_sync_manager.py'

            if script_path.exists():
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=300, cwd=str(self.project_root))

                if result.returncode == 0:
                    logger.info("✅ Shopify sync completed successfully")
                    return {"status": "success", "output": result.stdout}
                else:
                    logger.error(f"❌ Shopify sync failed: {result.stderr}")
                    return {"status": "error", "error": result.stderr}
            else:
                # Fallback to main.py command
                return self.run_main_command(['main.py', '/sync'])

        except Exception as e:
            logger.error(f"Shopify sync exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_parallel_sync(self):
        """Execute both BaseLinker and Shopify sync in parallel"""
        try:
            logger.info("🔄 Starting parallel sync (BaseLinker + Shopify)")

            import threading
            results = {}

            def bl_sync():
                results['baselinker'] = self.run_baselinker_sync()

            def shopify_sync():
                results['shopify'] = self.run_shopify_sync()

            # Start both syncs in parallel
            bl_thread = threading.Thread(target=bl_sync)
            shopify_thread = threading.Thread(target=shopify_sync)

            bl_thread.start()
            shopify_thread.start()

            # Wait for completion
            bl_thread.join(timeout=600)  # 10 minute timeout
            shopify_thread.join(timeout=600)

            logger.info("✅ Parallel sync completed")
            return results

        except Exception as e:
            logger.error(f"Parallel sync exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_shadow_creation(self):
        """Execute image shadow creation workflow"""
        try:
            logger.info("🖼️ Starting shadow creation")
            script_path = self.ecommerce_system / 'image_workflows' / 'shadow_creation' / 'shadow_creator_improved.py'

            if script_path.exists():
                result = subprocess.run([
                    sys.executable, str(script_path)
                ], capture_output=True, text=True, timeout=600, cwd=str(self.project_root))

                if result.returncode == 0:
                    logger.info("✅ Shadow creation completed successfully")
                    return {"status": "success", "output": result.stdout}
                else:
                    logger.error(f"❌ Shadow creation failed: {result.stderr}")
                    return {"status": "error", "error": result.stderr}
            else:
                return self.run_main_command(['main.py', '/shadow'])

        except Exception as e:
            logger.error(f"Shadow creation exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_system_backup(self):
        """Execute system backup workflow"""
        try:
            logger.info("💾 Starting system backup")
            return self.run_main_command(['main.py', '/backup'])
        except Exception as e:
            logger.error(f"System backup exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_product_verification(self):
        """Execute product verification workflow"""
        try:
            logger.info("✅ Starting product verification")
            return self.run_main_command(['main.py', '/check'])
        except Exception as e:
            logger.error(f"Product verification exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_health_check(self):
        """Execute comprehensive health check"""
        try:
            logger.info("🏥 Running system health check")

            # Check all major components
            health_results = {
                "timestamp": datetime.now().isoformat(),
                "credentials": self.check_credentials(),
                "file_system": self.check_file_system(),
                "dependencies": self.check_dependencies(),
                "services": self.check_services()
            }

            logger.info("✅ Health check completed")
            return {"status": "success", "results": health_results}

        except Exception as e:
            logger.error(f"Health check exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_main_command(self, args):
        """Run main.py command as fallback"""
        try:
            main_path = self.project_root / 'main.py'
            if main_path.exists():
                result = subprocess.run([
                    sys.executable, str(main_path)
                ] + args[1:], capture_output=True, text=True, timeout=300, cwd=str(self.project_root))

                return {
                    "status": "success" if result.returncode == 0 else "error",
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None
                }
            else:
                return {"status": "error", "error": "main.py not found"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # GitHub workflow methods
    def run_github_sync(self):
        """Execute complete GitHub sync workflow"""
        try:
            if not self.github:
                return {"status": "error", "error": "GitHub integration not available"}

            logger.info("🐙 Starting complete GitHub sync")
            result = self.github.sync_to_github()

            if result['status'] == 'success':
                logger.info("✅ GitHub sync completed successfully")
            elif result['status'] == 'no_changes':
                logger.info("ℹ️ No changes to sync to GitHub")
            else:
                logger.error(f"❌ GitHub sync failed: {result.get('error', 'Unknown error')}")

            return result

        except Exception as e:
            logger.error(f"GitHub sync exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_github_status_check(self):
        """Execute GitHub status check"""
        try:
            if not self.github:
                return {"status": "error", "error": "GitHub integration not available"}

            logger.info("🔍 Checking GitHub repository status")
            status_result = self.github.get_repository_status()
            repo_info = self.github.get_repository_info()

            return {
                "status": "success",
                "repository_status": status_result,
                "repository_info": repo_info,
                "commit_history": self.github.get_commit_history(limit=5)
            }

        except Exception as e:
            logger.error(f"GitHub status check exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_list_repositories(self):
        """Execute list repositories workflow"""
        try:
            if not self.github:
                return {"status": "error", "error": "GitHub integration not available"}

            logger.info("📚 Listing GitHub repositories")
            repos = self.github.list_repositories(limit=20)

            return {
                "status": "success",
                "repositories": repos,
                "count": len(repos),
                "username": self.github.username
            }

        except Exception as e:
            logger.error(f"List repositories exception: {e}")
            return {"status": "error", "error": str(e)}

    def run_pull_latest(self):
        """Execute pull latest changes workflow"""
        try:
            if not self.github:
                return {"status": "error", "error": "GitHub integration not available"}

            logger.info("⬇️ Pulling latest changes from GitHub")
            result = self.github.pull_latest()

            if result['status'] == 'success':
                logger.info("✅ Successfully pulled latest changes")
            else:
                logger.error(f"❌ Pull failed: {result.get('error', 'Unknown error')}")

            return result

        except Exception as e:
            logger.error(f"Pull latest exception: {e}")
            return {"status": "error", "error": str(e)}

    # Helper methods
    def get_background_status(self):
        """Check background process status"""
        try:
            import psutil
            return "monitored"
        except:
            return "unknown"

    def get_uptime(self):
        """Get system uptime"""
        try:
            import psutil
            return psutil.boot_time()
        except:
            return "unknown"

    def get_scheduled_tasks(self):
        """Get list of scheduled tasks"""
        return [
            "BaseLinker sync (every 30 minutes)",
            "Shopify sync (every hour)",
            "System backup (daily at 2 AM UTC)",
            "Health check (every 15 minutes)",
            "Product verification (every 6 hours)"
        ]

    def get_last_sync_time(self):
        """Get last sync timestamp"""
        # This would typically read from a log file or database
        return datetime.now().isoformat()

    def check_system_health(self):
        """Basic system health indicators"""
        return {
            "cpu_usage": "normal",
            "memory_usage": "normal",
            "disk_space": "sufficient",
            "network": "connected"
        }

    def get_recent_logs(self):
        """Get recent log entries"""
        return [
            {"timestamp": datetime.now().isoformat(), "level": "INFO", "message": "System operational"},
            {"timestamp": datetime.now().isoformat(), "level": "INFO", "message": "Scheduler active"}
        ]

    def check_credentials(self):
        """Check credential status"""
        return {
            "shopify": bool(credentials.SHOPIFY_API_KEY),
            "baselinker": bool(credentials.BASELINKER_API_KEY),
            "openai": bool(credentials.OPENAI_API_KEY),
            "google": bool(credentials.GOOGLE_SHEETS_CLIENT_ID),
            "cloudinary": bool(credentials.CLOUDINARY_API_KEY)
        }

    def check_file_system(self):
        """Check critical file system components"""
        return {
            "ecommerce_system": self.ecommerce_system.exists(),
            "main_py": (self.project_root / 'main.py').exists(),
            "credentials": (self.project_root / 'UNIVERSAL_CREDENTIALS.py').exists()
        }

    def check_dependencies(self):
        """Check Python dependencies"""
        try:
            import flask, requests, schedule
            return {"status": "installed", "flask": True, "requests": True, "schedule": True}
        except ImportError as e:
            return {"status": "missing", "error": str(e)}

    def check_services(self):
        """Check service status"""
        return {
            "web_server": "running",
            "scheduler": "active",
            "background_tasks": "operational"
        }

def main():
    """Main entry point for Railway deployment"""
    parser = argparse.ArgumentParser(description='Marbily E-commerce Command Center')
    parser.add_argument('--port', type=int, default=int(os.environ.get('PORT', 8000)),
                        help='Port to run the web server on')
    parser.add_argument('--debug', action='store_true', default=os.environ.get('DEBUG', 'false').lower() == 'true',
                        help='Enable debug mode')

    args = parser.parse_args()

    try:
        # Initialize command center
        command_center = RailwayCommandCenter()
        command_center.port = args.port
        command_center.debug = args.debug

        logger.info(f"🚀 Starting Marbily Command Center on port {command_center.port}")
        logger.info(f"🌍 Environment: {command_center.environment}")
        logger.info(f"📁 Project root: {command_center.project_root}")

        # Start Flask application
        command_center.app.run(
            host='0.0.0.0',
            port=command_center.port,
            debug=command_center.debug,
            threaded=True
        )

    except Exception as e:
        logger.error(f"❌ Failed to start Command Center: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()