class Button:
    def __init__(self, image, pos, text_input=None, font=None, base_color=None, hovering_color=None):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input

        if self.image is None:
            if self.text_input is not None and self.font is not None:
                self.text = self.font.render(self.text_input, True, self.base_color)
                self.image = self.text
            else:
                raise ValueError("Image or text must be provided.")
        
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        
        # Crée le rectangle du texte uniquement si nécessaire
        if self.text_input is not None and self.font is not None:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        else:
            self.text = None

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        if self.text is not None:
            screen.blit(self.text, self.text_rect)

    def changeColor(self, position):
        if self.text is not None:
            if self.rect.collidepoint(position):
                self.text = self.font.render(self.text_input, True, self.hovering_color)
            else:
                self.text = self.font.render(self.text_input, True, self.base_color)
