from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,BucketAlreadyExists)
import os
import sys
import subprocess
import json
import wf_meta as wf

minio_name = os.environ['MINIO_DOCKER_NAME']
minio_key = os.environ['MINIO_ACCESS_KEY']
minio_secret = os.environ["MINIO_SECRET_KEY"]

def upload_cwl(cwl,path = '',isWorkflow = False,isJob = False,bytes = False):

    if not bytes:

        file = path + cwl
        filename = get_filename(file)
        f = open(file,"rb")

    else:

        f = cwl
        filename = f.name

    if isWorkflow:
        folder = "workflows/"
    elif isJob:
        folder = "jobs/"
    else:
        folder = "commandLineTools/"


    minioClient = Minio(minio_name,
            access_key=minio_key,
            secret_key=minio_secret,
            secure=False)
    # minioClient = Minio('127.0.0.1:9000',
    #     access_key='92WUKA7ZAP4M3UOS0TNG',
    #     secret_key='uIgJzgatEyop9ZKWfRDSlgkAhDtOzJdF+Jw+N9FE',
    #     secure=False)

    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)

    try:
           minioClient.put_object('testbucket', folder + filename, f,size,metadata = {"name":filename})

    except ResponseError as err:
           return False

    #f.save(secure_filename(f.filename))
    return True

def get_wf_minio(workflow_name,job,path):

    minioClient = Minio(minio_name,
            access_key=minio_key,
            secret_key=minio_secret,
            secure=False)

    try:
        data = minioClient.get_object('testbucket', "workflows/" + workflow_name)
        with open(path + workflow_name, 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)

    except ResponseError as err:

        print(err)
        return(False)

    try:

        data = minioClient.get_object('testbucket', "jobs/" + job)

        with open(path + job, 'wb') as file_data:
            for d in data.stream(32*1024):
                file_data.write(d)

    except ResponseError as err:

        print(err)
        return(False)


    processes = wf.generate_wf_meta(workflow_name,path).get('wfdesc:hasProcess')

    if processes == None:
        return(True)

    for process in processes:

        commandLineTool = process.get('run')

        try:

            data = minioClient.get_object('testbucket', "commandLineTools/" + commandLineTool)

            with open(path + commandLineTool, 'wb') as file_data:
                for d in data.stream(32*1024):
                    file_data.write(d)

        except ResponseError as err:

            print(err)
            return(False)

        except:
            return(False)

    return(True)

def upload_file_minio(file,output_metadata):

    filename = get_filename(file)

    meta = {'name':output_metadata['name']}

    f = open(file,"rb")

    minioClient = Minio(minio_name,
            access_key=minio_key,
            secret_key=minio_secret,
            secure=False)

    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)

    try:
           minioClient.put_object('testbucket', filename, f,size,metadata = meta)

    except ResponseError as err:
           return False

    #f.save(secure_filename(f.filename))
    return True

def get_filename(full_path):
    return(full_path.split('/')[len(full_path.split('/')) -1 ])
