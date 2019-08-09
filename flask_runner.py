from flask import Flask, render_template, request, redirect,jsonify
import requests
import bash_in_python as wf_runner
import wf_meta as wf_parser
import wf_uploader as wf_upload
import json
import os
import yaml

app = Flask(__name__)

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
            print(files[f].name)
            workflow = files[f]
            i = 1
        else:
            commandTools.append(files[f])

    output_meta = wf_parser.pull_schema_meta(workflow,bytes = True)

    for output in output_meta:
        URL = "http://validator:5000/validatejson"
        req = requests.post(url = URL,json = output)
        print(req.json())
        valid = req.json()['valid']
        valid = True
        #valid = True
        if not valid:
            return(jsonify({"error":str(output.get('name')) + " missing required schema properties or invalid",
            "upload":False,
            "validation_result":req.json()['error']}))

    if wf_upload.upload_cwl(workflow,isWorkflow = True,bytes = True):
        for tool in commandTools:
            if wf_upload.upload_cwl(tool,isWorkflow = False,bytes = True):
                continue
            else:
                result = {"error":"Error uploading commandLineTool: " + str(tool.name)}
                return(jsonify(result))
        # if given.get('job'):
        #     job = given.get("job")
        #     if  not wf_upload.upload_cwl(job,path,isWorkflow = False,isJob = True):
        #         result = {"error":"Error uploading job: " + str(job)}
        #         return(jsonify(result))
    else:
        result = {"error":"Error uploading workflow"}
        return(jsonify(result))

    result = {"error": "","upload": True}

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
    # workflow = given['workflow']
    # commandTools = given['commandTools']
    # path = given['path']
    #
    # try: open(path + workflow, 'r')
    # except: return(jsonify({"error":"workflow not found"}))
    #
    # output_meta = wf_parser.pull_schema_meta(workflow,path)
    #
    # for output in output_meta:
    #     URL = "http://localhost:5000/validatejson"
    #     #req = requests.post(url = URL,json = output)
    #     valid = req.json()['valid']
    #     valid = True
    #     if not valid:
    #         return(jsonify({"error":str(output.get('name')) + " missing required schema properties or invalid",
    #         "upload":False,
    #         "validation_result":req.json()['error']}))
    #
    # if wf_upload.upload_cwl(workflow,path):
    #     for tool in commandTools:
    #         if wf_upload.upload_cwl(tool,path,isWorkflow = False):
    #             continue
    #         else:
    #             result = {"error":"Error uploading commandLineTool: " + str(tool)}
    #             return(jsonify(result))
    #     if given.get('job'):
    #         job = given.get("job")
    #         if  not wf_upload.upload_cwl(job,path,isWorkflow = False,isJob = True):
    #             result = {"error":"Error uploading job: " + str(job)}
    #             return(jsonify(result))
    # else:
    #     result = {"error":"Error uploading workflow"}
    #     return(jsonify(result))
    #
    # result = {"error": "","upload": True}
    #
    # return(jsonify(result))




if __name__ == "__main__":
    app.run(port=5002)
