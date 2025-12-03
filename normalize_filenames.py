import os
import urllib.parse

ROOT_DIR = "."
SITES_DIR = "sites"

def normalize_name(name):
    # Remove extension for processing
    base, ext = os.path.splitext(name)
    # Lowercase and replace spaces with underscores
    new_base = base.lower().replace(" ", "_")
    return new_base + ext

def main():
    rename_map = {}
    
    # 1. Identify and Rename Files
    print("--- Renaming Files ---")
    for root, dirs, files in os.walk(SITES_DIR):
        for file in files:
            if not file.endswith(".html"):
                continue
                
            old_path = os.path.join(root, file)
            new_name = normalize_name(file)
            new_path = os.path.join(root, new_name)
            
            if file != new_name:
                # Rename file
                os.rename(old_path, new_path)
                print(f"Renamed: {file} -> {new_name}")
                
                # Store mapping (relative paths for link replacement)
                # We need to handle both "File Name.html" and "sites/File Name.html"
                # But mostly we care about the filename part for replacements
                rename_map[file] = new_name
                
                # Also handle URL encoded versions
                # "Kom%20Ombo.html" -> "kom_ombo.html"
                encoded_old = urllib.parse.quote(file)
                if encoded_old != file:
                    rename_map[encoded_old] = new_name

    if not rename_map:
        print("No files needed renaming.")
        return

    print(f"\nCreated {len(rename_map)} rename mappings.")

    # 2. Update References in All Files
    print("\n--- Updating References ---")
    extensions = ('.html', '.js', '.css', '.csv', '.py', '.md')
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".git" in root or ".gemini" in root:
            continue
            
        for file in files:
            if not file.endswith(extensions):
                continue
                
            filepath = os.path.join(root, file)
            
            # Skip the script itself
            if "normalize_filenames.py" in filepath:
                continue

            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                changes_count = 0
                
                for old_name, new_name in rename_map.items():
                    if old_name in new_content:
                        new_content = new_content.replace(old_name, new_name)
                        changes_count += 1
                
                if changes_count > 0:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated {changes_count} links in: {filepath}")
                    
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    main()
