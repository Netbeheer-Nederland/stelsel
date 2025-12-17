import os, shutil, glob
from invoke import task
from urllib.request import urlretrieve

# Configuratie
DOCS_DIR = "docs"
STAGING_DIR = "_staging"
SITE_DIR = "_site"
REGISTERS_SOURCE_DIR = "registers"

# Windows compatibiliteit
PYTHON = "python"
JEKYLL = "bundle exec jekyll"

@task
def clean(c):
    """Ruim de gegenereerde site en tijdelijke data op."""
    print("🧹 Cleaning...")
    for folder in [STAGING_DIR, SITE_DIR]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   - {folder} verwijderd.")

@task
def setup(c):
    """Installeer dependencies (Python & Ruby)."""
    print("📦 Setup dependencies...")
    c.run(f"{PYTHON} -m pip install -r requirements.txt")
    
    print("💎 Checking Ruby dependencies...")
    c.run("gem list -i bundler || gem install bundler")
    c.run("bundle config set path 'vendor/bundle'")
    c.run("bundle install")

@task
def prepare_staging_dir(c):
    """Maak een schone _staging map en kopieer docs daarheen."""
    print(f"🏗  Preparing staging directory: {DOCS_DIR} -> {STAGING_DIR}")
    if os.path.exists(STAGING_DIR):
        shutil.rmtree(STAGING_DIR)
    shutil.copytree(DOCS_DIR, STAGING_DIR)

@task
def fetch_data(c):
    """Download externe data naar de _staging map."""
    print("⬇️  Downloading SKOS lookup table...")
    data_dir = os.path.join(STAGING_DIR, "_data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    url = "https://begrippen.netbeheernederland.nl/begrippen.json"
    dest = os.path.join(data_dir, "begrippen.json")
    
    urlretrieve(url, dest)
    print(f"   - Opgeslagen in {dest}")

@task
def gen_linkml_docs(c):
    """Genereer documentatie per modelversie in de _staging map."""
    print("⚙️  Generating LinkML documentation...")
    
    # We lezen uit de root 'registers' (source), maar schrijven naar '_staging/_registers'
    if not os.path.exists(REGISTERS_SOURCE_DIR):
        print(f"   [WARN] Bronmap '{REGISTERS_SOURCE_DIR}' niet gevonden.")
        return

    for model_name in os.listdir(REGISTERS_SOURCE_DIR):
        model_path = os.path.join(REGISTERS_SOURCE_DIR, model_name)
        if not os.path.isdir(model_path): continue

        for version_id in os.listdir(model_path):
            version_path = os.path.join(model_path, version_id)
            if not os.path.isdir(version_path): continue

            print(f"   - Processing {model_name} version {version_id}")

            # Doelmap in _staging
            out_dir = os.path.join(STAGING_DIR, "_registers", model_name, version_id)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            # 1. Kopieer SVG
            svg_file = os.path.join(version_path, f"{model_name}.drawio.svg")
            if os.path.exists(svg_file):
                shutil.copy(svg_file, out_dir)

            # 2. Draai gen-doc
            yaml_file = os.path.join(version_path, f"{model_name}.linkml.yml")
            if os.path.exists(yaml_file):
                # We voeren gen-doc uit tegen de _staging map
                cmd = f"gen-doc --template-directory templates -d {out_dir} {yaml_file}"
                c.run(cmd, hide=True)
            
            # 3. Cleanup .md files
            for md_file in glob.glob(os.path.join(out_dir, "*.md")):
                if not md_file.endswith("index.md"):
                    os.remove(md_file)

@task
def generate_indices(c):
    """Draai de helper scripts, met _staging als argument."""
    print("📑 Generating indices...")
    c.run(f"{PYTHON} scripts/generate_model_landing_pages.py {STAGING_DIR}")
    c.run(f"{PYTHON} scripts/concept_usages.py {STAGING_DIR}")

@task
def prepare_content(c):
    """De flow van content generatie."""
    # 1. Eerst de map opzetten
    prepare_staging_dir(c)
    # 2. Data downloaden in die map
    fetch_data(c)
    # 3. LinkML docs genereren in die map
    gen_linkml_docs(c)
    # 4. Indices genereren in die map
    generate_indices(c)

@task
def build(c):
    """Bouw de site voor productie."""
    # Genereer alles in _staging
    prepare_content(c)
    
    print("🚀 Jekyll Build...")
    # Bouw van _staging naar _site
    c.run(f"{JEKYLL} build -s {STAGING_DIR} -d {SITE_DIR}")

@task
def serve(c):
    """Draai lokaal."""
    # Genereer alles in _staging
    prepare_content(c)
    
    print("🌍 Starting Local Server...")
    c.run(f"{JEKYLL} serve -s {STAGING_DIR} -d {SITE_DIR} --livereload --incremental --open-url")

@task
def menu(c):
    """Toon menu."""
    while True:
        print("\n=== STELSEL MENU ===")
        print(" [1] Setup")
        print(" [2] Clean")
        print(" [3] Build (Generate + Jekyll)")
        print(" [4] Serve (Local)")
        print(" [Q] Quit")
        choice = input("Keuze: ").strip().lower()
        if choice == '1': setup(c)
        elif choice == '2': clean(c)
        elif choice == '3': build(c)
        elif choice == '4': serve(c)
        elif choice == 'q': break
