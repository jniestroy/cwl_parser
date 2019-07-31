#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3",  "/Users/justinniestroy-admin/Documents/Work/Randall Data/houlter data/calc_avg.py"]

inputs:
  file_number:
    type: int
    inputBinding:
      position: 1

stdout: cwl.output.json

outputs:
  example_out:
    type: stdout
stdout: output.txt
