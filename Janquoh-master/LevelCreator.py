import pygame
from os import environ

"""
# state 1 = Eraser
# state 2 = Wall
# state 3 = Make Border
# state 4 = Clean Field
# state 5 = Make Door

clipboard
"""

class Creator(object):
    def __init__(self, x, y, id):
        self.id = id
        self.rect = pygame.Rect(x, y, 25, 25)
        self.state = 1
        self.text = ""

    def Action(self,current, event, text):
        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP:
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(event.pos):
                if current == 2 or current == 1 or current == 5:
                    self.state = current
                if current == 5:
                    self.text = text
                print("tiler:", self.id, " /// state:", self.state)

class Tool(object):
    def __init__(self, x, y, id):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.id = id

    def Click(self, current, event, maps):
        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP:
            if self.rect.collidepoint(event.pos):
                if self.id == 1 or self.id == 2:
                    current = self.id
                if self.id == 3:
                    for x in range(38):
                        maps[x].state = 2
                        maps[x+950].state = 2
                    for x in range(26):
                        maps[x*38].state = 2
                        maps[x * 38-1].state = 2
                if self.id == 4:
                    for map in maps:
                        map.state = 1
                if self.id == 5:
                    current = self.id

                print("clicking in tool:", self.id, " /// state:", self.id)
            return current, maps

class TextBox(object):
    def __init__(self):
        self.color1 = pygame.Color(200,200,200)
        self.color2 = pygame.Color(50,150,250)
        self.font = pygame.font.Font(None, 25)
        self.color = self.color1
        self.active = False
        self.state = 0
        self.rect = pygame.Rect(1050, 550, 200, 30)
        self.text = ""

    def Write(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color2 if self.active else self.color1

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if event.key == pygame.K_LCTRL:
                    self.text = ""
            else:
                self.text += event.unicode

class Button(object):
    def __init__(self, x, y, id):
        self.rect = pygame.Rect(x, y, 200, 50)

    def Click(self, event, maps):
        if event.type != pygame.KEYDOWN and event.type != pygame.KEYUP:
            if self.rect.collidepoint(event.pos):
                Export(maps)

def Export(maps):
    file = [[" " for x in range(38)] for y in range(26)]

    for map in maps:
        if map.state == 1:
            map.state = ' '
        elif map.state == 2:
            map.state = 'a'
        elif map.state == 5:
            map.state = str(map.text)

    z = -1
    for y in range(len(file)):
        for x in range(len(file[0])):
            z += 1
            file[y][x] = maps[z].state

    for y in range(len(file)):
        for x in range(len(file[0])):
            print("printing :", y, ".", x, "- {", file[y][x], "}")

    print(file)

def EventHandler(current, maps, tools, buttons, text):
    for event in pygame.event.get():

        text.Write(event)

        for map in maps:
            map.Action(current, event, text.text)

        if pygame.mouse.get_pressed()[0]:
            for tool in tools:
                current, maps = tool.Click(current, event, maps)

            for button in buttons:
                button.Click(event, maps)

        if event.type == pygame.QUIT:
            exit(0)
    return current

def Draw(maps, tools, buttons, text, current):
    for map in maps:
        if map.state == 2:
            pygame.draw.rect(screen, (100, 100, 100), map.rect, 0)

        pygame.draw.rect(screen, (200, 200, 200), map.rect, 1)

    for button in buttons:
        pygame.draw.rect(screen, (100, 100, 100), button.rect, 1)

    for tool in tools:
        if tool.id == 1:
            screen.blit(pygame.image.load("Assets/eraser.png"), (tool.rect))
        elif tool.id == 2:
            screen.blit(pygame.image.load("Assets/wall.png"), (tool.rect))
        elif tool.id == 3:
            screen.blit(pygame.image.load("Assets/border.png"), (tool.rect))
        elif tool.id == 4:
            screen.blit(pygame.image.load("Assets/delete.png"), (tool.rect))
        elif tool.id == 5:
            screen.blit(pygame.image.load("Assets/wip.png"), (tool.rect))
        else:
            screen.blit(pygame.image.load("Assets/blank.png"), (tool.rect))

        pygame.draw.rect(screen, (100, 100, 100), tool.rect, 1)

    for tool in tools:
        if tool.id == current:
            pygame.draw.rect(screen, (200, 200, 0), tool.rect, 4)

    surface = text.font.render(text.text, True, text.color)
    screen.blit(surface, (text.rect.x + 5, text.rect.y + 5))
    pygame.draw.rect(screen, text.color, text.rect, 1)

def Create(maps, tools):
    id = 0
    if tools == []:
        x = 1000
        y = 25
        for row in range(8):
            for col in range(4):
                id += 1
                x += 50
                tools += [Tool(x, y, id)]

            y += 50
            x = 1000
        return tools

    if maps == []:
        x = y = 25
        for row in range(26):
            for col in range(38):
                id += 1
                maps += [Creator(x, y, id)]
                x += 25
            y += 25
            x = 25
        return maps

def Main():
    current = 0

    maps = []
    tools = []
    buttons = []

    buttons += [Button(1050, 475, 1)]

    maps = Create(maps, 0)
    tools = Create(0, tools)

    text = TextBox()

    while True:
        screen.fill((0, 0, 0))

        Draw(maps, tools, buttons, text, current)

        current = EventHandler(current, maps, tools, buttons, text)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()

    environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 25)
    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((1300, 700))

    clock = pygame.time.Clock()
    Main()