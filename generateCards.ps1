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
python main.py 'in' 'rpg-cards-typst-templates/in/data.yaml'

# Compile the Typst cards from the data.yaml file.
typst compile --root 'rpg-cards-typst-templates' 'rpg-cards-typst-templates/src/cards.typ' 'out/cards.pdf'
