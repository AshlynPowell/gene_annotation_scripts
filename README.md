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
- Add the genome assemblies you are using to the `genomes` folder in the format `<species_code>_genome.fasta`. 
- For each gene you are looking for, create a file called `<gene_name>_query.fasta` in the `scripts` directory then paste your query sequences into the file. Make sure you are using the protein sequence (i.e. amino acids not nucleotides) in the fasta format. If possible, it is good to use multiple query sequences for a gene to increase your chances of finding the gene. Query sequences can usually be found on Genbank or in the supplemental materials of a publication.

## Step 3: Make blast databases for genome assemblies
Navigate to the `genomes` directory and activate your conda environment for `blast` (if you don't have conda you can find instructions for installing it here: https://docs.anaconda.com/miniconda/miniconda-install/). 
Then run the following command on each of your genome assemblies. It only takes a second to run so you can do it interactively in your terminal. 
```
makeblastdb -dbtype nucl -in <species_code>_genome.fasta
```
You should now see a number of new files in this folder. 

## Step 4: Blast queries against genomes
You will run the `blast.job` script (and all the other scripts) from the `scripts` folder. Before running this script, make sure to edit the email at the top of the script and the name of the conda environment for blast (if yours is different from what is already in the script). Then, you can run the script with the following command.
```
sbatch blast.job <species_code> <gene_name>
```
You should see a file called `<species_code>_<gene_name>.out` in the `b_results` folder. If you open up that file you should see your blast results in a table format. 

## Step 5: Gene extraction
For this step you will need a conda environment with both `Pyfaidx` and `pandas` installed. Activate that conda environment then run the command below.
```
python gene_ext.py <species_code> <gene_name>
```
If the script outputs "Gene extracted" one or more times then it worked! You should also now see a file called `<species_code>_<gene_name>_gene.fa` in the `genes` folder.  

## Step 6: Initial annotation with augustus
Just like you did for the blast job script, make sure the email and conda environment are correct in `annotation.job` (you need a conda environment with augustus installed). Then run the script as follows.
```
sbatch annotation.job <species_code> <gene_name>
```
Check the `annotation` folder for a file named `<species_code>_<gene_name>.gff` to make sure it ran successfully. 

## Step 7 (optional): Blast queries in alignment format
This step is optional. You now should have all the files needed to manually check the annotation in Geneious Prime. However, if augustus didn't correctly annotate the gene (which is very common in silk genes), this step can help guide you in fixing the annotation. Once again, make sure the email and conda environments are correct in the `blast_align.job` script then run the command below.
```
sbatch blast_align.job <species_code> <gene_name>
```
## Step 8: Manually check/edit your annotation
You'll need to download the files in the `genes` and `annotation` directories. See here (https://rc.byu.edu/wiki/?id=Transferring+Files) for how to copy those files to your personal computer with `scp`. Then upload those files into Geneious Prime. Checking and editing the annotations can be tedious as it is a bit of a trial and error process. Here are some tips and tricks for manual annotations:
- If you are able to find information on the number and size introns/exons that are present in your query sequences on Genbank or in a publication that can help guide you. It may not be exactly the same in the species you're searching in depending on how closely related the species are, but it can give you a better idea of what you're looking for.
- Aligning the gene from your annotation with the query sequences you used can help you determine if you have the whole gene or if you need to add/extend or delete/shorten any exons. Any time you change the annotation, you should realign it with the queries to see your progress. 
- Using the search tool in Geneious Prime can help you find if specific nucleotide or protein sequences are present. This is most helpful if you noticed any motifs that seem more conserved within your query sequences, but that are missing from your annotation. You can search for the motif in Geneious and see if you can add an exon with the motif.  
- The output from `blast_align.job` can show you more precisely where the query aligns with your extracted region and help you know where intron/exon boundaries may be. It can also give you motifs you can look for with the search tool.
- Augustus seems to have trouble with the first exon in silk genes because it's often a short exon followed by a long intron. These can be hard to find manually if they aren't super conserved, but it can be helpful to use Geneious Prime's "Find ORFs" functionality under the "Annotate & Predict" tab to give you some potential first exons. You can also use this to help find internal exons if you check the "Include interior ORFs" box, but it's most helpful for the first exon.
- Any protein involved in silk should have a signal peptide at the beginning. You can check for a signal peptide in your annotation by running SignalP (https://services.healthtech.dtu.dk/services/SignalP-6.0/). If it says "Prediction: Signal Peptide (Sec/SPI)" at the top of the results that means there is a signal peptide in your sequence which can help confirm if you have found the correct first exon.
- You can also run blast in Geneious for a better visual of where blast results are in relation to your annotation. This can be especially helpful in searching for specific exons/regions of the gene that didn't have hits in the `blast_align` output as you can adjust the parameters to be less strict (e.g. smaller word size and higher e-value). Here are the steps for running blast in Geneious:
    - Check the box next the file you are searching and click `Blast` at the top. This should bring up a new window.
    - Click the drop-down for `Add/Remove Databases` and choose `Add Database`.
    - Name your database and make sure `Use 1 selected sequences` is checked then click `OK`.
    - Now click `Blast` at the top again. Click `Enter unformatted or FASTA sequence` for your `Query` and paste the sequence you are searching for.
    - Click the drop-down for `Database` and find the name of the database you just created.
    - To change the blast parameters, click `More Options` at the bottom. You can change the `Max Evalue` and `Word Size` parameters 10 and 2, respectively for a less strict blast search. Then click `Search` at the bottom.
    - Once it is done you can view an alignment of all the results together in a `Query Centric View` or view each result separately to see where they are in relation to your annotation (which can help determine if you have found the correct location of your exons).
- Make sure that anytime you edit the annotation that you are putting intron/exon boundaries at canonical splice sites (i.e. introns should start with GT and end with AG). This can be another confirming factor that you are correctly annotating the gene (i.e. if you are trying to change an intron or exon, whether or not the reading frame works with any of the canonical splice sites can indicate if you're looking in the right spot). 


