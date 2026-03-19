#!/bin/python3
import os
import json

def generate_index_adoc():
    base_dir = "Pages"
    # Header from the original file
    header = "= Eido Tal - Wiki\ninclude::utils/attribute-include[]\n\n====\n\n"
    footer = "===="

    sections_output = []
    nav_groups = {}

    # Iterate through subdirectories in 'Pages'
    if os.path.exists(base_dir):
        # Sort directories to keep the output consistent
        subdirs = sorted(
            [
                d
                for d in os.listdir(base_dir)
                if os.path.isdir(os.path.join(base_dir, d))
            ]
        )

        for subdir in subdirs:
            section_title = subdir.replace("_", " ").capitalize()
            section_content = f".{section_title}\n****\n"
            
            nav_groups[section_title] = []

            path = os.path.join(base_dir, subdir)
            files = sorted([f for f in os.listdir(path) if f.endswith(".adoc")])

            for file in files:
                name = file.replace(".adoc", "")
                section_content += f"* xref:./{base_dir}/{subdir}/{file}[{name}]\n"
                
                nav_groups[section_title].append({
                    "name": name,
                    "url": f"/Pages/{subdir}/{name}.html",
                    "local_url": f"output/html/Pages/{subdir}/{name}.html"
                })

            section_content += "****"
            sections_output.append(section_content)

    # Combine everything with the horizontal rule separator
    full_content = header + "\n\n''''\n\n".join(sections_output) + "\n\n" + footer

    with open("index.adoc", "w") as f:
        f.write(full_content)
    print("index.adoc has been updated.")

    update_docinfo(nav_groups)

def update_docinfo(nav_groups):
    # Template for docinfo.html
    docinfo_template = """
<link rel="stylesheet" href="{css_path}" />

<div class="top-nav">
    <div class="nav-logo">Wiki</div>

    <div class="dropdown">
        <button class="menu-btn" onclick="toggleMenu()">Menu ▾</button>
        <div id="nav-dropdown" class="dropdown-content">
            <a href="{home_url}" class="home-link">Home</a>
            {links}
        </div>
    </div>
</div>

<script>
    function toggleMenu() {{
        document.getElementById("nav-dropdown").classList.toggle("show");
    }}

    window.onclick = function (event) {{
        if (!event.target.matches(".menu-btn")) {{
            var dropdowns = document.getElementsByClassName("dropdown-content");
            for (var i = 0; i < dropdowns.length; i++) {{
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains("show")) {{
                    openDropdown.classList.remove("show");
                }}
            }}
        }}
    }};
</script>
"""

    def format_links(groups, is_local=False, base_path=""):
        html_parts = []
        for category, links in groups.items():
            html_parts.append(f'<div class="menu-category">{category}</div>')
            for l in links:
                url = f"file://{base_path}/{l['local_url']}" if is_local else l['url']
                html_parts.append(f'<a href="{url}" class="menu-item">{l["name"]}</a>')
        return "\n            ".join(html_parts)

    base_path = os.getcwd()

    # Generate remote version
    remote_links = format_links(nav_groups, is_local=False)
    remote_content = docinfo_template.format(
        css_path="/utils/docinfo.css",
        home_url="/index.html",
        links=remote_links
    )
    
    os.makedirs("utils/docinfo", exist_ok=True)
    with open("utils/docinfo/docinfo.html", "w") as f:
        f.write(remote_content)

    # Generate local version
    local_links = format_links(nav_groups, is_local=True, base_path=base_path)
    local_content = docinfo_template.format(
        css_path=f"file://{base_path}/utils/docinfo.css",
        home_url=f"file://{base_path}/output/html/index.html",
        links=local_links
    )
    
    os.makedirs("utils/docinfo-local", exist_ok=True)
    with open("utils/docinfo-local/docinfo.html", "w") as f:
        f.write(local_content)
    
    print("docinfo files updated with grouped navigation.")

if __name__ == "__main__":
    generate_index_adoc()
