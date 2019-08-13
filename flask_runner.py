from flask import Flask, render_template, request, redirect,jsonify
import requests
import bash_in_python as wf_runner
import wf_meta as wf_parser
import wf_uploader as wf_upload
import json
import os
import yaml

app = Flask(__name__)

minio_name = os.environ['MINIO_DOCKER_NAME']
minio_key = os.environ['MINIO_ACCESS_KEY']
minio_secret = os.environ["MINIO_SECRET_KEY"]

@app.route('/', methods=['GET'])
def homepage():

    return(str(os.listdir()))

@app.route('/run-wf',methods = ['POST'])
def run_wf():
    result = {}

    if request.data == b'':
        return(jsonify({'error':"Please POST JSON, with workflow, job, and path to directory"}))

    try:
        given = json.loads(request.data.decode('utf-8'))
    except:
        return(jsonify({'error':"Please POST JSON, with workflow, job, and path to directory"}))

    inputs = ["file",given['workflow'],given['job']]

    if given.get('path'):
        inputs.append(given.get('path'))
    else:
        inputs.append('minio')

    return(jsonify(wf_runner.workflow_main(inputs)))

@app.route('/post-wf',methods = ['POST'])
def post_wf():

    result = {}

    files = request.files

    i = 0

    commandTools = []

    for f in files:

        if i == 0:

            workflow = files[f]
            i = 1

        else:
            commandTools.append(files[f])

    wf_dict = yaml.safe_load(workflow)

    output_meta = wf_parser.pull_schema_meta(wf_dict,bytes = True)

    for output in output_meta:

        URL = "http://validator:5000/validatejson"
        req = requests.post(url = URL,json = output)
        valid = req.json()['valid']

        if not valid:
            return(jsonify({"error":str(output.get('name')) + " missing required schema properties or invalid",
            "upload":False,
            "validation_result":req.json()['error']}))


    wf_metadata = wf_parser.generate_wf_meta(wf_dict,bytes = True,name=workflow.name)

    req = requests.put("https://ors:8080/uid/test/",json = wf_metadata,verify = False)

    if req.json().get('created'):

            full_id = req.json()['created']['@id']

            _,_,base,namespace,name,id = full_id.split('/')

            wf_metadata['identifier'] = id

    ####################
    #Post wf to mongo
    ####################

    if wf_upload.upload_cwl(workflow,isWorkflow = True,bytes = True,id = id):
        commandlineids = []
        for tool in commandTools:

            tool_dict = yaml.safe_load(tool)

            tool_meta = wf_parser.generate_proccess_meta(tool_dict,bytes = True,name=tool.name)

            req = requests.put("https://ors:8080/uid/test/",json = tool_meta,verify = False)

            if req.json().get('created'):

                    full_id = req.json()['created']['@id']

                    _,_,base,namespace,name,id = full_id.split('/')

                    commandlineids.append(id)
            else:

                result = {"error":"Error minting id for commandLineTool: " + str(tool.name)}

                return(jsonify(result))

            if wf_upload.upload_cwl(tool,isWorkflow = False,bytes = True,id=id):

                continue

            else:

                result = {"error":"Error uploading commandLineTool: " + str(tool.name)}

                return(jsonify(result))

    else:

        result = {"error":"Error uploading workflow"}

        return(jsonify(result))

    result = {
            "upload": True,
            "workflow identifier":wf_metadata['id'],
            "commandLineTools Ids":commandlineids
            }

    return(jsonify(result))

@app.route('/post-job',methods = ['POST'])
def post_job():

    result = {}

    files = request.files

    i = 0

    jobs = []

    for f in files:

        jobs.append(files[f])

    for job in jobs:

        if wf_upload.upload_cwl(job,isJob = True,bytes = True):

            continue

        else:

            result = {"error":"Error uploading commandLineTool: " + str(job.name)}

            return(jsonify(result))


    result = {"error": "","upload": True}

    return(jsonify(result))



if __name__ == "__main__":
    app.run(port=5002)
