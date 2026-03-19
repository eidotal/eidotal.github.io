# GEMINI.md - Eido Tal Wiki

This project is a personal wiki and documentation site belonging to Eido Tal, built using **AsciiDoc** and hosted on GitHub Pages. It serves as a repository for notes on networking, hardware verification (SystemVerilog/DV), and development workflows.

## Project Overview

-   **Content Engine:** Asciidoctor (AsciiDoc to HTML/PDF)
-   **Structure:** Hierarchical content organized in the `Pages/` directory.
-   **Automation:** Managed via `Makefile`, `Taskfile.yaml`, and a custom Python script for index generation.
-   **Deployment:** GitHub Actions (`publish.yml`) triggers on push to `main` or `master`.

## Directory Structure

-   `Pages/`: Contains the core content categorized into:
    -   `About/`: Personal information (CV).
    -   `Network/`: Ethernet protocols, scale-up networks, and architectural diagrams.
    -   `svDV/`: SystemVerilog/UVM verification methodologies, logging, and Python-based regression tools.
    -   `Workflow/`: Documentation on Git, AsciiDoc, and AI-assisted workflows.
-   `scripts/`:
    -   `PyIndex.py`: Scans the `Pages/` directory and automatically updates `index.adoc` with links to all documentation pages.
-   `utils/`:
    -   `attribute-include`: Shared AsciiDoc attributes (e.g., icons, TOC settings).
    -   `docinfo/` & `docinfo-local/`: HTML head/footer injections and CSS for the site's layout.
-   `output/`: (Generated) Contains the compiled HTML and PDF versions of the site.

## Building and Running

The project supports both `make` and `task` (Taskfile) for automation.

### Key Commands

| Task | Command | Description |
| :--- | :--- | :--- |
| **Clean** | `make clean` or `task clean` | Removes the `output/` directory. |
| **Build HTML** | `make all` or `task html` | Generates the full site in `output/html/`. |
| **Build PDF** | `make PDF` or `task pdf` | Generates PDF versions in `output/pdf/`. |
| **Generate Index** | `python3 scripts/PyIndex.py` | Updates `index.adoc` based on current files in `Pages/`. |
| **Diagrams** | `make Diagram` or `task diagram` | Generates SVGs from `.mmd` (Mermaid) and `.d2` files. |
| **Install** | `make install` or `task install` | Installs system dependencies (`asciidoctor`, `gem`, `pygments.rb`). |
| **Preview** | `make open` or `task open` | Opens the generated local index in Firefox. |

## Development Conventions

1.  **Adding New Content:**
    -   Create a new `.adoc` file in the appropriate subdirectory of `Pages/`.
    -   Always include `include::utils/attribute-include[]` at the top of new files for consistent styling.
    -   Run `python3 scripts/PyIndex.py` to ensure the new page is linked from the main index.
2.  **Cross-Linking:**
    -   Use `xref:./relative/path/to/file.adoc[Link Text]` for internal links. The build process automatically handles converting these to `.html` suffixes during deployment.
3.  **Diagrams:**
    -   Store source files for diagrams (`.mmd`, `.d2`) in the same directory as the content they support.
    -   Run the diagram generation task to update the SVGs used in the docs.
4.  **Deployment:**
    -   Pushes to `main` are automatically built and deployed. The CI uses `make create`, which renders HTML files in-place within the source directories.
