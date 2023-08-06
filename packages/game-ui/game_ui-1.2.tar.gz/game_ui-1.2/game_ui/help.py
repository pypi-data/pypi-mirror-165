help = '''
ENG:

At the moment, pyUI has only buttons - square and round

To create a button:
    bt = Button(surface, **args)

    or

    Button(surface, **args)

    Arguments:
        surface - the window on which the button will be drawn
        x is the X coordinate

        y is the Y coordinate

        width - width of the button

        height - height of the button

        color - button color

        pressedColor - the color of the button when it is pressed

        selectedColor - the color of the button when the cursor is hovered over it

        func - the function that will be executed when the button is pressed

        text - the text of the button

        textColor - text color
    
    Methods:
        bt.setRender(bool)

        # indicates whether the button will be rendered on the screen, by default - yes



To create a round button:
    bt = roundButton(surface, **args)

    or

    roundButton(surface, **args)

    Arguments:
        surface - the window on which the button will be drawn

        x is the X coordinate

         y is the Y coordinate

        radius - the radius of the button size

        color - button color

        pressedColor - the color of the button when it is pressed

        selectedColor - the color of the button when the cursor is hovered over it

        func - the function that will be executed when the button is pressed

        text - the text of the button

        textColor - text color

        pressedText - the text of the button when the button is pressed

        fontSize - the font size of the text

        fast - indicates whether the function will be called after pressing the button or until the button is pressed

    Methods:
        bt.setRender(bool)

        # indicates whether the button will be rendered on the screen, by default - yes

        # ways to draw buttons in a loop
    
        bt.update() # first way, will only update the button that belongs to this variable

        for obj in Buttons: obj.update() # second way, will update all buttons


RU:

На данный момент в pyUI есть только кнопки - квадратные и круглые

Для создания кнопки:
    bt = Button(surface, **args)

    или

    Button(surface, **args)

    Аргументы:
        surface - окно на котором будет рисоваться кнопка
        x - координата по X

        y - координата по Y

        width - ширина кнопки

        height - высота кнопки

        color - цвет кнопки

        pressedColor - цвет кнопки когда она нажата

        selectedColor - цвет кнопки когда курсор наведен на нее

        func - функция которая будет выполняться при нажатии кнопки

        text - текст кнопки

        textColor - цвет текста

        pressedText - текст кнопки когда кнопка нажата

        fontSize - размер шрифта текста

        fast - говорит о том будет ли вызываться функция после отжатия кнопки или до тех пор пока кнопка нажата

    Методы:
        bt.setRender(bool)

        # говорит о том будет ли кнопка отрисововаться на экране, по умолчанию - да



Для создания круглой кнопки:
    bt = roundButton(surface, **args)

    или

    roundButton(surface, **args)

    Аргументы:
        surface - окно на котором будет рисоваться кнопка

        x - координата по X

        y - координата по Y

        radius - радиус размера кнопки

        color - цвет кнопки

        pressedColor - цвет кнопки когда она нажата

        selectedColor - цвет кнопки когда курсор наведен на нее

        func - функция которая будет выполняться при нажатии кнопки

        text - текст кнопки

        textColor - цвет текста

        pressedText - текст кнопки когда кнопка нажата

        fontSize - размер шрифта текста

        fast - говорит о том будет ли вызываться функция после отжатия кнопки или до тех пор пока кнопка нажата

    Методы:
        bt.setRender(bool)

        # говорит о том будет ли кнопка отрисововаться на экране, по умолчанию - да
    
        # способы отрисовки кнопок в цикле
    
        bt.update() # первый способ, обновит только кнопку которая принадлежит этой переменной

        for obj in Buttons: obj.update() # второй способ, обновит все кнопки

'''