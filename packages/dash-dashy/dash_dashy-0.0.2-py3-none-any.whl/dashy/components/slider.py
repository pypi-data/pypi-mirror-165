from typing import Optional, Union

import dash_bootstrap_components as dbc
from dash import dcc

from .attributes import Placement, SliderUpateMode
from .layout import col


def slider(
    id: str,
    title: str,
    min: int,
    max: int,
    step: int,
    value: Optional[Union[int, list[int]]] = None,
    marks: Optional[Union[dict[int, str], bool]] = True,
    update_mode: SliderUpateMode = SliderUpateMode.MOUSE_UP,
    tooltip: bool = False,
    tooltip_placement: Placement = Placement.BOTTOM,
    tooltip_always_visible: bool = False,
    vertical: bool = False,
    vertical_height: int = 400,
    allow_cross: bool = False,
) -> dbc.Col:
    """A slider

    Args:
        id: Id of the slider
        title: Title that will be displayed above the slider
        min: Min value of the slider
        max: Max value of the slider
        step: Step size between min and max range
        value: Initial value. If None 'min' will be use. If a list the slider will be a range slider.
        marks: Slider marks. If True marks will be generated. If None no marks will be visible.
               Can also pass a dict with custom marks
        update_mode: How the value of the slider should be updated.
        tooltip: If True a tooltip will be shown.
        tooltip_placement: Placement of the tooltip.
        tooltip_always_visible: If True the tooltip will always be shown, if False it will only show it on hover.
        vertical: If True the slider will be vertical
        vertical_height: Height in px if the slider is vertical
        allow_cross: If True and the slider is a range slider handles will not be able to cross each other.

    Returns:
        Slider component
    """
    if value is None:
        value = min

    kwargs = dict(
        id=id,
        min=min,
        max=max,
        step=step,
        updatemode=update_mode.value,
        value=value,
        className="w-100 h-100",
        vertical=vertical,
        verticalHeight=vertical_height,
    )

    if marks is None or isinstance(marks, dict):
        kwargs["marks"] = marks

    if tooltip is True:
        kwargs["tooltip"] = {
            Placement.class_name(): tooltip_placement.value,
            "always_visible": tooltip_always_visible,
        }

    if isinstance(value, list):
        kwargs["allowCross"] = allow_cross
        slider = dcc.RangeSlider(**kwargs)
    else:
        slider = dcc.Slider(**kwargs)

    return col([dbc.Label(title), slider], auto_size=False)
