# Script pour calculer les statistiques du projet (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   STATISTIQUES DU WIKI (GLOBAL)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Calcul global (excluant les dossiers cachés comme .git)
$allFiles = Get-ChildItem -Recurse -Filter "*.md" | Where-Object { $_.FullName -notmatch "\\\." }
$totalFiles = $allFiles.Count
$totalLines = ($allFiles | Get-Content | Measure-Object -Line).Lines

Write-Host "Nombre total de fichiers Markdown : $totalFiles"
Write-Host "Nombre total de lignes Markdown   : $totalLines"
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   STATISTIQUES PAR SECTION (.md)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Parcourir les dossiers de premier niveau (excluant les cachés)
Get-ChildItem -Directory | Where-Object { $_.Name -notmatch "^\." } | ForEach-Object {
    $dirFiles = Get-ChildItem -Path $_.FullName -Recurse -Filter "*.md"
    $count = $dirFiles.Count
    $lines = ($dirFiles | Get-Content | Measure-Object -Line).Lines
    if ($null -eq $lines) { $lines = 0 }
    
    $dirName = $_.Name
    Write-Host ("{0,-25} : {1,2} fichiers, {2,4} lignes" -f $dirName, $count, $lines)
}

Write-Host "==========================================" -ForegroundColor Cyan
