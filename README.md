# Personal Website - Diego Castro Viadero

This repository contains the source code for my personal website [diegocastroviadero.com](https://diegocastroviadero.com).

The site is built using [Hugo Blox](https://hugoblox.com) ![Hugo Blox Release][hugo-blox-release-shield] (Academic CV template), a powerful block-based framework for the [Hugo](https://gohugo.io) static site generator. It features a modern design powered by **Tailwind CSS v4** and includes an automated workflow to generate my CV in PDF format.

### ⚠️ Important: Template Overrides for Multilingual Authors

This repository contains local overrides in `layouts/_partials/functions/` for:

- `get_author_profile.html`
- `get_authors_data.html`

**Why are these here?**

The version of Hugo Blox used in this project (![Hugo Blox Release][hugo-blox-release-shield]) has a known limitation: the original `get_author_profile.html` does not support multilingual author data stored in subfolders (e.g., `data/en/authors/`).

To fix this, we have backported the logic from the Hugo Blox `main` branch (as of March 2026). This allows the site to correctly merge the base author data with language-specific translations.

**Future Maintenance:**

When upgrading to a newer version of Hugo Blox (posterior to ![Hugo Blox Release][hugo-blox-release-shield]):
 
1. Upgrade the Hugo Blox module
1. Temporarily rename the `layouts/_partials/functions/` folder to `layouts/_partials/myfunctions/` in order to be ignored
1. Rebuild de site locally `npm run dev`
1. Check if the "Resume" blocks still render correctly in all languages
1. If they do, these local overrides can be safely removed

---

## 🚀 Architecture & Workflow

This project uses a **Single Source of Truth** strategy. Personal data is managed in YAML files, which are then consumed by two different engines:
 
1. **CV Path (PDF)**:
  - **Merge**: Combines `data/authors/me.yaml` (global) with `data/<LANG>/authors/me.yaml`) (translations)
  - **Engine**: A custom Docker image running Pandoc + XeLaTeX
  - **Logic**: A Lua filter converts Hugo-specific Markdown and icons into valid LaTeX commands
1. **Web Path (HTML)**:
  - **Engine**: Hugo Blox ![Hugo Blox Release][hugo-blox-release-shield] + Hugo Extended
  - **Logic**: Local layout overrides merge the multilingual YAML data to render the "About" and "Resume" blocks
  - **Styles**: Tailwind CSS v4

## 🔧 Maintenance & Update Guide

Follow this specific order to ensure stability. Test locally after each step.
 
### Hugo Blox & Go Modules (The Engine)

This updates the core logic of the site (the "blocks").

- Where to check for news? [Hugo Blox GitHub Releases](https://github.com/HugoBlox/hugo-blox-builder/releases)
- How to update?
  1. Run `hugo mod get -u ./...` (This fetches the latest compatible versions)
  1. Run `hugo mod tidy` (This cleans up the `go.sum` file)
- Check:
  1. Run `npm run dev` and check if the layouts still look correct

### Node.js & Tailwind (The UI)

This updates Tailwind CSS v4 and the search engine (Pagefind).

- Where to check? Run `npm outdated` to see what's new
- How to update?
  1. Run `npm update`
  1. **Note**: Tailwind v4 is highly sensitive. If your CSS stops loading, check their [Migration Guide](https://tailwindcss.com/docs/v4-beta)
- Check:
  1. Run `npm run dev` and verify the styling (fonts, colors, spacing)

### Hugo Binary (The Compiler)

Updating the Hugo version itself.

- Where to check? [Hugo GitHub Releases](https://github.com/gohugoio/hugo/releases). Look for the "Extended" version
- How to update?
  1. Update your local Hugo installation (e.g., via `brew`, `choco`, or downloading the binary)
  1. **Crucial**: Once tested locally, you **must** manually update the version string in file to match:
    - `hugoblox.yaml` -> `build.hugo_version: '0.X.Y'`

### CV PDF Engine (Docker/Pandoc/LaTeX)

The CV generation depends on a Docker image.

- Where to check? [Pandoc/LaTeX Docker Hub](https://hub.docker.com/r/pandoc/latex). Look for new tags
- How to update?
  1. In `build.ps1`, update `$CV_BASE_TAG`
  1. Re-run `build.ps1` to update the local image
  1. In `.github/workflows/deploy.yaml`, update `CV_BASE_ENGINE_TAG`
  1. Update the tag in the rest of `*.ps1` scripts

## 📂 File Reference

| File / Path                   | Purpose                                                                                                                        |
|:------------------------------|:-------------------------------------------------------------------------------------------------------------------------------|
| `go.mod`                      | Manages Hugo Blox modules (the "engine")                                                                                       |
| `package.json`                | Manages UI dependencies (Tailwind CSS, Search engine)                                                                          |
| `hugoblox.yaml`               | Main configuration for the site theme and Hugo version pinning                                                                 |
| `data/authors/me.yaml`        | **Shared Data**: URLs, social links and fields that don't change between languages                                             |
| `data/<lang>/authors/me.yaml` | **Localized data**: Bio, Experience and Education summaries in specific languate                                               |
| `cv/`                         | Core CV logic. Contains LaTeX templates and the Lua filters for Pandoc                                                         |
| `cv/docker/`                  | Docker infrastructure. Includes `Dockerfile` and the `entrypoint.sh` wrapper                                                   |
| `cv/filters/`                 | **Lua Logic**: The "brain" that transforms dates, icons and URLs for the PDF engine                                            |
| `layouts/_partials/functions` | **Critical**: Local overrides to fix Hugo Blox ![Hugo Blox Release][hugo-blox-release-shield] multilingual author data merging |
| `static/uploads/`             | Destination for generated PDFs and other static assets                                                                         |
| `content/`                    | Markdown files for blog posts and project page                                                                                 |


## 🛠️ Technical Reference

### Local Development Commands

> Requires **Node.js**, **Hugo Extended** and **Docker**.

- **Web**: `npm run dev` (Runs Hugo with live reload)

### CV Generation Internals

The PDF generation is encapsulated in a Docker container to ensure LaTeX environment consistency.

- **Build Image**: `cd cv/docker && ./build.ps1` (Only needed if you change the Dockerfile or `entrypoint.sh`).
- **Generate PDFs**:
  - `./generate-cv.ps1 all`: Generates PDFs for all supported languages.
  - `./generate-cv.ps1 es`: Generates only the Spanish version.

**How the Lua Filter works:**

To bridge the gap between Hugo's Markdown and the strict LaTeX `moderncv` structure, the filter performs several automated transformations:

1. **Smart Date Processing**:
  - Automatically detects `YYYY-MM-DD` strings in YAML
  - Replaces the original field with a formatted `DD/MM/YYYY`
  - Generates auxiliary hidden fields: `_my` (Month/Year) and `_y` (Year only), allowing the LaTeX template to use different date granularities without manual editing
2. **Icon Translation**:
  - Detects Hugo-style icons: `{{< icon name="..." >}}`
  - Converts them into native LaTeX `\faicon{...}` calls, ensuring your skills and contact info look consistent in both Web and PDF
3. **Absolute URL Injection**:
  - Scans for relative links (e.g., `/uploads/my-file.pdf`)
  - Prepends the production domain (`https://diegocastroviadero.com`) so links remain functional when the CV is downloaded and opened offline
4. **LaTeX Sanitization**:
  - Converts Markdown summaries into clean LaTeX strings
  - Removes empty lines and fixes split `\item` entries to prevent compilation errors inside `cventry` blocks

## ❓ FAQ & Troubleshooting

### Why so many different technologies?

It might seem complex, but each part has a specific role in a modern static workflow:
 
- **Go (`go.mod`)**: Hugo is written in Go. Modern themes like Hugo Blox are distributed as **Go Modules** rather than simple folders. This file tells Hugo which version of the "engine" to fetch from the cloud
- **Node.js (`package.json`)**: Required for **Tailwind CSS v4** (styling) and **Pagefind** (the search engine). It handles the compilation of modern web assets
- **Docker**: Ensures that the CV PDF looks exactly the same on your computer and on GitHub, bypassing the "it works on my machine" headache with LaTeX dependencies

### What is the `go.sum` file?

It contains "digital fingerprints" (hashes) to ensure the modules you download haven't been tampered with. **Never edit this file manually**; let `hugo mod tidy` handle it.

### Why do I need "Hugo Extended"?

The "Extended" version includes the LibSass transpiler and advanced image processing libraries. Hugo Blox relies on these features to manage assets and themes correctly.

### Note on Package Managers (npm vs pnpm)

Although some Hugo Blox starters use `pnpm` by default, this repository has been migrated to **npm** for simplicity and compatibility with standard Windows environments.

> **Warning**: Avoid using `pnpm` in this repo to prevent conflicting lock files (`pnpm-lock.yaml` vs `package-lock.json`).

### Why are my CV dates appearing as `_my` or `_y` in the template?

These are "virtual fields" created by the **Lua Filter**. If you see them as raw text, ensure your Pandoc command is correctly calling `--lua-filter cv/filters/escape-yaml.lua`.

## 🔗 Useful Links

- Hugo Blox
  - [Hugo Blox - Site](https://hugoblox.com)
  - [Hugo Blox - Templates](https://hugoblox.com/templates)
  - [Hugo Blox - Blocks](https://hugoblox.com/blocks)
  - [Hugo Blox Documentation](https://docs.ownable.dev/hugoblox)
  - [Hugo Blox Repository](https://github.com/HugoBlox/kit)
- Icons supported by Hugo
  - [Devicon](https://devicon.dev)
  - [HeroIcons](https://heroicons.com)
  - [Simple Icons](https://simpleicons.org)
  - [FontAwesome v5 Icons](https://fontawesome.com/v5)
- CV Related links
  - [Pandoc/Latex Image](https://hub.docker.com/r/pandoc/latex)
  - [ModernCV Repo](https://github.com/moderncv/moderncv)
  - [TexLive Archive 2024 dependencies](https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2024/tlnet-final/archive)

[hugo-blox-release-shield]: https://img.shields.io/badge/version-v0.11.0-blue.svg