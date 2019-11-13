from shape import Shape


class Piece(object):

    def __init__(self, x, y, shape_letter):
        self.x = x
        self.y = y
        self.original_shape = Shape(shape_letter)
        self.shape = self.original_shape.get_shape()
        self.color = self.original_shape.get_color()
        self.rotation = 0
        self.letter = shape_letter

    def get_shape_letter(self):
        return self.letter

    def reset_piece(self, x, y):
        self.x = x
        self.y = y
        self.rotation = 0
