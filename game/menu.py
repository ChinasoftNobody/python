import logging

from game import MenuMeta, tk, MENU_SIZE

LOG = logging.getLogger(__file__)


class Menu(MenuMeta, tk.Frame):
    """
    主菜单
    """
    game_names = None

    def __init__(self):
        self.root = tk.Tk()
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        pos = (screenwidth - MENU_SIZE[0]) / 2, (screenheight - MENU_SIZE[1]) / 2
        self.root.geometry('%dx%d+%d+%d' % (MENU_SIZE[0], MENU_SIZE[1], pos[0], pos[1]))
        super().__init__(self.root)
        self.pack()

    def get_game_names(self) -> list:
        return super().get_game_names()

    def run_game(self, game_name) -> None:
        super().run_game(game_name)

    def stop_games(self) -> None:
        super().stop_games()

    def init_menu(self) -> None:
        LOG.info('init menu...')
        self.game_names = self.get_game_names()
        LOG.info('get game names: ' + repr(self.game_names))
        self._init_frame()

    def exit_game(self) -> None:
        super().exit_game()

    def _init_frame(self):
        self.hi_there = tk.Button(self, text='Hello world\n(click me)', command=self._say_hi)
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.root.destroy)
        self.quit.pack(side="bottom")
        self.mainloop()

    def _say_hi(self):
        print("hi there, everyone!")
