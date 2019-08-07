import os
import sys
import subprocess
import json
import wf_meta as wf
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,BucketAlreadyExists)

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


def workflow(inputs):

    if len(inputs) >= 4:
        path = inputs[3]

    else:
        path = ''

    workflow = inputs[1]
    yaml = inputs[2]

    wf_metadata = wf.generate_wf_meta(workflow,path)

    wf_result = run_workflow(workflow,yaml,path)

    if wf_result['success']:

        output_meta = generate_output_meta(wf_result['output'],wf_metadata,workflow,path)

    else:
        print("Workflow Failed to run.\n" + str(wf_result['output']))
        return
    for output in output_meta:
        print(upload_file_minio(output['path'],output))

#Takes metadata about output from wf and output once wf is run
def generate_output_meta(wf_output,corresponding_wf_meta,workflow,path):

    schema_meta = wf.pull_schema_meta(workflow,path)

    all_meta = combine_meta(schema_meta,corresponding_wf_meta,wf_output)

    return(all_meta)

def combine_meta(schema_meta,wf_meta,wf_output):
    total = []

    for output in schema_meta:

        object_meta = output

        if '@context' in wf_meta:

            object_meta['@context'] = {"base","http://schema.org",
                        "wfdesc:","https://wf4ever.github.io/ro/2016-01-28/wfdesc/"}

            del wf_meta['@context']


        object_meta['generated_by'] = wf_meta
        object_meta["path"] = wf_output[object_meta['name']].get('path')
        object_meta["size"] = wf_output[object_meta['name']].get('size')

        total.append(object_meta)

    return(total)


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

def upload_file_minio(file,output_metadata):

    filename = get_filename(file)

    meta = {'name':output_metadata['name']}

    f = open(file,"rb")

    minioClient = Minio('127.0.0.1:9000',
        access_key='92WUKA7ZAP4M3UOS0TNG',
        secret_key='uIgJzgatEyop9ZKWfRDSlgkAhDtOzJdF+Jw+N9FE',
        secure=False)

    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)

    try:
           minioClient.put_object('testbucket', filename, f,size,metadata = meta)

    except ResponseError as err:
           return 'There was an error'

    #f.save(secure_filename(f.filename))
    return 'file uploaded successfully'

def get_filename(full_path):
    return(full_path.split('/')[len(full_path.split('/')) -1 ])

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        workflow(sys.argv)
    else:
        print("Not enough inputs given to run workflow.")
