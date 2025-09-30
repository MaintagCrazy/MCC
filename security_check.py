#!/usr/bin/env python3
"""
Standalone Security Scanner CLI Tool
Quick credential leak detection before GitHub uploads
"""

import sys
from pathlib import Path

# Add integrations directory to path
sys.path.append(str(Path(__file__).parent / "ecommerce-ceo-system" / "integrations"))

def main():
    """Run security scan from command line"""
    try:
        from security_scanner import scan_before_github_upload

        print("🔍 Marbily Security Scanner")
        print("=" * 50)
        print("Scanning for credential leaks before GitHub upload...")
        print()

        # Run the scan
        is_safe = scan_before_github_upload()

        print()
        if is_safe:
            print("🎉 All clear! Safe to upload to GitHub.")
            sys.exit(0)
        else:
            print("⚠️  Security issues detected. Fix before uploading.")
            sys.exit(1)

    except ImportError as e:
        print(f"❌ Error importing security scanner: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running security scan: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()