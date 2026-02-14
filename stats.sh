#!/bin/bash

# Script pour calculer les statistiques du projet (Bash)

echo "=========================================="
echo "   STATISTIQUES DU WIKI (GLOBAL)"
echo "=========================================="

# Calcul global (excluant le dossier .git)
TOTAL_FILES=$(find . -type f -name "*.md" -not -path '*/.*' | wc -l)
TOTAL_LINES=$(find . -type f -name "*.md" -not -path '*/.*' -exec cat {} + | wc -l)

echo "Nombre total de fichiers Markdown : $TOTAL_FILES"
echo "Nombre total de lignes Markdown   : $TOTAL_LINES"
echo ""

echo "=========================================="
echo "   STATISTIQUES PAR SECTION (.md)"
echo "=========================================="

# Parcourir les dossiers de premier niveau
for dir in */; do
    # Exclure les dossiers cachés (comme .git)
    if [[ $dir != .* ]]; then
        DIR_NAME=$(basename "$dir")
        FILES=$(find "$dir" -type f -name "*.md" -not -path '*/.*' | wc -l)
        LINES=$(find "$dir" -type f -name "*.md" -not -path '*/.*' -exec cat {} + | wc -l)
        
        # Affichage formaté
        printf "%-25s : %2s fichiers, %4s lignes\n" "$DIR_NAME" "$FILES" "$LINES"
    fi
done
echo "=========================================="
