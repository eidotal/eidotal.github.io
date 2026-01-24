#!/bin/python3
import os


def generate_index_adoc():
    base_dir = "Pages"
    # Header from the original file
    header = "= Eido Tal - Wiki\ninclude::utils/attribute-include[]\n\n====\n\n"
    footer = "===="

    sections_output = []

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
            # Create a title from the directory name (e.g., 'svDV' -> 'SvDV')
            section_title = subdir.replace("_", " ").capitalize()

            section_content = f".{section_title}\n****\n"

            path = os.path.join(base_dir, subdir)
            files = sorted([f for f in os.listdir(path) if f.endswith(".adoc")])

            for file in files:
                name = file.replace(".adoc", "")
                # Replicate the xref format from the source
                section_content += f"* xref:./{base_dir}/{subdir}/{file}[{name}]\n"

            section_content += "****"
            sections_output.append(section_content)

    # Combine everything with the horizontal rule separator
    full_content = header + "\n\n''''\n\n".join(sections_output) + "\n\n" + footer

    with open("index.adoc", "w") as f:
        f.write(full_content)
    print("index.adoc has been updated based on the directory structure.")


if __name__ == "__main__":
    generate_index_adoc()
