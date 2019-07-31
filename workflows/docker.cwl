#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3", "-m", "calc_avg"]
hints:
  DockerRequirement:
    dockerPull: python
inputs:
  src:
    type: File
    inputBinding:
      position: 1
  file_number:
    type: int
    inputBinding:
      position: 2
outputs:
  example_out:
    type: stdout
stdout: output.txt
