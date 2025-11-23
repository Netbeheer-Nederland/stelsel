import yaml
import json
import glob
import os

# CONFIG
MODELS_DIR = "/registers"
OUTPUT_FILE = "/docs/_registers/concept_usages.json"

# --- Helper functies ---

def get_full_class_uri(data, class_name, class_def):
    """
    Construeert de volledige URI van een LinkML class.
    """
    prefixes = data.get('prefixes', {})
    default_prefix = data.get('default_prefix')
    base_uri = prefixes.get(default_prefix, "")
    
    # 1. Haal de raw waarde op (zoals jij vroeg)
    raw_uri = class_def.get('class_uri')

    # 2. Logica om de volledige URI te bouwen
    if raw_uri:
        if ":" in raw_uri:
            # Het is een CURIE (bv. 'schema:Person') -> expandeer
            prefix, local = raw_uri.split(":", 1)
            return prefixes.get(prefix, "") + local
        else:
            # Het is een lokale ID (bv. 'Aangeslotene') -> plak default prefix ervoor
            return base_uri + raw_uri
    else:
        # Geen class_uri opgegeven? LinkML gebruikt dan standaard de Class Naam
        return base_uri + class_name

# --- Main code ---

usages = {}

def expand_curie(curie, prefixes):
    if ":" not in curie: return curie
    prefix, local_id = curie.split(":", 1)
    if prefix in prefixes:
        return prefixes[prefix] + local_id
    return curie

files = glob.glob(os.path.join(MODELS_DIR, "**/*.linkml.yml"), recursive=True)

for file_path in files:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    if not data or 'classes' not in data: continue

    model_id = data.get('id')
    model_name = data.get('name', model_id)
    model_title = data.get('title', model_name)
    prefixes = data.get('prefixes', {})
    
    # Loop door classes
    for class_name, class_def in data.get('classes', {}).items():
        class_uri = get_full_class_uri(data, class_name, class_def)

        # Check alle soorten mappings
        all_mappings = []
        all_mappings.extend(class_def.get('exact_mappings', []))
        all_mappings.extend(class_def.get('close_mappings', []))
        all_mappings.extend(class_def.get('related_mappings', []))
        all_mappings.extend(class_def.get('narrow_mappings', []))
        all_mappings.extend(class_def.get('broad_mappings', []))
        
        for mapping in all_mappings:
            full_uri = expand_curie(mapping, prefixes)
            
            if full_uri not in usages:
                usages[full_uri] = []
            
            usages[full_uri].append({
                "model_title": model_title,
                "model_id": model_id,
                "model_name": model_name,
                "element_type": "Class",
                "element_name": class_name,
                "mapping": mapping, # begrip:aangeslotene
                "url": class_uri
            })

    # Hier zou je hetzelfde kunnen doen voor 'enums' en 'slots' (attributes)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(usages, f, indent=2)

print(f"Index gegenereerd: {len(usages)} begrippen gevonden in modellen.")
