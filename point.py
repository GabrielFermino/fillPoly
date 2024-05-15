class Point:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.cor = self.hex_to_rgb(color)

    def xy(self):
        return (self.x, self.y)
    
    @staticmethod
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hex(rgb_color):
        return '#%02x%02x%02x' % rgb_color