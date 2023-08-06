from collections import ChainMap
from typing import Dict

"""
    This stage takes sls data and constructs unique keys for each entity.
"""

__contracts__ = ["compile"]


def set_resource_key(name_tag_value, updated_sls_data, resource):
    if name_tag_value in updated_sls_data:
        resource_index = name_tag_value.split("-")[-1]
        if resource_index.isnumeric():
            resource_index = int(resource_index) + 1
            name_tag_arr = name_tag_value.split("-")
            name_tag_arr.pop()
            name_tag_value = "-".join(name_tag_arr)
        else:
            resource_index = 0

        return set_resource_key(
            name_tag_value + "-" + str(resource_index), updated_sls_data, resource
        )

    updated_sls_data[name_tag_value] = resource
    return updated_sls_data


def stage(hub):
    sls_data = hub.discovery.RUNS["SLS_DATA"]
    updated_sls_data = {}
    for item in sls_data:
        name_tag_value = item
        resource_attributes = list(sls_data[item].values())[0]
        resource_map = dict(ChainMap(*resource_attributes))
        resource_type = list(sls_data[item].keys())[0].replace(".present", "")
        if "tags" in resource_map:
            tags = (
                resource_map.get("tags")
                if isinstance(resource_map.get("tags"), Dict)
                else hub.idem_codegen.tool.tag_utils.convert_tag_list_to_dict(
                    resource_map.get("tags")
                )
            )
            if tags.get("name"):
                name_tag_value = tags.get("name")
            elif tags.get("Name"):
                name_tag_value = tags.get("Name")
        updated_sls_data = set_resource_key(
            resource_type + "." + name_tag_value, updated_sls_data, sls_data[item]
        )
    hub.discovery.RUNS["SLS_DATA_WITH_KEYS"] = updated_sls_data
    hub.discovery.RUNS["SLS_DATA_WITH_KEYS_ORIGINAL"] = updated_sls_data
    return updated_sls_data
