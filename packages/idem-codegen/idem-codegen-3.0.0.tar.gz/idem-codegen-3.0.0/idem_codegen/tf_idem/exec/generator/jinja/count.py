import re

from idem_codegen.tf_idem.tool.utils import replace_pattern
from idem_codegen.tf_idem.tool.utils import var_pattern_unprocessed1
from idem_codegen.tf_idem.tool.utils import var_pattern_unprocessed2


def get_count(
    hub, conditional_pattern, count_dict, idem_state_list, item, terraform_resource
):
    if not terraform_resource:
        return count_dict, idem_state_list
    for tf_resource_value in terraform_resource.values():
        for tf_resource_parameter in tf_resource_value.values():
            try:
                if "count" not in tf_resource_parameter:
                    return count_dict, idem_state_list
                idem_state_list.append(item.rsplit("-", 1)[0])
                if conditional_pattern.search(str(tf_resource_parameter.get("count"))):
                    count_dict["count_true_condition"] = int(
                        str(tf_resource_parameter.get("count"))
                        .split("?")[1]
                        .split(":")[0]
                    )
                    count_false_condition = (
                        str(tf_resource_parameter.get("count"))
                        .split("?")[1]
                        .split(":")[1]
                    )
                    if "}" in count_false_condition:
                        count_false_condition = int(
                            count_false_condition.replace("}", "")
                        )
                    count_dict["count_false_condition"] = count_false_condition
                    count_statement = str(tf_resource_parameter.get("count")).split(
                        "?"
                    )[0]
                    while re.search(var_pattern_unprocessed1, count_statement):
                        count_condition_parameterized = re.sub(
                            var_pattern_unprocessed1,
                            hub.tf_idem.tool.generator.jinja.utils.convert_var_to_param,
                            count_statement,
                        )
                        count_statement = count_condition_parameterized
                    while re.search(var_pattern_unprocessed2, count_statement):
                        count_condition_parameterized = re.sub(
                            var_pattern_unprocessed2,
                            hub.tf_idem.tool.generator.jinja.utils.convert_only_var_to_param,
                            count_statement,
                        )
                        count_statement = count_condition_parameterized
                    count_dict["count_statement"] = count_statement
                else:
                    count_dict["count_true_condition"] = tf_resource_parameter.get(
                        "count"
                    )
            except Exception as e:
                print(e)
    return count_dict, idem_state_list


def get_data_count_dict(
    hub, conditional_pattern, count_dict, resource_attribute, list_of_comments
):
    if "count" in resource_attribute["kwargs"]:
        if resource_attribute["kwargs"]["count"]:
            if conditional_pattern.search(str(resource_attribute["kwargs"]["count"])):
                count_dict["count_true_condition"] = int(
                    str(resource_attribute["kwargs"]["count"])
                    .split("?")[1]
                    .split(":")[0]
                )
                count_statement = str(resource_attribute["kwargs"]["count"]).split("?")[
                    0
                ]
                while re.search(var_pattern_unprocessed1, count_statement):
                    count_condition_parameterized = re.sub(
                        var_pattern_unprocessed1,
                        hub.tf_idem.tool.generator.jinja.utils.convert_var_to_param,
                        count_statement,
                    )
                    count_statement = count_condition_parameterized
                while re.search(var_pattern_unprocessed2, count_statement):
                    count_condition_parameterized = re.sub(
                        var_pattern_unprocessed2,
                        hub.tf_idem.tool.generator.jinja.utils.convert_only_var_to_param,
                        count_statement,
                    )
                    count_statement = count_condition_parameterized
                count_dict["count_statement"] = count_statement
            else:
                count_dict["count_true_condition"] = resource_attribute["kwargs"][
                    "count"
                ]
            del resource_attribute["kwargs"]["count"]
    if replace_pattern.search(str(resource_attribute)):
        list_of_comments.append(
            hub.tf_idem.tool.utils.REPLACE_COMMENT.format(resource="kwargs")
        )
