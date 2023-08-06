# An exec module that can run states


async def run(
    hub, path: str, name: str = None, acct_profile: str = None, *args, **kwargs
):
    """
    Run a state module from the CLI

    .. code-block:: bash

        $ idem exec state.run time.sleep duration=1 --output=json
    """
    ctx = await hub.idem.acct.ctx(
        f"states.{path}",
        acct_profile=acct_profile or hub.OPT.idem.get("acct_profile"),
        acct_key=hub.OPT.acct.get("acct_key"),
        acct_file=hub.OPT.acct.get("acct_file"),
    )

    ret = await hub.pop.loop.unwrap(hub.states[path](ctx, name=name, *args, **kwargs))

    return {"result": ret["result"], "comment": ret["comment"], "ret": ret["new_state"]}
