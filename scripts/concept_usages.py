import yaml
import json
import glob
import os

# CONFIG
MODELS_DIR = "registers"
OUTPUT_FILE = "docs/_registers/concept_usages.json"

# --- Helper functies ---

def add_usage(usages_dict, target_concept_uri, model_name, model_url, el_name, el_type, el_url):
    """Voegt een verwijzing toe aan de usages dictionary."""
    if not target_concept_uri: return
    
    if target_concept_uri not in usages_dict:
        usages_dict[target_concept_uri] = []
    
    # Voorkom exacte duplicaten
    entry = {
        "model_name": model_name,
        "model_url": model_url,
        "element_name": el_name,
        "element_type": el_type,
        "element_url": el_url
    }
    
    if entry not in usages_dict[target_concept_uri]:
        usages_dict[target_concept_uri].append(entry)

def get_full_uri(data, name, element_def, key_for_uri='class_uri'):
    """Generieke functie om URI op te bouwen voor class, slot of enum"""
    prefixes = data.get('prefixes', {})
    default_prefix = data.get('default_prefix')
    base_uri = prefixes.get(default_prefix, "")
    
    raw_uri = element_def.get(key_for_uri) or element_def.get('uri')
    
    if raw_uri:
        if ":" in raw_uri:
            prefix, local = raw_uri.split(":", 1)
            return prefixes.get(prefix, "") + local
        return base_uri + raw_uri
    return base_uri + name

# --- HOOFD LOGICA ---

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

    # 1. CLASSES
    for class_name, class_def in data.get('classes', {}).items():
        class_uri = get_full_uri(data, class_name, class_def, 'class_uri')
        
        # Verzamel mappings
        mappings = []
        mappings.extend(class_def.get('exact_mappings', []))
        mappings.extend(class_def.get('close_mappings', []))
        mappings.extend(class_def.get('related_mappings', []))
        mappings.extend(class_def.get('narrow_mappings', []))
        mappings.extend(class_def.get('broad_mappings', []))
        
        for m in mappings:
            full_map_uri = expand_curie(m, prefixes)
            add_usage(usages, full_map_uri, model_title, model_id, class_name, "entiteit", class_uri)

    # 2. SLOTS (Attributen/Relaties)
    for slot_name, slot_def in data.get('slots', {}).items():
        # Slots hebben vaak een 'slot_uri', anders fallback op naam
        slot_uri = get_full_uri(data, slot_name, slot_def, 'slot_uri')
        
        mappings = []
        mappings.extend(slot_def.get('exact_mappings', []))
        mappings.extend(slot_def.get('close_mappings', []))
        mappings.extend(class_def.get('related_mappings', []))
        mappings.extend(class_def.get('narrow_mappings', []))
        mappings.extend(class_def.get('broad_mappings', []))
        
        for m in mappings:
            full_map_uri = expand_curie(m, prefixes)
            add_usage(usages, full_map_uri, model_title, model_id, slot_name, "eigenschap", slot_uri)

    # 3. ENUMS (Lijsten)
    for enum_name, enum_def in data.get('enums', {}).items():
        enum_uri = get_full_uri(data, enum_name, enum_def, 'enum_uri')
        
        # 3a. Mappings op de Enum zelf (de lijst als geheel)
        mappings = []
        mappings.extend(enum_def.get('exact_mappings', []))
        mappings.extend(slot_def.get('close_mappings', []))
        mappings.extend(class_def.get('related_mappings', []))
        mappings.extend(class_def.get('narrow_mappings', []))
        mappings.extend(class_def.get('broad_mappings', []))
        
        for m in mappings:
            full_map_uri = expand_curie(m, prefixes)
            add_usage(usages, full_map_uri, model_title, model_id, enum_name, "waardelijst", enum_uri)
            
        # 3b. Mappings op de waarden (Permissible Values -> meaning)
        for val_name, val_def in enum_def.get('permissible_values', {}).items():
            
            # Soms is val_def None (als het puur een lijst strings is in YAML), vang dat af:
            if not val_def: continue
            
            # Check op 'meaning' (dit is de specifieke LinkML term voor semantic mapping van waarden)
            meaning = val_def.get('meaning')
            
            if meaning:
                full_meaning_uri = expand_curie(meaning, prefixes)
                
                add_usage(
                    usages, 
                    full_meaning_uri, 
                    model_title, 
                    model_id, 
                    f"{enum_name}: {val_name}", # Duidelijke naam: "Type: Waarde"
                    "waarde", 
                    enum_uri
                )














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
                "model_name": model_title,
                "model_uri": model_id,
                "element_name": class_name,
                "element_type": "entiteit",
                "element_uri": class_uri
            })

    # Hier zou je hetzelfde kunnen doen voor 'enums' en 'slots' (attributes)

with open(OUTPUT_FILE, 'w') as f:
    json.dump(usages, f, indent=2)

print(f"Index gegenereerd: {len(usages)} begrippen gevonden in modellen.")
