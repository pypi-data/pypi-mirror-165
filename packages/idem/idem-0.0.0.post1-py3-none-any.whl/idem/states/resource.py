__contracts__ = ["recreate"]


async def present(hub, ctx, name: str, resource_id=None, **kwargs):
    if resource_id:
        current_state = ctx.old_state
    else:
        # Create a new resource by calling the APIs
        ret = {"resource_id": 1}

        # Use the resource id to get the state in a consistent way
        current_state = await hub.exec.resource.get(
            ctx=ctx, name=name, resource_id=ret["resource_id"]
        )

    # Update the resource as needed
    return {
        "old_state": ctx.old_state,
        "new_state": current_state,
        "result": True,
        "comment": None,
        "name": name,
    }


async def absent(hub, ctx, name: str, resource_id=None, **kwargs):
    ...


async def describe(hub, ctx):
    ...
