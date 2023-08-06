from idem_codegen.tf_idem.tool.utils import replace_pattern


def look_for_possible_improvements(hub, tf_resource, resource_attributes):
    list_of_comments = []
    for resource_attribute in resource_attributes:
        for resource_attribute_key in resource_attribute:
            (
                tf_resource_value,
                _,
                is_attribute_different,
            ) = hub.tf_idem.tool.utils.get_tf_equivalent_idem_attribute(
                tf_resource,
                list(tf_resource.keys())[0],
                resource_attribute_key,
            )
            if isinstance(tf_resource_value, str) and replace_pattern.search(
                tf_resource_value
            ):
                list_of_comments.append(
                    hub.tf_idem.tool.utils.REPLACE_COMMENT.format(
                        resource=resource_attribute_key
                    )
                )
    return list_of_comments
