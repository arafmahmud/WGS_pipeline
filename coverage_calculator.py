import os
import subprocess
samples = ["PUT SAMPLE IDS HERE" ]
for sample_num in samples:

	maping = "bwa mem -t 12 reference.fa {}/*R1.fastq {}/*R2.fastq > {}/aln_map.sam".format(sample_num,sample_num,sample_num)
	os.system(maping)
	samtobam = "samtools view -S -b {}/aln_map.sam > {}/aln.bam".format(sample_num,sample_num)
	os.system(samtobam)
	bamsort = "samtools sort {}/aln.bam --reference reference.fa > {}/aln_sort.bam".format(sample_num, sample_num)
	os.system(bamsort)
	coverdir = "mkdir coverage"
	os.system(coverdir)
	calculate_coverage = "samtools depth {}/aln_sort.bam".format(sample_num) + "|  awk '" +"{"+ "sum+=$3" +"} END "+ "{" + '''print "{}, ",sum/NR'''.format(sample_num) + "}'" +">"  + "coverage/{}.txt".format(sample_num)
	subprocess.call(calculate_coverage, shell = "true")

catev = "cat coverage/*.txt > covlist.csv"
os.system(catev)

###bwa index -a bwtsw air.fa

