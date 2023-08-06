import base64
import io
import datetime

import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd

from .layout import col, div, row
from .table import table


def upload(
    id: str, multiple: bool = False, max_size: int = -1, min_size: int = 0
) -> dbc.Col:
    """Upload component to upload and use files.

    Args:
        id (str): Iof the component
        multiple (bool, optional): If multiple files should be able to be uploaded. Defaults to False.
        max_size (int, optional): Max file size int bytes. Defaults to -1.
        min_size (int, optional): Min file size in bytes. Defaults to 0.
    """
    style = {
        "height": "60px",
        "lineHeight": "60px",
        "borderWidth": "1px",
        "borderStyle": "dashed",
        "borderRadius": "5px",
        "textAlign": "center",
    }

    children = html.Div(["Drag and Drop or ", html.A("Select Files")])

    return col(
        [
            row(
                dcc.Upload(
                    id=id,
                    children=children,
                    style=style,
                    multiple=multiple,
                    max_size=max_size,
                    min_size=min_size,
                ),
                margin=0,
            )
        ],
        auto_size=False,
        margin=0,
    )


def upload_and_show(
    id: str, app, multiple: bool = False, max_size: int = -1, min_size: int = 0
) -> dbc.Col:
    """Upload component that also generates a table when a csv or excel file is uploaded

    Args:
        id (str): Iof the component
        app (DashyApp): The Dashy app. Needed in order to create the callback generating the table
        multiple (bool, optional): If multiple files should be able to be uploaded. Defaults to False.
        max_size (int, optional): Max file size int bytes. Defaults to -1.
        min_size (int, optional): Min file size in bytes. Defaults to 0.
    """
    # id of the output element that will hold the table
    output_id = f"{id}-output"

    # callback to generate the table showing the uploaded data
    @app.cb(
        inputs=(id, "contents"),
        outputs=(output_id, "children"),
        states=[(id, "filename"), (id, "last_modified")],
    )
    def update_output(list_of_contents, list_of_names, list_of_dates):
        if list_of_contents is not None:

            if not isinstance(list_of_contents, list):
                list_of_contents = [list_of_contents]
            if not isinstance(list_of_names, list):
                list_of_names = [list_of_names]
            if not isinstance(list_of_dates, list):
                list_of_dates = [list_of_dates]

            children = [
                _generate_table(n, d, _parse_csv(c, n), table_id=f"{id}-table")
                for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
            ]
            return children

    upload_comp = upload(id=id, multiple=multiple, max_size=max_size, min_size=min_size)
    upload_comp.children.append(row(div(id=output_id)))
    return upload_comp


def _generate_table(filename, file_date, df, table_id: str):
    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(file_date)),
            table(data=df, id=table_id),
        ]
    )


def _parse_csv(contents, filename) -> pd.DataFrame:
    """Parse and read the csv or xls into a dataframe"""
    _content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            raise ValueError("Can only parse CSV or Excel files")
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return df
