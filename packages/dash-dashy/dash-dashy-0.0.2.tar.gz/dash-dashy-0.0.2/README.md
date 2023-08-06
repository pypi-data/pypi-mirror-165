
<h1 align="center">
    Dashy
</h1>

<h4 align="center">A small framework built on top of <a href="https://github.com/plotly/dash" target="_blank">Plotly Dash</a> and <a href="https://github.com/facultyai/dash-bootstrap-components" target="_blank">Dash Bootstrap Components</a> intended to make it easy and quick to build dashboards without having to think about all the small details.</h4>

<p align="center">
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/wynss/dashy/CI">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/dash-dashy">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/dash-dashy">
    <img alt="GitHub" src="https://img.shields.io/github/license/wynss/dashy">
</p>

<p align="center">
  <a href="#install">How To Use</a> |
  <a href="#key-features">Key Features</a> |
  <a href="#future">Future</a> |
  <a href="#credits">Credits</a> |
  <a href="#license">License</a>
</p>

<!-- ![screenshot]() -->

## Install
```bash
pip install dash-dashy
```


## Key Features

### Simpler callbacks
Dash callbacks usually looks like
```python
@app.callback(
  Output('container', 'children'),
  Input('btn-1', 'n_clicks'),
  Input('btn-2', 'n_clicks'),
  Input('btn-3', 'n_clicks'),
  State('dropdown', 'value'))
def some_callback_func(...):
  ...
```
In order to make callbacks less verbose Dashy apps has its own callback decorator using only list and tuples as arguments. The example above reduces to
```python
@app.cb(
  inputs=[('btn-1', 'n_clicks'), ('btn-2', 'n_clicks'), ('btn-3', 'n_clicks')],
  outputs=('container', 'children'),
  states=('dropdown', 'value'))
def some_callback_func(...):
  ...
```
Dashy also assume an implicit order of the decorator arguments which is, inputs -> outputs -> states. This is handy for simple callbacks like
```python
# callback taking buttons clicks as input and outputs 'children' to 'container'
@app.cb(('btn-1', 'n_clicks'), ('container', 'children'))
def some_callback_func(...):
  ...
```
Dashy callbacks also does not require an explicit output.
```python
# do something when the button is clicked
@app.cb(('btn-1', 'n_clicks'))
def some_callback_func(...):
  ...
```

### High level function components
All components in Dashy are functions, import what you need or everything
```python
# import individual components
from dashy.components import navbar, button, graph, dropdown
# or
import dashy.components as dc
```
### Layout
Dashy utilizes bootstrap's grid system and tries to handle as much of the layout as possible while still making the dashboards look good. Import the `container` `row` and `col` components and build your layout.
```python
from dashy.components import container, row, col

layout = container([
  row([
    # your components
  ]),
  col([
    # more components
  ])
])
```

### Complete app example
Building an app with a navbar, tabs and a callback to switch tabs becomes
```python
from dashy import create_app
from dashy.components import navbar, tabs, div


app = create_app(__name__, layout=[
    navbar('My App', dark=True),
    tabs(id='tabs', labels=['Tab1', 'Tab2', 'Tab3'], content_id='tab-content')
])


@app.cb(('tabs', 'active_tab'), ('tab-content', 'children'))
def switch_tabs(tab_id: str):
    return div(f'Hello from {tab_id}')


if __name__ == "__main__":
    app.launch()
```


## Future
- [ ] Integrate all components with bootstrap themes
- [ ] Dashboard templates

## Credits

This software uses the following awesome open source packages:

- [Plotly Dash](https://github.com/plotly/dash)
- [Dash Bootstrap Components](https://github.com/facultyai/dash-bootstrap-components)

## License

MIT
