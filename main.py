#!/usr/bin/env python3
"""
Marbily E-commerce Main Command Dispatcher
Single entry point for all workflow automation
"""

import sys
import os
import json

def load_command_config():
    """Load command configuration from .claude_code_commands.json"""
    config_file = os.path.join(os.path.dirname(__file__), '.claude_code_commands.json')
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Command configuration file not found")
        return {}

def handle_catalog_command_wrapper(subcommand=None, args=None):
    """Handle catalog-related commands"""
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'Catalog PDF'))
    from catalog import handle_catalog_command
    
    if not subcommand:
        subcommand = "generate"
    
    return handle_catalog_command(subcommand, args)

def handle_email_command_wrapper(subcommand=None, args=None):
    """Handle email intelligence commands"""
    import subprocess
    import sys
    import os

    # Use the virtual environment with all required packages
    venv_python = os.path.join(os.path.dirname(__file__), 'ecommerce-ceo-system', 'bulletproof-image-sorter', 'venv', 'bin', 'python3')
    script_path = os.path.join(os.path.dirname(__file__), 'ecommerce-ceo-system', 'email_intelligence.py')

    if not subcommand:
        subcommand = "analyze"

    try:
        # Run the email intelligence script in the correct environment
        cmd = [venv_python, script_path, subcommand]
        if args:
            cmd.extend(args)

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))

        # Print output
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Failed to run email intelligence: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py /<command> [args]")
        print("\nAvailable commands:")
        
        config = load_command_config()
        for cmd, details in config.items():
            print(f"  /{cmd}: {details.get('description', 'No description')}")
            if 'subcommands' in details:
                for subcmd, subdesc in details['subcommands'].items():
                    print(f"    {subcmd}: {subdesc}")
        return
    
    command = sys.argv[1].lstrip('/')  # Remove leading slash
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    print(f"🚀 Executing command: /{command}")
    
    if command == "catalog":
        subcommand = args[0] if args else "generate"
        remaining_args = args[1:] if len(args) > 1 else []
        success = handle_catalog_command_wrapper(subcommand, remaining_args)
        
        if success:
            print("✅ Catalog command completed successfully")
        else:
            print("❌ Catalog command failed")
            sys.exit(1)
    
    elif command == "email":
        subcommand = args[0] if args else "analyze"
        remaining_args = args[1:] if len(args) > 1 else []
        result = handle_email_command_wrapper(subcommand, remaining_args)

        if result is not None:
            print("✅ Email intelligence command completed successfully")
        else:
            print("❌ Email intelligence command failed")
            sys.exit(1)

    elif command == "help":
        config = load_command_config()
        print("\n📋 AVAILABLE COMMANDS:")
        print("=" * 50)

        # Add email command manually since it might not be in config
        print(f"\n/email")
        print(f"  Description: Smart email intelligence and analysis")
        print("  Subcommands:")
        print("    analyze: Analyze recent emails (default)")
        print("    status: System health status")
        print("    cleanup: Clean old data")

        for cmd, details in config.items():
            print(f"\n/{cmd}")
            print(f"  Description: {details.get('description', 'No description')}")
            if 'subcommands' in details:
                print("  Subcommands:")
                for subcmd, subdesc in details['subcommands'].items():
                    print(f"    {subcmd}: {subdesc}")

    else:
        print(f"❌ Unknown command: {command}")
        print("Run 'python3 main.py help' for available commands")
        sys.exit(1)

if __name__ == "__main__":
    main()