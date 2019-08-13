import os
import sys
import subprocess
import json
import wf_meta as wf
from minio import Minio
import wf_uploader as wf_upload
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,BucketAlreadyExists)
import tempfile
import shutil
import yaml

minio_name = os.environ['MINIO_DOCKER_NAME']
minio_key = os.environ['MINIO_ACCESS_KEY']
minio_secret = os.environ["MINIO_SECRET_KEY"]

#Create wf metadata
#Run Workflow
#Create Output Object metadata
#Post Output Objects to Minio
def workflow_main(inputs):

    workflow = inputs[1]
    yaml = inputs[2]
    path = inputs[3]

    if path == 'minio':

        path = str(os.getcwd()) + 'randompaththatshouldntexist12345/'
        path1= str(os.getcwd()) + 'randompaththatshouldntexist12345/'

        try:
            os.mkdir(path)

        except:
            shutil.rmtree(path1)
            os.mkdir(path)

        valid = wf_upload.get_wf_minio(workflow,yaml,path)

        if not valid:

            return({"error":"Not all required objects found on Minio"})

        result = workflow_main(['tes',workflow,yaml,path])

        #shutil.rmtree(path1)

        return(result)

    #print("Path is " + path)
    wf_metadata = wf.generate_wf_meta(workflow,path)



    if not isinstance(wf_metadata,dict):

        return({"result":"Workflow not found please check path"})

    wf_result = run_workflow(workflow,yaml,path)

    if wf_result['success']:

        output_meta = generate_output_meta(wf_result['output'],wf_metadata,workflow,yaml,path)

    else:

        print("Workflow Failed to run.\n" + str(wf_result['output']))

        return({"error":"Workflow failed to run","cwltool output":str(wf_result['output'])})

    result = {"wfprov:WorkflowRun":wf_metadata}

    result['outputs'] = {}

    for output in output_meta:

        req = requests.put("https://ors:8080/uid/test/",json = output,verify = False)

        if req.json().get('created'):

                full_id = req.json()['created']['@id']

                _,_,base,namespace,name,id = full_id.split('/')

                output['identifier'] = id

                if wf_upload.upload_file_minio(output['path'],output):

                    result['outputs'][output['name']] = {'upload':"success","object_meta":output}

                else:

                    result['outputs'][output['name']] = {"upload":"failed"}

    return(result)

#run cwl-tool in python via subprocess
def run_workflow(workflow,yaml,path):

    if path != '':
        os.chdir(path)


    cmd = 'cwltool'

    out = subprocess.Popen([cmd,workflow,yaml],
               stdout=subprocess.PIPE,
               stderr=subprocess.STDOUT)

    stdout,stderr = out.communicate()

    if 'Final process status is success' in str(stdout):

        output = parse_stdout(str(stdout))

        return({"success":True,"output":output})

    else:
        return({"success":False,"output":str(stdout)})



#Takes metadata about output from wf and output once wf is run
def generate_output_meta(wf_output,corresponding_wf_meta,workflow,yaml,path):

    schema_meta = wf.pull_schema_meta(workflow,path)

    updated_wf_meta = wf.update_input_values(corresponding_wf_meta,yaml,path)

    all_meta = combine_meta(schema_meta,updated_wf_meta,wf_output)

    return(all_meta)

#combine object meta from multiple sources into final meta object
def combine_meta(schema_meta,wf_meta,wf_output):
    total = []

    for output in schema_meta:

        object_meta = output

        if '@context' in wf_meta:

            object_meta['@context'] = {"base":"http://schema.org",
                        "wfdesc:":"https://wf4ever.github.io/ro/2016-01-28/wfdesc/"}

            del wf_meta['@context']


        object_meta['generated_by'] = wf_meta
        object_meta["path"] = wf_output[object_meta['name']].get('path')
        object_meta["size"] = wf_output[object_meta['name']].get('size')

        total.append(object_meta)

    return(total)


def parse_stdout(stdout):

    start = 0
    count = 0
    check = 0

    output = ''

    for element in stdout:

        if element == '{':

            start = 1
            count = count + 1

        if start == 1:
            #new lines were causing problems and
            #not removable with replace

            if element == '\\':

                check = 1
                continue

            if element == 'n' and check == 1:

                check = 0
                continue

            output = output + element

        if element == '}':

            count = count - 1

            if count == 0:
                start = 0

    #output = output.strip('\n')
    return(json.loads(str(output)))

def get_filename(full_path):
    return(full_path.split('/')[len(full_path.split('/')) -1 ])




# if __name__ == "__main__":
#     if len(sys.argv) >= 3:
#         print(workflow_main(sys.argv))
#     else:
#         print("Not enough inputs given to run workflow.")
