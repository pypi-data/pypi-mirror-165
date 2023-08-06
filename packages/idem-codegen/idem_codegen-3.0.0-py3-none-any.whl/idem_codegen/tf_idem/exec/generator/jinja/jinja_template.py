import ruamel
from jinja2 import Template
from ruamel.yaml.comments import CommentedMap


def jinja_if_for_loop(
    hub, ch, count_dict, item, list_of_comments, sls_data, sls_data_count_obj
):
    count_item = item[:-1] + f"{{{{{ch}}}}}"
    sls_file_data_with_comment = CommentedMap({count_item: sls_data[item]})
    if len(list_of_comments) > 0:
        sls_file_data_with_comment.yaml_set_start_comment("\n".join(list_of_comments))
    obj = ruamel.yaml.round_trip_dump(sls_file_data_with_comment)
    if (
        count_dict["count_statement"] is not None
        and count_dict["count_false_condition"] == 0
    ):
        if_loop = f"{{% if {(count_dict['count_statement']).replace('{{ ', '').replace(' }}', '').replace('&&', 'and').replace('||', 'or')} %}}\n"
        for_loop = f"{{% for {ch} in range({count_dict['count_true_condition']}) %}}\n"
        end_loop = "{% endfor %}"
        end_if = "{% endif %}"
        tm = Template(
            "\n{{if_loop}}{{ for_loop }}{{ obj }}{{ end_loop }}\n{{end_if}}\n\n"
        )
        tm.stream(
            if_loop=if_loop,
            for_loop=for_loop,
            obj=obj,
            end_loop=end_loop,
            end_if=end_if,
        ).dump(sls_data_count_obj)
    else:
        for_loop = f"{{% for {ch} in range({count_dict['count_true_condition']}) %}}\n"
        end_loop = "{% endfor %}"
        tm = Template("\n{{ for_loop }}{{ obj }}{{ end_loop }}\n\n")
        tm.stream(for_loop=for_loop, obj=obj, end_loop=end_loop).dump(
            sls_data_count_obj
        )


def jinja_if_condition(
    hub, count_dict, item, list_of_comments, sls_data, sls_data_count_obj
):
    sls_file_data_with_comment = CommentedMap({item: sls_data[item]})
    if len(list_of_comments) > 0:
        sls_file_data_with_comment.yaml_set_start_comment("\n".join(list_of_comments))
    obj = ruamel.yaml.round_trip_dump(sls_file_data_with_comment)
    if count_dict["count_statement"] is not None:
        if_loop = f"{{% if {(count_dict['count_statement']).replace('{{ ', '').replace(' }}', '').replace('&&', 'and').replace('||', 'or')} %}}\n"
        end_if = "{% endif %}"
        tm = Template("\n{{if_loop}}{{ obj }}{{end_if}}\n\n")
        tm.stream(if_loop=if_loop, obj=obj, end_if=end_if).dump(sls_data_count_obj)
    else:
        tm = Template("\n{{ obj }}\n")
        tm.stream(obj=obj).dump(sls_data_count_obj)


def jinja_if_not_condition(
    hub, count_dict, item, list_of_comments, sls_data, sls_data_count_obj
):
    sls_file_data_with_comment = CommentedMap({item: sls_data[item]})
    if len(list_of_comments) > 0:
        sls_file_data_with_comment.yaml_set_start_comment("\n".join(list_of_comments))
    obj = ruamel.yaml.round_trip_dump(sls_file_data_with_comment)
    if (
        count_dict["count_statement"] is not None
        and count_dict["count_true_condition"] == 0
    ):
        if_loop = f"{{% if not {(count_dict['count_statement']).replace('{{ ', '').replace(' }}', '').replace('&&', 'and').replace('||', 'or')} %}}\n"
        end_if = "{% endif %}"
        tm = Template("\n{{if_loop}}{{ obj }}{{end_if}}\n\n")
        tm.stream(if_loop=if_loop, obj=obj, end_if=end_if).dump(sls_data_count_obj)
