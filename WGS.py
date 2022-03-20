import os
import argparse 





parser = argparse.ArgumentParser(prog="WGS.py", formatter_class=argparse.RawTextHelpFormatter, description="""
WGS_pipeline is an automated pipeline for Microbial Sequence assembly\n""",epilog="""
    Examples:
    python3 WGS.py -i input_folder""")


parser.add_argument("-i", "--input", type=str, default="", required=True, help="input folder directory")



args = parser.parse_args()



###########parse sample IDs

input_dir = "ls {} > files.txt".format(args.input)
os.system(input_dir)
fol = open("files.txt", "r")
folder = fol.read()
folders = folder.split("\n")
folders = folders[:-1]
print(folders)


#####################

class WGSpipeline:

	def __init__(self, foldr, sample):
		self.foldr = foldr
		self.sample = sample


	def unzip(self):
		print("🅄🄽🄿🄰🄲🄺🄸🄽🄶...")		
		unpack = "gzip -d {foldr}/{sample}/*.gz".format(foldr = self.foldr, sample = self.sample)
		os.system(unpack)
		


	def mkdr(self):
		mkdr = "mkdir {foldr}/{sample}/fastqc_report {foldr}/{sample}/trimmed".format(foldr = self.foldr, sample = self.sample)
		os.system(mkdr)

	def fastqc(self):
		print("🄶🄴🄽🄴🅁🄰🅃🄸🄽🄶 🅀🄲 🅁🄴🄿🄾🅁🅃....")		
		fqc = "/home/ahmed/lssd_home/FastQC/fastqc -o {foldr}/{sample}/fastqc_report -t 2 {foldr}/{sample}/{sample}*.fastq".format(foldr = self.foldr, sample = self.sample)
		os.system(fqc)
		
	
	def trimmer_fastp(self):
		print("🄿🄴🅁🄵🄾🅁🄼🄸🄽🄶 🅀🅄🄰🄻🄸🅃🅈 🅃🅁🄸🄼🄼🄸🄽🄶....")
		trim = 	"fastp -i {foldr}/{sample}/{sample}_R1.fastq -I {foldr}/{sample}/{sample}_R2.fastq \
			-o {foldr}/{sample}/trimmed/{sample}_R1.fastq -O {foldr}/{sample}/trimmed/{sample}_R2.fastq \
			--trim_front1 15 trim_front2 15 --trim_poly_g --trim_tail1 3 --trim_tail2 3 ".format(foldr = self.foldr, sample = self.sample)
		os.system(trim)

	def assembly(self):
		print("🄰🅂🅂🄴🄼🄱🄻🅈")
		assemble = "spades -k 21,33,55,77 --careful --pe1-1 {foldr}/{sample}/trimmed/{sample}_R1.fastq \
				 --pe1-2 {foldr}/{sample}/trimmed/{sample}_R2.fastq -o {foldr}/{sample}/assembly -t 12".format(foldr = self.foldr, sample = self.sample)
		os.system(assemble)


	def annotate(self):
		print("🄰🄽🄽🄾🅃🄰🅃🄸🄽🄶")
		annotation = "/home/ahmed/My_tools/prokka-master/bin/prokka --outdir {foldr}/{sample}/prokka --prefix {sample} {foldr}/{sample}/assembly/contigs.fasta".format(foldr = self.foldr, sample = self.sample)
		os.system(annotation)

	def assessment(self):
		print("🄰🅂🅂🄴🄼🄱🄻🅈 🄰🅂🅂🄴🅂🅂🄼🄴🄽🅃......")
		assess = "/home/ahmed/My_tools/quast-5.0.2/quast.py -o {foldr}/{sample}/quast_results -g {foldr}/{sample}/prokka/*.gff \
			 -t 12 -1 {foldr}/{sample}/trimmed/*_R1.fastq -2 {foldr}/{sample}/trimmed/*_R2.fastq \
			 --gene-thresholds 1,1000 {foldr}/{sample}/assembly/contigs.fasta --glimmer".format(foldr = self.foldr, sample = self.sample)
		os.system(assess)


for sample_id in folders:
	
	pipeline = WGSpipeline(args.input, sample_id)
	pipeline.unzip()
	pipeline.mkdr()
	pipeline.fastqc()
	pipeline.trimmer_fastp()
	pipeline.assembly()
	pipeline.annotate()
	pipeline.assessment()

os.system("rm -r files.txt")
