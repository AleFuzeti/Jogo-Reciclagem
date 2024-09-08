import pygame
from settings import BIN_IMAGES

# Classes de sprites
class TrashBin(pygame.sprite.Sprite):
    def __init__(self, x, y, category):
        super().__init__()
        self.image = pygame.image.load(BIN_IMAGES[category]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (113, 163))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.category = category

class RecyclableItem(pygame.sprite.Sprite):
    def __init__(self, x, y, category, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))
        self.category = category
        self.name = image_path.split('/')[-1].split('.')[0]
        self.dragging = False

    def update(self, mouse_pos):
        if self.dragging:
            self.rect.center = mouse_pos
