param(
    [Parameter(Mandatory = $true)]
    [string]$TemplateName
)

docker run --rm `
    -v "${PWD}:/data" `
    -w /data `
    dicastro/pandoc-latex-cv:3.6.4.0-alpine `
    content/en/authors/admin/_index.md `
    --lua-filter cv/filters/escape-yaml.lua `
    --columns 1000 `
    --pdf-engine xelatex `
    --from markdown+yaml_metadata_block `
    --template "cv/cover-letters/templates/$TemplateName-cover-letter-en.tex" `
    -o "cv/cover-letters/generated/$TemplateName-cover-letter-en-diego-castro.pdf"