from typing import Optional
from enum import Enum

from dash import dash_table
import pandas as pd


class Selectable(Enum):
    SINGLE = "single"
    MULTI = "multi"
    FALSE = False


class SortAction(Enum):
    NONE = "none"
    NATIVE = "native"


class FilterAction(Enum):
    NONE = "none"
    NATIVE = "native"


class SortMode(Enum):
    SINGLE = "single"
    MULTI = "multi"


def table(
    data: pd.DataFrame,
    id: str,
    columns: Optional[list[dict]] = None,
    page_size: int = 10,
    row_selectable: Selectable = Selectable.FALSE,
    col_selectable: Selectable = Selectable.FALSE,
    cell_selectable: bool = False,
    sort_action: SortAction = SortAction.NATIVE,
    sort_mode: SortMode = SortMode.SINGLE,
    filter_action: FilterAction = FilterAction.NONE,
):
    """A Data Table.

    Args:
        data (pd.DataFrame): Data frame that should be displayed in the table
        id (str): Id of the table
        columns (Optional[list[dict]], optional): Columns of the table. Will be generated from the dataframe if not provided.
        page_size (int, optional): Max columns per page. Defaults to 10.
        row_selectable (Selectable, optional): If rows should be selectable. Defaults to Selectable.FALSE.
        col_selectable (Selectable, optional): If cols should be selectable. Defaults to Selectable.FALSE.
        cell_selectable (bool, optional): If cells should be selectable. Defaults to False.
        sort_action (SortAction, optional): If sorting should be available. Defaults to SortAction.NATIVE.
        sort_mode (SortMode, optional): If single or multisort should be performed on the columns. Defaults to SortMode.SINGLE.
        filter_action (FilterAction, optional): If filtering should be available. Defaults to FilterAction.NONE.
    """
    if columns is None:
        columns = [{"name": i, "id": i} for i in data.columns]

    data = data.to_dict("records")

    return dash_table.DataTable(
        data=data,
        columns=columns,
        id=id,
        page_size=page_size,
        filter_action=filter_action.value,
        sort_action=sort_action.value,
        sort_mode=sort_mode.value,
        row_selectable=row_selectable.value,
        column_selectable=col_selectable.value,
        cell_selectable=cell_selectable,
    )
