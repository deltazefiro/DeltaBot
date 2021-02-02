import ctypes
import os
import random
import shutil
import string

from .display import DisplayGomoku

get_relative_path = lambda p: os.path.join(os.path.dirname(__file__), p)
gomoku = ctypes.CDLL(get_relative_path('search.so'))
RANDPOOL = string.ascii_letters + string.digits


class GomokuGame(object):
    # TODO: 使用多线程调用搜索，防止阻碍事件循环
    get_c_chessboard = ctypes.c_int * 255

    def __init__(self, game_id):
        self.chessboard = [0] * 225
        self.display = DisplayGomoku()

        os.makedirs(get_relative_path(f'data/pic/{game_id}'), exist_ok=True)
        self.game_id = game_id

    def __del__(self):
        shutil.rmtree(get_relative_path(f'data/pic/{self.game_id}'))

    def get_C_chessboard(self):
        return (ctypes.c_int * 255)(*self.chessboard)

    def search(self):
        r = gomoku.cSearch(self.get_C_chessboard())
        return r // 15, r % 15

    def estimate(self):
        return gomoku.cEstimate(self.get_C_chessboard())

    def set_chess(self, x, y, player: int):
        if not self.chessboard[x * 15 + y]:
            self.chessboard[x * 15 + y] = player
            return True
        return False

    def update_display(self):
        for i, player in enumerate(self.chessboard):
            if player:
                self.display.draw_chess(i // 15, i % 15, player)

    def get_img(self):
        fp = os.path.join(get_relative_path(f'data/pic/{self.game_id}'),
                          "".join(random.choices(RANDPOOL, k=10)) + '.png')
        self.display.img.save(fp)
        return 'file://' + fp

# if __name__ == '__main__':
#     game = GomokuGame()
#     while True:
#         x_, y_ = input('x, y >> ').split()
#         game.update(int(x_)-1, int(y_)-1)
#         game.get_display_img().show()
