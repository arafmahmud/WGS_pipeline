import os
import argparse


parser = argparse.ArgumentParser(prog="WGS_pipeline.py", formatter_class=argparse.RawTextHelpFormatter, description="""
WGS_pipeline is an automated pipeline for Microbial Sequence assembly\n""",epilog="""
    Examples:
    python3 WGS_pipeline.py -i input_folder""")


parser.add_argument("-i", "--input", type=str, default="", required=True, help="input folder directory")



args = parser.parse_args()

input_dir = "ls {} > samples.txt".format(args.input)
os.system(input_dir)
fol = open("samples.txt", "r")
folder = fol.read()
folders = folder.split("\n")
folders = folders[:-1]
print(folders)

for i in folders:

	unzip = "gzip -d {}/{}/*.gz".format(args.input,i)
	os.system(unzip)
	mkdr = "mkdir {}/{}/fastqc_report {}/{}/trimmed {}/{}/Kraken {}/{}/Kraken/kraken1 {}/{}/Kraken/kraken2".format(args.input,i,args.input,i,args.input,i,args.input,i,args.input,i)
		
	os.system(mkdr)

	fastqc = "fastqc -o {}/{}/fastqc_report -t 2 {}/{}/*.fastq".format(args.input,i,args.input,i)
	os.system(fastqc)
	

	trimmer = "trimmomatic PE -threads 6 {}/{}/{}_R1.fastq {}/{}/{}_R1.fastq -baseout {}/{}/trimmed/trimmed.fastq ILLUMINACLIP:/home/ahmed/NexteraPE-PE.fa:2:30:10:8 HEADCROP:15 SLIDINGWINDOW:4:15 TRAILING:3".format(args.input,i,i,args.input,i,i,args.input,i)
	os.system(trimmer)
	

	assembly = "spades -k 21,33,55,77 --careful --pe1-1 {}/{}/trimmed/*_1P.fastq  --pe1-2 {}/{}/trimmed/*_2P.fastq -o {}/{}/assembly".format(args.input,i,args.input,i,args.input,i)
	os.system(assembly)

	annotation = "prokka --outdir {}/{}/prokka --prefix AMR {}/{}/assembly/contigs.fasta".format(args.input,i,args.input,i)
	os.system(annotation)

	assess = "/home/ahmed/My_tools/quast-5.0.2/quast.py -o {}/{}/quast_results -g {}/{}/prokka/*.gff -t 4 -1 {}/{}/trimmed/*_2P.fastq -2 {}/{}/trimmed/*_2P.fastq --gene-thresholds 1,1000 {}/{}/assembly/contigs.fasta --glimmer".format(args.input,i,args.input,i,args.input,i,args.input,i,args.input,i)
	os.system(assess)
	print(unzip,"\n",mkdr,"\n",  fastqc,"\n", trimmer,"\n", assembly,"\n", annotation,"\n", assess)





