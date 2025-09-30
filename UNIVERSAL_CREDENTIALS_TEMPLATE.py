#!/usr/bin/env python3
"""
Universal Credentials Template for Marbily E-commerce System
Copy this file to UNIVERSAL_CREDENTIALS.py and fill in your actual credentials
"""

# ═══════════════════════════════════════════════════════════════
# TEMPLATE - Replace with your actual credentials
# ═══════════════════════════════════════════════════════════════

credentials = {
    # ─────────────────────────────────────────────────────────────
    # E-COMMERCE PLATFORM APIS
    # ─────────────────────────────────────────────────────────────

    # BaseLinker API Configuration
    'baselinker_token': 'YOUR_BASELINKER_TOKEN_HERE',

    # Shopify API Configuration
    'shopify_access_token': 'YOUR_SHOPIFY_ACCESS_TOKEN_HERE',
    'shopify_shop_domain': 'YOUR_SHOP.myshopify.com',

    # ─────────────────────────────────────────────────────────────
    # AI AND AUTOMATION APIS
    # ─────────────────────────────────────────────────────────────

    # OpenAI API Configuration
    'openai_api_key': 'YOUR_OPENAI_API_KEY_HERE',

    # Anthropic Claude API Configuration
    'anthropic_api_key': 'YOUR_ANTHROPIC_API_KEY_HERE',
    'anthropic_project_id': 'YOUR_ANTHROPIC_PROJECT_ID_HERE',

    # OpenRouter API Configuration
    'openrouter_api_key': 'YOUR_OPENROUTER_API_KEY_HERE',

    # Replicate API Configuration
    'replicate_api_token': 'YOUR_REPLICATE_API_TOKEN_HERE',

    # ─────────────────────────────────────────────────────────────
    # GOOGLE SERVICES INTEGRATION
    # ─────────────────────────────────────────────────────────────

    # Google OAuth Configuration
    'google_client_id': 'YOUR_GOOGLE_CLIENT_ID_HERE',
    'google_client_secret': 'YOUR_GOOGLE_CLIENT_SECRET_HERE',

    # ─────────────────────────────────────────────────────────────
    # IMAGE AND MEDIA SERVICES
    # ─────────────────────────────────────────────────────────────

    # Cloudinary Configuration
    'cloudinary_cloud_name': 'YOUR_CLOUDINARY_CLOUD_NAME_HERE',
    'cloudinary_api_key': 'YOUR_CLOUDINARY_API_KEY_HERE',
    'cloudinary_api_secret': 'YOUR_CLOUDINARY_API_SECRET_HERE',

    # ─────────────────────────────────────────────────────────────
    # DATABASE CONFIGURATION
    # ─────────────────────────────────────────────────────────────

    # MySQL Database Configuration
    'mysql_host': 'YOUR_MYSQL_HOST_HERE',
    'mysql_user': 'YOUR_MYSQL_USER_HERE',
    'mysql_password': 'YOUR_MYSQL_PASSWORD_HERE',
    'mysql_database': 'YOUR_MYSQL_DATABASE_HERE',

    # Supabase Configuration
    'supabase_url': 'YOUR_SUPABASE_URL_HERE',
    'supabase_anon_key': 'YOUR_SUPABASE_ANON_KEY_HERE',

    # ─────────────────────────────────────────────────────────────
    # EMAIL AND COMMUNICATION
    # ─────────────────────────────────────────────────────────────

    # Gmail Configuration
    'gmail_user': 'YOUR_GMAIL_ADDRESS_HERE',
    'gmail_password': 'YOUR_GMAIL_APP_PASSWORD_HERE',

    # GoDaddy Email Configuration
    'godaddy_email': 'YOUR_GODADDY_EMAIL_HERE',
    'godaddy_password': 'YOUR_GODADDY_PASSWORD_HERE',

    # ─────────────────────────────────────────────────────────────
    # VERSION CONTROL AND DEPLOYMENT
    # ─────────────────────────────────────────────────────────────

    # GitHub Configuration
    'github_token': 'YOUR_GITHUB_TOKEN_HERE',
    'github_username': 'YOUR_GITHUB_USERNAME_HERE',

    # Railway Configuration
    'railway_token': 'YOUR_RAILWAY_TOKEN_HERE',
}

def test_credentials():
    """Test all credential connections"""
    print("🧪 Testing Credential Connections")
    print("=" * 50)

    # Check which credentials are configured
    configured = []
    missing = []

    for key, value in credentials.items():
        if value and not value.startswith('YOUR_'):
            configured.append(key)
        else:
            missing.append(key)

    print(f"✅ Configured: {len(configured)} credentials")
    print(f"❌ Missing: {len(missing)} credentials")

    if configured:
        print(f"\n🔧 Configured Services:")
        for cred in configured:
            print(f"   ✅ {cred}")

    if missing:
        print(f"\n⚠️  Missing Configuration:")
        for cred in missing:
            print(f"   ❌ {cred}")

    print(f"\n📋 Setup Instructions:")
    print(f"   1. Copy this template to UNIVERSAL_CREDENTIALS.py")
    print(f"   2. Replace YOUR_*_HERE placeholders with actual credentials")
    print(f"   3. Run test_credentials() to verify setup")

    return len(configured), len(missing)

if __name__ == '__main__':
    test_credentials()