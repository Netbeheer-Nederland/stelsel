import os, shutil, sys, glob
from invoke import task
from urllib.request import urlretrieve


# ==============================================================================
# CONFIGURATIE
# ==============================================================================

def running_in_docker():
    return os.environ.get("RUNNING_IN_DOCKER")

DOCS_DIR = "docs"
STAGING_DIR = "_staging"
SITE_DIR = "_site"
REGISTERS_SOURCE_DIR = "registers"
REGISTERS_TARGET_DIR = os.path.join(STAGING_DIR, "_registers")

PYTHON = sys.executable
JEKYLL = "jekyll" if running_in_docker() else "bundle exec jekyll"

# ==============================================================================
# HULPFUNCTIES (LOGICA)
# ==============================================================================

def clean_dir(path):
    """Veilig map leegmaken."""
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError:
            pass # Negeren als bestand in gebruik is

def fetch_external_data():
    """Download externe data (zoals begrippenlijst)."""
    print("⬇️  Externe data downloaden...")
    data_dir = os.path.join(STAGING_DIR, "_data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    url = "https://begrippen.netbeheernederland.nl/begrippen.json"
    dest = os.path.join(data_dir, "begrippen.json")
    
    try:
        urlretrieve(url, dest)
        print(f"   - Opgeslagen: {dest}")
    except Exception as e:
        print(f"   ⚠️ FOUT bij downloaden: {e}")

def choose_register_and_version():
    models = [
        d for d in os.listdir(REGISTERS_SOURCE_DIR)
        if os.path.isdir(os.path.join(REGISTERS_SOURCE_DIR, d))
    ]

    if not models:
        print("⚠️ Geen registers gevonden.")
        return None, None

    print("\n📚 Kies een register:")
    for i, m in enumerate(models, 1):
        print(f"[{i}] {m}")
    print("[A] Alle registers")
    print("[Q] Annuleren")

    choice = input("> ").strip().lower()
    if choice in ("q", ""):
        return None, None
    if choice == "a":
        return None, None

    try:
        model = models[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Ongeldige keuze")
        return None, None

    versions_path = os.path.join(REGISTERS_SOURCE_DIR, model)
    versions = [
        d for d in os.listdir(versions_path)
        if os.path.isdir(os.path.join(versions_path, d))
    ]

    print(f"\n📦 Kies een versie van '{model}':")
    for i, v in enumerate(versions, 1):
        print(f"[{i}] {v}")
    print("[A] Alle versies")

    choice = input("> ").strip().lower()
    if choice == "a":
        return model, None

    try:
        version = versions[int(choice) - 1]
        return model, version
    except (ValueError, IndexError):
        print("❌ Ongeldige keuze")
        return None, None

def generate_linkml_docs(c, only_model=None, only_version=None):
    """Genereer documentatie per modelversie (LinkML -> Markdown)."""
    print("⚙️  LinkML documentatie genereren...")

    if not os.path.exists(REGISTERS_SOURCE_DIR):
        print(f"   [WARN] Bronmap '{REGISTERS_SOURCE_DIR}' niet gevonden.")
        return

    for model_name in os.listdir(REGISTERS_SOURCE_DIR):
        if only_model and model_name != only_model:
            continue

        model_path = os.path.join(REGISTERS_SOURCE_DIR, model_name)
        if not os.path.isdir(model_path):
            continue

        for version_id in os.listdir(model_path):
            if only_version and version_id != only_version:
                continue

            version_path = os.path.join(model_path, version_id)
            if not os.path.isdir(version_path):
                continue

            yaml_file = os.path.join(version_path, f"{model_name}.linkml.yml")
            svg_file = os.path.join(version_path, f"{model_name}.drawio.svg")

            if not os.path.exists(yaml_file) or not os.path.exists(svg_file):
                print(f"Skipping {model_name}/{version_id}: missing files")
                continue

            out_dir = os.path.join(REGISTERS_TARGET_DIR, model_name, version_id)
            os.makedirs(out_dir, exist_ok=True)

            shutil.copy(svg_file, out_dir)

            print(f"{model_name}/{version_id}:")
            cmd = f"gen-doc --template-directory templates -d {out_dir} {yaml_file}"
            c.run(cmd)

            for md_file in glob.glob(os.path.join(out_dir, "*.md")):
                if not md_file.endswith("index.md"):
                    os.remove(md_file)

def copy_content():
    print(f"📂 Content kopiëren: {DOCS_DIR} -> {STAGING_DIR}")
    shutil.copytree(DOCS_DIR, STAGING_DIR, dirs_exist_ok=True)

def generate_indices(c):
    """Draai aanvullende Python scripts voor indexen en usages."""
    print("📑 Indexen genereren...")
    c.run(f"{PYTHON} scripts/generate_model_landing_pages.py {STAGING_DIR}", hide=True)
    c.run(f"{PYTHON} scripts/concept_usages.py {STAGING_DIR}", hide=True)

# ==============================================================================
# HOOFDTAKEN (MENU)
# ==============================================================================

@task
def setup(c):
    """Installeren: Zet alle dependencies klaar."""
    print("📦 Dependencies installeren...")
    c.run(f"{PYTHON} -m pip install -r requirements.txt")
    
    print("💎 Ruby dependencies...")
    c.run("bundle config set path 'vendor/bundle'")
    c.run("bundle install")
    
    print("✅ Klaar.")

@task
def update_all(c):
    """Verversen: Draai dit om wijzigingen in data/modellen door te voeren."""

    # Verwijder oude staging rommel
    print("🧹 Opruimen...")
    shutil.rmtree(STAGING_DIR, ignore_errors=True)

    copy_content()
    
    # Generatoren draaien
    fetch_external_data()
    generate_linkml_docs(c)
    generate_indices(c)
    
    print("✅ Data bijgewerkt.")

@task
def update_static_content(c):
    copy_content()
    print("✅ Data bijgewerkt.")

@task
def update_single_register(c):
    copy_content()

    fetch_external_data()

    model, version = choose_register_and_version()
    if model is None and version is None:
        print("⏹️ Afgebroken.")
        return

    generate_linkml_docs(c, only_model=model, only_version=version)
    generate_indices(c)

    print("✅ Register bijgewerkt.")

@task
def serve(c):
    """Starten: Start de website lokaal."""
    print("\n🌍 Server start... (Ctrl+C om te stoppen)")
    if running_in_docker():
        c.run(f"{JEKYLL} serve -H 0.0.0.0 -s {STAGING_DIR} -d {SITE_DIR} --livereload --incremental --open-url")
    else:
        c.run(f"{JEKYLL} serve -s {STAGING_DIR} -d {SITE_DIR} --livereload --incremental --open-url")

@task
def build(c):
    """Productie build (voor CI/CD)."""
    update_all(c)
    c.run(f"{JEKYLL} build -s {STAGING_DIR} -d {SITE_DIR}")

# ==============================================================================
# INTERACTIEF MENU
# ==============================================================================

@task(default=True)
def menu(c):
    tasks = [
        ("Alles verversen", update_all),
        ("Eén register verversen", update_single_register),
        ("Statische inhoud verversen", update_static_content),
        ("Website starten", serve)
    ]

    if not running_in_docker():
        tasks.insert(0, ("Installeren", setup))

    while True:
        print("\n=== STELSEL TOOL ===")
        for i, task in enumerate(tasks, 1):
            print(f"[{i}] {task[0]}")
        print("[Q] Stoppen")

        try:
            choice = input("\nKies een optie: ").strip().lower()
        except KeyboardInterrupt:
            break

        if choice == 'q':
            break

        try:
            tasks[int(choice) - 1][1](c)
        except (ValueError, IndexError, TypeError):
            print("❌ Ongeldige keuze")
