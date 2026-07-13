import sys, os, yaml

BUILD_DIR = sys.argv[1] if len(sys.argv) > 1 else "docs" # Lees de build-dir uit argumenten, standaard is "docs"

BASE_INPUT_MODELS = "registers"
BASE_OUTPUT_MODELS = os.path.join(BUILD_DIR, "_registers")

os.makedirs(BASE_OUTPUT_MODELS, exist_ok=True)

def get_model_metadata(yaml_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    name = data.get("title") or data.get("name")
    version = str(data.get("version", os.path.basename(os.path.dirname(yaml_path))))
    return name, version

# Itereer over modellen
for model_dir in sorted(os.listdir(BASE_INPUT_MODELS)):
    model_path = os.path.join(BASE_INPUT_MODELS, model_dir)
    if not os.path.isdir(model_path): continue

    model_name = None
    latest_version = None
    latest_stable_version = None
    for version_dir in sorted(os.listdir(model_path), reverse=True):
        yaml_path = os.path.join(model_path, version_dir, f"{model_dir}.linkml.yml")
        if not os.path.exists(yaml_path):
            continue
        if latest_version is None:
            latest_version = version_dir
        _, version_number = get_model_metadata(yaml_path)
        if "-draft" not in version_number:
            latest_stable_version = version_dir
            break
    redirect_target = latest_stable_version or latest_version
    if redirect_target is not None:
        yaml_path = os.path.join(model_path, redirect_target, f"{model_dir}.linkml.yml")
        model_name, _ = get_model_metadata(yaml_path)
    else:
        print(f'Skipping {model_dir}: no redirect target')
        continue

    # Genereer _registers/<modelnaam>/index.md
    model_output_dir = os.path.join(BASE_OUTPUT_MODELS, model_dir)
    os.makedirs(model_output_dir, exist_ok=True)

    model_index_path = os.path.join(model_output_dir, "index.md")
    with open(model_index_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f'title: "{model_name}"\n')
        f.write(f'redirect: "{redirect_target}"\n')
        f.write("---\n\n")
        f.write(f"# {model_name}\n\n")
