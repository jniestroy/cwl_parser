cwlVersion: v1.0

doc: |
  # Metaphlan-ISBCGC

  # Overview
  This is an example of how to add a description to a tool. This uses markdown and can show things like images and links.

dct:creator:
    foaf:name: "Hsinyi Tsang"
    foaf:mbox: "hsinyi.confidential@nih.gov"

class: CommandLineTool
baseCommand: [tar, xjf]
stdout: $(inputs.unzippedFileName)
hints:
  - class: DockerRequirement
    dockerPull: stevetsa/metaphlan:2
inputs:
  fastq:
    type: File
    inputBinding:
      position: 1
  unzippedFileName:
    type: string
  stdoutflag:
    type: string
    inputBinding:
      position: 2
outputs:
  unzippedFile:
    type: stdout
