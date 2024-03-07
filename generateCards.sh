venv/bin/activate
python main.py 'in' 'rpg-cards-typst-templates/in/data.yaml'
typst compile --root 'rpg-cards-typst-templates' 'rpg-cards-typst-templates/src/cards.typ' 'out/cards.pdf'
