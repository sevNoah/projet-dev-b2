class Animation:
    def __init__(self, sprite_sheet, animation_steps, animation_speed, y_offset, loop=True):
        self.sprite_sheet = sprite_sheet
        self.animation_list = []
        self.animation_steps = animation_steps
        self.animation_speed = animation_speed
        self.loop = loop  # ✅ nouveau paramètre
        self.current_frame = 0
        self.animation_timer = 0.0
        self.finished = False  # ✅ pour savoir si l'animation est finie
        self.y_offset = y_offset

        # Découper les frames
        for x in range(self.animation_steps):
            self.animation_list.append(self.sprite_sheet.get_image(x, self.y_offset, 150, 3))

    def animate(self, delta_time):
        if self.finished:
            return self.animation_list[-1]  # 🛑 Si animation finie, reste sur la dernière image

        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= self.animation_steps:
                if self.loop:
                    self.current_frame = 0  # 🔁 boucle
                else:
                    self.current_frame = self.animation_steps - 1  # 🛑 reste sur la dernière frame
                    self.finished = True  # ✅ Marquer comme terminé

        return self.animation_list[self.current_frame]

    def reset(self):
        self.current_frame = 0
        self.animation_timer = 0.0
        self.finished = False  # ✅ on réactive
