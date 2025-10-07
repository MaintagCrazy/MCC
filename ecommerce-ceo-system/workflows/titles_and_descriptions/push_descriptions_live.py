#!/usr/bin/env python3
"""
Push Updated Chair Descriptions Live to Shopify
===============================================

Syncs the updated descriptions from Google Sheets to live Shopify products
using the Product IDs from column D.
"""

import gspread
import sys
import os
import requests
import time
from google.oauth2.service_account import Credentials

# Add parent directory to path for credentials
sys.path.insert(0, '/Users/datnguyen/Marbily claude code')
from UNIVERSAL_CREDENTIALS import credentials

class ShopifyDescriptionPusher:
    """Push updated descriptions to live Shopify products"""

    def __init__(self, sheet_id: str = None):
        """Initialize with Google Sheets and Shopify connections"""
        self.sheet_id = sheet_id or credentials.GOOGLE_SHEET_ID
        self.shopify_store = credentials.SHOPIFY_STORE
        self.shopify_token = credentials.SHOPIFY_PASSWORD  # This is the access token
        self.setup_sheets_connection()

    def setup_sheets_connection(self):
        """Setup Google Sheets API connection"""
        service_account_file = "/Users/datnguyen/Marbily claude code/ecommerce-ceo-system/api_credentials/google-sheets-service-account.json"
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.sheet = self.gc.open_by_key(self.sheet_id).sheet1

    def update_shopify_product_description(self, product_id: str, title: str, description: str) -> bool:
        """Update a single Shopify product's title and description"""

        # Ensure store URL includes .myshopify.com
        store_url = self.shopify_store
        if not store_url.endswith('.myshopify.com'):
            store_url = f"{store_url}.myshopify.com"

        url = f"https://{store_url}/admin/api/2023-10/products/{product_id}.json"

        headers = {
            'X-Shopify-Access-Token': self.shopify_token,
            'Content-Type': 'application/json'
        }

        data = {
            "product": {
                "id": product_id,
                "title": title,
                "body_html": description
            }
        }

        try:
            response = requests.put(url, headers=headers, json=data)

            if response.status_code == 200:
                return True
            else:
                print(f"❌ Error updating product {product_id}: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"❌ Exception updating product {product_id}: {e}")
            return False

    def push_chairs_live(self) -> bool:
        """Push product descriptions live to Shopify for rows 231-390"""

        try:
            print("🚀 PUSHING PRODUCT DESCRIPTIONS LIVE TO SHOPIFY")
            print("=" * 60)

            # Get data for rows 231-390
            start_row, end_row = 231, 390
            data_range = f'A{start_row}:H{end_row}'
            bulk_data = self.sheet.get(data_range, value_render_option='UNFORMATTED_VALUE')

            # Group by PID to handle variants together
            pid_groups = {}
            for i, row_data in enumerate(bulk_data):
                if len(row_data) > 7:  # Ensure we have columns A-H
                    actual_row = start_row + i
                    product_id = str(row_data[3]) if row_data[3] else None  # Column D
                    title = row_data[6] if row_data[6] else ""              # Column G
                    description = row_data[7] if row_data[7] else ""        # Column H

                    if product_id and product_id != "PID":
                        if product_id not in pid_groups:
                            pid_groups[product_id] = {
                                'title': title,
                                'description': description,
                                'rows': []
                            }
                        pid_groups[product_id]['rows'].append(actual_row)

            print(f"📊 Found {len(pid_groups)} unique products to update on Shopify")

            success_count = 0
            total_count = len(pid_groups)

            for product_id, data in pid_groups.items():
                title = data['title']
                description = data['description']
                rows = data['rows']

                print(f"\n🔄 Updating Shopify Product ID: {product_id}")
                print(f"   Title: {title[:80]}...")
                print(f"   Rows: {rows}")

                # Update on Shopify
                success = self.update_shopify_product_description(product_id, title, description)

                if success:
                    print(f"✅ Successfully updated product {product_id}")
                    success_count += 1
                else:
                    print(f"❌ Failed to update product {product_id}")

                # Rate limiting - wait between requests
                time.sleep(1)

            print(f"\n🎉 SYNC COMPLETED!")
            print(f"✅ Successfully updated: {success_count}/{total_count} products")

            if success_count == total_count:
                print("🌟 ALL PRODUCT DESCRIPTIONS (ROWS 231-390) ARE NOW LIVE ON SHOPIFY!")
            else:
                print(f"⚠️ {total_count - success_count} products failed to update")

            return success_count == total_count

        except Exception as e:
            print(f"❌ Error pushing descriptions live: {e}")
            return False


def main():
    """Push product descriptions live to Shopify for rows 231-390"""

    pusher = ShopifyDescriptionPusher()

    success = pusher.push_chairs_live()

    if success:
        print("\n🎉 All descriptions successfully pushed live to Shopify!")
    else:
        print("\n❌ Some descriptions failed to push live!")


if __name__ == "__main__":
    main()