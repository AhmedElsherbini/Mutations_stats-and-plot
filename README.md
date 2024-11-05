# Mutations_stats-and-plot

**Kindly if you find this repo useful for your work, cite & star this repo**

This simple Python3 script aims to analyze your protein or gene alignment file, get the longest conserved region, and statistics of your mutations, and plot them nicely.

## Usage

**Do you have a reference protein (or gene)?**


Well, just put your reference  as the top sequence.

```bash
python mut_stats_plot.py -i test.afa -f fasta -r

```
**No reference?**

No problem

Then, we will consider the most common (base/aa) as the reference.

```bash
python mut_stats_plot.py -i test.afa -f fasta 

```

**Dependencies ?** 

You need to have Biopython, adjusText , pandas, numpy and argparse (get them via pip3 or conda)

**What do I get ?**

1-FASTA file with the longest conserved region in your alignment which can be important for (eg: domain or conserved pocket analysis for protein) or to design a PCR for the gene) 

2-CSV file with the frequency of the mutations in your alignment file. 

4-PDF graph which is similar in concept to Manhattan plot **PS: Y axis here is % not -log(p)!)**.
  ![alt text](https://github.com/AhmedElsherbini/Mutations_stats-and-plot/blob/main/mutations_per_position_atest.afa-1.png)


## Contributing
Everything is CRYSTAL clear. But anyhow, contact us here or directly via email: drahmedsherbini@yahoo.com

