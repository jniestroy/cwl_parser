def generate_wf_meta(workflow):
    meta = {
        "@context":{"wfdesc":"https://wf4ever.github.io/ro/2016-01-28/wfdesc/"},
        "@type":"wfdesc:Wokflow",
        "name":workflow
    }

    with open(path + workflow, 'r') as cwl_file:
        wf_dict = yaml.safe_load(cwl_file)

    #Grab Inputs into Workflow

    inputs = get_inputs(workflow)

    #Gather Worflow Outputs

    outputs = get_outputs(workflow)

    #Scripts ran

    scripts = get_generating_scripts(workflow)

    #scripts might be steps in wf still unsure about this

    meta = meta + inputs + outputs + scripts


    return(meta)

#Might want to include the yaml file that was run as well
def generate_output_meta(output,corresponding_wf_meta):

    #simple meta about object pull from object ???
    output_meta = simple_output_features(output) #like name type etc...

    #from wf used to generate object grab required Inputs
    inputs_to_generate = corresponding_wf_meta['inputs']

    #Again grab scipts required to create output
    scripts_to_generate = corresponding_wf_meta['scripts']

    final_meta = output_meta + inputs_to_generate + scripts_to_generate

    return(final_meta)
