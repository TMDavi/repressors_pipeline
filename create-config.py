#!/usr/bin/env python3
#last update David Apr 2025

from os import path
import argparse
import glob
import os

parser = argparse.ArgumentParser(description='Takes all fastq files from a folder and creates a snakemake config file for processing the datasets.')
parser.add_argument('input_folder', type=str, help='Input folder containing the FASTQ files')
parser.add_argument('--config_file', type=str, default='config.yaml', help='File to write config file [default: config.yaml]')
parser.add_argument('--threads', type=int, default=4, help='Maximum number of threads for each task in the pipeline [default: 4]')
parser.add_argument('--project_name', type=str,default='DNA_repressores', help='Project name [default: None]')
args = parser.parse_args()

if path.isdir(args.input_folder):
    config = open(args.config_file, "w")
    config.write("workdir: %s\n\n" % (os.getcwd()))
    config.write("threads: %d\n" % (args.threads))
    config.write("project_name: %s\n" % (args.project_name))
    config.write("samples:\n")
    forward = sorted(glob.iglob(args.input_folder + "/**/*_R1.*", recursive=True))
    for f in forward:
        partition = f.partition("_R1.")
        sample = partition[0].split("/")[-1]
        r = partition[0] + "_R2." + partition[2]
        config.write("    '%s':\n" % (sample))
        config.write("        forward: '%s'\n" % (f))
        config.write("        reverseR: '%s'\n" % (r))
    config.close()
else:
    print("Please provide a folder containing FASTQ files")
