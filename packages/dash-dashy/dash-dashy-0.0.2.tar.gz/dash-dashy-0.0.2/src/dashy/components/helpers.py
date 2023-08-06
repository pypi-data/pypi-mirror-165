def create_options(labels, values=None) -> list[dict[str, str]]:
    if values is not None:
        options = [
            {"label": label, "value": value} for label, value in zip(labels, values)
        ]
        return options

    options = []
    for label in labels:
        if not isinstance(label, str):
            raise ValueError(f"Labels must be strings was {type(label)}")
        options.append({"label": label, "value": value_from_label(label)})
    return options


def value_from_label(label):
    return label.lower().replace(" ", "-").replace("/", "-")


def get_margin_class(
    margin: int,
    margin_top: int,
    margin_bottom: int,
    margin_left: int,
    margin_right: int,
) -> str:
    """
    Create the bootstrap margin class(es). If any side is specified
    """
    margins = [margin_top, margin_bottom, margin_left, margin_right]
    return f"m-{margin} " + " ".join(
        [f"{k}-{v}" for k, v in zip(["mt", "mb", "ms", "me"], margins) if v is not None]
    )


def get_padding_class(
    padding: int,
    padding_top: int,
    padding_bottom: int,
    padding_left: int,
    padding_right: int,
) -> str:
    """
    Create the bootstrap padding class(es). If any side is specified
    """
    paddings = [padding_top, padding_bottom, padding_left, padding_right]
    return f"p-{padding} " + " ".join(
        [
            f"{k}-{v}"
            for k, v in zip(["pt", "pb", "ps", "pe"], paddings)
            if v is not None
        ]
    )
