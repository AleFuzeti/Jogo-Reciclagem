import pygame
import random
from settings import WIDTH, HEIGHT, FONT, SMALL_FONT, COLORS, ITEM_IMAGES
from sprites import TrashBin

# Função para criar as lixeiras na tela
def create_bins():
    bins = pygame.sprite.Group()
    categories = list(COLORS.keys())
    for i, category in enumerate(categories):
        bin = TrashBin(50 + i * 150, HEIGHT - 200, category)
        bins.add(bin)
    return bins

# Função para criar uma lista de todos os itens
def create_item_list():
    items = []
    for category, images in ITEM_IMAGES.items():
        for image_path in images:
            items.append((category, image_path))
    random.shuffle(items)
    return items

def inicializa():
    pygame.init()
    # Configurações da tela
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Jogo de Reciclagem")
    # Fontes
    font = pygame.font.SysFont(FONT, 36)
    small_font = pygame.font.SysFont(SMALL_FONT, 24)
    smaller_font = pygame.font.SysFont(SMALL_FONT, 16)
    
    bins = create_bins()
    items = create_item_list()
        
    return screen, font, small_font, smaller_font, bins, items