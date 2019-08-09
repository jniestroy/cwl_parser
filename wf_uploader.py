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
    print(isJob)
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
