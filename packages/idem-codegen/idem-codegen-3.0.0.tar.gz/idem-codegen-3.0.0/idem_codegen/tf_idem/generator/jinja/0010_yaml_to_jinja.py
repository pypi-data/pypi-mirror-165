import io
import re
from collections import ChainMap
from typing import Any
from typing import Dict

import ruamel

from idem_codegen.idem_codegen.tool.utils import (
    separator,
)

__contracts__ = ["add_jinja"]

from idem_codegen.tf_idem.tool.utils import (
    ternary_operator_pattern,
    ternery_operator_pattern_in_jinja,
)

attributes_to_ignore = ["resource_id", "arn"]


def add_jinja(hub, sls_data: Dict[str, Any], sls_original_data: Dict[str, Any]):
    terraform_resource_map = hub.tf_idem.RUNS["TF_RESOURCE_MAP"]

    # If we do not have terraform_resource_map we cannot parameterize,
    # raise an error if it's not found in hub
    idem_state_list = []
    ch = "i"
    sls_data_count_obj = io.StringIO()
    count_dict = dict(
        count_true_condition=None, count_false_condition=None, count_statement=None
    )
    if not terraform_resource_map:
        hub.log.warning(
            "Not able to parameterize, Terraform resource map is not found in hub."
        )
        return sls_data
    for item in sls_data:
        list_of_comments = []
        # deleting the extra idem state based on count
        if len(idem_state_list) > 0:
            if item.rsplit("-", 1)[0] in idem_state_list:
                del sls_data[item]
                continue
        count_dict["count_true_condition"] = 1
        if not item.startswith("data."):
            resource_attributes = list(sls_data[item].values())[0]
            resource_type = list(sls_data[item].keys())[0].replace(".present", "")
            dict(ChainMap(*resource_attributes))

            if not sls_original_data.get(item):
                continue

            original_data_attributes = list(sls_original_data[item].values())[0]
            original_resource_id = dict(ChainMap(*original_data_attributes)).get(
                "resource_id"
            )
            # get terraform resource to look for parameters used
            terraform_resource = terraform_resource_map.get(
                f"{resource_type}{separator}{original_resource_id}"
            )
            if resource_type != "aws.ec2.security_group_rule":
                (
                    count_dict,
                    idem_state_list,
                ) = hub.tf_idem.exec.generator.jinja.count.get_count(
                    ternary_operator_pattern,
                    count_dict,
                    idem_state_list,
                    item,
                    terraform_resource,
                )

                for resource_attribute in resource_attributes:
                    for (
                        resource_attribute_key,
                        resource_attribute_value,
                    ) in resource_attribute.items():

                        if (
                            terraform_resource
                            and resource_attribute_key not in attributes_to_ignore
                        ):
                            (
                                tf_resource_value,
                                tf_resource_key,
                                is_attribute_different,
                            ) = hub.tf_idem.tool.utils.get_tf_equivalent_idem_attribute(
                                terraform_resource,
                                list(terraform_resource.keys())[0],
                                resource_attribute_key,
                            )
                            if (
                                isinstance(count_dict["count_true_condition"], int)
                                and count_dict["count_true_condition"] > 1
                            ):
                                if resource_attribute_key == "name":
                                    resource_attribute[
                                        resource_attribute_key
                                    ] = f'{{{{ params.get("{item[:-1]}"+({ch} | string))}}}}'
                                    continue
                                try:
                                    updated_resource_attribute = hub.idem_codegen.tool.nested_iterator.recursively_iterate_over_resource_attribute(
                                        resource_attribute_value,
                                        hub.tf_idem.tool.generator.jinja.utils.handle_count_index_in_argument_binding,
                                        ch=ch,
                                        resource_attribute=resource_attribute,
                                        resource_attribute_key=resource_attribute_key,
                                        tf_resource_value=tf_resource_value,
                                    )
                                    if updated_resource_attribute:
                                        resource_attribute[
                                            resource_attribute_key
                                        ] = updated_resource_attribute
                                except Exception:
                                    hub.log.warning("Invalid argument binding.")

                            # handle count.index from resource_attribute_value
                            hub.tf_idem.tool.generator.jinja.utils.handle_count_index(
                                ch,
                                resource_attribute,
                                resource_attribute_key,
                                resource_attribute_value,
                            )

                            # convert to if-else jinja template for ternery fields
                            if re.search(
                                ternery_operator_pattern_in_jinja,
                                str(resource_attribute[resource_attribute_key]),
                            ):
                                if_else_formatted_value = hub.tf_idem.tool.generator.jinja.utils.convert_attribute_value_to_if_else(
                                    resource_attribute_key,
                                    resource_attribute[resource_attribute_key],
                                )
                                if if_else_formatted_value:
                                    resource_attribute[
                                        resource_attribute_key
                                    ] = ruamel.yaml.scalarstring.LiteralScalarString(
                                        if_else_formatted_value
                                    )
                        elif resource_attribute_key == "resource_id":
                            if (
                                isinstance(count_dict["count_true_condition"], int)
                                and count_dict["count_true_condition"] > 1
                            ):
                                resource_attribute[
                                    resource_attribute_key
                                ] = f'{{{{ params.get("{item[:-1]}"+({ch} | string))}}}}'

                if terraform_resource:
                    list_of_comments.extend(
                        hub.tf_idem.exec.generator.jinja.comments.look_for_possible_improvements(
                            terraform_resource, resource_attributes
                        )
                    )
        else:
            resource_attributes = list(sls_data[item].values())[0]
            dict(ChainMap(*resource_attributes))
            for resource_attribute in resource_attributes:
                if "kwargs" not in resource_attribute:
                    continue
                hub.tf_idem.exec.generator.jinja.count.get_data_count_dict(
                    ternary_operator_pattern,
                    count_dict,
                    resource_attribute,
                    list_of_comments,
                )
        if (
            isinstance(count_dict["count_true_condition"], int)
            and count_dict["count_true_condition"] > 1
        ):
            hub.tf_idem.exec.generator.jinja.jinja_template.jinja_if_for_loop(
                ch, count_dict, item, list_of_comments, sls_data, sls_data_count_obj
            )
            ch = chr(ord(ch) + 1)
        elif (
            isinstance(count_dict["count_true_condition"], int)
            and count_dict["count_true_condition"] == 0
        ):
            hub.tf_idem.exec.generator.jinja.jinja_template.jinja_if_not_condition(
                count_dict, item, list_of_comments, sls_data, sls_data_count_obj
            )
        else:
            hub.tf_idem.exec.generator.jinja.jinja_template.jinja_if_condition(
                count_dict, item, list_of_comments, sls_data, sls_data_count_obj
            )

    return sls_data_count_obj
