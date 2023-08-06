import io
import re

from jinja2 import Template

from idem_codegen.tf_idem.tool.utils import arg_reference_regex_pattern
from idem_codegen.tf_idem.tool.utils import count_index_pattern
from idem_codegen.tf_idem.tool.utils import params_variable_ends_with_count_pattern
from idem_codegen.tf_idem.tool.utils import ternery_operator_pattern_in_jinja
from idem_codegen.tf_idem.tool.utils import var_pattern_unprocessed1
from idem_codegen.tf_idem.tool.utils import var_pattern_unprocessed2


def handle_count_index(
    hub, ch, resource_attribute, resource_attribute_key, resource_attribute_value
):
    while re.search(count_index_pattern, str(resource_attribute_value)):
        res = re.search(count_index_pattern, str(resource_attribute_value))
        start_index = res.start()
        end_index = res.end()
        resource_attribute_value = (
            str(resource_attribute_value)[:start_index]
            + "+( ("
            + str(resource_attribute_value)[start_index + 2 :]
        )
        resource_attribute[resource_attribute_key] = (
            str(resource_attribute_value)[: end_index + 1]
            + ") | string)"
            + str(resource_attribute_value)[end_index + 2 :]
        )

    if isinstance(resource_attribute_value, str) and '-${count.index}"' in str(
        resource_attribute_value
    ):
        resource_attribute[resource_attribute_key] = resource_attribute_value.replace(
            '-${count.index}"', f'-"+({ch} | string)'
        )
        resource_attribute_value = resource_attribute_value.replace(
            '-${count.index}"', f'-"+({ch} | string)'
        )
    if isinstance(resource_attribute_value, str) and "-${count.index}" in str(
        resource_attribute_value
    ):
        resource_attribute[resource_attribute_key] = resource_attribute_value.replace(
            "-${count.index}", f'-"+({ch} | string)'
        )
        resource_attribute_value = resource_attribute_value.replace(
            "-${count.index}", f'-"+({ch} | string)'
        )
    if isinstance(resource_attribute_value, str) and "[count.index]" in str(
        resource_attribute_value
    ):
        resource_attribute[resource_attribute_key] = resource_attribute[
            resource_attribute_key
        ].replace("[count.index]", f"[{ch}]")
        resource_attribute_value = resource_attribute[resource_attribute_key].replace(
            "[count.index]", f"[{ch}]"
        )
    if isinstance(resource_attribute_value, str) and "count.index" in str(
        resource_attribute_value
    ):
        resource_attribute[resource_attribute_key] = resource_attribute[
            resource_attribute_key
        ].replace("count.index", f"{ch}")


def handle_count_index_in_argument_binding(
    hub,
    resource_attribute_value,
    ch,
    resource_attribute,
    resource_attribute_key,
    tf_resource_value,
):
    if hub.tf_idem.tool.utils.arg_reference_regex_pattern.search(
        resource_attribute_value
    ) and "count.index" in str(tf_resource_value):
        for arg_ref in arg_reference_regex_pattern.findall(resource_attribute_value):
            ref_chain_list = str(arg_ref[2 : arg_ref.index("}")]).split(":")

            if len(ref_chain_list) < 3:
                hub.log.warning("Argument binding is Invalid.")
                return
        resource_name = ref_chain_list[1]
        updated_resource_name_with_count = re.sub(r".$", f"{{{{{ch}}}}}", resource_name)
        return resource_attribute_value.replace(
            resource_name, updated_resource_name_with_count
        )


def convert_attribute_value_to_if_else(hub, attribute_key, attribute_value):
    while re.search(
        ternery_operator_pattern_in_jinja,
        str(attribute_value),
    ):
        while re.search(var_pattern_unprocessed1, str(attribute_value)):
            resolved_value = re.sub(
                var_pattern_unprocessed1,
                hub.tf_idem.tool.generator.jinja.utils.convert_var_to_param,
                attribute_value,
            )
            attribute_value = resolved_value
        while re.search(var_pattern_unprocessed2, str(attribute_value)):
            resolved_value = re.sub(
                var_pattern_unprocessed2,
                hub.tf_idem.tool.generator.jinja.utils.convert_only_var_to_param,
                attribute_value,
            )
            attribute_value = resolved_value

        converted_value = hub.idem_codegen.tool.nested_iterator.recursively_iterate_over_resource_attribute(
            attribute_value,
            convert_ternary_to_if_else,
            attribute_key=attribute_key,
            attribute_value=attribute_value,
        )
        return converted_value


def convert_ternary_to_if_else(
    resource_attribute_value, attribute_key, attribute_value
):
    sls_data_count_obj1 = io.StringIO()
    statement = resource_attribute_value

    test_expression = statement.split("?")[0]

    true_condition = statement.split("?")[1].split(" : ")[0]
    false_condition = statement.split("?")[1].split(" : ")[1]

    if true_condition[1] == '"' and true_condition[-1] == '"':
        true_condition = true_condition[2:-1]
    if false_condition[0] == '"' and false_condition[-1] == '"':
        false_condition = false_condition[2:-1]

    converted_true_expression = true_condition
    converted_false_expression = false_condition

    if_loop = f"{{% if {test_expression} %}}\n"
    if_start = if_loop.replace("{{ ", "").replace(" }}", "")
    else_start = "{% else %}\n"
    end_if = "{% endif %}"
    tm = Template(
        "{{ if_start }}- {{ key }}: {{ true_condition }}\n{{ else_start }}- {{ key }}: {{false_condition}}\n{{ "
        "end_if }}"
    )
    tm.stream(
        if_start=if_start,
        true_condition=converted_true_expression,
        else_start=else_start,
        false_condition=converted_false_expression,
        end_if=end_if,
        key=attribute_key,
    ).dump(sls_data_count_obj1)
    return sls_data_count_obj1.getvalue()


def convert_var_to_param(hub, var_input):
    variable_name = var_input.group()[6:]
    return f'{{{{ params["{variable_name}"] }}}}'


def convert_only_var_to_param(hub, var_input):
    variable_name = var_input.group()[4:]
    # If the variable name ends with count format is different.
    if re.search(params_variable_ends_with_count_pattern, variable_name):
        count_variable = variable_name[-2:-1]
        return f'{{{{ params["{variable_name[0:-3]}"][{count_variable}] }}}}'
    return f'{{{{ params["{variable_name}"] }}}}'
