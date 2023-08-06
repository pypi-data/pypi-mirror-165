async def get(hub, ctx, name=None, resource_id=None):
    return {
        "result": True,
        "comment": None,
        "ret": {"resource_id": resource_id, "name": name},
    }
