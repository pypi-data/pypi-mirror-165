"""
Test States
===========

Provide test case states that enable easy testing of things to do with state
calls, e.g. running, calling, logging, output filtering etc.

.. code-block:: yaml

    always-passes-with-any-kwarg:
      test.nop:
        - name: foo
        - something: else
        - foo: bar

    always-passes:
      test.succeed_without_changes:
        - name: foo

    always-fails:
      test.fail_without_changes:
        - name: foo

    always-changes-and-succeeds:
      test.succeed_with_changes:
        - name: foo

    always-changes-and-fails:
      test.fail_with_changes:
        - name: foo
"""
import inspect
import threading

TREQ = {
    "treq": {
        "require": [
            "test.nop",
        ]
    },
    "unique": ["unique_op"],
}

UNIQUE_LOCK = threading.Lock()

__contracts__ = ["resource"]


def __init__(hub):
    hub.states.test_regex.ACCT = ["test_regex"]


def succeed_without_changes_regex(hub, ctx, name, **kwargs):
    """
    name
        A unique string.
    """
    ret = {
        "name": name,
        "changes": {},
        "result": True,
        "comment": "Success describe regular expression!",
    }
    return ret


def none_without_changes_regex(hub, ctx, name, **kwargs):
    """
    name
        A unique string.
    """
    ret = {
        "name": name,
        "changes": {},
        "result": None,
        "comment": "None describe regular expression!",
    }
    return ret


def present(
    hub,
    ctx,
    name: str,
    old_state=None,
    changes=None,
    new_state=None,
    result=True,
    force_save=None,
):
    """
    Return the previous old_state, if it's not specified in sls, and the given new_state.
    Raise an error on fail
    """
    if old_state is None:
        old_state = ctx.get("old_state")
    ret = {
        "name": name,
        "old_state": old_state,
        "new_state": new_state,
        "changes": changes,
        "result": result,
        "comment": None,
    }
    if force_save is not None:
        ret["force_save"] = force_save
    return ret


def absent(hub, ctx, name: str, new_state=None, result=True):
    old_state = ctx.get("old_state")
    return {
        "name": name,
        "old_state": old_state,
        "new_state": new_state,
        "result": result,
        "comment": None,
    }


async def describe(hub, ctx):
    """
    Get the functions
    """
    ret = {}
    for func in hub.states.test_regex:
        name = func.__name__
        if name in ("present", "absent", "succeed_with_arg_bind", "describe"):
            continue
        ref = f"test_regex.{name}"
        state_name = f"Description of regex {ref}"
        ret[state_name] = {ref: []}

        # Collect args
        for arg, p in func.signature.parameters.items():
            if arg in ("hub", "ctx", "kwargs"):
                continue
            elif arg == "name":
                ret[state_name][ref].append({arg: name})
            else:
                if p.default == inspect._empty:
                    ret[state_name][ref].append({arg: None})
                else:
                    ret[state_name][ref].append({arg: p.default})

    return ret
