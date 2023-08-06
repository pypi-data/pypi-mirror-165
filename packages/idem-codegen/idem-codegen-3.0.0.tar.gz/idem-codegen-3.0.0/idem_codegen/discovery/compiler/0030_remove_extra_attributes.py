def stage(hub):
    sls_data = hub.discovery.RUNS["SLS_DATA_WITH_KEYS"]
    sls_data_cleaned_up = hub.idem_codegen.tool.remove_extra_attributes.remove_extra_attributes_from_sls_data(
        sls_data
    )
    hub.discovery.RUNS["SLS_DATA_WITH_KEYS"] = sls_data_cleaned_up
