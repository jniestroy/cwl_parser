#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3","/Figure WF Files/create_fig.py"]

inputs:
  clean:
    type: File
    inputBinding:
      position: 1

outputs:
  figure:
    type: File
    outputBinding:
      glob: figure.png
