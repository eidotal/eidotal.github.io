import os
import json
import re

def generate_index(pages_dir, output_file):
    search_data = []
    
    # Files to index
    files_to_index = []
    
    # Add main index.adoc
    if os.path.exists("index.adoc"):
        files_to_index.append("index.adoc")
        
    # Add all Pages/**/*.adoc
    for root, dirs, files in os.walk(pages_dir):
        for file in files:
            if file.endswith(".adoc"):
                files_to_index.append(os.path.join(root, file))

    for file_path in files_to_index:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        title = ""
        content = []
        
        for line in lines:
            if not title and line.startswith("= "):
                title = line.strip("= ").strip()
            elif not line.startswith("include::") and not line.startswith(":") and not line.startswith("//"):
                # Simple content extraction: skip attributes and comments
                clean_line = line.strip()
                if clean_line:
                    content.append(clean_line)
        
        # ID is the relative path to the HTML version
        if file_path == "index.adoc":
            rel_path = "index.html"
        else:
            rel_path = file_path.replace(".adoc", ".html")
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
        
        search_data.append({
            "id": "/" + rel_path if not rel_path.startswith("/") else rel_path,
            "title": title if title else file_path,
            "body": " ".join(content)
        })

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(search_data, f, indent=2)
    print(f"Search index generated with {len(search_data)} entries at {output_file}")

if __name__ == "__main__":
    generate_index("Pages", "output/html/search-data.json")
