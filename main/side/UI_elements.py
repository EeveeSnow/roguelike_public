import pygame


class Slider:
    def __init__(self, position: tuple, upperValue: int = 90, sliderWidth: int = 150,
                 text: str = "Изменение угла",
                 outlineSize: tuple = (1920, 30)) -> None:
        self.position = position
        self.outlineSize = outlineSize
        self.text = text
        self.sliderWidth = sliderWidth
        self.upperValue = upperValue

    # renders slider and the text showing the value of the slider
    def render(self, screen) -> None:
        # draw outline and slider rectangles
        pygame.draw.rect(screen, (0, 0, 0), (self.position[0], self.position[1],
                                             self.outlineSize[0], self.outlineSize[1]), 3)

        pygame.draw.rect(screen, (0, 0, 0), (self.position[0], self.position[1],
                                             self.sliderWidth / 100 * self.upperValue, self.outlineSize[1]))

        # determite size of font
        self.font = pygame.font.SysFont("Segoe UI", 20)

        # create text surface with value
        valueSurf = self.font.render(
            f"{self.text}: {round(self.sliderWidth)}%", True, (255, 255, 255))

        # centre text
        textx = self.position[0] + (self.outlineSize[0] / 2) - \
            (valueSurf.get_rect().width / 2)
        texty = self.position[1] + (self.outlineSize[1] / 2) - \
            (valueSurf.get_rect().height / 2)

        screen.blit(valueSurf, (textx, texty))

    @property
    def sliderValue(self):
        return self.sliderWidth

    @sliderValue.setter
    def sliderValue(self, value):
        self.sliderWidth = value


class Button:
    def __init__(self, position: tuple, butHeigth: int = 70, butWidth: int = 300, text: str = "Кнопка"):
        self.position = position
        self.width = butWidth
        self.heigth = butHeigth
        self.text = text

    def mouse_in(self, mous_pos):
        x, y = mous_pos
        px, py = self.position
        if x > px and x < px + self.width:
            if y > py and y < py + self.heigth:
                return True
            else:
                return False
        else:
            return False

    def render(self, screen):
        mousePos = pygame.mouse.get_pos()
        if self.mouse_in(mousePos):
            pygame.draw.rect(screen, (112, 112, 112),
                             (self.position[0] - 1, self.position[1] - 1, self.width + 1, self.heigth + 1), 4)
            pygame.draw.rect(
                screen, (255, 255, 255), (self.position[0], self.position[1], self.width, self.heigth))
        else:
            pygame.draw.rect(screen, (112, 112, 112),
                             (self.position[0] - 1, self.position[1] - 1, self.width + 1, self.heigth + 1), 4)
            pygame.draw.rect(
                screen, (237, 237, 237), (self.position[0], self.position[1], self.width, self.heigth))
        # determite size of font
        self.font = pygame.font.SysFont("Segoe UI", 30)

        # create text surface with value
        valueSurf = self.font.render(f"{self.text}", True, (112, 112, 112))
        textx = self.position[0] + (self.width / 2) - \
            (valueSurf.get_rect().width / 2)
        texty = self.position[1] + (self.heigth / 2) - \
            (valueSurf.get_rect().height / 2)
        screen.blit(valueSurf, (textx, texty))


class Rect(Button):
    def __init__(self, position: tuple, butHeigth: int = 70, butWidth: int = 300, text: str = "Кнопка"):
        super().__init__(position, butHeigth=butHeigth, butWidth=butWidth, text=text)

    def render(self, screen):
        pygame.draw.rect(screen, (112, 112, 112),
                         (self.position[0] - 1, self.position[1] - 1, self.width + 1, self.heigth + 1), 4)
        pygame.draw.rect(screen, (237, 237, 237),
                         (self.position[0], self.position[1], self.width, self.heigth))
        self.font = pygame.font.SysFont("Segoe UI", 30)

        # create text surface with value
        valueSurf = self.font.render(f"{self.text}", True, (112, 112, 112))
        textx = self.position[0] + (self.width / 2) - \
            (valueSurf.get_rect().width / 2)
        texty = self.position[1] + (self.heigth / 2) - \
            (valueSurf.get_rect().height / 2)
        screen.blit(valueSurf, (textx, texty))


class Text(Button):
    def __init__(self, position: tuple, butHeigth: int = 70, butWidth: int = 300, text: str = "Кнопка",
     color: tuple = (112, 112, 112), background: tuple = None):
        super().__init__(position, butHeigth=butHeigth, butWidth=butWidth, text=text)
        self.color = color
        self.background = background

    def render(self, screen):

        self.font = pygame.font.SysFont("Segoe UI", 30)
        self.valueSurf = self.font.render(
            f"{self.text}", True, self.color, self.background)
        self.textx = self.position[0] + (self.width / 2) - \
            (self.valueSurf.get_rect().width / 2)
        self.texty = self.position[1] + (self.heigth / 2) - \
            (self.valueSurf.get_rect().height / 2)

        screen.blit(self.valueSurf, (self.textx, self.texty))


class OptionBox():

    def __init__(self, x, y, w, h, color, highlight_color, font, option_list, selected=0):
        self.color = color
        self.highlight_color = highlight_color
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.option_list = option_list
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def draw(self, surf):
        pygame.draw.rect(
            surf, self.highlight_color if self.menu_active else self.color, self.rect)
        pygame.draw.rect(surf, (0, 0, 0), self.rect, 2)
        msg = self.font.render(self.option_list[self.selected], 1, (0, 0, 0))
        surf.blit(msg, msg.get_rect(center=self.rect.center))

        if self.draw_menu:
            for i, text in enumerate(self.option_list):
                rect = self.rect.copy()
                rect.y += (i+1) * self.rect.height
                pygame.draw.rect(surf, self.highlight_color if i ==
                                 self.active_option else self.color, rect)
                msg = self.font.render(text, 1, (0, 0, 0))
                surf.blit(msg, msg.get_rect(center=rect.center))
            outer_rect = (self.rect.x, self.rect.y + self.rect.height,
                          self.rect.width, self.rect.height * len(self.option_list))
            pygame.draw.rect(surf, (0, 0, 0), outer_rect, 2)

    def update(self, event_list):
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i+1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.active_option
        return -1
