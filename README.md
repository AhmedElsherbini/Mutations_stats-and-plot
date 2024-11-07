# Mutations_stats-and-plot

**Kindly if you find this repo useful for your work, cite & star this repo**

This simple Python3 script aims to analyze your protein (or gene) alignment file, get the longest conserved region, and statistics of your mutations, and plot them nicely in a way similar to the Manhattan GWAS plot.

## Usage

**Do you have a reference protein (or gene) in your alignment file?**


Well, just put your reference  as the top sequence.

```bash
python mut_stats_plot.py -i test.afa -f fasta -r

```
**No reference?**

No problem

Then, we do not provide <code>-r</code> argument. And we will consider the most common (base/aa) as the reference.

```bash
python mut_stats_plot.py -i test.afa -f fasta 

```

**Dependencies ?** 

You need to have Biopython, adjusText , pandas, numpy and argparse (get them via pip3 or conda)

**What do you get ?**

1-FASTA file with the longest conserved region in your alignment which can be important for (eg: domain or conserved pocket analysis of your favorite protein) or to design a PCR for your gene-of-interest) 

2-CSV file with the frequency (%) of the mutations in your alignment file. 

3-CSV file with the  frequency (count) of mutation combination pattern to answer a question like **Which mutation comes with which mutation ?**  

4-CSV file with the mutation per each sequence.

5-a graph in PDF format which is similar in concept to the Manhattan GWAS plot (the dashed line is 10 %).
**PS: Y axis is % NOT -log(p)**


![alt text](https://github.com/AhmedElsherbini/Mutations_stats-and-plot/blob/main/mutations_per_position_atest.afa-1.png)




## Contributing
Everything is CRYSTAL clear. But anyhow, contact us here or directly via email: drahmedsherbini@yahoo.com

