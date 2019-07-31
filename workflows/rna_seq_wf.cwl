# Assembling full workflow

# array of records

cwlVersion: v1.0
class: Workflow
requirements:
  - class: InlineJavascriptRequirement
  - class: ScatterFeatureRequirement

inputs:
  input_bam:
    type:
      type: array
      items:
        type: record
        fields:
          bam:
            type: File
          output:
            type: string

outputs:
  sam_file:
    type: File[]
    outputSource: bam_to_sam/sam_file


steps:
  bam_to_sam:
    run: samtools.cwl
    scatter: input_bam
    scatterMethod: dotproduct
    in:
      header:
        default: True
      input_bam: input_bam
    out: [sam_file]
