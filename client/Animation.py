class Animation:
    def __init__(self, sprite_sheet, animation_steps, animation_speed, y_offset):
        self.sprite_sheet = sprite_sheet
        self.animation_list = []
        self.animation_steps = animation_steps
        self.animation_speed = animation_speed
        self.current_frame = 0
        self.animation_timer = 0.0
        self.y_offset = y_offset

        # Découper les frames de l'animation et les ajouter à la liste
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, self.y_offset, 150, 3))

    def animate(self, delta_time):
        # Incrémenter le timer avec le temps écoulé
        self.animation_timer += delta_time

        # Si le timer dépasse la vitesse d'animation
        if self.animation_timer >= self.animation_speed:
            # Passer à la frame suivante
            self.current_frame += 1
            self.animation_timer = 0.0

        # Retourner l'image actuelle
        if self.current_frame < self.animation_steps:
            return self.animation_list[self.current_frame]
        else:
            return None

    def reset(self):
        self.current_frame = 0
        self.animation_timer = 0.0
