import pygame

pygame.init()

class Button:
    def __init__(self, surface, **args):
        
        Buttons.append(self)
        
        self.px, self.py = 0, 0
        self.width, self.height = 100, 100
        self.surface = surface
        
        self.color = (150, 150, 150)   # цвет кнопки
        self.pressedColor = (80, 80, 80)   # цвет кнопки когда она нажата
        self.selectedColor = (120, 120, 120)   # цвет кнопки когда курсор наведен на нее
        self.func = 'notFunc'   # функция которая будет вызываться при нажатии кнопки
        self.defaultText = ''   # текст кнопки
        self.textColor = (255, 255, 255)   # цвет текста
        self.text = self.defaultText
        self.pressedText = self.text   # текст кнопки когда кнопка нажата
        self.fontSize = 70   # размер шрифта
        self.fast = False   # говорит о том будет ли вызываться функция после отжатия кнопки или до тех пор пока кнопка нажата
        self.font = pygame.font.Font(None, self.fontSize)
        self.mode = 0   # режим цвета кнопки
        self.press = False
        self.render = True
        
        self.rect = pygame.Rect(self.px, self.py, self.width, self.height)

        for arg in args:
            get = str(arg)

            if get == 'x':
                self.px = args[get]
            if get == 'y':
                self.py = args[get]
                
            if get == 'width':
                self.width = args[get]
            if get == 'height':
                self.height = args[get]

            if get == 'color':
                self.color = args[get]
            if get == 'pressedColor':
                self.pressedColor = args[get]
            if get == 'selectedColor':
                self.selectedColor = args[get]
            if get == 'func':
                self.func = args[get]
            if get == 'text':
                self.defaultText = args[get]
            if get == 'fast':
                self.fast = args[get]
            if get == 'pressedText':
                self.pressedText = args[get]
            if get == 'fontSize':
                self.fontSize = args[get]
            if get == 'textColor':
                self.textColor = args[get]
            
        self.text = self.defaultText
        self.pressedText = self.text
        self.rect = pygame.Rect(self.px, self.py, self.width, self.height)
        self.font = pygame.font.Font(None, self.fontSize)
    
    def setRender(self, value):
        if value == True:
            self.render = True
        elif value == False:
            self.render = False
    
    def pressed(self):
        if self.press:
            return True
    
    def config(self, **args):
        for arg in args:
            get = str(arg)

            if get == 'x':
                self.px = args[get]
            if get == 'y':
                self.py = args[get]
                
            if get == 'width':
                self.width = args[get]
            if get == 'height':
                self.height = args[get]

            if get == 'color':
                self.color = args[get]
            if get == 'pressedColor':
                self.pressedColor = args[get]
            if get == 'selectedColor':
                self.selectedColor = args[get]
            if get == 'func':
                self.func = args[get]
            if get == 'text':
                self.defaultText = args[get]
            if get == 'fast':
                self.fast = args[get]
            if get == 'pressedText':
                self.pressedText = args[get]
            if get == 'fontSize':
                self.fontSize = args[get]
            if get == 'textColor':
                self.textColor = args[get]
            
        self.text = self.defaultText
        self.pressedText = self.text
        self.rect = pygame.Rect(self.px, self.py, self.width, self.height)
        self.font = pygame.font.Font(None, self.fontSize)
    
    def update(self):
        
        mousePos = pygame.mouse.get_pos()
        
        bt1, bt2, bt3 = pygame.mouse.get_pressed()
        
        if not self.fast:
            if bt1 and self.rect.collidepoint(mousePos) and not self.press:
                self.text = self.pressedText
                self.mode = 1
                self.press = True
            if not bt1 and self.press and self.rect.collidepoint(mousePos):
                self.text = self.defaultText
                if self.func != 'notFunc':
                    self.func()
                self.mode = 0
                self.press = False
        
            mousePos = pygame.mouse.get_pos()
            if not self.rect.collidepoint(mousePos) and self.press and bt1:
                self.text = self.defaultText
                self.mode = 0
                self.press = False
            if self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 2
            if not self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 0
        
        if self.fast:
            if bt1 and self.rect.collidepoint(mousePos):
                self.text = self.pressedText
                self.mode = 1
                if self.func != 'notFunc':
                    self.func()
                self.press = True
            if not bt1 and self.press and self.rect.collidepoint(mousePos):
                self.text = self.defaultText
                self.mode = 0
                self.press = False
        
            mousePos = pygame.mouse.get_pos()
            if not self.rect.collidepoint(mousePos) and self.press and bt1:
                self.text = self.defaultText
                self.mode = 0
                self.press = False
            if self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 2
            if not self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 0
        self.draw()
            
    def draw(self):

        if self.render:
            if self.mode == 0:
                pygame.draw.rect(self.surface, self.color, self.rect)
            elif self.mode == 1:
                pygame.draw.rect(self.surface, self.pressedColor, self.rect)
            elif self.mode == 2:
                pygame.draw.rect(self.surface, self.selectedColor, self.rect)

            text = self.font.render(self.text, 1, self.textColor)
            textWin = text.get_rect(center=(self.rect.x + self.width // 2, self.rect.y + self.height // 2))
            self.surface.blit(text, textWin)

class roundButton:
    def __init__(self, surface, **args):
        
        Buttons.append(self)
        
        self.px, self.py = 0, 0
        self.radius = 50
        self.ballRect = int(self.radius * 2 ** 0.5)
        self.surface = surface
        
        self.color = (150, 150, 150)   # цвет кнопки
        self.pressedColor = (80, 80, 80)   # цвет кнопки когда она нажата
        self.selectedColor = (120, 120, 120)   # цвет кнопки когда курсор наведен на нее
        self.func = 'notFunc'   # функция которая будет вызываться при нажатии кнопки
        self.defaultText = ''   # текст кнопки
        self.textColor = (255, 255, 255)   # цвет текста
        self.text = self.defaultText
        self.pressedText = self.text   # текст кнопки когда кнопка нажата
        self.fontSize = 70   # размер шрифта
        self.fast = False   # говорит о том будет ли вызываться функция после отжатия кнопки или до тех пор пока кнопка нажата
        self.font = pygame.font.Font(None, self.fontSize)
        self.mode = 0   # режим цвета кнопки
        self.press = False
        self.render = True
        
        self.rect = pygame.Rect(self.px, self.py, self.ballRect, self.ballRect)

        for arg in args:
            get = str(arg)

            if get == 'x':
                self.px = args[get]
            if get == 'y':
                self.py = args[get]
            
            if get == 'radius':
                self.radius = args[get]

            if get == 'color':
                self.color = args[get]
            if get == 'pressedColor':
                self.pressedColor = args[get]
            if get == 'selectedColor':
                self.selectedColor = args[get]
            if get == 'func':
                self.func = args[get]
            if get == 'text':
                self.defaultText = args[get]
            if get == 'fast':
                self.fast = args[get]
            if get == 'pressedText':
                self.pressedText = args[get]
            if get == 'fontSize':
                self.fontSize = args[get]
            if get == 'textColor':
                self.textColor = args[get]
            
        self.text = self.defaultText
        self.pressedText = self.text
        self.ballRect = int(self.radius * 2 ** 0.5)
        self.rect = pygame.Rect(self.px, self.py, self.ballRect, self.ballRect)
        self.font = pygame.font.Font(None, self.fontSize)
    
    def setRender(self, value):
        if value == True:
            self.render = True
        elif value == False:
            self.render = False
    
    def pressed(self):
        if self.press:
            return True
    
    def config(self, **args):
        for arg in args:
            get = str(arg)

            if get == 'x':
                self.px = args[get]
            if get == 'y':
                self.py = args[get]
            
            if get == 'radius':
                self.radius = args[get]

            if get == 'color':
                self.color = args[get]
            if get == 'pressedColor':
                self.pressedColor = args[get]
            if get == 'selectedColor':
                self.selectedColor = args[get]
            if get == 'func':
                self.func = args[get]
            if get == 'text':
                self.defaultText = args[get]
            if get == 'fast':
                self.fast = args[get]
            if get == 'pressedText':
                self.pressedText = args[get]
            if get == 'fontSize':
                self.fontSize = args[get]
            if get == 'textColor':
                self.textColor = args[get]
            
        self.text = self.defaultText
        self.pressedText = self.text
        self.ballRect = int(self.radius * 2 ** 0.5)
        self.rect = pygame.Rect(self.px, self.py, self.ballRect, self.ballRect)
        self.font = pygame.font.Font(None, self.fontSize)
    
    def update(self):
        
        mousePos = pygame.mouse.get_pos()
        
        bt1, bt2, bt3 = pygame.mouse.get_pressed()
        
        if not self.fast:
            if bt1 and self.rect.collidepoint(mousePos) and not self.press:
                self.text = self.pressedText
                self.mode = 1
                self.press = True
            if not bt1 and self.press and self.rect.collidepoint(mousePos):
                self.text = self.defaultText
                if self.func != 'notFunc':
                    self.func()
                self.mode = 0
                self.press = False
        
            mousePos = pygame.mouse.get_pos()
            if not self.rect.collidepoint(mousePos) and self.press and bt1:
                self.text = self.defaultText
                self.mode = 0
                self.press = False
            if self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 2
            if not self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 0
        
        if self.fast:
            if bt1 and self.rect.collidepoint(mousePos):
                self.text = self.pressedText
                self.mode = 1
                if self.func != 'notFunc':
                    self.func()
                self.press = True
            if not bt1 and self.press and self.rect.collidepoint(mousePos):
                self.text = self.defaultText
                self.mode = 0
                self.press = False
        
            mousePos = pygame.mouse.get_pos()
            if not self.rect.collidepoint(mousePos) and self.press and bt1:
                self.text = self.defaultText
                self.mode = 0
                self.press = False
            if self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 2
            if not self.rect.collidepoint(mousePos) and not self.press and not bt1:
                self.mode = 0
        self.draw()
            
    def draw(self):

        if self.render:
            if self.mode == 0:
                pygame.draw.circle(self.surface, self.color, self.rect.center, self.radius)
            elif self.mode == 1:
                pygame.draw.circle(self.surface, self.pressedColor, self.rect.center, self.radius)
            elif self.mode == 2:
                pygame.draw.circle(self.surface, self.selectedColor, self.rect.center, self.radius)

            text = self.font.render(self.text, 1, self.textColor)
            textWin = text.get_rect(center=(self.rect.x + self.ballRect // 2, self.rect.y + self.ballRect // 2))
            self.surface.blit(text, textWin)

Buttons = []