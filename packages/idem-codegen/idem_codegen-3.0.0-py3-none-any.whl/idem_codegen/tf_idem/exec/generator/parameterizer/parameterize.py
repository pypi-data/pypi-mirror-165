import io
import json
import re

import ruamel
from jinja2 import Template


def merge_common_local_tags(hub, additional_tags):
    sls_tags_obj1 = io.StringIO()
    common_tags = f'{{% set x = params["local_tags"].copy() %}}'
    resource_tags = f"{{% do x.update({hub.tf_idem.tool.generator.parameterizer.utils.adjust_format_of_additional_tags(json.dumps(dict(additional_tags)))}) %}}"
    tags_variable = "{{x}}"

    tm = Template(
        " {{ common_tags }}\n        {{ resource_tags }}\n    {{ tags_variable }}"
    )
    tm.stream(
        common_tags=common_tags,
        resource_tags=resource_tags,
        tags_variable=tags_variable,
    ).dump(sls_tags_obj1)
    return ruamel.yaml.scalarstring.LiteralScalarString(sls_tags_obj1.getvalue())


def format_tf_tags(hub, resolved_value, attribute_value, parameterized_value):
    if re.search(r"\${merge\(", resolved_value):
        resolved_value = resolved_value.replace("'", '"')
        try:
            format_additional_tags_str = (
                resolved_value.replace("${merge(local.tags,,", "")
                .replace(",)}", "")
                .replace("{{ ", "")
                .replace("}} ", "")
                .replace(" {{", "")
                .replace(" }}", "")
                .replace("{{", "")
                .replace("}}", "")
                .replace("'", '"')
            )

            format_additional_tags_str_p = format_additional_tags_str.replace(
                '["', '[\\"'
            ).replace('"]', '\\"]')
            additional_tags = json.loads(format_additional_tags_str_p)

            parameterized_value = (
                hub.tf_idem.exec.generator.parameterizer.parameterize.merge_common_local_tags(
                    additional_tags
                )
                # f'{{{{ params.get("local_tags") + {hub.tf_idem.tool.generator.parameterizer.utils.adjust_format_of_additional_tags(json.dumps(dict(additional_tags)))}}}}}'
            )
        except Exception as e:
            print("Exception in loading additional tags :: ", e)
    elif "local." in resolved_value:
        json_loads = json.loads(json.dumps(resolved_value))
        if isinstance(attribute_value, list):
            parameterized_value = re.sub(
                r"\${local.[\w-]+}",
                hub.tf_idem.tool.generator.parameterizer.utils.convert_local_to_param,
                str(json_loads),
            )
        else:
            parameterized_value = re.sub(
                r"\${local.[\w-]+}",
                hub.tf_idem.tool.generator.parameterizer.utils.convert_local_to_param_dict,
                str(json_loads),
            )
    return parameterized_value


def format_tags(
    hub,
    resource_attribute_value,
    attribute_key,
    attribute_value,
    tf_resource_key,
    additional_function=None,
):
    if attribute_key == "tags" and isinstance(attribute_value, list):
        resource_attribute_value = (
            hub.tf_idem.tool.generator.parameterizer.utils.convert_tags_dict_list(
                resource_attribute_value
            )
        )
    return resource_attribute_value


def is_attr_value_in_variables(hub, idem_resource_val, complete_dict_of_variables):
    for attr_key, attribute_value in complete_dict_of_variables.items():
        if attribute_value == idem_resource_val:
            return attr_key
    return None
