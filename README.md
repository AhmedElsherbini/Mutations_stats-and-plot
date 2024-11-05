# Mutations_stats-and-plot

**Kindly if you find this repo useful for your work, cite & star this repo**

This simple Python3 script aims to analyze your protein or gene alignment file, get the longest conserved region, and statistics of your mutations, and plot them nicely.

## Usage

Do you have a reference?
Well, just arrange it as the top sequence.

```bash
python mut_stats_plot.py -i test.afa -f fasta -r

```

No reference! No problem my friend, then, we will consider the most common (base/aa) as the reference.

```bash
python mut_stats_plot.py -i test.afa -f fasta 

```

As dependencies, you need to have Biopython and argparse (get them via pip3 or conda)


## Contributing
Everything is CRYSTAL clear. But anyhow, contact us here or directly via email: drahmedsherbini@yahoo.com

