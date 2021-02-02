import ctypes
import pathlib

import display
DisplayGomoku = display.DisplayGomoku
# from .display import DisplayGomoku

libname = pathlib.Path().absolute() / "search.so"
gomoku = ctypes.CDLL(libname)

USER = 1
BOT = 2

class GomokuGame(object):
    get_c_chessboard = ctypes.c_int * 255

    def __init__(self):
        self.chessboard = [0]*225
        self.display = DisplayGomoku()

    def get_C_chessboard(self):
        return (ctypes.c_int * 255)(*self.chessboard)

    def search(self):
        r = gomoku.cSearch(self.get_C_chessboard())
        return r // 15, r % 15

    def estimate(self):
        return gomoku.cEstimate(self.get_C_chessboard())

    def set_chess(self, x, y, player: int):
        if not self.chessboard[x*15+y]:
            self.chessboard[x*15+y] = player

    def update_display(self):
        for i, player in enumerate(self.chessboard):
            if player:
                self.display.draw_chess(i//15, i%15, player)

    def get_display_img(self):
        return self.display.get_img()

    def update(self, x, y):
        self.set_chess(x, y, USER)
        sco = self.estimate()
        if sco > 5*1e5:
            self.update_display()
            return 1

        x, y = self.search()
        self.set_chess(x, y, BOT)
        sco = self.estimate()
        self.update_display()
        if sco < -5*1e5:
            return 0


if __name__ == '__main__':
    game = GomokuGame()
    while True:
        x_, y_ = input('x, y >> ').split()
        game.update(int(x_)-1, int(y_)-1)
        game.update_display()
        game.get_display_img().show()
