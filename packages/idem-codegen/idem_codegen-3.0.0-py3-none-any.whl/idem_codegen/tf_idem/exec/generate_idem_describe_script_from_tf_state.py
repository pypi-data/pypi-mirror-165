def init(hub):
    tf_state_file_path = hub.OPT.idem_codegen.tf_state_file_path
    tf_state_data = hub.idem_codegen.tool.utils.read_json(tf_state_file_path)
    idem_describe_path = "aws\\.()\\..*"
    for tf_state_resource in tf_state_data["resources"]:
        tf_state_resource.get("type")
