from typing import Optional, Union

from dash.development.base_component import Component
from dash import html
import dash_bootstrap_components as dbc

from .helpers import get_margin_class, get_padding_class


def container(
        children: list = None,
        fluid: bool = True,
        margin: int = 1,
        margin_right: int = None,
        margin_left: int = None,
        margin_top: int = None,
        margin_bottom: int = None,
        padding: int = 0,
        padding_right: int = None,
        padding_left: int = None,
        padding_top: int = None,
        padding_bottom: int = None,
        **kwargs
) -> dbc.Container:
    """Container component. Use this to hold rows and cols with components.

    The margin and padding is specified in bootstrap fashion, 0-5. (0 - 3rem)

    Args:
        children (list, optional): Children of the container. Defaults to None.

        fluid (bool, optional): If True the container-fluid class will be applied, and the Container
                                will expand to fill available space. Defaults to True.

        margin (int, optional): Margin will be ovvride if any specific margin is specified. Defaults to 1.
        margin_right (int, optional): Margin left. Defaults to None.
        margin_left (int, optional): Margin right. Defaults to None.
        margin_top (int, optional): Margin top. Defaults to None.
        margin_bottom (int, optional): Margin bottom. Defaults to None.
        padding (int, optional): Padding. Defaults to 0.
        padding_right (int, optional): Padding right. Defaults to None.
        padding_left (int, optional): Padding left. Defaults to None.
        padding_top (int, optional): Padding top. Defaults to None.
        padding_bottom (int, optional): Padding bottom. Defaults to None.

    Returns:
        dbc.Container
    """
    kwargs = {
        'className': (
            f'{get_margin_class(margin, margin_top, margin_bottom, margin_left, margin_right)} '
            f'{get_padding_class(padding, padding_top, padding_bottom, padding_left, padding_right)}'
        ),
        **kwargs
    }
    return dbc.Container(children, fluid=fluid, **kwargs)


def row(
    children: Union[list, str, Component],
    margin: int = 1,
    margin_right: int = None,
    margin_left: int = None,
    margin_top: int = None,
    margin_bottom: int = None,
    padding: int = 0,
    padding_right: int = None,
    padding_left: int = None,
    padding_top: int = None,
    padding_bottom: int = None,
    auto_size: bool = True,
    **kwargs
) -> dbc.Row:
    """Row component.

    The margin and padding is specified in bootstrap fashion, 0-5. (0 - 3rem)

    Args:
        children (list, optional): Children of the container. Defaults to None.
        margin (int, optional): Margin will be ovvride if any specific margin is specified. Defaults to 1.
        margin_right (int, optional): Margin left. Defaults to None.
        margin_left (int, optional): Margin right. Defaults to None.
        margin_top (int, optional): Margin top. Defaults to None.
        margin_bottom (int, optional): Margin bottom. Defaults to None.
        padding (int, optional): Padding. Defaults to 0.
        padding_right (int, optional): Padding right. Defaults to None.
        padding_left (int, optional): Padding left. Defaults to None.
        padding_top (int, optional): Padding top. Defaults to None.
        padding_bottom (int, optional): Padding bottom. Defaults to None.
        auto_size (bool): if True the row will make its size fit its content otherwise it will take the space available.

    Returns:
        dbc.Row
    """
    kwargs = {
        'className': (
            f"{get_margin_class(margin, margin_top, margin_bottom, margin_left, margin_right)} "
            f"{get_padding_class(padding, padding_top, padding_bottom, padding_left, padding_right)} "
            f"{'row-auto justify-items-start' if auto_size else 'justify-items-stretch'} d-flex align-items-center"
        ),
        **kwargs
    }
    return dbc.Row(children, **kwargs)


def col(
        children: Union[list, str, Component],
        margin: int = 1,
        margin_right: Optional[int] = None,
        margin_left: Optional[int] = None,
        margin_top: Optional[int] = None,
        margin_bottom: Optional[int] = None,
        padding: int = 0,
        padding_right: int = None,
        padding_left: int = None,
        padding_top: int = None,
        padding_bottom: int = None,
        auto_size: bool = True,
        **kwargs
) -> dbc.Col:
    """Col component.

    The margin and padding is specified in bootstrap fashion, 0-5. (0 - 3rem)

    Args:
        children (list, optional): Children of the container. Defaults to None.
        margin (int, optional): Margin will be overridden if any specific margin is specified. Defaults to 1.
        margin_right (int, optional): Margin left. Defaults to None.
        margin_left (int, optional): Margin right. Defaults to None.
        margin_top (int, optional): Margin top. Defaults to None.
        margin_bottom (int, optional): Margin bottom. Defaults to None.
        padding (int, optional): Padding. Defaults to 0.
        padding_right (int, optional): Padding right. Defaults to None.
        padding_left (int, optional): Padding left. Defaults to None.
        padding_top (int, optional): Padding top. Defaults to None.
        padding_bottom (int, optional): Padding bottom. Defaults to None.
        auto_size (bool): if True the col will make its size fit its content otherwise it will take the space available.

    Returns:
        dbc.Col
    """
    kwargs = {
        'className': (
            f"{get_margin_class(margin, margin_top, margin_bottom, margin_left, margin_right)} "
            f"{get_padding_class(padding, padding_top, padding_bottom, padding_left, padding_right)} "
            f"{'col-auto align-items-start' if auto_size else 'align-items-stretch'} d-flex flex-column"
        ),
        **kwargs
    }
    return dbc.Col(children, **kwargs)


def div(children: Optional[Union[list, str, int, float]] = None, id: str = None, hidden: bool = False):
    """Wrapper for html.Div"""
    kwargs = {k: v for k, v in locals().items() if v is not None}
    return html.Div(**kwargs)
