<#
.SYNOPSIS
    Full workflow to generate RPG cards from source Obsidian markdown files.
.DESCRIPTION
    1. Run the Python script to convert the markdown files to a single data.yaml file.
    2. Compile the Typst cards from the data.yaml file.
.NOTES
    This WILL NOT copy the image files for the cards. The image files must be manually copied to 'rpg-cards-typst-templates/in'.
#>

# Activates the virtual environment and installs the required packages.
& 'venv/Scripts/activate'

# Run the Python script to convert the markdown files to a single data.yaml file.
Write-Host "Converting the markdown files to a single data.yaml file..." -ForegroundColor Cyan
python main.py --input-markdown-directory 'in/markdown' --input-image-directory 'in/images' --output-file-path 'rpg-cards-typst-templates/in/data.yaml' --output-image-directory 'rpg-cards-typst-templates/in'

# Compile the Typst cards from the data.yaml file.
Write-Host "Compiling the Typst cards..." -ForegroundColor Cyan
typst compile --root 'rpg-cards-typst-templates' 'rpg-cards-typst-templates/src/cards.typ' 'out/cards.pdf'
