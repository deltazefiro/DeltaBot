from PIL import Image, ImageDraw

class DisplayGomoku(object):
    d = 1000
    ld = int(d * 0.005)
    margin = 0.1
    a = margin * d  # grid_upper
    b = (1 - margin) * d  # grid_lower
    c = b - a

    def __init__(self):
        self.img = Image.new('RGB', (self.d, self.d), (233, 233, 233))
        self.drawer = ImageDraw.Draw(self.img)

        for i in range(15):
            self.drawer.line([(self.c / 14 * i + self.a, self.a), (self.c / 14 * i + self.a, self.b)], fill='black',
                             width=self.ld)
            self.drawer.line([(self.a, self.c / 14 * i + self.a), (self.b, self.c / 14 * i + self.a)], fill='black',
                             width=self.ld)

            self.drawer.text((self.c / 14 * i + self.a, self.b + 3 * self.ld), str(i + 1), fill='black')
            self.drawer.text((self.a - 8 * self.ld, self.c / 14 * (14-i) + self.a), str(i + 1), fill='black', align='right')

    def draw_chess(self, x, y, player, high_lighted=False):
        color = 'black' if player == 1 else 'white'
        x, y = self.c / 14 * x + self.a, self.c / 14 * (14-y) + self.a
        r = 10 * self.ld
        self.drawer.ellipse([(x - r / 2, y - r / 2), (x + r / 2, y + r / 2)], fill=color,
                            outline='yellow' if high_lighted else 'grey', width=self.ld)

    def get_img(self):
        return self.img

    def show(self):
        self.img.show()

if __name__ == '__main__':
    drawer = DisplayGomoku()
    drawer.draw_chess(3, 2, 1, True)
    drawer.draw_chess(0, 0, 2)
    drawer.show()
