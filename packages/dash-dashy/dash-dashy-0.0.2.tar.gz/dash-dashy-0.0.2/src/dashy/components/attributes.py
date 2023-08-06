from enum import Enum


class Size(Enum):
    SM = "sm"
    MD = "md"
    LG = "lg"

    @staticmethod
    def class_name() -> str:
        return "size"


class Placement(Enum):
    AUTO = "auto"
    AUTO_START = "auto-start"
    AUTO_END = "auto-end"
    TOP = "top"
    TOP_START = "top-start"
    TOP_END = "top-end"
    RIGHT = "right"
    RIGHT_START = "right-start"
    RIGHT_END = "right-end"
    BOTTOM = "bottom"
    BOTTOM_START = "bottom-start"
    BOTTOM_END = "bottom-end"
    LEFT = "left"
    LEFT_START = "left-start"
    LEFT_END = "left-end"

    @staticmethod
    def class_name() -> str:
        return "placement"


class Trigger(Enum):
    HOVER = "hover"
    CLICK = "click"
    FOCUS = "focus"
    LEGACY = "legacy"

    @staticmethod
    def class_name() -> str:
        return "trigger"


class Color(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "sucess"
    INFO = "info"
    WARNING = "warning"
    DANGER = "danger"
    LIGHT = "light"
    DARK = "dark"


class InputType(Enum):
    NUMBER = "number"
    TEXT = "text"
    PASSWORD = "password"
    EMAIL = "email"
    RANGE = "range"
    SEARCH = "search"
    TEL = "tel"
    URL = "url"
    HIDDEN = "hidden"


class SliderUpateMode(Enum):
    DRAG = "drag"
    MOUSE_UP = "mouseup"
