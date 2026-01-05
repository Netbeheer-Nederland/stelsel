import os, shutil, sys, glob
from invoke import task
from urllib.request import urlretrieve

# ==============================================================================
# CONFIGURATIE
# ==============================================================================

DOCS_DIR = "docs"
STAGING_DIR = "_staging"
SITE_DIR = "_site"
REGISTERS_SOURCE_DIR = "registers"
REGISTERS_TARGET_DIR = os.path.join(STAGING_DIR, "_registers")

PYTHON = sys.executable
JEKYLL = "bundle exec jekyll"

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

def generate_linkml_docs(c):
    """Genereer documentatie per modelversie (LinkML -> Markdown)."""
    print("⚙️  LinkML documentatie genereren...")
    
    if not os.path.exists(REGISTERS_SOURCE_DIR):
        print(f"   [WARN] Bronmap '{REGISTERS_SOURCE_DIR}' niet gevonden.")
        return

    # Loop door bronmodellen
    for model_name in os.listdir(REGISTERS_SOURCE_DIR):
        model_path = os.path.join(REGISTERS_SOURCE_DIR, model_name)
        if not os.path.isdir(model_path): continue

        for version_id in os.listdir(model_path):
            version_path = os.path.join(model_path, version_id)
            if not os.path.isdir(version_path): continue

            # Doelmap in _staging
            out_dir = os.path.join(REGISTERS_TARGET_DIR, model_name, version_id)
            os.makedirs(out_dir, exist_ok=True)

            # 1. Kopieer SVG (indien aanwezig)
            svg_file = os.path.join(version_path, f"{model_name}.drawio.svg")
            if os.path.exists(svg_file):
                shutil.copy(svg_file, out_dir)

            # 2. Draai gen-doc (LinkML tool)
            yaml_file = os.path.join(version_path, f"{model_name}.linkml.yml")
            if os.path.exists(yaml_file):
                # Let op: gen-doc commando moet beschikbaar zijn in shell
                cmd = f"gen-doc --template-directory templates -d {out_dir} {yaml_file}"
                print(f"{model_name}/{version_id}:")
                c.run(cmd)
            
            # 3. Cleanup .md files (behalve index)
            for md_file in glob.glob(os.path.join(out_dir, "*.md")):
                if not md_file.endswith("index.md"):
                    os.remove(md_file)
    print()

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
def update(c):
    """Verversen: Draai dit om wijzigingen in data/modellen door te voeren."""
    print(f"📂 Content kopiëren: {DOCS_DIR} -> {STAGING_DIR}")
    
    # Stap 1: Statische content (overschrijven toegestaan)
    shutil.copytree(DOCS_DIR, STAGING_DIR, dirs_exist_ok=True)
    
    # Stap 2: Generatoren draaien
    fetch_external_data()
    generate_linkml_docs(c)
    generate_indices(c)
    
    print("✅ Data bijgewerkt.")

@task
def serve(c):
    """Starten: Start de website lokaal (begint met schone lei)."""
    # Verwijder oude staging rommel
    print("🧹 Opruimen...")
    shutil.rmtree(STAGING_DIR, ignore_errors=True)
    
    # Bouw alles vers op
    update(c)
    
    print("\n🌍 Server start... (Ctrl+C om te stoppen)")
    c.run(f"{JEKYLL} serve -s {STAGING_DIR} -d {SITE_DIR} --livereload --incremental --open-url")

@task
def build(c):
    """Productie build (voor CI/CD)."""
    update(c)
    c.run(f"{JEKYLL} build -s {STAGING_DIR} -d {SITE_DIR}")

# ==============================================================================
# INTERACTIEF MENU
# ==============================================================================

@task(default=True)
def menu(c):
    while True:
        print("\n=== STELSEL TOOL ===")
        print(" [1] Setup  (Installeren)")
        print(" [2] Start  (Website bekijken)")
        print(" [3] Update (Verversen tijdens draaien)")
        print(" [Q] Stop")
        
        try:
            choice = input("\nKies een optie: ").strip().lower()
        except KeyboardInterrupt:
            break
            
        if choice == '1': setup(c)
        elif choice == '2': serve(c)
        elif choice == '3': update(c)
        elif choice == 'q': break
