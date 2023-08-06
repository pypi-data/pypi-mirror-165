"""Utilities."""


import ast

from flet.control import Control


STATE_ATTRS_REGISTRY = {
    "TextField": ["value"],
}


def checkif_import_friendly(src, raise_=True):
    last = ast.parse(src).body[-1]

    if isinstance(last, ast.Expr) and isinstance(last.value, ast.Call):
        if raise_:
            raise RuntimeError(
                f"Call `{ast.unparse(last)}` must be under an `if` statement")

    else:
        return True
    return False


def is_control_or_list_of(obj):
    return isinstance(obj, Control) or (
        isinstance(obj, list) and all(
            [isinstance(e, Control)
             for e in obj]
        )
    )


def inplace_recurse_controls(
        action, control: Control, seen: list = None) -> None:
    """Traverse a tree of controls and perform the action.

    NOTE: This function is intended to do in-place processing, so
    actions modifying the tree itself should be made with care.
    """
    if seen is None:
        seen = []

    if id(control) in seen:
        return
    seen.append(id(control))
    action(control)

    for attr in filter(
            is_control_or_list_of, vars(control).values()):
        if isinstance(attr, Control):
            inplace_recurse_controls(action, attr, seen)

        else:
            for entry in attr:
                inplace_recurse_controls(action, entry, seen)
    return
