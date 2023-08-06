"""
The sls resolver is used to gather sls files, render them and return the initial
phase 1 highdata. This involves translating sls references into file paths,
downloading those sls files and then rendering them.

Once an sls file is rendered the include statements are resolved as well.
"""
import copy
import re
from typing import List


def __init__(hub):
    hub.idem.resolve.HARD_FAIL = False


async def gather(
    hub, name: str, *sls, sources: List[str], params_processing: bool = False
):
    """
    Gather the named sls references
    """
    cfn = await hub.idem.resolve.get_blocks(name, sls, sources)
    if cfn:
        await hub.idem.resolve.render(name, params_processing)


async def get_blocks(hub, name: str, sls, sources: List[str]) -> bool:
    # Returns 'False' if the SLS file cannot be found
    for sls_ref in sls:
        cfn = None
        file_name = None
        try:
            file_name, cfn = await hub.idem.get.ref(name, sls_ref, sources)
        except Exception as e:
            hub.log.debug(f"{e.__class__.__name__}: {e}")
            if hub.idem.resolve.HARD_FAIL:
                raise
        if not cfn:
            msg = f"SLS ref '{sls_ref}' did not resolve to a file"
            hub.log.debug(msg)
            hub.idem.RUNS[name]["errors"].append(msg)
            return False

        blocks = hub.rend.init.blocks(fn=file_name, content=cfn)
        hub.idem.RUNS[name]["blocks"][sls_ref] = blocks
        hub.idem.RUNS[name]["sls_refs"][sls_ref] = file_name
        hub.idem.RUNS[name]["resolved"].add(sls_ref)

    return True


async def render(hub, name: str, params_processing: bool):
    """
    Pop the available blocks and render them if they have satisfied requisites
    """
    rendered = {}
    for sls_ref, blocks in copy.deepcopy(list(hub.idem.RUNS[name]["blocks"].items())):
        cfn = hub.idem.RUNS[name]["sls_refs"][sls_ref]
        for bname, block in blocks.items():
            clear = True
            for key, val in block.get("keys", {}).items():
                # TODO: This should be an additional render requisite plugin
                # subsystem, change it to a subsystem as soon as any new conditionals
                # are added!!
                clear = False
                if key == "require":
                    for tag, data in hub.idem.RUNS[name]["running"].items():
                        if data["name"] == val:
                            clear = True
                            break
                if clear:
                    continue
            if clear:
                state = await hub.rend.init.parse_bytes(
                    block,
                    hub.idem.RUNS[name]["render"],
                    hub.idem.RUNS[name]["params"],  # params
                )
                await hub.idem.resolve.introduce(
                    name, state, sls_ref, cfn, params_processing
                )
                rendered[sls_ref] = bname
    for sls_ref, bname in rendered.items():
        hub.idem.RUNS[name]["blocks"][sls_ref].pop(bname, None)


async def introduce(hub, name, state, sls_ref, cfn, params_processing: bool):
    """
    Introduce the raw state into the running dataset
    """
    if not isinstance(state, dict):
        hub.idem.RUNS[name]["errors"].append(
            f"SLS {sls_ref} is not formed as a dict but as a {type(state)}"
        )
        return
    if "include" in state:
        if not isinstance(state["include"], list):
            hub.idem.RUNS[name]["errors"].append(
                f'Include Declaration in SLS {sls_ref} is not formed as a list but as a {type(state["include"])}'
            )
        include = state.pop("include")
    else:
        include = []
    hub.idem.resolve.meta(name, state, sls_ref)
    hub.idem.resolve.extend(name, state, sls_ref)
    hub.idem.resolve.exclude(name, state, sls_ref)
    hub.idem.resolve.decls(name, state, sls_ref, params_processing)
    hub.idem.resolve.iorder(name, state)
    await hub.idem.resolve.includes(name, include, sls_ref, cfn)

    # If we are just doing parameter parsing and not doing state execution,
    # skip the next steps.
    if not params_processing:
        await hub.idem.event.put(
            profile="idem-high",
            body=state,
            tags={"type": "state-high-data", "ref": "idem.resolve.introduce"},
        )
        hub.idem.RUNS[name]["high"].update(state)


def iorder(hub, name, state):
    """
    Take a state and apply the iorder system
    """
    for id_ in state:
        for s_dec in state[id_]:
            if not isinstance(s_dec, str):
                # PyDSL OrderedDict?
                continue

            if not isinstance(state[id_], dict):
                # Include's or excludes as lists?
                continue
            if not isinstance(state[id_][s_dec], list):
                # Bad syntax, let the verify seq pick it up later on
                continue

            found = False
            if s_dec.startswith("_"):
                continue

            for arg in state[id_][s_dec]:
                if isinstance(arg, dict):
                    if len(arg) > 0:
                        if next(iter(arg)) == "order":
                            found = True
            if not found:
                if not isinstance(state[id_][s_dec], list):
                    # quite certainly a syntax error, managed elsewhere
                    continue
                state[id_][s_dec].append({"order": hub.idem.RUNS[name]["iorder"]})
                hub.idem.RUNS[name]["iorder"] += 1


def extend(hub, name, state, sls_ref):
    """
    Resolve the extend statement
    """
    if "extend" in state:
        ext = state.pop("extend")
        if not isinstance(ext, dict):
            hub.idem.RUNS[name]["errors"].append(
                f'Extension value in SLS "{sls_ref}" is not a dictionary'
            )
            return
        for id_ in ext:
            if not isinstance(ext[id_], dict):
                hub.idem.RUNS[name]["errors"].append(
                    f'Extension ID "{id_}" in SLS "{sls_ref}" is not a dictionary'
                )
                continue
            if "__sls__" not in ext[id_]:
                ext[id_]["__sls__"] = sls_ref
            # if '__env__' not in ext[id_]:
            #    ext[id_]['__env__'] = saltenv
            for key in list(ext[id_]):
                if key.startswith("_"):
                    continue
                if not isinstance(ext[id_][key], list):
                    continue
                if "." in key:
                    comps = key.split(".")
                    ext[id_][comps[0]] = ext[id_].pop(key)
                    ext[id_][comps[0]].append(comps[1])
        state.setdefault("__extend__", []).append(ext)


def meta(hub, name, state, sls_ref):
    if "META" in state:
        raw_meta = state.pop("META")
        hub.idem.RUNS[name]["meta"]["SLS"][sls_ref] = raw_meta
    for id_ in state:
        if isinstance(state[id_], dict):
            if "META" in state[id_]:
                ref = f"{sls_ref}.{id_}"
                raw_meta = state[id_].pop("META")
                hub.idem.RUNS[name]["meta"]["ID_DECS"][ref] = raw_meta


def exclude(hub, name, state, sls_ref):
    """
    Resolve any exclude statements
    """
    if "exclude" in state:
        exc = state.pop("exclude")
        if not isinstance(exc, list):
            hub.idem.RUNS[name]["errors"].append(
                f"Exclude Declaration in SLS {sls_ref} is not formed as a list"
            )
        state.setdefault("__exclude__", []).extend(exc)


def decls(hub, name, state, sls_ref, params_processing: bool):
    """
    Resolve and state formatting and data insertion
    """
    for id_ in state:
        if not isinstance(state[id_], dict):
            if id_ == "__extend__":
                continue
            if id_ == "__exclude__":
                continue

            # In case of params_processing being true, such as when we are doing
            # parameter processing only: we will just read the key and value pairs and add
            # to hub.idem.RUNS[name]["params"] dict. Then we can access the parameter value
            # as {{ params.get('foo') }}
            if params_processing and state[id_] is not None:
                hub.idem.RUNS[name]["params"][id_] = state[id_]
                continue

            if isinstance(state[id_], str):
                # Is this is a short state, it needs to be padded
                if "." in state[id_]:
                    comps = state[id_].split(".")
                    state_ref = ".".join(comps[:-1])
                    state[id_] = {"__sls__": sls_ref, state_ref: [comps[-1]]}
                    continue

            hub.idem.RUNS[name]["errors"].append(
                f"ID {id_} in SLS {sls_ref} is not a dictionary"
            )
            continue

        # This handles the parameter parsing when value is of type dict.
        # Similar to the case above where we handled non dict value types: here
        # we will just read the key and value pairs and add to
        # hub.idem.RUNS[name]["params"] dict. This will ensure we will be able to
        # access these objects like: {{ params.get('foo').get('bar') }}
        # In similar manner array elements can be accessed like:
        # {{ params['foo_array'][0] }}
        if params_processing:
            hub.idem.RUNS[name]["params"][id_] = state[id_]
            continue

        skeys = set()
        for key in list(state[id_]):
            if key.startswith("_"):
                continue
            if not isinstance(state[id_][key], list):
                continue
            if "." in key:
                comps = key.split(".")
                # Idem doesn't support state files such as:
                #
                #     /etc/redis/redis.conf:
                #       file.managed:
                #         - user: redis
                #         - group: redis
                #         - mode: 644
                #       file.comment:
                #           - regex: ^requirepass
                ref = ".".join(comps[:-1])
                if ref in skeys:
                    hub.idem.RUNS[name]["errors"].append(
                        f'ID "{id_}" in SLS "{sls_ref}" contains multiple state declarations of the same type'
                    )
                    continue
                state[id_][ref] = state[id_].pop(key)
                state[id_][ref].append(comps[-1])
                skeys.add(ref)
                continue
            skeys.add(key)
        if "__sls__" not in state[id_]:
            state[id_]["__sls__"] = sls_ref


async def includes(hub, name, include, sls_ref, cfn):
    """
    Parse through the includes and download not-yet-resolved includes
    """
    for inc_sls in include:
        if inc_sls.startswith("."):
            match = re.match(r"^(\.+)(.*)$", inc_sls)
            if match:
                levels, include = match.groups()
            else:
                hub.idem.RUNS[name]["errors"].append(
                    f'Badly formatted include {inc_sls} found in SLS "{sls_ref}"'
                )
                continue
            level_count = len(levels)
            p_comps = sls_ref.split(".")
            if cfn.endswith("/init.sls"):
                p_comps.append("init")
            if level_count > len(p_comps):
                hub.idem.RUNS[name]["errors"].append(
                    f'Attempted relative include of "{inc_sls}" within SLS {sls_ref} goes beyond top level package'
                )
                continue
            inc_sls = ".".join(p_comps[:-level_count] + [include])
        if inc_sls not in hub.idem.RUNS[name]["resolved"]:
            await hub.idem.resolve.gather(
                name, inc_sls, sources=hub.idem.RUNS[name]["sls_sources"]
            )
