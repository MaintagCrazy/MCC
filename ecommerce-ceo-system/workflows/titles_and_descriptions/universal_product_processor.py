#!/usr/bin/env python3
"""
Universal Product Processor for Titles and Descriptions - HYBRID VERSION
=========================================================================

Combines the best of both approaches:
- 5-7 line structured descriptions with size intelligence
- AI-generated competitive smart bullets that don't repeat description
- Enhanced Claude 4.5 Sonnet vision analysis (10+ features)
- Creative naming with anti-duplicate system

Features:
- Individual Claude 4.5 Sonnet vision analysis for each product
- Loads existing names at startup to prevent duplicates
- AI-generated unique bullet points with NO template repetition
- Varied Polish adjectives (elegancki, minimalistyczny, klasyczny, etc.)
- Creative abstract/city names instead of human names
- Proper Polish grammar rules for material descriptions
- HTML template generation with standardized styling
- Row-based product categorization support
"""

import gspread
import sys
import os
import time
import random
from google.oauth2.service_account import Credentials
import base64
import requests
import json
from typing import Dict, List, Tuple, Optional

# Add parent directory to path for credentials
sys.path.insert(0, '/Users/datnguyen/Marbily claude code')
sys.path.insert(0, '/Users/datnguyen/Marbily claude code/ecommerce-ceo-system')
from UNIVERSAL_CREDENTIALS import credentials
from utils.polish_grammar import PolishGrammar

class UniversalProductProcessor:
    """Universal processor for product titles and descriptions"""

    def __init__(self, sheet_id: str = None):
        """Initialize with Google Sheets connection"""
        self.sheet_id = sheet_id or credentials.GOOGLE_SHEET_ID
        self.openrouter_api_key = credentials.OPENROUTER_API_KEY
        self.used_names = set()
        self.grammar = PolishGrammar()
        self.setup_sheets_connection()
        self.load_existing_names()  # CRITICAL: Load names at startup

    def setup_sheets_connection(self):
        """Setup Google Sheets API connection"""
        service_account_file = "/Users/datnguyen/Marbily claude code/ecommerce-ceo-system/api_credentials/google-sheets-service-account.json"
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
        self.gc = gspread.authorize(creds)
        self.sheet = self.gc.open_by_key(self.sheet_id).sheet1

    def load_existing_names(self):
        """Load all existing names from column F to prevent duplicates"""
        try:
            print("🔄 Loading existing names from column F...")
            existing_names = self.sheet.col_values(6)  # Column F = index 6

            # Filter out header and empty values
            for name in existing_names[1:]:  # Skip header row
                if name and name != "Unique Name" and not name.startswith("Abstract"):
                    self.used_names.add(name)

            print(f"✅ Loaded {len(self.used_names)} existing names")
            if self.used_names:
                print(f"   Examples: {list(self.used_names)[:5]}")
        except Exception as e:
            print(f"⚠️ Warning: Could not load existing names: {e}")

    # Style and naming configurations - TIMELESS AESTHETIC WORDS ONLY
    # NO salesy words like "luksusowy", "spektakularny", "przepiękny"
    POLISH_ADJECTIVES = [
        "minimalistyczny",  # minimalist - timeless
        "klasyczny",        # classic - timeless
        "nowoczesny",       # modern - clean
        "skandynawski",     # Scandinavian - aesthetic
        "industrialny"      # industrial - aesthetic
    ]

    CREATIVE_NAMES = [
        # European Cities - Sophisticated & Furniture-Appropriate
        "Milan", "Vienna", "Oslo", "Prague", "Paris", "Barcelona", "Rome",
        "Stockholm", "Copenhagen", "Helsinki", "Zurich", "Berlin", "Amsterdam",
        "Lyon", "Geneva", "Florence", "Venice", "Monaco", "Dresden", "Lisbon",
        "Porto", "Madrid", "Brussels", "Munich", "Salzburg", "Turin", "Basel",

        # Soft Abstract Concepts - Minimalist & Aesthetic
        "Echo", "Wave", "Harmony", "Balance", "Clarity", "Unity", "Serenity",
        "Essence", "Horizon", "Vision", "Legacy", "Spirit", "Radiance",
        "Dawn", "Dusk", "Mist", "Sky", "Rain", "Cloud", "Breeze",
        "Grace", "Bloom", "Flow", "Rhythm", "Pulse", "Form", "Line",
        "Calm", "Still", "Pure", "Soft", "Light", "Shadow", "Shade"
    ]

    def get_image_from_url(self, image_url: str) -> Optional[str]:
        """Get base64 encoded image data from URL"""
        try:
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                return base64.b64encode(response.content).decode('utf-8')
        except Exception as e:
            print(f"Error getting image: {e}")
        return None

    def analyze_product_with_claude(self, image_url: str, product_type: str, dimensions: Dict = None) -> Dict:
        """Use Claude 4.5 Sonnet via OpenRouter to analyze product with COMPETITIVE FEATURES

        CRITICAL: Includes dimension context to verify product type - images can be deceiving!
        A 70cm tall table is NOT a coffee table, it's a dining table.
        """
        try:
            image_data = self.get_image_from_url(image_url)
            if not image_data:
                return self.get_fallback_analysis(product_type)

            # Extract dimensions for context
            height = dimensions.get('height', 'unknown') if dimensions else 'unknown'
            width = dimensions.get('width', 'unknown') if dimensions else 'unknown'
            depth = dimensions.get('depth', 'unknown') if dimensions else 'unknown'

            # ENHANCED prompt with DIMENSION CONTEXT for smart product type detection
            prompt = f"""Analyze this furniture image in EXTREME detail for e-commerce listing.

CRITICAL CONTEXT - ACTUAL DIMENSIONS (use these to verify product type!):
- Height: {height} cm
- Width: {width} cm
- Depth: {depth} cm
- Currently classified as: {product_type}

DIMENSION VERIFICATION (IMPORTANT!):
- Coffee tables (stolik kawowy): 40-50cm height
- Dining tables (stół): 70-80cm height
- Chairs (krzesło): seat height 45-50cm, total height 80-90cm
- Armchairs (fotel): seat height 40-45cm, total height 70-85cm

If the dimensions don't match the current classification, CORRECT IT in your response!

IMAGE ANALYSIS - What you actually see:
1. MATERIAL: Primary material? (marble, wood, fabric, leather, metal, glass)
2. STYLE: Pick ONLY ONE timeless aesthetic word - NO salesy words!
   ALLOWED: minimalistyczny, klasyczny, nowoczesny, skandynawski, industrialny
   FORBIDDEN: luksusowy, elegancki, spektakularny, wspaniały, przepiękny, ekskluzywny
3. SHAPE: Exact shape? (okrągły/round, prostokątny/rectangular, kwadratowy/square, owalny/oval, organiczny/organic, nieregularny/irregular)
4. COLOR: Specific color tones and finishes you see
5. SURFACE_FINISH: (high-gloss/matte/textured/natural/polished)
6. PATTERN: Any veining, grain, texture patterns you see
7. EDGE_TREATMENT: Edge style (rounded/sharp/beveled/organic/irregular)
8. BASE_STYLE: Base/leg design (cylindrical/conical/legs/pedestal/flat)
9. UNIQUE_FEATURES: What makes this product visually distinctive?
10. MATERIAL_QUALITY: Visual quality indicators (natural imperfections, uniformity, craftsmanship)

11. PRODUCT NAME - Generate ONE elegant abstract name that resonates with this specific product:

CRITICAL NAME RULES - Tailor name to material personality:
- **Wood products** → Natural/organic abstracts (one word): Grove, Timber, Grain, Oak, Cedar, Ash, Willow, Birch, Forest, Branch, Beam, Bark, Root, Leaf
- **Marble/stone products** → Modern/architectural (one word): Axis, Form, Edge, Line, Plane, Structure, Angle, Column, Arc, Peak, Ridge, Crest
- **Leather products** → Italian/sophisticated (one word): Bellezza, Lusso, Comodo, Morbido, Eleganza, Pelle, Forma, Stile
- **Fabric/boucle products** → Soft/tactile (one word): Plush, Velvet, Cloud, Nest, Cozy, Soft, Silk, Cashmere, Linen

Generate a UNIQUE name that feels right for THIS specific piece - consider the material, shape, and overall aesthetic!
Name must be: minimalist, neutral, abstract, sophisticated, furniture-appropriate

Respond in JSON:
{{
    "corrected_product_type": "table/coffee_table/chair/armchair (use dimensions to verify!)",
    "material": "...",
    "style": "...",
    "shape": "...",
    "color": "...",
    "color_details": "...",
    "surface_finish": "...",
    "pattern": "...",
    "edge_treatment": "...",
    "base_style": "...",
    "unique_features": ["feature1", "feature2", "feature3"],
    "material_quality": "...",
    "dimension_match": "true/false (do dimensions match the product type?)",
    "confidence": "high/medium/low",
    "suggested_name": "one elegant abstract name tailored to this product"
}}"""

            # Call Claude 4.5 Sonnet via OpenRouter
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-sonnet-4.5",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}
                                }
                            ]
                        }
                    ],
                    "max_tokens": 1500
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                # Extract JSON from response
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()

                return json.loads(content)
            else:
                print(f"⚠️ OpenRouter API error: {response.status_code}")
                return self.get_fallback_analysis(product_type)

        except Exception as e:
            print(f"❌ Vision analysis error: {e}")
            return self.get_fallback_analysis(product_type)

    def get_fallback_analysis(self, product_type: str) -> Dict:
        """Fallback analysis when vision fails"""
        fallback_materials = {
            "chair": "fabric",
            "table": "wood",
            "coffee_table": "marble",
            "armchair": "fabric"
        }

        return {
            "corrected_product_type": product_type,  # No correction in fallback
            "material": fallback_materials.get(product_type, "wood"),
            "style": random.choice(self.POLISH_ADJECTIVES),
            "shape": "prostokątny",
            "color": "naturalny",
            "color_details": "naturalny ton",
            "surface_finish": "polished",
            "pattern": "natural grain",
            "edge_treatment": "rounded",
            "base_style": "legs",
            "unique_features": ["klasyczna konstrukcja"],
            "material_quality": "wysoka jakość",
            "dimension_match": "unknown",  # Can't verify without vision
            "confidence": "low"
        }

    def generate_unique_name(self, style: str, material: str) -> str:
        """Generate unique creative name avoiding duplicates"""
        attempts = 0
        max_attempts = 50

        while attempts < max_attempts:
            name = random.choice(self.CREATIVE_NAMES)
            if name not in self.used_names:
                self.used_names.add(name)
                return name
            attempts += 1

        # Fallback: create hybrid name
        fallback_name = f"{random.choice(['Neo', 'Ultra', 'Prime'])}{random.choice(self.CREATIVE_NAMES)}"
        self.used_names.add(fallback_name)
        return fallback_name

    def create_polish_title(self, product_type: str, style: str, material: str, unique_name: str, dimensions: str = "", shape: str = "") -> str:
        """Create grammatically correct Polish title using the grammar module"""
        return self.grammar.create_title(product_type, style, material, unique_name, dimensions, shape)

    def generate_smart_bullets(self, product_type: str, analysis: Dict,
                              description_text: str, dimensions: Dict) -> List[str]:
        """Generate competitive bullets using AI - works for ALL products universally"""

        try:
            # Prepare context for AI
            material = analysis.get('material', 'unknown')
            shape = analysis.get('shape', 'unknown')
            surface_finish = analysis.get('surface_finish', 'unknown')
            pattern = analysis.get('pattern', 'none')
            edge_treatment = analysis.get('edge_treatment', 'unknown')
            base_style = analysis.get('base_style', 'unknown')
            unique_features = analysis.get('unique_features', [])

            # Calculate functional context
            width = dimensions.get('width', 'unknown')
            depth = dimensions.get('depth', 'unknown')
            height = dimensions.get('height', 'unknown')

            # Determine seating capacity for tables
            seating_capacity = "unknown"
            if product_type in ['table']:
                try:
                    w = float(width) if width != 'brak danych' else 0
                    d = float(depth) if depth != 'brak danych' else 0

                    if w >= 200 or d >= 180:
                        seating_capacity = "8-10 osób"
                    elif w >= 160 or d >= 140:
                        seating_capacity = "6-8 osób"
                    elif w >= 120:
                        seating_capacity = "4-6 osób"
                    else:
                        seating_capacity = "4 osoby"
                except:
                    seating_capacity = "unknown"

            # Product type context
            type_context = {
                'coffee_table': 'stolik kawowy do salonu przy sofie',
                'table': 'stół jadlany do posiłków',
                'chair': 'krzesło do siedzenia przy stole',
                'armchair': 'fotel do wypoczynku'
            }.get(product_type, product_type)

            prompt = f"""You are writing bullet points for a furniture e-commerce listing in Polish.

PRODUCT TYPE: {product_type} ({type_context})
MATERIAL: {material}
SHAPE: {shape}
SURFACE FINISH: {surface_finish}
PATTERN: {pattern}
EDGE TREATMENT: {edge_treatment}
BASE/LEG STYLE: {base_style}
UNIQUE VISUAL FEATURES: {', '.join(unique_features) if unique_features else 'none noted'}
DIMENSIONS: {width}cm x {depth}cm x {height}cm
SEATING CAPACITY: {seating_capacity if product_type == 'table' else 'N/A'}

EXISTING DESCRIPTION (DO NOT REPEAT):
{description_text}

TASK: Generate exactly 6 bullet points in Polish that include:
1. VISION-BASED features (what you can see): shape, pattern, edge style, finish, base design
2. PERFORMANCE claims (safe to assume): scratch-resistant, heat-resistant, weight capacity, durability
3. FUNCTIONAL benefits: seating capacity (tables), usage context, ease of cleaning, stability
4. MATERIAL-SPECIFIC: uniqueness (marble patterns), natural characteristics, quality indicators

CRITICAL LANGUAGE RULES:
- Use SIMPLE, PRACTICAL language - NO poetic or dramatic words!
- NO words like: dramatyczne, rzeźbiarska, spektakularny, wspaniały, przepiękny
- YES words like: naturalny, solidny, trwały, praktyczny, funkcjonalny, wygodny
- Be DIRECT and FACTUAL, not artistic or flowery
- Write like a practical furniture salesperson, not a poet

RULES:
- NEVER repeat info from description above
- Be SPECIFIC (not generic): mention actual visible features
- Include competitive claims other sellers use
- Each bullet 5-10 words in Polish
- Mix vision + performance + functional across all 6 bullets
- For tables: MUST include seating capacity if dining table
- For marble/stone: use simple descriptions like "naturalny wzór marmuru", "białe żyłki"
- For wood: mention grain or finish simply
- For fabric/leather: mention comfort or durability

EXAMPLES OF GOOD SIMPLE BULLETS:
- "Blat z naturalnego marmuru z białymi żyłkami" (simple, not "dramatyczne złote żyły")
- "Solidna trójnożna podstawa z metalowych nóg" (simple, not "rzeźbiarska podstawa")
- "Odporna na zarysowania polerowana powierzchnia" (performance)
- "Wygodnie pomieści 6-8 osób przy posiłku" (functional for tables)
- "Każdy stolik ma unikalny wzór marmuru" (material-specific, simple)
- "Stabilna konstrukcja odporna na obciążenia" (vision + functional)

Return ONLY a JSON array of 6 strings (no explanations):
["bullet 1", "bullet 2", "bullet 3", "bullet 4", "bullet 5", "bullet 6"]"""

            # Call Claude to generate bullets
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-sonnet-4.5",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 800
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content'].strip()

                # Extract JSON array
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                elif '[' in content:
                    # Find the array
                    start = content.index('[')
                    end = content.rindex(']') + 1
                    content = content[start:end]

                bullets = json.loads(content)

                # Ensure exactly 6 bullets
                if len(bullets) >= 6:
                    return bullets[:6]
                else:
                    # Pad with generic but safe bullets
                    while len(bullets) < 6:
                        bullets.append("Montaż w 10-15 minut z dołączoną instrukcją")
                    return bullets
            else:
                print(f"⚠️ Bullet generation API error: {response.status_code}")
                return self.get_fallback_bullets(product_type, material, seating_capacity)

        except Exception as e:
            print(f"⚠️ AI bullet generation error: {e}")
            return self.get_fallback_bullets(product_type, material, seating_capacity if product_type == 'table' else None)

    def get_fallback_bullets(self, product_type: str, material: str, seating_capacity: str = None) -> List[str]:
        """Fallback bullets when AI fails - simple, practical language"""

        bullets = []

        # Material-specific - SIMPLE LANGUAGE
        if material in ['marble', 'granite', 'stone'] or 'marble' in material.lower():
            bullets.append("Blat z naturalnego marmuru z unikalnym wzorem")
            bullets.append("Polerowana powierzchnia odporna na zarysowania")
        elif material == 'wood':
            bullets.append("Blat z naturalnego drewna")
            bullets.append("Lakierowana powierzchnia odporna na wilgoć")
        elif material in ['fabric', 'leather']:
            bullets.append("Wygodne miękkie siedzisko")
            bullets.append("Łatwe w czyszczeniu i utrzymaniu")
        else:
            bullets.append("Solidne materiały i trwałe wykończenie")
            bullets.append("Wytrzyma codzienne użytkowanie przez lata")

        # Product-specific
        if product_type in ['chair', 'armchair']:
            bullets.append("Wygodne oparcie wspierające plecy")
            bullets.append("Stabilna konstrukcja stalowa")
        elif product_type == 'table' and seating_capacity:
            bullets.append(f"Wygodnie pomieści {seating_capacity}")
            bullets.append("Stabilna konstrukcja odporna na obciążenia")
        elif product_type == 'coffee_table':
            bullets.append("Praktyczna wysokość do kawy przy sofie")
            bullets.append("Stabilna podstawa zapewnia bezpieczeństwo")

        # Universal competitive claims
        bullets.append("Antypoślizgowe nakładki chronią podłogę")
        bullets.append("Prosty montaż w 10-15 minut")

        return bullets[:6]

    def generate_html_description(self, product_type: str, style: str, material: str,
                                 unique_name: str, dimensions: Dict, analysis: Dict,
                                 color_list: str = "Różne kolory") -> str:
        """Generate HTML description with 5-7 line structured content + AI smart bullets

        HYBRID APPROACH:
        - Descriptions: 5-7 structured lines with size intelligence (YOUR PREFERENCE)
        - Bullets: AI-generated competitive bullets that don't repeat description
        - Actual colors: Uses real color variants from sheet, not generic "Różne kolory"
        """

        # Get dimensions with defaults
        height = dimensions.get('height', 'brak danych')
        width = dimensions.get('width', 'brak danych')
        depth = dimensions.get('depth', 'brak danych')

        # Extract vision analysis data
        shape = analysis.get('shape', '')
        color_details = analysis.get('color_details', analysis.get('color', ''))
        material_details = analysis.get('material_details', '')
        visual_features = analysis.get('visual_features', '')

        # Product type translations
        type_descriptions = {
            "chair": "krzesło",
            "table": "stół",
            "coffee_table": "stolik kawowy",
            "armchair": "fotel"
        }
        polish_type = type_descriptions.get(product_type, "mebel")

        # SIZE INTELLIGENCE for tables
        size_descriptor = ""
        if product_type in ["table", "coffee_table"]:
            try:
                w = float(width) if width != 'brak danych' else 0
                d = float(depth) if depth != 'brak danych' else 0

                if shape == "okrągły" or "round" in shape.lower():
                    # Round table - use width as diameter
                    if w >= 90:
                        size_descriptor = f"okrągły stolik {int(w)}cm"
                    else:
                        size_descriptor = "kompaktowy okrągły stolik"
                elif w >= 180 or d >= 180:
                    size_descriptor = f"duży stół {int(w)}x{int(d)}cm dla 6-8 osób"
                elif w >= 120 or d >= 120:
                    size_descriptor = f"średni stół {int(w)}x{int(d)}cm dla 4-6 osób"
                elif w >= 80 or d >= 80:
                    size_descriptor = f"kompaktowy stolik {int(w)}x{int(d)}cm"
                else:
                    size_descriptor = polish_type
            except:
                size_descriptor = polish_type
        else:
            size_descriptor = polish_type

        # DESCRIPTION GENERATION - 5-7 lines with actual vision data
        desc_lines = []

        # Line 1: Introduction with style and shape
        if size_descriptor and shape:
            desc_lines.append(f"{style.title()} {size_descriptor} {unique_name} łączy nowoczesny design z funkcjonalnością.")
        elif size_descriptor:
            desc_lines.append(f"{style.title()} {size_descriptor} {unique_name} to eleganckie rozwiązanie do salonu.")
        else:
            desc_lines.append(f"{style.title()} {polish_type} {unique_name} wyróżnia się designem i jakością wykonania.")

        # Line 2: Material visual details from vision
        if material == "marble":
            if color_details and "czarn" in color_details.lower():
                desc_lines.append("Czarny marmur z naturalnymi białymi żyłkami tworzy unikalne wzory na każdym blacie.")
            elif color_details and "biał" in color_details.lower():
                desc_lines.append("Biały marmur z delikatnymi szarymi żyłkami nadaje wnętrzu luksusowy charakter.")
            else:
                desc_lines.append("Naturalny marmur z unikalnym układem żył sprawia, że każdy egzemplarz jest jedyny w swoim rodzaju.")
        elif material == "wood":
            desc_lines.append("Naturalny drewniany blat z widocznym usłojeniem dodaje ciepła każdemu wnętrzu.")
        else:
            desc_lines.append("Wysokiej jakości materiały zapewniają trwałość i elegancki wygląd.")

        # Lines 3-4: Size-specific usage and capacity
        if product_type == "coffee_table":
            try:
                w = float(width) if width != 'brak danych' else 0
                if w >= 100:
                    desc_lines.append("Przestronny blat pomieści filiżanki, książki i dekoracje.")
                    desc_lines.append("Idealny jako centralny punkt salonu przy sofie lub narożniku.")
                elif w >= 80:
                    desc_lines.append("Kompaktowy rozmiar doskonale sprawdzi się w mniejszych salonach.")
                    desc_lines.append("Wystarczająco duży na filiżanki kawy i piloty, nie zajmuje dużo miejsca.")
                else:
                    desc_lines.append("Niewielkie wymiary idealnie pasują do małych przestrzeni.")
                    desc_lines.append("Praktyczne miejsce na książkę i kubek herbaty przy fotelu.")
            except:
                desc_lines.append("Doskonale sprawdzi się w salonie jako centralny element strefy wypoczynkowej.")
                desc_lines.append("Praktyczna przestrzeń na codzienne drobiazgi i dekoracje.")

        elif product_type == "table":
            try:
                w = float(width) if width != 'brak danych' else 0
                if w >= 180:
                    desc_lines.append("Duży blat wygodnie pomieści 6-8 osób podczas rodzinnych posiłków.")
                    desc_lines.append("Idealny do jadalni jako główny stół do codziennych obiadów i świątecznych spotkań.")
                elif w >= 120:
                    desc_lines.append("Średni rozmiar idealny dla 4-6 osób w jadalni lub kuchni.")
                    desc_lines.append("Wszechstronny stół do codziennego użytku i niedzielnych obiadów.")
                else:
                    desc_lines.append("Kompaktowy wymiar dla 2-4 osób, świetny do małych kuchni.")
                    desc_lines.append("Funkcjonalny stół do codziennych posiłków w niewielkiej przestrzeni.")
            except:
                desc_lines.append("Praktyczny stół do codziennego użytku w jadalni lub kuchni.")
                desc_lines.append("Wygodna przestrzeń do wspólnych posiłków i spotkań.")

        # Line 5-6: Material properties and maintenance
        if material == "marble":
            desc_lines.append("Polerowana powierzchnia odporna na zarysowania i łatwa w utrzymaniu czystości.")
            desc_lines.append("Wystarczy przetrzeć wilgotną szmatką - marmur zachowa piękny wygląd na lata.")
        elif material == "wood":
            desc_lines.append("Powierzchnia zabezpieczona lakierem odpornym na codzienne użytkowanie.")
            desc_lines.append("Łatwe czyszczenie wilgotną ściereczką, odporność na plamy i wodę.")
        else:
            desc_lines.append("Trwała powierzchnia odporna na codzienne użytkowanie i łatwa w czyszczeniu.")

        # Line 7: Longevity and quality
        desc_lines.append("Solidna stalowa konstrukcja zapewnia stabilność i długowieczność na lata użytkowania.")

        # Join only first 7 lines (in case we generated more)
        desc_text = " ".join(desc_lines[:7])

        # AI-GENERATED SMART BULLETS (from Downloads version)
        bullet_items = self.generate_smart_bullets(product_type, analysis, desc_text, dimensions)

        # Material info for spec table - FIX: Use actual material detected by vision
        material_map = {
            "fabric": "miękka tapicerka materiałowa",
            "leather": "skóra ekologiczna",
            "wood": "naturalne drewno",
            "marble": "naturalny marmur",
            "marble top with painted metal base": "naturalny marmur",
            "marble and metal": "naturalny marmur",
            "marble top with metal base": "naturalny marmur",
            "metal": "metal lakierowany",
            "glass": "hartowane szkło"
        }
        # Clean the material string and map it
        material_clean = material.lower().strip()
        surface_material = material_map.get(material_clean, "naturalny marmur" if "marble" in material_clean or "marmur" in material_clean else "wysokiej jakości materiał")

        # Generate HTML template
        template = f'''<style>
  body{{font-family:Arial,sans-serif;font-size:12px;line-height:1.4;color:#333}}
  .desc{{margin-bottom:16px;color:#555}}
  .bullet-list{{list-style:none;padding:0;margin:0 0 20px 0}}
  .bullet-list li{{position:relative;padding-left:20px;margin-bottom:8px}}
  .bullet-list li:before{{content:"●";color:#e63946;position:absolute;left:0;top:0;line-height:1}}

  .spec-wrap{{display:flex;gap:20px;flex-wrap:wrap}}
  .spec-card{{flex:1;min-width:260px;background:#f8f8f8;padding:12px;border-radius:3px}}
  .spec-card h3{{margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#333}}
  .subhead{{margin:15px 0 8px 0;font-size:15px;font-weight:bold;color:#333}}

  .row{{margin-bottom:8px;display:flex;align-items:flex-start;gap:12px}}
  .row .label{{color:#777;font-size:13px;flex:0 0 auto;white-space:nowrap}}
  .row .val{{font-size:13px;color:#333;flex:1;text-align:right;white-space:normal}}
</style>
<!-- OPIS -->
<div class="desc">{desc_text} <br><br>Dostępny w wersji: {color_list}</div>
<!-- BULLET LIST -->
<ul class="bullet-list">'''

        # Add bullet points
        for item in bullet_items:
            template += f'\n<li>{item}</li>'

        template += f'''
</ul>
<!-- TABELA SPECYFIKACJI -->
<div class="spec-wrap">
<!-- Wymiary -->
<div class="spec-card">
<h3>Wymiary</h3>'''

        # Add dimension rows ONLY if they have actual values (not "brak danych")
        if height != 'brak danych':
            # Remove " cm" if already in the value to avoid "cm cm"
            height_clean = str(height).replace(' cm', '').replace('cm', '').strip()
            template += f'''
<div class="row">
<span class="label">Wysokość całkowita</span><span class="val">{height_clean} cm</span>
</div>'''

        if width != 'brak danych':
            width_clean = str(width).replace(' cm', '').replace('cm', '').strip()
            template += f'''
<div class="row">
<span class="label">Szerokość całkowita</span><span class="val">{width_clean} cm</span>
</div>'''

        if depth != 'brak danych':
            depth_clean = str(depth).replace(' cm', '').replace('cm', '').strip()
            template += f'''
<div class="row">
<span class="label">Głębokość całkowita</span><span class="val">{depth_clean} cm</span>
</div>'''

        template += f'''
<div class="subhead">Dostępność i Dostawa</div>
<div class="row">
<span class="label">Dostępność</span><span class="val">na stanie w Warszawie</span>
</div>
<div class="row">
<span class="label">Dostawa</span><span class="val">1-3 dni roboczych</span>
</div>
</div>
<!-- Konstrukcja -->
<div class="spec-card">
<h3>Konstrukcja</h3>
<div class="row">
<span class="label">Materiał ramy</span><span class="val">stal lakierowana proszkowo</span>
</div>
<div class="row">
<span class="label">Blat</span><span class="val">{surface_material}</span>
</div>
<div class="subhead">Montaż</div>
<div class="row">
<span class="label">Czas montażu</span><span class="val">około 10-15 minut</span>
</div>
<div class="row">
<span class="label">Sposób montażu</span><span class="val">przykręcenie nóg do blatu</span>
</div>
<div class="row">
<span class="label">Gwarancja</span><span class="val">24 miesiące</span>
</div>
</div>
</div>'''

        return template

    def process_product_range(self, start_row: int, end_row: int,
                             product_type_mapping: Dict[Tuple[int, int], str],
                             delay_seconds: float = 3.0) -> bool:
        """
        Process a range of products with individual Claude analysis

        Args:
            start_row: Starting row number (inclusive)
            end_row: Ending row number (inclusive)
            product_type_mapping: Dict mapping (start, end) tuples to product types
            delay_seconds: Delay between processing items (3 seconds for API rate limits)

        Returns:
            Success status
        """

        try:
            print(f"🚀 PROCESSING PRODUCTS {start_row}-{end_row} WITH CLAUDE 4.5 SONNET")
            print("=" * 80)

            # Get bulk data
            data_range = f'A{start_row}:AW{end_row}'
            bulk_data = self.sheet.get(data_range, value_render_option='UNFORMATTED_VALUE')

            # Group by PID
            pid_groups = {}
            for i, row_data in enumerate(bulk_data):
                if len(row_data) > 3:
                    actual_row = start_row + i
                    pid = str(row_data[3]) if row_data[3] else None
                    sku = str(row_data[0]) if row_data[0] else None

                    # Use Product ID if available, otherwise use SKU as grouping key
                    group_key = pid if (pid and pid != "PID") else sku

                    if group_key and group_key not in ["PID", "SKU", ""]:
                        if group_key not in pid_groups:
                            pid_groups[group_key] = []
                        pid_groups[group_key].append((actual_row, row_data))

            print(f"📊 Found {len(pid_groups)} unique PIDs to process")

            processed_count = 0
            updates = []

            for pid, rows in pid_groups.items():
                print(f"\n🔄 Processing PID {pid} ({len(rows)} variants)")

                first_row_num, first_row_data = rows[0]

                # COLLECT ALL COLORS FOR THIS PID (Column E = index 4)
                colors_for_pid = []
                for row_num, row_data in rows:
                    if len(row_data) > 4 and row_data[4]:
                        color = str(row_data[4]).strip()
                        if color and color not in colors_for_pid:
                            colors_for_pid.append(color)

                # Format color list
                color_list = ", ".join(colors_for_pid) if colors_for_pid else "Różne kolory"
                print(f"🎨 Colors available: {color_list}")

                # Determine product type based on row range
                product_type = "unknown"
                for (range_start, range_end), ptype in product_type_mapping.items():
                    if range_start <= first_row_num <= range_end:
                        product_type = ptype
                        break

                # Get image URL (columns L-S = indices 11-18)
                image_url = None
                for img_idx in range(11, 19):  # Check columns L through S
                    if len(first_row_data) > img_idx and first_row_data[img_idx]:
                        image_url = first_row_data[img_idx]
                        break

                if not image_url:
                    print(f"⚠️ No image URL for PID {pid}, skipping")
                    continue

                # EXTRACT DIMENSIONS FIRST (columns AF-AW = indices 31-48)
                # AF=31 (height), AG=32 (width), AH=33 (depth)
                dimensions = {
                    'height': first_row_data[31] if len(first_row_data) > 31 and first_row_data[31] else 'brak danych',
                    'width': first_row_data[32] if len(first_row_data) > 32 and first_row_data[32] else 'brak danych',
                    'depth': first_row_data[33] if len(first_row_data) > 33 and first_row_data[33] else 'brak danych'
                }

                print(f"🖼️ Analyzing image: {image_url[:80]}...")
                print(f"📏 Dimensions: {dimensions['height']}H x {dimensions['width']}W x {dimensions['depth']}D cm")

                # CLAUDE 4.5 VISION ANALYSIS WITH DIMENSION CONTEXT
                analysis = self.analyze_product_with_claude(image_url, product_type, dimensions)

                material = analysis.get('material', 'wood')

                # CLEAN STYLE: Take ONLY first word, ensure it's timeless (no "luksusowy")
                style_raw = analysis.get('style', 'nowoczesny')
                # If Claude returned multiple words (e.g., "nowoczesny, luksusowy"), take only first
                style = style_raw.split(',')[0].strip() if ',' in style_raw else style_raw.strip()
                # Remove salesy words
                if style.lower() in ['luksusowy', 'elegancki', 'spektakularny', 'wspaniały', 'ekskluzywny']:
                    style = 'nowoczesny'  # Default to timeless

                # CHECK IF CLAUDE CORRECTED THE PRODUCT TYPE BASED ON DIMENSIONS
                corrected_type = analysis.get('corrected_product_type', product_type)
                dimension_match = analysis.get('dimension_match', 'true')

                if corrected_type != product_type:
                    print(f"⚠️ PRODUCT TYPE CORRECTED: {product_type} → {corrected_type} (based on dimensions!)")
                    product_type = corrected_type

                print(f"👁️ Vision: {material}, {style}, {analysis.get('shape')}, confidence: {analysis.get('confidence')}")
                print(f"✅ Dimension match: {dimension_match}")

                # USE Claude's context-aware suggested name!
                unique_name = analysis.get('suggested_name', 'Form')

                # Ensure uniqueness - if name already used, ask Claude to generate another
                if unique_name in self.used_names:
                    unique_name = self.generate_unique_name(style, material)
                    print(f"✨ Name collision - using fallback: {unique_name}")
                else:
                    self.used_names.add(unique_name)
                    print(f"✨ Claude suggested name: {unique_name}")

                # Get shape from Claude analysis
                shape = analysis.get('shape', '')

                # Create dimension string for ALL tables (coffee tables and dining tables)
                dim_str = ""
                if product_type in ["table", "dining_table", "coffee_table"]:
                    try:
                        w = float(dimensions['width']) if dimensions['width'] != 'brak danych' else 0
                        d = float(dimensions['depth']) if dimensions['depth'] != 'brak danych' else 0

                        # Round tables: use single dimension (no diameter symbol)
                        if shape in ["okrągły", "round"] and w > 0:
                            dim_str = f"{int(w)}cm"
                        # Rectangular/square tables: use WxD
                        elif w > 0 and d > 0:
                            dim_str = f"{int(w)}x{int(d)}cm"
                    except:
                        pass

                # Create title with dimensions AND shape
                title = self.create_polish_title(product_type, style, material, unique_name, dim_str, shape)

                description = self.generate_html_description(
                    product_type, style, material, unique_name, dimensions, analysis, color_list
                )

                print(f"✅ Generated: {title}")

                # Update all rows for this PID
                for row_num, _ in rows:
                    # Update unique name (column F)
                    updates.append({
                        'range': f'F{row_num}',
                        'values': [[unique_name]]
                    })
                    # Update title (column G)
                    updates.append({
                        'range': f'G{row_num}',
                        'values': [[title]]
                    })
                    # Update description (column H)
                    updates.append({
                        'range': f'H{row_num}',
                        'values': [[description]]
                    })

                processed_count += 1

                # Delay between processing (API rate limit)
                if delay_seconds > 0:
                    time.sleep(delay_seconds)

            # Execute batch updates
            if updates:
                print(f"\n💾 Executing {len(updates)} updates...")

                batch_size = 50
                for i in range(0, len(updates), batch_size):
                    batch = updates[i:i + batch_size]
                    self.sheet.batch_update(batch)
                    print(f"   Updated batch {i//batch_size + 1}/{(len(updates) + batch_size - 1)//batch_size}")

            print(f"\n🎉 Successfully processed {processed_count} PIDs!")
            print(f"✨ All products now have Claude-generated descriptions with unique names!")

            return True

        except Exception as e:
            print(f"❌ Error processing products: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Universal Product Processor - Flexible row range processing"""

    processor = UniversalProductProcessor()

    # Parse command line arguments - NOW REQUIRED
    if len(sys.argv) >= 3:
        start_row = int(sys.argv[1])
        end_row = int(sys.argv[2])
        print(f"🔢 Processing rows {start_row}-{end_row}")
    elif len(sys.argv) == 2:
        # Single row argument - process just that row
        start_row = int(sys.argv[1])
        end_row = start_row
        print(f"🔢 Processing single row: {start_row}")
    else:
        print("❌ ERROR: Row range required!")
        print("\n📖 USAGE:")
        print("  python3 universal_product_processor.py <start_row> <end_row>")
        print("  python3 universal_product_processor.py <single_row>")
        print("\n✨ EXAMPLES:")
        print("  python3 universal_product_processor.py 231 232")
        print("  python3 universal_product_processor.py 145 187")
        print("  python3 universal_product_processor.py 250")
        print("\n💡 TIP: Provide the exact row numbers you want to process from the Google Sheet")
        sys.exit(1)

    # Product type mapping - extended range to cover all possible rows
    product_type_mapping = {
        (145, 187): "table",           # Dining tables
        (188, 211): "chair",           # Dining chairs
        (212, 247): "coffee_table",    # Coffee tables
        (248, 262): "armchair",        # Armchairs/fotele
        (263, 300): "chair"            # Additional chairs
    }

    # Process the range
    success = processor.process_product_range(
        start_row=start_row,
        end_row=end_row,
        product_type_mapping=product_type_mapping,
        delay_seconds=3.0
    )

    if success:
        print("\n🎉 Complete processing finished!")
    else:
        print("\n❌ Processing failed!")


if __name__ == "__main__":
    main()
