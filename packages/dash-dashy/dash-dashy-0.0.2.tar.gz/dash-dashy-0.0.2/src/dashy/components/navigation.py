from typing import List, Optional, Union

import dash_bootstrap_components as dbc
from dash import html, dcc

from .attributes import Color
from .helpers import value_from_label
from .layout import container


def navbar(
    title: str,
    fluid=True,
    color: Color = Color.PRIMARY,
    dark=False,
    links: List[str] = None,
) -> dbc.NavbarSimple:
    """A Navbar

    Args:
        title: Title of the Navbar
        fluid: If True the contents of the navbar will fill the available horizontal space. Defaults to True.
        color: Color of the navbar. Defaults to Color.PRIMARY.
        dark: If True the text in the children of the Navbar to use light colors for contrast/visibility.
                               Defaults to False.
        links: List of links to add. Defaults to None.
    """
    children = []
    if links is not None:
        for link in links:
            children.append(
                dbc.NavItem(
                    dbc.NavLink(
                        link,
                        id=value_from_label(link),
                        href=f"/{value_from_label(link)}",
                        active="exact",
                    )
                )
            )

    return dbc.NavbarSimple(
        children, brand=title, fluid=fluid, dark=dark, color=color.value
    )


def sidebar(
    title: str, id: str, links: Optional[list[str]], text: Optional[str]
) -> html.Div:
    """A sidebar.

    The urls are built by converting the link string to kebab-case. So for example 'My Analysis' yields the url '/my-analysis'.

    Args:
        title: Title fo the sidebar
        id: Id of the sidebar
        links: Links that will be available. These will be mapped to urls to be used for callbacks.
        text: Description text that will be displayed
    """

    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            html.H2(title),
            html.Hr(),
            html.P(text, className="lead") if text else None,
            dbc.Nav(
                [
                    dbc.NavLink(link, href=f"/{value_from_label(link)}", active="exact")
                    for link in links
                ],
                vertical=True,
                pills=True,
            )
            if links
            else None,
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id=f"{id}-content", style=CONTENT_STYLE)

    return html.Div([dcc.Location(id=f"{id}-url"), sidebar, content])


def tabs(
    labels: List[str],
    id: str,
    content_id: Optional[str],
    tab_ids: Optional[List[str]] = None,
    active_tab: Optional[Union[str, int]] = None,
) -> dbc.Container:
    """Create a set of tabs to navigate between different contents.

    Args:
        labels: Tab labels, the text that will be shown for each tab.
        id: Id of the tabs
        content_id : Id of the content element that will be populated when switching tab.
        tab_ids: Ids for each tab, will be created if not passed. Defaults to None.
        active_tab: Sets the active tab, by index or label. Defaults to None.

    Returns:
        dbc.Container: Containing the tabs
    """
    if tab_ids is None:
        tab_ids = [label.lower().replace(" ", "-") for label in labels]

    tab_element_kwargs = {
        "children": [
            dbc.Tab(label=label, tab_id=tab_id)
            for label, tab_id in zip(labels, tab_ids)
        ],
        "id": id,
    }

    if active_tab is not None:
        if isinstance(active_tab, int):
            active_tab = tab_ids[active_tab]
        tab_element_kwargs["active_tab"] = active_tab

    tab_element = dbc.Tabs(**tab_element_kwargs)

    if content_id is None:
        content_id = "tab-content"

    return container(
        id="tab-container",
        children=[tab_element, container(id=content_id, fluid=True)],
        fluid=True,
    )
