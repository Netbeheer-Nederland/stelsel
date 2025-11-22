import sys
import os
import xml.etree.ElementTree as ET
import yaml
import re
import unicodedata

# TODO:
# - relaties naar entiteiten in andere registers
# - max-multipliciteit van eigenschap
# - sorteer classes


CARDINALITY_MAPPING = {
    'none':      {'required': False, 'multivalued': True, 'annotation': '"*"'},
    'ERmandOne':     {'required': True, 'multivalued': False, 'annotation': '1..1'},
    'ERzeroToOne': {'required': False, 'multivalued': False, 'annotation': '0..1'},
    'ERoneToMany':{'required': True, 'multivalued': True, 'annotation': '1..*'},
    'ERzeroToMany':{'required': False, 'multivalued': True, 'annotation': '"*"'},
}

def clean_and_convert_name(name_raw, is_entity_name=False, parse_slot_prefixes_symbols=True):
    if name_raw is None: name_raw = ""
    cleaned_name = re.sub(r'\s+', ' ', name_raw).strip()

    flags = {
        'is_part_of_natural_key': False, 'is_required_explicit': False,
        'is_optional_explicit': False, 'is_derivable': False,
    }
    temp_name = cleaned_name

    if not is_entity_name and parse_slot_prefixes_symbols:
        if temp_name.startswith('●'):
            flags['is_required_explicit'] = True
            temp_name = temp_name[1:].strip()
        elif temp_name.startswith('○'):
            flags['is_optional_explicit'] = True
            temp_name = temp_name[1:].strip()
        elif temp_name.startswith('#'):
            flags['is_part_of_natural_key'] = True
            temp_name = temp_name[1:].strip()
            if temp_name.startswith('○'):
                flags['is_optional_explicit'] = True
                temp_name = temp_name[1:].strip()
            else:
                flags['is_required_explicit'] = True
    
    # '/' parsing: als parse_slot_prefixes_symbols True is, of als het een entiteitsnaam is (voor /MyEntity)
    # Voor slots, als parse_slot_prefixes_symbols False is, parsen we '/' hier niet als speciaal.
    if (not is_entity_name and parse_slot_prefixes_symbols) or is_entity_name:
        if temp_name.startswith('/'):
            flags['is_derivable'] = True
            temp_name = temp_name[1:].strip()

    name_without_symbols_for_description = temp_name.strip()
    linkml_name = name_without_symbols_for_description

    if is_entity_name:
        linkml_name = linkml_name.replace('"', '').replace("'", "").replace("\\", "")
        if not linkml_name:
            linkml_name = "InvalidEntityName"
    else:
        linkml_name = linkml_name.replace('"', '').replace("'", "").replace("\\", "")
        if name_raw.strip().startswith('⏲') and not any(name_raw.strip()[1:].lstrip().lower().startswith(kw) for kw in ["tijdlijn", "levensduur"]):
             print(f"Info: Slotnaam '{name_raw}' begon met ⏲ maar niet met een bekende tijdlijn annotatie. ⏲ wordt als deel van de naam gezien indien overgebleven.")
        if not linkml_name:
            linkml_name = "invalid_slot_name"
    return linkml_name, flags, name_without_symbols_for_description

import html # BELANGRIJK: voeg deze import toe bovenaan je script

def parse_drawio_xml(xml_string):
    cells = {}
    try:
        root = ET.fromstring(xml_string)
        for cell in root.findall(".//mxCell"): cells[cell.get('id')] = cell
    except Exception as e: print(f"Fout bij parsen XML: {e}"); return None, None

    entities_data = {}
    candidate_slots = []

    # Eerste pass: Entiteiten identificeren
    for cell_id, cell in cells.items():
        style = cell.get('style', '')
        value_raw_xml = cell.get('value', '') 
        
        value_text_only = ""
        if value_raw_xml:
            value_decoded = html.unescape(value_raw_xml)
            value_processed = value_decoded.replace('\u00A0', ' ') # Non-breaking space
            value_processed = re.sub(r'<[^>]+>', ' ', value_processed).strip() # Strip alle HTML
            value_text_only = re.sub(r'\s+', ' ', value_processed).strip() # Normaliseer whitespace

        is_entity_shape = False
        if cell.get('vertex') == '1':
            if 'swimlane' in style or \
               ('childLayout=stackLayout' in style and 'horizontal=1' in style) or \
               'shape=entity' in style:
                is_entity_shape = True
        
        parent_id_check = cell.get('parent')
        if parent_id_check and parent_id_check in entities_data: is_entity_shape = False

        if is_entity_shape and value_text_only:
            entity_name_linkml, _, _ = clean_and_convert_name(value_text_only, is_entity_name=True)
            if not entity_name_linkml or entity_name_linkml == "InvalidEntityName":
                # print(f"Waarschuwing: Entiteit '{value_text_only}' (ID: {cell_id}) ongeldig. Overslaan.")
                continue
            entities_data[cell_id] = {
                'name_raw': value_text_only, 'name_linkml': entity_name_linkml, 'id': cell_id,
                'flags': {'has_timeline_geldigheid': False, 'has_timeline_registratie': False,
                          'has_timeline_effectuering': False, 'has_levensduur': False,
                          'levensduur_begin': None, 'levensduur_einde': None}
            }

    # Tweede pass: Attributen, Tijdlijnen, Relaties
    for cell_id, cell in cells.items():
        parent_id_xml = cell.get('parent')
        raw_xml_value_from_cell = cell.get('value', '') # Ruwe XML-waarde
        style = cell.get('style', '')
        source_id, target_id = cell.get('source'), cell.get('target')

        if cell.get('vertex') == '1' and raw_xml_value_from_cell and parent_id_xml in entities_data:
            # print(f"DEBUG Raw Cell Value (ID {cell_id}): {raw_xml_value_from_cell[:200]}")

            decoded_value = html.unescape(raw_xml_value_from_cell)
            processed_value = decoded_value.replace('\u00A0', ' ')
            # print(f"DEBUG Value na unescape en U+00A0 (ID {cell_id}): {processed_value[:200]}")
            
            line_break_separator = "%%%LINE_BREAK%%%"
            processed_value_with_sep = re.sub(r'</?(div|p|br)(/?)?>', line_break_separator, processed_value, flags=re.IGNORECASE)
            # print(f"DEBUG Value na separator normalisatie (ID {cell_id}): {processed_value_with_sep[:200]}")

            text_no_html = re.sub(r'<[^>]+>', '', processed_value_with_sep) # Strip resterende HTML
            # print(f"DEBUG Value na HTML strip (ID {cell_id}): {text_no_html[:200]}")
            
            raw_lines = text_no_html.split(line_break_separator)
            attribute_lines_from_cell = []
            for i, line_segment in enumerate(raw_lines):
                final_line = re.sub(r'\s+', ' ', line_segment).strip() 
                # print(f"DEBUG Gesplitste en genormaliseerde regel {i} (ID {cell_id}): '{final_line}'")
                if final_line:
                    attribute_lines_from_cell.append(final_line)
            
            if not attribute_lines_from_cell and raw_xml_value_from_cell.strip(): # Fallback
                temp_fallback = html.unescape(raw_xml_value_from_cell)
                temp_fallback = temp_fallback.replace('\u00A0', ' ')
                temp_fallback = re.sub(r'<[^>]+>', '', temp_fallback) 
                temp_fallback = re.sub(r'\s+', ' ', temp_fallback).strip()
                if temp_fallback:
                    attribute_lines_from_cell = [temp_fallback]
                    # print(f"DEBUG Fallback regel (ID {cell_id}): '{temp_fallback}'")

            if not attribute_lines_from_cell: continue

            current_entity_flags = entities_data[parent_id_xml]['flags']
            active_attribute_parts = None

            def finalize_active_attribute_and_clear():
                nonlocal active_attribute_parts
                if active_attribute_parts:
                    # print(f"DEBUG Finalizing. raw_parts: {active_attribute_parts['raw_parts']}")
                    # print(f"DEBUG Finalizing. name_parts: {active_attribute_parts['name_parts']}")
                    combined_name_for_cleaning = " ".join(active_attribute_parts['name_parts']).strip()
                    # print(f"DEBUG Finalizing. combined_name_for_cleaning: '{combined_name_for_cleaning}'")
                    
                    is_combined_derivable = False
                    if combined_name_for_cleaning.startswith('/'):
                        is_combined_derivable = True
                        combined_name_for_cleaning = combined_name_for_cleaning[1:].strip()

                    linkml_name, _, name_without_symbols = clean_and_convert_name(
                        combined_name_for_cleaning, 
                        is_entity_name=False, 
                        parse_slot_prefixes_symbols=False 
                    )
                    final_flags = active_attribute_parts['flags'].copy()
                    if is_combined_derivable: final_flags['is_derivable'] = True
                    raw_full_name = " ".join(active_attribute_parts['raw_parts']).strip()
                    # print(f"DEBUG Finalizing. raw_full_name voor output: '{raw_full_name}'")
                    
                    if not linkml_name or linkml_name == "invalid_slot_name":
                        if raw_full_name: print(f"Waarschuwing: Attribuut '{raw_full_name}' (van entiteit '{entities_data[parent_id_xml]['name_linkml']}') resulteerde in ongeldige LinkML slotnaam. Overslaan.")
                    else:
                        # print(f"DEBUG Toevoegen aan candidate_slots: name_linkml='{linkml_name}', name_raw='{raw_full_name}'")
                        candidate_slots.append({
                            'type': 'attribute', 'parent_entity_id': parent_id_xml,
                            'name_raw': raw_full_name, 'name_linkml': linkml_name,
                            'name_without_symbols': name_without_symbols, 'flags': final_flags,
                        })
                active_attribute_parts = None

            for line_content in attribute_lines_from_cell:
                # print(f"DEBUG Verwerkte regel voor attribuut/tijdlijn (ID {cell_id}): '{line_content}'")
                if not line_content: continue

                is_timeline_annotation = False
                if line_content.startswith('⏲'):
                    finalize_active_attribute_and_clear()
                    timeline_text_original_case = line_content[1:].lstrip()
                    timeline_text_lower = timeline_text_original_case.lower()
                    if not timeline_text_lower: 
                        current_entity_flags['has_timeline_geldigheid'] = True; is_timeline_annotation = True
                    elif timeline_text_lower.startswith("levensduur"):
                        current_entity_flags['has_levensduur'] = True; is_timeline_annotation = True
                        match_l = re.match(r"levensduur", timeline_text_original_case, re.IGNORECASE)
                        remaining = timeline_text_original_case[match_l.end():].lstrip() if match_l else ""
                        attrs_match = re.match(r"^\s*\(([^,]+),\s*([^)]+)\)\s*", remaining)
                        if attrs_match:
                            current_entity_flags['levensduur_begin'] = attrs_match.group(1).strip()
                            current_entity_flags['levensduur_einde'] = attrs_match.group(2).strip()
                    elif timeline_text_lower.startswith("tijdlijn geldigheid"): current_entity_flags['has_timeline_geldigheid'] = True; is_timeline_annotation = True
                    elif timeline_text_lower.startswith("tijdlijn registratie"): current_entity_flags['has_timeline_registratie'] = True; is_timeline_annotation = True
                    elif timeline_text_lower.startswith("tijdlijn effectuering"): current_entity_flags['has_timeline_effectuering'] = True; is_timeline_annotation = True
                    else: pass 
                    if is_timeline_annotation: continue

                is_new_attribute_start_symbol = False
                if line_content.startswith(('●', '○', '#', '/')):
                    is_new_attribute_start_symbol = True

                if is_new_attribute_start_symbol or not active_attribute_parts:
                    finalize_active_attribute_and_clear()
                    name_part_after_prefixes, initial_flags, _ = clean_and_convert_name(
                        line_content, is_entity_name=False, parse_slot_prefixes_symbols=True
                    )
                    active_attribute_parts = {
                        'name_parts': [name_part_after_prefixes.strip()] if name_part_after_prefixes.strip() else [],
                        'flags': initial_flags, 'raw_parts': [line_content] 
                    }
                else: 
                    if active_attribute_parts:
                        active_attribute_parts['name_parts'].append(line_content.strip())
                        active_attribute_parts['raw_parts'].append(line_content)
            finalize_active_attribute_and_clear()

        elif cell.get('edge') == '1' and source_id in entities_data and target_id in entities_data:
            relation_label_raw_xml = raw_xml_value_from_cell # Gebruik hier ook de algemene raw_xml_value_from_cell
            
            cleaned_label = ""
            if relation_label_raw_xml:
                cleaned_label = html.unescape(relation_label_raw_xml)
                cleaned_label = cleaned_label.replace('\u00A0', ' ')
                cleaned_label = re.sub(r'<[^>]+>', ' ', cleaned_label).strip()
                cleaned_label = re.sub(r'\s+', ' ', cleaned_label).strip()
            
            if not cleaned_label and relation_label_raw_xml.strip(): 
                cleaned_label = "relatie" 
            elif not cleaned_label: 
                cleaned_label = "relatie" 

            base_name, flags, label_no_sym = clean_and_convert_name(cleaned_label, is_entity_name=False)
            if not base_name or base_name == "invalid_slot_name":
                continue

            start_arrow_match = re.search(r'startArrow=([^;]*)', style)
            end_arrow_match = re.search(r'endArrow=([^;]*)', style)
            candidate_slots.append({
                'type': 'relation', 'id': cell_id, 'parent_entity_id': source_id,
                'relation_target_id': target_id, 'name_raw': cleaned_label,
                'name_linkml_base': base_name, 'label_without_symbols': label_no_sym, 'flags': flags,
                'cardinality_source_style': start_arrow_match.group(1) if start_arrow_match else 'none',
                'cardinality_target_style': end_arrow_match.group(1) if end_arrow_match else 'none',
            })
    return entities_data, candidate_slots

def convert_to_linkml_schema(entities_data, candidate_slots):
    schema_dict = {
        "id": "https://voorbeeld.com/mijnmodel",
        "name": "mijnmodel",
        "title": "Conceptueel informatiemodel",
        "description": "Automatisch gegenereerd schema.",
        "version": "1.0.0-draft",
        "default_range": "Tekst",
        "prefixes": {
            "mijmodel": "https://voorbeeld.com/mijnmodel",
            "nbnl": "https://begrippen.netbeheernederland.nl/energiesysteembeheer/nl/page/",
            "nbility": "https://nbility-model.github.io/NBility-business-capabilities-Archi/"
        },
        "default_prefix": "https://voorbeeld.com/mijnmodel/",
        "classes": {},
        "types": {
            "Datum": {
                "description": "kalenderdatum, zonder tijdsaanduiding",
                "base": "date"
            },
            "Geheel getal": {
                "description": "getal zonder decimalen",
                "base": "int",
            },
            "Getal": {
                "description": "voorstelling van een hoeveelheid",
                "base": "float"
            },
            "Tekst": {
                "description": "aanduiding bedoeld voor mensen, zonder vaste structuur of betekenis",
                "base": "str"
            },
            "Tijdsduur": {
                "description": "lengte van een tijdsinterval, bijvoorbeeld een uur of een dag",
                "base": "duration"
            },
            "Tijdstip": {
                "description": "exacte aanduiding van datum en tijd, inclusief eventueel tijdzone-informatie",
                "base": "datetime"
            },
            "Waar of onwaar": {
                "description": "binaire aanduiding die aangeeft of een propositie of kenmerk van toepassing is (waar) of niet van toepassing is (onwaar)",
                "base": "bool"
            },
            "URI": {
                "description": "uniforme aanduiding van een externe of interne bron",
                "base": "uri"
            }
        }
    }
    if not entities_data: return schema_dict

    entity_id_to_linkml_name = {eid: d['name_linkml'] for eid, d in entities_data.items()}
    slots_by_entity_id = {}
    for s_info in candidate_slots:
        pid = s_info['parent_entity_id']
        slots_by_entity_id.setdefault(pid, []).append(s_info)

    for eid, einfo in entities_data.items():
        class_name = einfo['name_linkml']
        entity_flags = einfo.get('flags', {})
        class_def = {"description": f"Definitie van {class_name}"}
        
        annotations = {}
        if entity_flags.get('has_timeline_geldigheid'): annotations['tijdlijn_geldigheid'] = True
        if entity_flags.get('has_timeline_registratie'): annotations['tijdlijn_registratie'] = True
        if entity_flags.get('has_timeline_effectuering'): annotations['tijdlijn_effectuering'] = True
        if entity_flags.get('has_levensduur'):
            annotations['levensduur'] = True
            if entity_flags.get('levensduur_begin'): annotations['levensduur_begin'] = entity_flags['levensduur_begin']
            if entity_flags.get('levensduur_einde'): annotations['levensduur_einde'] = entity_flags['levensduur_einde']
        if annotations: class_def['annotations'] = annotations
        
        schema_dict["classes"][class_name] = class_def
        class_attrs, natural_keys = {}, []

        for s_info in slots_by_entity_id.get(eid, []):
            s_flags = s_info['flags']
            s_def = {}
            s_name_linkml = ""

            if s_info['type'] == 'attribute':
                s_name_linkml = s_info['name_linkml']
                is_req = False
                if s_flags.get('is_optional_explicit'): is_req = False
                elif s_flags.get('is_required_explicit'): is_req = True
                if is_req: s_def['required'] = True
                if s_flags.get('is_derivable'): s_def.setdefault('annotations', {})['derivation_rule'] = '<some rule>'
                
            elif s_info['type'] == 'relation':
                target_id = s_info['relation_target_id']
                target_linkml_name = entity_id_to_linkml_name.get(target_id)
                if not target_linkml_name: print(f"Waarschuwing: Relatie van {class_name} naar onbekend doel ID {target_id}. Overslaan."); continue

                base_slot_name = s_info['name_linkml_base']
                target_slot_part = target_linkml_name.replace(" ", "_")
                s_name_linkml = f"{base_slot_name.lower()} ({target_slot_part})" if base_slot_name.lower() not in ["relatie", ""] else target_slot_part
                s_name_linkml, _, _ = clean_and_convert_name(s_name_linkml, is_entity_name=False, parse_slot_prefixes_symbols=False)

                if not s_name_linkml or s_name_linkml == "invalid_slot_name": print(f"Waarschuwing: Relatie slotnaam ongeldig. Overslaan."); continue
                
                card_info = CARDINALITY_MAPPING.get(s_info['cardinality_target_style'], CARDINALITY_MAPPING['none'])
                inv_card_info = CARDINALITY_MAPPING.get(s_info['cardinality_source_style'], CARDINALITY_MAPPING['none'])
                
                s_def = {"range": target_linkml_name, "required": card_info['required'],
                           "multivalued": card_info['multivalued'],
                           "annotations": {"inverse_cardinality": inv_card_info['annotation']}}
                if s_flags.get('is_derivable'): s_def['annotations']['derivation_rule'] = '<some rule>'

            if s_name_linkml:
                if s_name_linkml not in class_attrs:
                    class_attrs[s_name_linkml] = s_def
                    if s_flags.get('is_part_of_natural_key'): natural_keys.append(s_name_linkml)
                else: print(f"Waarschuwing: Duplicaat slot '{s_name_linkml}' in '{class_name}'.")
        
        if class_attrs: class_def['attributes'] = {k: class_attrs[k] for k in sorted(class_attrs.keys(), key=lambda x: x.lower())}
        if natural_keys: class_def['unique_keys'] = {"primary_key": {"unique_key_slots": sorted(natural_keys, key=lambda x: x.lower())}}
    
    return schema_dict

def main():
    input_file = None
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        if not os.path.exists(input_file): print(f"Fout: Bestand '{input_file}' niet gevonden."); sys.exit(1)
            
    if input_file is None:
        print("--- Draw.io naar LinkML Converter ---\n[Conventies details... zie code of vorige output]\n")
        while True:
            try:
                input_f_path = input("Pad naar draw.io XML (of 'exit'): ").strip()
                if input_f_path.lower() == 'exit': sys.exit(0)
                if os.path.exists(input_f_path): input_file = input_f_path; break
                else: print("Fout: Bestand niet gevonden.")
            except KeyboardInterrupt: print("\nGestopt."); sys.exit(0)
    
    if not input_file: print("Geen input. Stoppen."); sys.exit(1)

    try:
        print(f"Lezen: {input_file}")
        with open(input_file, 'r', encoding='utf-8') as f: xml_content = f.read()
        
        print("Parsen draw.io data...")
        entities_data, candidate_slots = parse_drawio_xml(xml_content)
        
        if entities_data is None: print("XML parsen mislukt."); sys.exit(1)
        if not entities_data and not candidate_slots: print("Geen entiteiten/slots gevonden.")

        num_attrs = sum(1 for s in candidate_slots if s['type'] == 'attribute')
        num_rels = sum(1 for s in candidate_slots if s['type'] == 'relation')
        print(f"Gevonden: {len(entities_data)} entiteiten, {num_attrs} attributen, {num_rels} relaties.")
        
        print("Converteren naar LinkML...")
        linkml_schema = convert_to_linkml_schema(entities_data, candidate_slots)
        
        out_dir = os.path.dirname(input_file)
        in_fname_base, _ = os.path.splitext(os.path.basename(input_file))
        if in_fname_base.lower().endswith('.drawio'): in_fname_base = in_fname_base[:-len('.drawio')]
        out_f_path = os.path.join(out_dir, f"{in_fname_base}.yaml")
        
        print(f"Opslaan LinkML schema naar: {out_f_path}")
        with open(out_f_path, 'w', encoding='utf-8') as f:
            yaml.dump(linkml_schema, f, sort_keys=False, indent=2, default_flow_style=False, allow_unicode=True)
        
        print("\nConversie voltooid!")
    except FileNotFoundError: print(f"Fout: Bestand '{input_file}' niet gevonden.")
    except Exception as e: print(f"\nOnverwachte fout: {e}"); import traceback; traceback.print_exc()
    finally: input("\nDruk op Enter om af te sluiten...")

if __name__ == "__main__":
    main()