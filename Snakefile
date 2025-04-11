configfile: 'config.yaml'

rule all:
    input:
        f"merged_output/merged_output.tsv"

rule fastp:
    input:
        forward = lambda wildcards: os.path.abspath(config["samples"][wildcards.sample]["forward"]),
        reverseR = lambda wildcards: os.path.abspath(config["samples"][wildcards.sample]["reverseR"])
    output:
        forward = "results/{sample}/fastp/{sample}_R1_trimmed.fastq.gz",
        reverseR = "results/{sample}/fastp/{sample}_R2_trimmed.fastq.gz"
        report = "results/{sample}/fastp/{sample}_fastp_report.html"
    params:
        outdir = "results/{sample}/fastp"
    log:
        stdout = "results/{sample}/fastp/log-stdout.txt",
        stderr = "results/{sample}/fastp/log-stderr.txt"
    benchmark:
        "results/{sample}/fastqc/benchmark.txt"
    threads:
        config["threads"]
    shell:
        "fastp -i {input.forward} -I {input.reverseR} -o {output.forward} -O {output.reverseR} -q 20 -w 15 -h {output.report} -j {params.outdir}/fastp.json --detect_adapter_for_pe 2> {log.stderr} 1> {log.stdout}"

rule bowtie:
    input:
        forward = "results/{sample}/fastp/{sample}_R1_trimmed.fastq.gz",
        reverseR = "results/{sample}/fastp/{sample}_R2_trimmed.fastq.gz"
    output:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}.sam"
    log:
        stdout = "results/{sample}/bowtie2/log-stdout.txt",
        stderr = "results/{sample}/bowtie2/log-stderr.txt"
    benchmark:
        "benchmarks/{sample}.bowtie2.benchmark.txt"
    threads: 30
    shell:
        f"bowtie2 -x Banco_repressor/{config['project_name']} -1 {input.forward} -2 {input.reverseR} -S {output} --very_sensitive --no-unal -p {threads} 2> {log.stderr} 1> {log.stdout}"

rule samtools_view:
    input:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}.sam"
    output:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}.bam"
    shell:
        "samtools view -Sb {input} > {output}"
        
rule samtools_sort:
    input:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}.bam"
    output:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}_sorted.bam"
    shell:
        "samtools sort -o {output} {input}"

rule samtools_index:
    input:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}_sorted.bam"
    output:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}_sorted.bam.bai"
    shell:
        "samtools index {input}"

rule samtools_idxstats:
    input:
        f"results/{{sample}}/mapped_reads/{{sample}}_vs_{config['project_name']}_sorted.bam"
    output:
        f"results/{{sample}}/idxstats/{{sample}}_vs_{config['project_name']}_idxstats.txt"
    shell:
        "samtools idxstats {input} > {output}"

rule merge_idxstats:
    input:
        expand(
            f"results/{{sample}}/idxstats/{{sample}}_vs_{config['project_name']}_idxstats.txt", 
            sample=config["sample"].keys()
        )
    output:
        f"merged_output/merged_output.tsv"
    shell:
        "python scripts/merge_samples.py --files {input} --output {output}"
