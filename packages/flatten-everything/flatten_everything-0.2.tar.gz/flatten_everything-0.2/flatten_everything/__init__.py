class ProtectedTuple(tuple):
    pass


class ProtectedList(list):
    pass


class ProtectedDict(dict):
    pass


class ProtectedSet(set):
    pass


def flatt_dict(
    v,
    forbidden=(list, tuple, set, frozenset),
    allowed=(
        str,
        int,
        float,
        complex,
        bool,
        bytes,
        type(None),
        ProtectedTuple,
        ProtectedList,
        ProtectedDict,
        ProtectedSet,
    ),
):

    if isinstance(v, dict):
        for k, v2 in v.items():
            yield from flatt_dict(v2, forbidden=forbidden, allowed=allowed)
    elif isinstance(v, forbidden):
        for v2 in v:
            if isinstance(v2, allowed):
                yield v2
            else:
                yield from flatten_everything(v2, forbidden=forbidden, allowed=allowed)
    elif isinstance(v, allowed):
        yield v
    else:
        try:
            for v2 in v:
                try:
                    if isinstance(v2, allowed):
                        yield v2
                    else:
                        yield from flatt_dict(v2, forbidden=forbidden, allowed=allowed)
                except Exception:
                    yield v2
        except Exception:

            yield v


def flatten_everything(
    item,
    forbidden=(list, tuple, set, frozenset),
    allowed=(
        str,
        int,
        float,
        complex,
        bool,
        bytes,
        type(None),
        ProtectedTuple,
        ProtectedList,
        ProtectedDict,
        ProtectedSet,
    ),
    dict_variation=(
        "collections.defaultdict",
        "collections.UserDict",
        "collections.OrderedDict",
    ),
):

    if isinstance(item, allowed):
        yield item
    elif isinstance(item, forbidden):
        for xaa in item:
            try:
                yield from flatten_everything(
                    xaa,
                    forbidden=forbidden,
                    allowed=allowed,
                    dict_variation=dict_variation,
                )
            except Exception:

                yield xaa
    elif isinstance(item, dict):

        yield from flatt_dict(item, forbidden=forbidden, allowed=allowed)
    elif str(type(item)) in dict_variation:
        yield from flatt_dict(dict(item), forbidden=forbidden, allowed=allowed)

    elif "DataFrame" in str(type(item)):

        yield from flatt_dict(
            item.copy().to_dict(), forbidden=forbidden, allowed=allowed
        )

    else:
        try:
            for ini2, xaa in enumerate(item):
                try:
                    if isinstance(xaa, dict):

                        yield from flatt_dict(
                            item, forbidden=forbidden, allowed=allowed
                        )
                    elif isinstance(xaa, allowed):
                        yield xaa
                    else:
                        yield from flatten_everything(
                            xaa,
                            forbidden=forbidden,
                            allowed=allowed,
                            dict_variation=dict_variation,
                        )
                except Exception:

                    yield from flatten_everything(
                        xaa,
                        forbidden=forbidden,
                        allowed=allowed,
                        dict_variation=dict_variation,
                    )
        except Exception:

            yield item

