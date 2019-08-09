#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3", "/multiply.py"]

inputs:
  x:
    type: File
    inputBinding:
      position: 1
  y:
    type: int
    inputBinding:
      position: 2



outputs:
  answer:
    type: stdout
stdout: output_test1.txt
