"""Extract netlist from component port connectivity.

Assumes two ports are connected when they have same width, x, y

.. code:: yaml

    connections:
        - coupler,N0:bendLeft,W0
        - coupler,N1:bendRight,N0
        - bednLeft,N0:straight,W0
        - bendRight,N0:straight,E0

    ports:
        - coupler,E0
        - coupler,W0

"""

from typing import Any, Callable, Dict, List, Optional

import omegaconf

from gdsfactory.component import Component, ComponentReference
from gdsfactory.name import clean_name
from gdsfactory.pdk import get_layer
from gdsfactory.serialization import clean_value_json
from gdsfactory.snap import snap_to_grid
from gdsfactory.types import LayerSpec


def get_instance_name_from_alias(
    component: Component,
    reference: ComponentReference,
) -> str:
    """Returns the instance name from the label.

    If no label returns to instanceName_x_y

    Args:
        component: with labels.
        reference: reference that needs naming.
    """
    return reference.name


def get_instance_name_from_label(
    component: Component,
    reference: ComponentReference,
    layer_label: LayerSpec = "LABEL_INSTANCE",
) -> str:
    """Returns the instance name from the label.

    If no label returns to instanceName_x_y

    Args:
        component: with labels.
        reference: reference that needs naming.
        layer_label: ignores layer_label[1].
    """
    layer_label = get_layer(layer_label)

    x = snap_to_grid(reference.x)
    y = snap_to_grid(reference.y)
    labels = component.labels

    # default instance name follows component.aliases
    text = clean_name(f"{reference.parent.name}_{x}_{y}")

    # try to get the instance name from a label
    for label in labels:
        xl = snap_to_grid(label.position[0])
        yl = snap_to_grid(label.position[1])
        if x == xl and y == yl and label.layer == layer_label[0]:
            # print(label.text, xl, yl, x, y)
            return label.text

    return text


def get_netlist_yaml(
    component: Component,
    full_settings: bool = False,
    tolerance: int = 1,
    exclude_port_types: Optional[List] = None,
    **kwargs,
) -> Dict:
    """Returns instances, connections and placements yaml string content."""
    return omegaconf.OmegaConf.to_yaml(
        get_netlist(
            component=component,
            full_settings=full_settings,
            tolerance=tolerance,
            exclude_port_types=exclude_port_types,
            **kwargs,
        )
    )


def get_netlist(
    component: Component,
    full_settings: bool = False,
    tolerance: int = 1,
    exclude_port_types: Optional[List] = None,
    get_instance_name: Callable[..., str] = get_instance_name_from_alias,
) -> Dict[str, Any]:
    """From a component returns instances, connections and placements dict.

    Assumes that ports with same width, x, y are connected.

    Args:
        component: to extract netlist.
        full_settings: True returns all, false changed settings.
        layer_label: label to read instanceNames from (if any).
        tolerance: tolerance in nm to consider two ports connected.
        exclude_port_types: a list of port types to exclude from netlisting (optional)

    Returns:
        instances: Dict of instance name and settings.
        connections: Dict of Instance1Name,portName: Instace2Name,portName.
        placements: Dict of instance names and placements (x, y, rotation).
        port: Dict portName: ComponentName,port.
        name: name of component.

    """
    placements = {}
    instances = {}
    connections = {}
    top_ports = {}

    for reference in component.references:
        c = reference.parent
        origin = reference.origin
        x = float(snap_to_grid(origin[0]))
        y = float(snap_to_grid(origin[1]))
        reference_name = get_instance_name(
            component,
            reference,
        )

        instance = {}

        if c.info:
            instance.update(component=c.name, info=clean_value_json(c.info))

        # Prefer name from settings over c.name
        if c.settings:
            settings = c.settings.full if full_settings else c.settings.changed

            instance.update(
                component=getattr(c.settings, "function_name", c.name),
                settings=clean_value_json(settings),
            )

        instances[reference_name] = instance
        placements[reference_name] = dict(
            x=x,
            y=y,
            rotation=int(reference.rotation or 0),
            mirror=reference.x_reflection or 0,
        )

    # store where ports are located
    name2port = {}

    # Initialize a dict of port locations to Instance1Name,PortNames
    port_locations = {}

    # TOP level ports
    ports = component.get_ports(depth=0)
    top_ports_list = set()
    for port in ports:
        src = port.name
        name2port[src] = port
        top_ports_list.add(src)

    # lower level ports
    for reference in component.references:
        for port in reference.ports.values():
            reference_name = get_instance_name(
                component,
                reference,
            )
            src = f"{reference_name},{port.name}"
            name2port[src] = port

    # build connectivity port_locations = Dict[Tuple(x,y,width), set of portNames]
    for name, port in name2port.items():
        if exclude_port_types and port.port_type in exclude_port_types:
            continue
        xywt = [
            round(1000 * snap_to_grid(v, nm=tolerance))
            for v in (port.x, port.y, port.width)
        ] + [port.port_type]
        xywt = tuple(xywt)
        if xywt not in port_locations:
            port_locations[xywt] = set()
        port_locations[xywt].add(name)

    for xywt, names_set in port_locations.items():
        if len(names_set) > 2:
            x, y, w, t = xywt
            raise ValueError(
                "more than 2 connections at "
                f"{x / 1000, y / 1000} {list(names_set)}, width  = {w / 1000} "
            )
        if len(names_set) == 2:
            names_list = list(names_set)
            src = names_list[0]
            dst = names_list[1]
            if src in top_ports_list:
                top_ports[src] = dst
            elif dst in top_ports_list:
                top_ports[dst] = src
            else:
                src_dest = sorted([src, dst])
                connections[src_dest[0]] = src_dest[1]

    connections_sorted = {k: connections[k] for k in sorted(list(connections.keys()))}
    placements_sorted = {k: placements[k] for k in sorted(list(placements.keys()))}
    instances_sorted = {k: instances[k] for k in sorted(list(instances.keys()))}
    return dict(
        connections=connections_sorted,
        instances=instances_sorted,
        placements=placements_sorted,
        ports=top_ports,
        name=component.name,
    )


def get_netlist_recursive(
    component: Component,
    component_suffix: str = "",
    get_netlist_func: Callable = get_netlist,
    get_instance_name: Callable[..., str] = get_instance_name_from_alias,
    **kwargs,
) -> Dict[str, Any]:
    """Returns recursive netlist for a component and subcomponents.

    Args:
        component: to extract netlist.
        component_suffix: suffix to append to each component name.
            useful if to save and reload a back-annotated netlist.
        get_netlist_func: function to extract individual netlists.

    Keyword Args:
        full_settings: True returns all, false changed settings.
        layer_label: label to read instanceNames from (if any).
        tolerance: tolerance in nm to consider two ports connected.

    Returns:
        Dictionary of netlists, keyed by the name of each component.

    """
    all_netlists = {}

    # only components with references (subcomponents) warrant a netlist
    if component.references:
        netlist = get_netlist_func(component, **kwargs)
        all_netlists[f"{component.name}{component_suffix}"] = netlist

        # for each reference, expand the netlist
        for ref in component.references:
            rcell = ref.parent
            grandchildren = get_netlist_recursive(
                component=rcell,
                component_suffix=component_suffix,
                get_netlist_func=get_netlist_func,
                **kwargs,
            )
            all_netlists.update(grandchildren)
            if ref.ref_cell.references:
                inst_name = get_instance_name(component, ref)
                netlist_dict = {"component": f"{rcell.name}{component_suffix}"}
                if hasattr(rcell, "settings") and hasattr(rcell.settings, "full"):
                    netlist_dict.update(settings=rcell.settings.full)
                if hasattr(rcell, "info"):
                    netlist_dict.update(info=rcell.info)
                netlist["instances"][inst_name] = netlist_dict

    return all_netlists


def _demo_ring_single_array() -> None:
    import gdsfactory as gf

    c = gf.components.ring_single_array()
    c.get_netlist()


def _demo_mzi_lattice() -> None:
    import gdsfactory as gf

    coupler_lengths = [10, 20, 30, 40]
    coupler_gaps = [0.1, 0.2, 0.4, 0.5]
    delta_lengths = [10, 100, 200]

    c = gf.components.mzi_lattice(
        coupler_lengths=coupler_lengths,
        coupler_gaps=coupler_gaps,
        delta_lengths=delta_lengths,
    )
    c.get_netlist()
    print(c.get_netlist_yaml())


if __name__ == "__main__":
    # from pprint import pprint
    # from omegaconf import OmegaConf
    # import gdsfactory as gf
    # from gdsfactory.tests.test_component_from_yaml import sample_2x2_connections

    # c = gf.read.from_yaml(sample_2x2_connections)
    # c = gf.components.ring_single()
    # c.show(show_ports=True)
    # pprint(c.get_netlist())

    # n = c.get_netlist()
    # yaml_str = OmegaConf.to_yaml(n, sort_keys=True)
    # c2 = gf.read.from_yaml(yaml_str)
    # gf.show(c2)

    import gdsfactory as gf

    c = gf.components.mzi(delta_length=10)
    n = c.get_netlist()
    print("\n".join(n["instances"].keys()))

    c = gf.read.from_yaml(c.get_netlist())
    c.show()

    # coupler_lengths = [10, 20, 30, 40]
    # coupler_gaps = [0.1, 0.2, 0.4, 0.5]
    # delta_lengths = [10, 100, 200]

    # c = gf.components.mzi_lattice(
    #     coupler_lengths=coupler_lengths,
    #     coupler_gaps=coupler_gaps,
    #     delta_lengths=delta_lengths,
    # )
    # n = c.get_netlist_recursive()
