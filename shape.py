class Shape:
    def __init__(self, shape_letter):
        self.shape = self.get_shape_form(shape_letter)
        self.color = self.get_shape_color(shape_letter)

    def get_shape(self):
        return self.shape

    def get_color(self):
        return self.color

    def get_shape_form(self, shape_letter):
        # shapes = [S, Z, I, O, J, L, T]

        if shape_letter == 'S':
            form = [['.....',
                     '......',
                     '..00..',
                     '.00...',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..00.',
                     '...0.',
                     '.....']]

        elif shape_letter == 'Z':
            form = [['.....',
                     '.....',
                     '.00..',
                     '..00.',
                     '.....'],
                    ['.....',
                     '..0..',
                     '.00..',
                     '.0...',
                     '.....']]

        elif shape_letter == 'I':
            form = [['..0..',
                     '..0..',
                     '..0..',
                     '..0..',
                     '.....'],
                    ['.....',
                     '0000.',
                     '.....',
                     '.....',
                     '.....']]

        elif shape_letter == 'O':
            form = [['.....',
                     '.....',
                     '.00..',
                     '.00..',
                     '.....']]

        elif shape_letter == 'J':
            form = [['.....',
                     '.0...',
                     '.000.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..00.',
                     '..0..',
                     '..0..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.000.',
                     '...0.',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..0..',
                     '.00..',
                     '.....']]

        elif shape_letter == 'L':
            form = [['.....',
                     '...0.',
                     '.000.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..0..',
                     '..00.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.000.',
                     '.0...',
                     '.....'],
                    ['.....',
                     '.00..',
                     '..0..',
                     '..0..',
                     '.....']]

        elif shape_letter == 'T':
            form = [['.....',
                     '..0..',
                     '.000.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..0..',
                     '..00.',
                     '..0..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.000.',
                     '..0..',
                     '.....'],
                    ['.....',
                     '..0..',
                     '.00..',
                     '..0..',
                     '.....']]

        return form

    def get_shape_color(self, shape_letter):
        color = None
        if shape_letter == 'S':
            color = (0, 255, 0)
        elif shape_letter == 'Z':
            color = (255, 0, 0)
        elif shape_letter == 'I':
            color = (0, 255, 255)
        elif shape_letter == 'O':
            color = (255, 255, 0)
        elif shape_letter == 'J':
            color = (255, 165, 0)
        elif shape_letter == 'L':
            color = (0, 0, 255)
        elif shape_letter == 'T':
            color = (128, 0, 128)

        return color
