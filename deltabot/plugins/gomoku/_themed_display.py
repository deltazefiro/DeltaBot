from PIL import Image, ImageDraw, ImageFont

ALPHABET = 'ABCDEFGHIJKLMNO'

class DisplayGomoku(object):
    d = 800
    ld = int(d * 0.005)
    margin = 0.1
    a = margin * d  # grid_upper
    b = (1 - margin) * d  # grid_lower
    c = b - a

    bgcolor = '#384259'
    color1 = '#7ac7c4'
    color2 = '#c4edde'
    color3 = '#f73859'

    # font = ImageFont.load('ubuntu')

    def __init__(self):
        self.img = Image.new('RGB', (self.d, self.d), self.bgcolor)
        self.drawer = ImageDraw.Draw(self.img)

        for i in range(15):
            self.drawer.line([(self.c / 14 * i + self.a, self.a), (self.c / 14 * i + self.a, self.b)], fill=self.color1,
                             width=self.ld)
            self.drawer.line([(self.a, self.c / 14 * i + self.a), (self.b, self.c / 14 * i + self.a)], fill=self.color1,
                             width=self.ld)

            self.drawer.text((self.c / 14 * i + self.a, self.b + 3 * self.ld), ALPHABET[i], fill=self.color1)
            self.drawer.text((self.a - 8 * self.ld, self.c / 14 * (14-i) + self.a), str(i+1), fill=self.color1, align='right')

    def draw_chess(self, x, y, player, high_lighted=False):
        color = 'black' if player == 1 else 'white'
        x, y = self.c / 14 * x + self.a, self.c / 14 * (14-y) + self.a
        r = 10 * self.ld
        self.drawer.ellipse([(x - r / 2, y - r / 2), (x + r / 2, y + r / 2)], fill=color,
                            outline=self.color3 if high_lighted else self.color2, width=self.ld)

    def show(self):
        self.img.show()


if __name__ == '__main__':
    drawer = DisplayGomoku()
    drawer.draw_chess(3, 2, 1, True)
    drawer.draw_chess(0, 0, 2)
    drawer.show()
