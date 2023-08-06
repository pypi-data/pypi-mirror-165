def stage(hub):
    sls_data = hub.tf_idem.RUNS["SLS_DATA_WITH_KEYS"]
    sls_data_cleaned_up = hub.idem_codegen.tool.remove_extra_attributes.remove_extra_attributes_from_sls_data(
        sls_data
    )
    hub.tf_idem.RUNS["SLS_DATA_WITH_KEYS"] = sls_data_cleaned_up

    sls_data_original = hub.tf_idem.RUNS["SLS_DATA"]
    for sls_resource in sls_data_original:
        cleaned_up_resource = sls_data_cleaned_up[
            sls_data_original[sls_resource]["resource_path"]
        ]
        if cleaned_up_resource:
            sls_data_original[sls_resource]["resource"] = cleaned_up_resource
    hub.tf_idem.RUNS["SLS_DATA"] = sls_data_original
