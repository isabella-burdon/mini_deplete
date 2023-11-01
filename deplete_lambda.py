import subprocess as sp
import gzip

# Define count fastq function
def count_fastq_reads(fastq_file):
    try:
        with gzip.open(fastq_file, 'rb') as f:
            line_count = sum(1 for line in f)
    except gzip.BadGzipFile:
        # If it's not a gzipped file, try opening it as a regular text file
        with open(fastq_file, 'r') as f:
            line_count = sum(1 for line in f)
    return line_count // 4  # Each read consists of 4 lines in a Fastq file

print(""" 
      Lambda phage read depletion selected.""")

# get inputs
run_name = input(""" 
    What is the run name common to these files: """)

lambda_fasta_filepath = "ref_genomes/phage_lambda.fasta"
fastq_filepath = f"fastq_files/storage_extraction/aggregated_fastqs/{run_name}.fastq.gz"
output_filepath = f"fastq_files/storage_extraction/lambda_depleted/{run_name}"

confirm_variables = input(f"""
    Are these variables correct?
    
    lambda_fasta_filepath: "ref_genomes/phage_lambda.fasta"
    fastq_filepath: "your_data/{run_name}.fastq.gz"
    output_filepath: "output/{run_name}.LEFT_BLANK_INTENTIONALLY"

    [y/n] : """)

while confirm_variables != "y":
    print("please continue to manual file path input: ")

    lambda_fasta_filepath = input("""
        Please type custom phage lambda reference genome file path 
        (i.e. root/folder/reference.fasta): """)

    fastq_filepath = input("""
        Please type custom reads file path 
        (i.e. root/folder/filename.fastq.gz) : """)

    output_filepath = input("""
        Please type custom desired output path and ensure this directory has already been made
        NB: DO NOT state file type ".fastq.gz"
        (i.e. root/folder/out_file_name) : """)
    
    # confirm inputs

    print(f""" 
        
        Please confirm the following paths are correct:

        lambda phage reference genome path = {lambda_fasta_filepath}
        reads file path = {fastq_filepath}
        output file path = {output_filepath}

    """)

    run = input("[y/n] : ")

    if run != "y":
        print("""
            Please restart code
            """)
        
    else:
        while run == "y": 
            print("""
                Processing inputs...
                """)
            break

else:
    while confirm_variables == "y": 
        print("""
        Depleting reads mapped to phage lambda...
        """)
        break

# Run minimap2 and samtools commands
command_map_lambda = f"minimap2 -t 4 -ax map-ont {lambda_fasta_filepath} {fastq_filepath} | samtools view -f 4 -b -o {output_filepath}_lambda.bam && samtools fastq -f 4 -0 {output_filepath}_lambda.fastq {output_filepath}_lambda.bam"
    
try:
    lambda_result = sp.run(command_map_lambda, shell=True, check=True, stderr=sp.PIPE, text=True)
    lambda_minimap2_report = lambda_result.stderr
    print(f"""
          Phage lambda reads depleted. 
          Writing summary...
          """)
except sp.CalledProcessError:
    print("An error occurred during processing. Please check your inputs and dependencies.")

# write a summary report
count_pre_depletion = count_fastq_reads(fastq_filepath)
count_post_lambda_depletion = count_fastq_reads(f"{output_filepath}_lambda.fastq")

summary = f"""
Run name: {run_name}

Summary stats:
    Total reads (post lambda depletion): {count_post_lambda_depletion}
    Proportion of reads mapped to phage lambda: %{round((count_pre_depletion - count_post_lambda_depletion)/count_pre_depletion*100, 2)}
    Number of reads mapped to lambda phage (and depleted): {count_pre_depletion - count_post_lambda_depletion}

Reads as mapped:
    Number of reads pre depletion: {count_pre_depletion}
    Number of reads post lambda depletion: {count_post_lambda_depletion}

Paths submitted to program:
    lambda phage fasta reference genome path ={lambda_fasta_filepath}
    Fastq reads file path = {fastq_filepath}
    Output file path = {output_filepath}

Lambda depletion minimap2 generated report:
{lambda_minimap2_report}
"""

print(summary)

last_slash_index = output_filepath.rfind("/")

if last_slash_index != -1:
    # Remove the last portion of the string
    output_filepath_cd = output_filepath[:last_slash_index]

summary_file_path = f"{output_filepath_cd}/{run_name}_summary.txt"
with open(summary_file_path, "w") as summary_file:
    summary_file.write(summary)

print(f"""
      Summary txt file written and saved to: 
      {output_filepath_cd}/{run_name}_summary.txt
      """)