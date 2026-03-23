#!/bin/sh

generate_cv() {
  local LANG=$1

  echo ">> Generating CV in $LANG..."

  # Comprobar si existe el archivo de idioma antes de fallar
  if [ ! -f "data/${LANG}/authors/me.yaml" ]; then
      echo "ERROR: Not found data/${LANG}/authors/me.yaml"
      return 1
  fi

  pandoc /dev/null \
    --metadata-file "data/authors/me.yaml" \
    --metadata-file "data/${LANG}/authors/me.yaml" \
    --lua-filter "cv/filters/escape-yaml.lua" \
    --columns 1000 \
    --pdf-engine xelatex \
    --from markdown \
    --template "cv/templates/moderncv-template-${LANG}.tex" \
    -o "static/uploads/cv-diego-castro-viadero-${LANG}.pdf"
}

if [ "$1" = "all" ]; then
    for lang in es en fr; do
        generate_cv "$lang"
    done
else
    generate_cv "${1:-es}"
fi