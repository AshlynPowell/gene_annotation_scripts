#!/usr/bin/env python3
import sys
import os
import pandas as pd
from pyfaidx import Fasta

species = sys.argv[1]
gene = sys.argv[2]
b_result = "../b_results/" + species + "_" + gene + ".out"
genome_path = "../genomes/" + species + "_genome.fasta"
output_path = "../genes/" + species + "_" + gene + "_gene.fa"

genome = Fasta(genome_path)

flank=50000
bit_score = 45
print_messages = True

if (not os.path.isfile(b_result)):
        print("No blast result file")
        exit()

def check_flank(coords):
        if coords['first'] < -1:
                coords['first'] = 0
        contig_length = len(genome[coords['contig']])
        if coords['last'] > contig_length:
                coords['last'] = contig_length

        return coords

def write_file(coords, output_path, i):
        if i == 0:
                with open(output_path, "w") as output:

                        seq = genome[coords['contig']][coords['first']:coords['last']]

                        if coords['reverse']:
                                seq = reverse_complement(seq)

                        output.write(f">{species}_{gene}_(contig:{coords['contig']})\n{str(seq)}\n")
                        print("Gene extracted")
        else:
                with open(output_path, "a") as output:

                        seq = genome[coords['contig']][coords['first']:coords['last']]

                        if coords['reverse']:
                                seq = reverse_complement(seq)

                        output.write(f">{species}_{gene}_(contig:{coords['contig']})\n{str(seq)}\n")
                        print("Gene extracted")

def get_coords(contig_rows, contig):  #The df is made out of the ouput file of the blast run.

        reverse = 0
        forward = 0
        all_values = []

        for row in contig_rows:

                start = int(row[8])
                end = int(row[9])

                if start < end:
                        forward += 1
                else:
                        reverse += 1

                all_values.append(start)
                all_values.append(end)

        coords = {'first':min(all_values) - flank, 'last':max(all_values) + flank, 'contig':contig, "reverse":reverse>forward}
        return(coords)

def gene_ext(b_reult, flank):  #The df is made out of the ouput file of the blast run.
        all_coords = []

        df = pd.read_csv(b_result, sep="\t", header=None, names=["query acc.ver", "subject acc.ver", "% identity", "alignment length", "mismatches", "gap opens", "q. start", "q. end", "s. start", "s. end", "evalue", "bit score"])
        top_scores = df.loc[(df['bit score'] >= bit_score)].drop_duplicates(subset=['subject acc.ver'])
        top_contigs = top_scores['subject acc.ver'].tolist()
        if top_contigs == []:
                print(f"Need better blast results (bit score >= {bit_score})")
                exit()

        for contig in top_contigs:        
                contig_rows = df.loc[(df['subject acc.ver'] == contig)].values.tolist()
                coords = get_coords(contig_rows, contig)
                all_coords.append(coords)

        return(all_coords)


def reverse_complement(seq):
        new_seq = ""
        complement = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N', 'n':'n', 'a':'t', 't':'a', 'c':'g', 'g':'c'}
        for nuc in seq:
                new_seq = new_seq + str(complement.get(str(nuc)))
        return new_seq[::-1]



all_coords = gene_ext(b_result, flank)
for i, coords in enumerate(all_coords):
        coords = check_flank(coords)
        write_file(coords, output_path, i)



