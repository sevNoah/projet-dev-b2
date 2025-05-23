import pygame

class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, scale):
        """Découpe une portion de l'image et applique la transparence."""
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        return image

    def get_images_custom_sizes(self, widths, height, scale):
        """Découpe des images de tailles différentes à l’horizontale."""
        images = []
        x = 0
        for width in widths:
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            image.blit(self.sheet, (0, 0), pygame.Rect(x, 0, width, height))
            image = pygame.transform.scale(image, (width * scale, height * scale))
            images.append(image)
            x += width
        return images