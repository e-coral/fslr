# FSLR

- [Overview](#overview) 
- [Installation guide](#installation-guide)
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Options](#options)
- [Outputs](#outputs)
- [Tests](#tests)

## Overview
FSLR (Fusion-Seq Long Read) was designed for the sequence characterization of long-read amplicons 
generated using ONT R9/10 flow cells. FSLR facilitates the alignment of long-reads and clusters events with multiple 
supporting reads.

## Installation guide

```
git clone https://github.com/kcleal/fslr.git
cd fslr
pip install -r requirements.txt
pip install .
```
Typical install time on a standard computer: ~1s

## Dependencies

### Software

* bwa: bwa-0.7.19 (r1273) available at: https://github.com/lh3/bwa
* tantan: version: tantan 49, available at: https://gitlab.com/mcfrith/tantan
* samtools: version: samtools 1.21, htslib 1.22.1, available at: https://github.com/samtools
* dodi: version: dodi-0.4.6, available at: https://github.com/kcleal/dodi
* abpoa: version 1.5.1, available at: https://github.com/yangao07/abPOA

### Operating system

FSLR was tested on:
* Linux
* macOS

## Usage

```
fslr --name samp1 \
     --out samp1_out \
     --ref T2T.fa \
     --primers 21q1,17p6 \
     --basecalled basecalled/samp1/pass \
     --procs 16
     --cluster-mask subtelomere,L1_TALEN
```

## Options

| Option                    | Description                                                                                                                                         |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| `--name`                  | Sample name.                                                                                                                                        |
| `--out`                   | Output folder.                                                                                                                                      |
| `--ref`                   | Reference genome.                                                                                                                                   |
| `--basecalled`            | Folder of basecalled reads in fastq format to analyse.                                                                                              |
| `--primers`               | Comma-separated list of primer names. Make sure these are listed in primers.csv.                                                                    |
| `--trim-threshold`        | Threshold in range 0-1. Fraction of maximum primer alignment score; primer sites with lower scores are labelled False.                              |
| `--keep-temp`             | Keep temp files.                                                                                                                                    |
| `--regions`               | Target regions in bed form to perform biased mapping.                                                                                               |
| `--bias`                  | Multiply alignment score by bias if alignment falls within target regions.                                                                          |
| `--procs`                 | Number of processors to use.                                                                                                                        |
| `--skip-alignment`        | Skip alignment step.                                                                                                                                |
| `--skip-interval-cluster` | Skip clustering step.                                                                                                                               |
| `--jaccard-cutoffs`       | Comma-separated list of Jaccard similarity thresholds for N-1 intersections e.g. where index=0 corresponds to one the threshold for 1 intersection. |
| `--overlap`               | A number between 0 and 1. Zero means two reads don't overlap at all, while 1 means the start and end of the reads is identical.                     |
| `--n-alignment-diff`      | How much the number of alignments in one cluster can differ. Fraction in the range 0-1.                                                             |
| `--qlen-diff`             | Max difference in query length. Fraction in the range 0-1.                                                                                          |
| `--cluster-mask`          | Comma separated list of regions/chromosomes to be excluded from the clustering e.g.:                                                                |
|                           | subtemoleric regions, L1_TALEN.                                                                                                                     |
| `--filter-false`          | Use reads with both primers labeled.                                                                                                                |

## Outputs

Out folder:

* .without_primers.fq: Contains sequences of reads without identifiable primers.
* .mappings.bed: A text file that stores genomic regions as coordinates associated with the split-reads.
* .mappings.cluster.bed: Contains the same information about the reads as .mappings.bed with two additional columns; cluster and n_reads. The cluster column stores the cluster id-s of the reads. The n_reads column shows the number of reads within a cluster.
* .mappings_merged.bed: This file contains genomic regions of all the "singletons" from the initial alignment and the re-aligned consensus sequences.
* .bwa_dodi.bam: Alignment file after the initial alignment step.
* .bwa_dodi_cluster_merged.bam: Alignment file containing the "singletons" and the consensus sequences.
* .bai: Index files.
* .filter_counts_summary.csv: Contains information about the filtered reads.

Out/cluster folder:

* .cluster.consensus.fa: Consensus sequences of each cluster.
* .cluster.without_primers.fq: Consensus sequences without an identified primer.
* abpoa_logfile.txt: Messages (standard output) created by abPOA while generating the consensus sequences.
* .cluster.purity.csv: List the cluster id-s, the number of reads within a cluster, the consensus sequences and the proportion of reads within a cluster that have a specific primer.

## Tests

Run test from the fslr directory using:
```
python -m unittest discover -v
```
 Typical test runtime: ~7s

