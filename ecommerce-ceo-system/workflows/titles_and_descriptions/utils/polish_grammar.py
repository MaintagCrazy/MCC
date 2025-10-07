#!/usr/bin/env python3
"""
Polish Grammar Module for Product Titles
========================================

This module provides grammatically correct Polish title generation with proper
adjective declension based on noun gender.

Usage:
    from utils.polish_grammar import PolishGrammar

    grammar = PolishGrammar()
    title = grammar.create_title("chair", "klasyczny", "fabric", "Stockholm")
    # Result: "klasyczne krzesło Stockholm z miękkiej tapicerki"
"""

class PolishGrammar:
    """Polish grammar handler for product titles"""

    def __init__(self):
        # Product type mapping with gender info
        self.type_mapping = {
            "chair": {"name": "krzesło", "gender": "neuter"},
            "table": {"name": "stół", "gender": "masculine"},
            "dining_table": {"name": "stół", "gender": "masculine"},  # FIX: Add dining_table
            "coffee_table": {"name": "stolik kawowy", "gender": "masculine"},
            "armchair": {"name": "fotel", "gender": "masculine"},
            "sofa": {"name": "sofa", "gender": "feminine"},
            "lamp": {"name": "lampa", "gender": "feminine"},
            "shelf": {"name": "półka", "gender": "feminine"}
        }

        # Adjective declensions for all genders
        self.adjective_forms = {
            "klasyczny": {"masculine": "klasyczny", "neuter": "klasyczne", "feminine": "klasyczna"},
            "nowoczesny": {"masculine": "nowoczesny", "neuter": "nowoczesne", "feminine": "nowoczesna"},
            "elegancki": {"masculine": "elegancki", "neuter": "eleganckie", "feminine": "elegancka"},
            "minimalistyczny": {"masculine": "minimalistyczny", "neuter": "minimalistyczne", "feminine": "minimalistyczna"},
            "vintage": {"masculine": "vintage", "neuter": "vintage", "feminine": "vintage"},
            "industrialny": {"masculine": "industrialny", "neuter": "industrialne", "feminine": "industrialna"},
            "skandynawski": {"masculine": "skandynawski", "neuter": "skandynawskie", "feminine": "skandynawska"},
            "loftowy": {"masculine": "loftowy", "neuter": "loftowe", "feminine": "loftowa"},
            "retro": {"masculine": "retro", "neuter": "retro", "feminine": "retro"},
            "rustykalny": {"masculine": "rustykalny", "neuter": "rustykalne", "feminine": "rustykalna"},
            "nowoczesny": {"masculine": "nowoczesny", "neuter": "nowoczesne", "feminine": "nowoczesna"},
            "stylowy": {"masculine": "stylowy", "neuter": "stylowe", "feminine": "stylowa"},
            "komfortowy": {"masculine": "komfortowy", "neuter": "komfortowe", "feminine": "komfortowa"},
            "praktyczny": {"masculine": "praktyczny", "neuter": "praktyczne", "feminine": "praktyczna"},
            "funkcjonalny": {"masculine": "funkcjonalny", "neuter": "funkcjonalne", "feminine": "funkcjonalna"}
        }

        # Material descriptions with proper declension
        # CRITICAL: ALL materials MUST have adjectival forms for titles
        self.material_mapping = {
            # Fabric materials - adjectival forms for chairs/armchairs
            "fabric": {"masculine": "tapicerowany", "neuter": "tapicerowane", "feminine": "tapicerowana"},
            "boucle": {"masculine": "boucle", "neuter": "boucle", "feminine": "boucle"},  # Invariable
            "bouclé teddy texture": {"masculine": "boucle", "neuter": "boucle", "feminine": "boucle"},
            "fabric (boucle/teddy texture)": {"masculine": "boucle", "neuter": "boucle", "feminine": "boucle"},
            "fabric (bouclé teddy texture)": {"masculine": "boucle", "neuter": "boucle", "feminine": "boucle"},

            # Leather materials
            "leather": {"masculine": "skórzany", "neuter": "skórzane", "feminine": "skórzana"},
            "leather and metal": {"masculine": "skórzany", "neuter": "skórzane", "feminine": "skórzana"},

            # Hard materials - marble
            "marble": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble and metal": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble top with metal base": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble top with polished metal base": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble top with polished stainless steel base": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble and polished metal": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble and wood with metal accents": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble top with painted metal base": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble top with painted wood or metal base": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},
            "marble and brushed metal": {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"},

            # Hard materials - stone/granite
            "stone": {"masculine": "kamienny", "neuter": "kamienne", "feminine": "kamienna"},
            "granite": {"masculine": "granitowy", "neuter": "granitowe", "feminine": "granitowa"},
            "Granite or marble composite with metal base": {"masculine": "kamienny", "neuter": "kamienne", "feminine": "kamienna"},
            "terrazzo": {"masculine": "lastryko", "neuter": "lastryko", "feminine": "lastryko"},  # Invariable

            # Other hard materials
            "wood": {"masculine": "drewniany", "neuter": "drewniane", "feminine": "drewniana"},
            "metal": {"masculine": "metalowy", "neuter": "metalowe", "feminine": "metalowa"},
            "glass": {"masculine": "szklany", "neuter": "szklane", "feminine": "szklana"},
            "concrete": {"masculine": "betonowy", "neuter": "betonowe", "feminine": "betonowa"}
        }

    def decline_adjective(self, adjective: str, gender: str) -> str:
        """Decline Polish adjectives for proper grammar"""
        adj_lower = adjective.lower()

        if adj_lower in self.adjective_forms:
            return self.adjective_forms[adj_lower][gender]
        else:
            # For unknown adjectives, try basic rules
            if gender == "neuter":
                if adj_lower.endswith("y"):
                    return adjective[:-1] + "e"
                elif adj_lower.endswith("i"):
                    return adjective[:-1] + "e"
            elif gender == "feminine":
                if adj_lower.endswith("y"):
                    return adjective[:-1] + "a"
                elif adj_lower.endswith("i"):
                    return adjective[:-1] + "a"

            return adjective  # Return as-is if no rule applies

    def get_material_description(self, material: str, gender: str) -> str:
        """Get properly declined material description

        CRITICAL: ALWAYS return a material - never empty!
        """
        # Try exact match first
        material_desc = self.material_mapping.get(material, None)

        if material_desc:
            if isinstance(material_desc, dict):
                return material_desc[gender]
            return material_desc

        # Fallback: Try to match partial keywords
        material_lower = material.lower()

        if "marble" in material_lower or "marmur" in material_lower:
            return {"masculine": "marmurowy", "neuter": "marmurowe", "feminine": "marmurowa"}[gender]
        elif "granite" in material_lower or "granit" in material_lower:
            return {"masculine": "granitowy", "neuter": "granitowe", "feminine": "granitowa"}[gender]
        elif "stone" in material_lower or "kamień" in material_lower or "kamien" in material_lower:
            return {"masculine": "kamienny", "neuter": "kamienne", "feminine": "kamienna"}[gender]
        elif "terrazzo" in material_lower or "lastryko" in material_lower:
            return "lastryko"
        elif "leather" in material_lower or "skór" in material_lower:
            return {"masculine": "skórzany", "neuter": "skórzane", "feminine": "skórzana"}[gender]
        elif "boucle" in material_lower or "bouclé" in material_lower:
            return "boucle"
        elif "fabric" in material_lower or "tapic" in material_lower:
            return {"masculine": "tapicerowany", "neuter": "tapicerowane", "feminine": "tapicerowana"}[gender]
        elif "wood" in material_lower or "drew" in material_lower:
            return {"masculine": "drewniany", "neuter": "drewniane", "feminine": "drewniana"}[gender]
        elif "metal" in material_lower:
            return {"masculine": "metalowy", "neuter": "metalowe", "feminine": "metalowa"}[gender]

        # Last resort fallback - return something!
        print(f"⚠️ Unknown material '{material}' - using generic 'nowoczesny'")
        return {"masculine": "nowoczesny", "neuter": "nowoczesne", "feminine": "nowoczesna"}[gender]

    def create_title(self, product_type: str, style: str, material: str, unique_name: str, dimensions: str = "", shape: str = "") -> str:
        """Create grammatically correct Polish title - CLEAN FORMAT

        COFFEE TABLES: "Nowoczesny okrągły stolik kawowy z kamienia 53cm Name"
        DINING TABLES: "Skandynawski prostokątny stół jadalny z drewna 160x90cm Name"
        ARMCHAIRS: "Nowoczesny fotel Name z tkaniny boucle"
        CHAIRS: "Nowoczesne krzesło Name z tkaniny"

        Format: Style + Shape + Type + z [material] + Dimensions + Name
        """

        # Get product type info
        type_info = self.type_mapping.get(product_type, {"name": "mebel", "gender": "masculine"})
        polish_type = type_info["name"]
        gender = type_info["gender"]

        # Decline style adjective based on gender
        style_declined = self.decline_adjective(style, gender)

        # Get material genitive for "z [material]" phrase
        material_genitive = self._get_material_genitive(material)

        # Decline shape adjective based on gender
        shape_declined = ""
        if shape:
            shape_map = {
                "okrągły": {"masculine": "okrągły", "neuter": "okrągłe", "feminine": "okrągła"},
                "prostokątny": {"masculine": "prostokątny", "neuter": "prostokątne", "feminine": "prostokątna"},
                "kwadratowy": {"masculine": "kwadratowy", "neuter": "kwadratowe", "feminine": "kwadratowa"},
                "owalny": {"masculine": "owalny", "neuter": "owalne", "feminine": "owalna"},
                "round": {"masculine": "okrągły", "neuter": "okrągłe", "feminine": "okrągła"},
                "rectangular": {"masculine": "prostokątny", "neuter": "prostokątne", "feminine": "prostokątna"},
                "square": {"masculine": "kwadratowy", "neuter": "kwadratowe", "feminine": "kwadratowa"},
                "oval": {"masculine": "owalny", "neuter": "owalne", "feminine": "owalna"}
            }
            shape_declined = shape_map.get(shape.lower(), {}).get(gender, "")

        # Build title based on product type
        if product_type == "coffee_table":
            # COFFEE TABLES: Style + Shape + stolik kawowy + z [material] + Dimensions + Name
            if shape_declined and dimensions:
                title = f"{style_declined} {shape_declined} {polish_type} z {material_genitive} {dimensions} {unique_name}"
            elif dimensions:
                title = f"{style_declined} {polish_type} z {material_genitive} {dimensions} {unique_name}"
            else:
                title = f"{style_declined} {polish_type} z {material_genitive} {unique_name}"

        elif product_type in ["table", "dining_table"]:
            # DINING TABLES: Style + Shape + stół jadalny + z [material] + Dimensions + Name
            if shape_declined and dimensions:
                title = f"{style_declined} {shape_declined} stół jadalny z {material_genitive} {dimensions} {unique_name}"
            elif dimensions:
                title = f"{style_declined} stół jadalny z {material_genitive} {dimensions} {unique_name}"
            else:
                title = f"{style_declined} stół jadalny z {material_genitive} {unique_name}"

        elif product_type == "armchair":
            # ARMCHAIRS: Style + fotel + Name + z [material]
            title = f"{style_declined} {polish_type} {unique_name} z {material_genitive}"

        else:
            # CHAIRS: Style + krzesło + Name + z [material]
            title = f"{style_declined} {polish_type} {unique_name} z {material_genitive}"

        # Capitalize first letter
        return title[0].upper() + title[1:] if title else title

    def _get_material_genitive(self, material: str) -> str:
        """Get genitive (dopełniacz) form of material for 'z [material]' construction"""
        material_lower = material.lower()

        # Genitive forms for common materials
        genitive_map = {
            "marble": "marmuru",
            "marble and metal": "marmuru",
            "marble top with metal base": "marmuru",
            "marble top with polished metal base": "marmuru",
            "stone": "kamienia",
            "granite": "granitu",
            "granite or marble composite with metal base": "kamienia",
            "terrazzo": "lastryko",
            "leather": "skóry",
            "leather and metal": "skóry",
            "fabric": "tkaniny",
            "boucle": "tkaniny boucle",
            "fabric (boucle/teddy texture)": "tkaniny boucle",
            "fabric (bouclé teddy texture)": "tkaniny boucle",
            "wood": "drewna",
            "metal": "metalu",
            "glass": "szkła",
            "concrete": "betonu"
        }

        # Try exact match
        if material in genitive_map:
            return genitive_map[material]

        # Fallback based on keywords
        if "marble" in material_lower or "marmur" in material_lower:
            return "marmuru"
        elif "granite" in material_lower or "granit" in material_lower:
            return "granitu"
        elif "stone" in material_lower or "kamień" in material_lower or "kamien" in material_lower:
            return "kamienia"
        elif "terrazzo" in material_lower or "lastryko" in material_lower:
            return "lastryko"
        elif "leather" in material_lower or "skór" in material_lower:
            return "skóry"
        elif "boucle" in material_lower or "bouclé" in material_lower:
            return "tkaniny boucle"
        elif "fabric" in material_lower or "tapic" in material_lower:
            return "tkaniny"
        elif "wood" in material_lower or "drew" in material_lower:
            return "drewna"
        elif "metal" in material_lower:
            return "metalu"

        return "materiału"  # Generic fallback

    def get_product_types(self) -> list:
        """Get list of supported product types"""
        return list(self.type_mapping.keys())

    def get_adjectives(self) -> list:
        """Get list of supported adjectives"""
        return list(self.adjective_forms.keys())

    def get_materials(self) -> list:
        """Get list of supported materials"""
        return list(self.material_mapping.keys())


# Quick test function
def test_grammar():
    """Test the grammar system"""
    grammar = PolishGrammar()

    test_cases = [
        ("chair", "klasyczny", "fabric", "Stockholm"),
        ("table", "nowoczesny", "wood", "Berlin"),
        ("coffee_table", "elegancki", "marble", "Prague"),
        ("sofa", "minimalistyczny", "leather", "Vienna")
    ]

    print("🧪 Testing Polish Grammar System:")
    print("=" * 50)

    for product_type, style, material, name in test_cases:
        title = grammar.create_title(product_type, style, material, name)
        print(f"✅ {product_type} + {style} + {material} → {title}")


if __name__ == "__main__":
    test_grammar()