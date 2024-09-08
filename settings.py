# settings.py

WIDTH, HEIGHT = 830, 600

FONT, SMALL_FONT = 'Comic Sans MS','Comic Sans MS'

COLORS = {
    'Papel': (0, 0, 255),        # Azul
    'Plástico': (255, 0, 0),     # Vermelho
    'Vidro': (0, 255, 0),        # Verde
    'Metal': (255, 255, 0),      # Amarelo
    'Orgânico': (108, 60, 12),   # Marrom
}

BIN_PATH  = 'assets\lixeiras\\'

BIN_IMAGES = {
    'Papel': BIN_PATH + 'papel.png',
    'Plástico': BIN_PATH + 'plastico.png',
    'Vidro': BIN_PATH + 'vidro.png',
    'Metal': BIN_PATH + 'metal.png',
    'Orgânico': BIN_PATH + 'organico.png',
}

ITEM_PATH = 'assets\lixos\\'

import os

ITEM_IMAGES = {}

# Iterate through each category directory in ITEM_PATH
for category in os.listdir(ITEM_PATH):
    category_path = os.path.join(ITEM_PATH, category)
    if os.path.isdir(category_path):
        # List all files in the category directory
        files = [os.path.join(category_path, file) for file in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, file))]
        # Add the category and its files to ITEM_IMAGES
        ITEM_IMAGES[category] = files


