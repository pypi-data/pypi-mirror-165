async def pre_present(hub, ctx):
    print(1)
    kwargs = ctx.get_arguments()
    func_ctx = kwargs.get("ctx")

    # Try to get the resource using known kwargs
    path = ctx.ref.split("states.", maxsplit=1)[1]
    resource = await hub.exec[path].get(
        ctx=func_ctx, name=kwargs["name"], resource_id=kwargs["resource_id"]
    )

    # Resource couldn't be found
    if not resource:
        # Remove the resource id so that a new resource gets created in the present function
        kwargs["resource_id"] = None
    else:
        func_ctx["old_state"] = resource
