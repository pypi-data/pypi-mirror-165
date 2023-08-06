import sass

from dashy.utils import PROJECT_ROOT


class Theme:
    def __init__(self):

        self.main_color = None
        self.background_color = None
        self.container_background = None
        self.accent_color = None
        self.font_color = None

        self.white = "#FFFFFF"
        self.black = "#000000"

    def compile(self):
        with open(str(PROJECT_ROOT / "assets" / "main.scss"), "r") as f:
            sass_src = f.read()

        sass_src = (
            f"$main_color: {self.main_color};\n"
            f"$background_color: {self.background_color};\n"
            f"$container_background_color: {self.container_background};\n"
            f"$accent_color: {self.accent_color};\n"
            f"$font_color: {self.font_color};\n" + sass_src
        )

        with open(str(PROJECT_ROOT / "assets" / "main.css"), "w") as f:
            f.write(sass.compile(string=sass_src))


class StandardTheme(Theme):
    def __init__(self):
        super().__init__()

        # Colors
        self.main_color = "#2A3F5F"
        self.background_color = "#e5e8e6"
        self.container_background = "#FFFFFF"
        self.accent_color = "#00BC9D"
        self.font_color = "#FFFFFF"


class DarkTheme(Theme):
    def __init__(self):
        super(DarkTheme, self).__init__()

        # Colors
        self.main_color = "#262D32"
        self.background_color = "#323C44"
        self.container_background = "#FFFFFF"
        self.accent_color = "#5DBBAE"
        self.font_color = "#FFFFFF"


class TorchBoardTheme(Theme):
    def __init__(self):
        super(TorchBoardTheme, self).__init__()

        # Colors
        self.main_color = "#262D32"
        self.background_color = "#323C44"
        self.container_background = "#FFFFFF"
        self.accent_color = "#5DBBAE"
        self.font_color = "#E0E0E0"
        self.graph_main_color = "#EE5136"
