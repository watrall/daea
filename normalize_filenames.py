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
    
    # 1. Identify and Rename Files AND Directories
    # We need to walk top-down to rename files, but bottom-up to rename directories?
    # Actually, os.walk is top-down by default.
    # If we rename a directory, the walk might get confused.
    # Let's collect all renames first, then execute.
    
    to_rename = [] # List of (old_path, new_path, is_dir)

    print("--- Scanning for Renames ---")
    for root, dirs, files in os.walk(SITES_DIR, topdown=False): # Bottom-up to handle child files before parent dirs
        # Rename Files
        for file in files:
            if not file.endswith(".html"):
                continue
            
            old_name = file
            new_name = normalize_name(file)
            
            if old_name != new_name:
                old_path = os.path.join(root, old_name)
                new_path = os.path.join(root, new_name)
                to_rename.append((old_path, new_path, old_name, new_name))

        # Rename Directories
        for d in dirs:
            old_name = d
            new_name = old_name.lower().replace(" ", "_")
            
            if old_name != new_name:
                old_path = os.path.join(root, old_name)
                new_path = os.path.join(root, new_name)
                to_rename.append((old_path, new_path, old_name, new_name))

    # Execute Renames
    print(f"Found {len(to_rename)} items to rename.")
    for old_path, new_path, old_name, new_name in to_rename:
        try:
            # On case-insensitive filesystems (Mac/Windows), renaming "File" to "file" might fail or do nothing
            # if we don't use an intermediate step.
            temp_path = old_path + ".tmp"
            os.rename(old_path, temp_path)
            os.rename(temp_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
            
            rename_map[old_name] = new_name
            # Also handle URL encoded versions
            encoded_old = urllib.parse.quote(old_name)
            if encoded_old != old_name:
                rename_map[encoded_old] = new_name
                
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")

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
