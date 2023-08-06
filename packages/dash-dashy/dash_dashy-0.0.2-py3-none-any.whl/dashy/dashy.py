import logging
from functools import wraps

import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
from dash_bootstrap_components import themes
import plotly.graph_objs as go


logging.basicConfig(format="%(levelname)s %(asctime)-15s %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def create_app(name: str, layout: list = None, theme=themes.FLATLY, **kwargs):
    """
    Create an dashy app

    Args:
        name: Name of the app
        layout: UI layout to be display by the app
        theme: UI Theme to be used
    Returns:
        DashyApp
    """

    app = DashyApp(
        theme=theme, layout=layout, name=name, external_stylesheets=[theme], **kwargs
    )

    return app


class DashyApp(dash.Dash):
    """
    Small wrapper class for dash.Dash class
    """

    def __init__(self, theme, layout: list, **kwargs):
        super().__init__(**kwargs)

        # self.theme = theme()
        self.hidden_div_count = 0
        self.layout = html.Div(layout)

    def launch(self, debug=False, **kwargs):

        # Generate css files for theme
        # self.theme.compile()

        # Start server
        self.run_server(debug=debug, **kwargs)

    def cb(self, inputs, outputs=None, states=None):
        """
        wrapper function for the original Dash callback function.
        This in order to make it more flexible and also take away some limitations.
        """

        # Handle outputs
        if outputs is None:
            self.hidden_div_count += 1
            output_id = f"auto-hidden-{self.hidden_div_count}"
            output_element = "children"
            self.layout.children.append(
                html.Div(id=output_id, style={"display": "none"})
            )
            outputs = [(output_id, output_element)]
        elif not isinstance(outputs, tuple) and not isinstance(outputs, list):
            raise ValueError("'inputs' needs to be a tuple or a list of tuples")
        elif isinstance(outputs, tuple):
            outputs = [outputs]

        output_list = []
        for o in outputs:
            if not isinstance(o, tuple):
                raise ValueError(f"an input must be tuple was: {type(o)}")
            if len(o) != 2:
                raise ValueError("an input must contain exactly 2 strings")
            output_id, output_element = o
            output_list.append(Output(output_id, output_element))
        if len(output_list) == 1:
            output_list = output_list[0]

        # Handle inputs
        if not isinstance(inputs, tuple) and not isinstance(inputs, list):
            raise ValueError("'inputs' needs to be a tuple or a list of tuples")
        elif isinstance(inputs, tuple):
            inputs = [inputs]

        input_list = []
        for i in inputs:
            if not isinstance(i, tuple):
                raise ValueError(f"an input must be tuple was: {type(i)}")
            if len(i) != 2:
                raise ValueError("an input must contain exactly 2 strings")

            input_id, input_element = i
            input_list.append(Input(input_id, input_element))

        # handle states
        state_list = []
        if states is not None:

            if not isinstance(states, tuple) and not isinstance(states, list):
                raise ValueError("'states' needs to be a tuple or a list of tuples")
            elif isinstance(states, tuple):
                states = [states]

            for s in states:
                if not isinstance(s, tuple):
                    raise ValueError(f"a state must be tuple was: {type(s)}")
                if len(s) != 2:
                    raise ValueError("a state must contain exactly 2 strings")
                state_id, state_element = s
                state_list.append(State(state_id, state_element))

        def decorator_callback(func):
            # Create real Dash callback
            @self.callback(output=output_list, inputs=input_list, state=state_list)
            def dash_update(*args, **kwargs):
                components = func(*args, **kwargs)
                # components = self.apply_theme(components)
                return components

            # For completeness
            wraps(func)

            def wrapper():
                return None

            return wrapper

        return decorator_callback

    def apply_theme(self, components):
        """
        Recursively apply theme to components

        Args:
            components: list of components

        Returns:
            components or None
        """
        if components is None:
            return

        if isinstance(components, go.Figure):
            self._apply_to_figure(components)

        if isinstance(components, (list, tuple)):
            for comp in components:
                if isinstance(comp, dcc.Graph):
                    # Add theme colors to layout
                    self._apply_to_figure(comp.figure)
                if isinstance(comp, go.Figure):
                    self._apply_to_figure(comp)

                elif hasattr(comp, "children"):
                    self.apply_theme(comp.children)
        return components

    def _apply_to_figure(self, figure):
        figure.layout.paper_bgcolor = self.theme.white
        figure.layout.plot_bgcolor = self.theme.white

        figure.layout.font["color"] = self.theme.black

        figure.layout.xaxis["zerolinecolor"] = self.theme.background_color
        figure.layout.yaxis["zerolinecolor"] = self.theme.background_color

        figure.layout.xaxis["gridcolor"] = self.theme.background_color
        figure.layout.yaxis["gridcolor"] = self.theme.background_color

        margin = figure.layout.margin
        default_margin = {
            "l": margin.l if margin.l is not None else 40,
            "r": margin.r if margin.r is not None else 40,
            "b": margin.b if margin.b is not None else 40,
            "t": margin.t if margin.t is not None else 70,
            "pad": margin.pad if margin.pad is not None else 0,
        }
        figure.layout.margin = default_margin

        title_text = figure.layout.title["text"]
        if title_text is not None:
            figure.layout.title = dict(
                text=title_text, x=0.5, y=1.0, pad=dict(t=30), font=dict(size=18)
            )
