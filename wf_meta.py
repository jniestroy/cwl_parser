import yaml

def generate_wf_meta(workflow,path = ''):

    meta = {

        "@context":{"wfdesc":"https://wf4ever.github.io/ro/2016-01-28/wfdesc/"},
        "@type":"wfdesc:Wokflow",
        "name":workflow

    }
    try:
        with open(path + workflow, 'r') as cwl_file:
            wf_dict = yaml.safe_load(cwl_file)
    except:
        return("Workflow File does not Exist")
    #Grab Inputs into Workflow

    inputs = get_inputs(wf_dict)

    #Gather Worflow Outputs

    outputs = get_outputs(wf_dict)

    #Scripts ran

    scripts = get_generating_scripts(wf_dict,path)

    #scripts might be steps in wf still unsure about this

    meta["wfdesc:hasInput"] = inputs

    meta["wfdesc:hasProcess"] = scripts

    meta['wfdesc:hasOutput'] = outputs

    return(meta)

def parse_dict_steps(steps,path):

    steps_list = []

    for step in steps:

        meta = {
            "@type":"wfdesc:Process",
            "name":step,
            "run":steps[step].get('run')
        }

        try:

            with open(path + meta['run']) as f:
                cwl_process = yaml.safe_load(f)

            meta['commandRun'] = cwl_process.get("baseCommand")

            steps_list.append(meta)

        except:

            steps_list.append(meta)

            continue

    return(steps_list)

def parse_list_steps(steps,path):

    steps_list = []

    for step in steps:

        meta = {
            "@type":"wfdesc:Process",
            "name":step.get('id'),
            "run":step.get('run')
        }

        try:

            with open(path + meta['run']) as f:
                cwl_process = yaml.safe_load(f)

            meta['commandRun'] = cwl_process.get("baseCommand")

            steps_list.append(meta)

        except:

            steps_list.append(meta)
            continue

    return(steps_list)

def get_generating_scripts(workflow,path):

    steps = workflow.get('steps')

    if steps == None:
        return([])

    elif isinstance(steps,list):
        steps_list = parse_list_steps(steps,path)

    else:
        steps_list = parse_dict_steps(steps,path)

    return(steps_list)

def get_outputs(workflow):

    outputs = gather_outputs(workflow)

    if isinstance(outputs,list):

        hasOutputs = get_list_outputs(outputs)

    else:

        hasOutputs =  get_dict_outputs(outputs)

    return(hasOutputs)

def get_inputs(workflow):

    inputs = gather_inputs(workflow)

    if isinstance(inputs,list):

        hasInputs = get_list_inputs(inputs)

    else:

        hasInputs =  get_dict_inputs(inputs)

    return(hasInputs)

def get_list_outputs(outputs):

    hasOutputs = []

    for output in outputs:

        out_dict = {
            "@type":"wfdesc:Parameter",
            "name":output.get('id'),
            "datatype": output.get("type")
        }

        if out_dict['datatype'] == "File" or out_dict['datatype'] == "File?":
            out_dict['outputSource'] = output.get('outputSource')

        hasOutputs.append(out_dict)

    return(hasOutputs)

def get_list_inputs(inputs):

    input_list = []

    for inp in inputs:

        input_dict = {
            "@type":"wfdesc:Parameter",
            "name":inp['id']
        }

        if isinstance(inp.get('type'),dict):

            input_dict['datatype'] = inp.get('type').get('type')

        else:
            input_dict['datatype'] = inp.get('type')

        input_list.append(input_dict)

    return(input_list)

def get_dict_outputs(outputs):

    hasOutputs = []

    for output_name in outputs:

        out_dict = {
        "@type":"wfdesc:Parameter",
        "name":output_name,
        }

        if isinstance(outputs[output_name],dict):
            out_dict['datatype'] = outputs[output_name].get('type')

            if out_dict['datatype'] == "File" or out_dict['datatype'] == "File?":
                out_dict['outputSource'] = outputs[output_name].get('outputSource')

        hasOutputs.append(out_dict)

    return(hasOutputs)



def get_dict_inputs(inputs):

    input_list = []

    for input_name in inputs:

        input_dict = {
            "@type":"wfdesc:Parameter",
            "name":input_name,
        }

        if isinstance(inputs[input_name],dict):

            datatype = inputs[input_name]
        #if variable isn't simple type find type
            if isinstance(datatype,dict):

                if datatype.get('class'):

                    input_dict['datatype'] = 'File'

                else:

                    #This is where type was in rna.yaml might
                    if isinstance(datatype.get('type'),dict):

                        input_dict['datatype'] = datatype.get('type').get('type')

                    else:

                        input_dict['datatype'] = datatype.get('type')

            else:
                input_dict['datatype'] = datatype
        else:
            input_dict['datatype'] = inputs[input_name]

        input_list.append(input_dict)

    return(input_list)


def gather_inputs(step_dict):

    if step_dict.get('in'):
        return step_dict.get('in')

    elif step_dict.get('inputs'):
        return step_dict.get('inputs')

    return({})

def gather_outputs(step_dict):

    if step_dict.get('out'):
        return step_dict.get('out')

    elif step_dict.get('outputs'):
        return step_dict.get('outputs')

    return({})

def update_input_values(workflow,yamlfile,path):
    with open(path + yamlfile, 'r') as cwl_file:
        input_dict = yaml.safe_load(cwl_file)
    for inp in workflow['wfdesc:hasInput']:
        input_name = inp['name']
        file_type = inp['datatype']
        if file_type == 'File':
            inp['path'] = input_dict[input_name]['path']
        elif file_type == 'Array':
            continue
        else:
            inp['value'] = input_dict[input_name]
    return(workflow)


def pull_schema_meta(workflow,path):

    with open(path + workflow, 'r') as cwl_file:
        wf_dict = yaml.safe_load(cwl_file)

    outputs = gather_outputs(wf_dict)

    schema_meta = []

    for output_name in outputs:
        schema = {}
        for key in outputs[output_name]:
            if 'schema:' in key:
                if key == 'schema:type':
                    schema['@type'] = outputs[output_name][key]
                    continue
                schema[key.replace('schema:','')] = parse_key(outputs[output_name][key])
        schema['name'] = output_name
        schema_meta.append(schema)
    return(schema_meta)


def parse_key(value):

    if isinstance(value,dict):

        updated_dict = {}

        for key, val in value.items():
            if isinstance(val,dict):
                updated_dict[key.replace('schema:','')] = parse_key(val)
            else:
                if key == 'schema:type':
                    updated_dict['@type'] = val
                    continue
                updated_dict[key.replace('schema:','')] = val
        return(updated_dict)
    else:
        return(value)
