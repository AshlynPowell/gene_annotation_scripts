# Gene Annotation Scripts
This repository includes scripts for pulling and annotating individual genes from whole genome assemblies (primarily silk genes from caddisfly genomes). 

## Step 1: Set up directories
You will need to create a number of directories that the scripts will use to access and store the different files used throughout the annotation process. The following command will create all the directories you will need.
```
mkdir annotation b_results b_results_align genes genomes scripts
```
## Step 2: Add scripts and input files
Next, you need to add all of the scripts and input files listed below. Make sure to follow the formats given for the file names so you don't run into errors later on. 
- Add all of the scripts from this repository to the `scripts` directory you just created. 
- Add the genome assemblies you are searching to the `genomes` folder in the format `<species_code>_genome.fasta`. 
- For each gene you are looking for, create a file called `<gene_name>_query.fasta` in the `scripts` directory then paste your query sequences into the file. Make sure you are using the protein sequence (i.e. amino acids not nucleotides) in the fasta format. If possible, it is good to use multiple query sequences for a gene (i.e. the same gene in multiple closely related species) to increase your chances of finding the gene. Query sequences can usually be found on Genbank or in the supplemental materials of publications.

## Step 3: Make blast databases for genome assemblies
Navigate to the `genomes` directory and activate your conda enviroment for `blast` (if you don't have conda you can find instructions for installing it here: https://docs.anaconda.com/miniconda/miniconda-install/). 
The run the following command on each of your genome assemblies. It only takes a second to run so you can do it interactively. 
```
makeblastdb -dbtype nucl -in <species_code>_genome.fasta
```
You should now see a number of new files in this folder. 

## Step 4: Blast queries against genomes
You will run the `blast.job` script from the `scripts` folder. Before running this script, make sure to edit the email at the top of the script and the name of the conda environment for blast (if yours is different from what is already in the script). Then, you can run the script with the following command.
```
sbatch blast.job <species_code> <gene_name>
```
You should see a file called `<species_code>_<gene_name>.out` in the `b_results` folder. If you open up that file you should see your blast results in a table format. 

## Step 5: Extract genes from genomes
For this step you will need a conda environment with `Pyfaidx` and `pandas` installed. Activate that conda environment then run the command below.
```
python gene_ext.py <species_code> <gene_name>
```
If the script outputs "Gene extracted" one or more times then it worked! You should also now see a file called `<species_code>_<gene_name>_gene.fa` in the `genes` folder.  

## Step 6: Initial annotation with augustus
Just like you did for the blast job script, make sure the email and conda environment are correct in `annotation.job` (you need a conda environemnt with augustus installed). Then run the script as follows.
```
sbatch annotation.job <species_code> <gene_name>
```
Check the `annotation` folder for a file named `<species_code>_<gene_name>.gff` to make sure it ran successfully. 

## Step 7 (optional): Blast queries in alignment format
This step is optional. You now should have all the files needed to manually check the annotation in Geneious Prime. However, if augustus didn't correctly annotate the gene (which is highly likely), this step can help guide you in fixing the annotation. Once again, make sure the email and conda environments are correct in the `blast_align.job` script then run the command below.
```
sbatch blast_align.job <species_code> <gene_name>
```
## Step 8: Manually check/edit your annotation
You'll need to download the files in the `genes` and `annotation` directories. See here (https://rc.byu.edu/wiki/?id=Transferring+Files) for how to copy those files to your personal computer with `scp`. Then upload those files into Geneious Prime. Checking and editing the annotations can be tedious as it is a bit of a trial and error process. If you are able to find information on how many introns/exons are present in the query sequences you used that can help guide you. Additionally, the output from `blast_align.job` can show you where the query aligns with your extracted region. Here is a general description of the manual annotation process. (**Copied from opsin paper supplement, need to edit a bit - add running signalp**)

To manually verify the annotation for each opsin sequence, we first aligned the translation—from the AUGUSTUS annotation—with the outgroup sequences of the same opsin type using MUSCLE (Edgar, 2004). In instances where the caddisfly opsin sequence did not fully align with the outgroup sequences, the annotation was manually modified in Geneious Prime v2023.0.4 (https://www.geneious.com) until the entire gene sequence aligned with the outgroups. This was done by first removing or shortening CDS regions that did not align with or varied greatly from the outgroup sequences, causing large gaps in the alignment. Then, for regions of the gene that were present in the outgroup sequences but missing from the annotation, we used the search tool in Geneious to find conserved motifs from within those regions and added or extended CDS annotations accordingly. When extending and shortening the CDS regions of the annotation, we ensured that every intron region occurred at canonical splice sites. After we made these manual adjustments to the annotation, we re-aligned the translation with the outgroup sequences, and the alignment was reassessed for completeness, i.e. that all exons and core motif regions were present in the alignment for each sequence from each species. If additional changes were necessary, the same process of adjusting the annotation was followed until the gene aligned with the outgroup sequences. 

