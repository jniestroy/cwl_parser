import yaml

#Accepts wf cwl File
#inputs is yaml input file
#parse_wf is main function
def parse_wf(workflow,inputs):

    meta = {"@type":"wfdesc:Wokflow"}

    with open(workflow, 'r') as cwl_file:
        wf_dict = yaml.safe_load(cwl_file)

    if isinstance(inputs,dict):
        input_dict = inputs

    else :
        with open(inputs, 'r') as input_file:
            input_dict = yaml.safe_load(input_file)

    meta['wfdesc:hasInput'] = get_wf_inputs(wf_dict,input_dict)
    #break wf into steps and add each to metadata
    meta.update(parse_steps(wf_dict.get('steps')))

    meta['wfdesc:hasOutput'] = get_outputs(wf_dict)

    return(meta)

def parse_procss(process,inputs):

    meta = {"@type":"wfdesc:Process"}

    with open(workflow, 'r') as cwl_file:
        proc_dict = yaml.safe_load(cwl_file)

    with open(inputs, 'r') as input_file:
        input_dict = yaml.safe_load(input_file)

    meta['wfdesc:hasInput'] = get_wf_inputs(proc_dict,input_dict)
    meta['commandRun'] = proc_dict.get('baseCommand')
    meta['wfdesc:hasOutput'] = get_outputs(wf_dict)

    return(meta)

#Makes metadata for each step in a workflow
#Breaks up steps into processes and SubWorkflows
def parse_steps(steps):

    if steps == None:
        return({})

    steps_dict = {"wfdesc:hasProcess":[],"wfdesc:hasSubWorkflow":[]}

    for step in steps:

        try:
            with open(steps[step].get('run')) as f:
                cwl_process = yaml.safe_load(f)

        except:

            steps_dict["wfdesc:hasProcess"].append(step)
            continue

        if cwl_process['class'] == 'Workflow':

            inputs = gather_inputs(steps[step])
            steps_dict['wfdesc:hasSubWorkflow'].append(parse_cwl(cwl_process,inputs))

        else:
            #Grab Process inputs
            inputs = gather_inputs(steps[step])

            process = {"@type":"wfdesc:Process","name":step}
            process['commandRun'] = cwl_process.get('baseCommand')
            #Add process inputs to dict
            process["wfdesc:hasInput"] = get_process_inputs(cwl_process,inputs)
            process["wfdesc:hasOutput"] = get_outputs(cwl_process)
            steps_dict["wfdesc:hasProcess"].append(process)

    return(steps_dict)
#Giant disaster of function that reads inputs from workflow and grabs values
#from the input yaml file
def get_wf_inputs(workflow,inputs):

    hasInputs = []

    try:

        #input name is key in dictionary
        #input name should be name of individual input
        #datatype is named poorly
        #if input is not array datatype is the inputs type
        #otherwise its a dictionary with all the type information about
        #that input
        for input_name, datatype in gather_inputs(workflow).items():

            input_dict = {
                "@type":"wfdesc:Parameter",
                "name":input_name,
            }

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
                 
            if input_dict.get("datatype") == 'File':
                input_dict['file'] = inputs.get(input_name).get('path')
            #if the datatype is array things get messy
            #need to rewrite this section and make function instead of below
            if input_dict['datatype'] == 'array':

                #make items key to store all elements of input array
                #item_struct is the structure of each element taken from
                #the wf definition file
                input_dict['items'] = []
                #reason for all the gets is thats where it was in rna.yaml
                item_struct = datatype.get('type').get('items').get('fields')
                #for loop over each element in the given inputs file
                for item in inputs.get(input_name):

                    #Since an item in array can have multiple elements for loop
                    #through them all
                    elements = []
                    for element in item_struct:

                        element_dict = {"@type":"wfdesc:Parameter",
                                       "name":element,
                                       "datatype":item_struct[element].get('type')
                                       }

                        if element_dict.get("datatype") == 'File':
                            element_dict['file'] = item[element].get('path')
                        else:
                            element_dict['value'] = item[element]

                        elements.append(element_dict)

                    input_dict['items'].append(elements)

            else:
                input_dict['value'] = inputs.get(input_name)

            hasInputs.append(input_dict)

    #Purpose of the except is if inputs file is invalid or nonexistient
    except:

        if workflow.get('inputs'):
            hasInputs.append("Error parsing cwl. Check all inputs match expected names.")

    return(hasInputs)

def get_process_inputs(workflow,inputs):

    hasInputs = []

    try:

        for input_name, datatype in gather_inputs(workflow).items():#workflow.get('inputs').items():

            input_dict = {
                "@type":"wfdesc:Parameter",
                "name":input_name,
                "datatype":datatype.get('type')
            }
            input_dict['value'] = inputs.get(input_name)
            hasInputs.append(input_dict)

    except:

        if workflow.get('inputs'):
            hasInputs.append("Error parsing cwl. Check all inputs match expected names.")

    return(hasInputs)

#cwl changed from inputs to in in version 1.3 or 1.03
#so since both are still acceptable function grabs input regardless of syntax
def gather_inputs(step_dict):

    if step_dict.get('in'):
        return step_dict.get('in')

    elif step_dict.get('inputs'):
        return step_dict.get('inputs')

    return({})

def get_outputs(workflow):
    hasOutputs = []
    try:
        for output_name, datatype in gather_outputs(workflow).items():#workflow.get('inputs').items():
            output_dict = {
                "@type":"wfdesc:Parameter",
                "name":output_name,
                "datatype":datatype.get("type")
            }
            if datatype.get('outputSource'):
                output_dict['outputSource'] = datatype.get('outputSource')
            hasOutputs.append(output_dict)
    except:
        if workflow.get('outputs'):
            hasOutputs.append("Error parsing cwl. Check all inputs match expected names.")
    return(hasOutputs)

def gather_outputs(step_dict):
    if step_dict.get('out'):
        return step_dict.get('out')
    elif step_dict.get('outputs'):
        return step_dict.get('outputs')
    return({})
