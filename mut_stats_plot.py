import argparse
from Bio import AlignIO
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

import argparse
from Bio import AlignIO
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

def extract_conserved_sequence(input_file, file_format, use_reference):
    # Read alignment file
    aln = AlignIO.read(input_file, file_format)
    # Identify consensus sequence or reference sequence
    ref_seq = str(aln[0].seq).upper() if use_reference else None
    # Identify longest conserved region based on alignment
    longest_conserved_segment = find_longest_conserved_segment_in_alignment(aln)

    # Save longest conserved sequence to file
    save_conserved_sequence(longest_conserved_segment, input_file)

    # Analyze mutations
    analyze_mutations(aln, input_file, ref_seq)

def find_longest_conserved_segment_in_alignment(aln):
    alignment_length = aln.get_alignment_length()
    longest_segment = ""
    current_segment = []

    # Loop through each position in alignment
    for position in range(alignment_length):
        column = str(aln[:, position]).upper()

        # Check if all bases in column are identical
        if all(base == column[0] for base in column):
            current_segment.append(column[0])  # Extend current conserved segment
        else:
            # If a break in conservation, evaluate and reset current segment
            if len(current_segment) > len(longest_segment):
                longest_segment = "".join(current_segment)
            current_segment = []  # Reset current segment

    # Final check in case the longest segment is at the end
    if len(current_segment) > len(longest_segment):
        longest_segment = "".join(current_segment)

    return longest_segment

def save_conserved_sequence(longest_segment, input_file):
    with open(f"longest_conserved_{input_file}.fasta", "w") as result_file:
        result_file.write(f">longest_conserved_sequence_in_{input_file}\n{longest_segment}")
    print(f"Saved longest conserved sequence to 'longest_conserved_{input_file}.fasta'")

def analyze_mutations(aln, input_file, reference_seq=None):
    alignment_length = aln.get_alignment_length()
    mutation_data = []
    positions = []
    mutation_frequencies = []
    total_sequences = len(aln)

    for position in range(alignment_length):
        column = str(aln[:, position]).upper()
        counts = Counter(column)
        freq_dict = {base: count / total_sequences * 100 for base, count in counts.items()}

        # Determine wild type base
        if reference_seq and position < len(reference_seq):
            wild_type = reference_seq[position]
        else:
            wild_type = max(freq_dict, key=freq_dict.get) if freq_dict else ""

        mutations = {base: freq for base, freq in freq_dict.items() if base != wild_type}
        top_mutation = max(mutations, key=mutations.get) if mutations else ""
        top_mutation_freq = mutations[top_mutation] if top_mutation else 0

        positions.append(position + 1)
        mutation_data.append(f"{wild_type}{position + 1}{top_mutation}" if top_mutation else "Conserved")
        mutation_frequencies.append(top_mutation_freq)

    save_mutation_data(mutation_data, positions, mutation_frequencies, input_file)
    create_mutation_plot(positions, mutation_data, mutation_frequencies, input_file)

# Additional code for mutation saving, plotting, and command-line interface remains unchanged




def save_mutation_data(mutation_data, positions, mutation_frequencies, input_file):
    mutation_df = pd.DataFrame({
        "Position": positions,
        "WT -> mutant": mutation_data,
        "Mutation Frequency %": mutation_frequencies,
    })
    mutation_df = mutation_df[(mutation_df != 0).all(1)]
    mutation_df.to_csv(f"mutations_{input_file}.csv", index=False)
    print(f"Saved mutation data to 'mutations_{input_file}.csv'")

def create_mutation_plot(positions, mutation_data, mutation_frequencies, input_file):
    plt.figure(figsize=(12, 7))
    plt.scatter(positions, mutation_frequencies, color="blue", label="Top Mutation Frequency %")
    plt.axhline(y=10, color='red', linestyle='--', label="10% mutations frequency threshold")
    plt.xlabel("Position")
    plt.ylabel("Top Mutation Frequency %")
    plt.title("Mutation Prevalence by Position")
    plt.legend()

    # List to store text annotations for adjustment
    texts = []

    # Annotate only mutations with frequency > 10%
    for i, freq in enumerate(mutation_frequencies):
        if freq > 10:
            text = plt.text(
                positions[i], freq, mutation_data[i], 
                ha='center', va='bottom', fontsize=9, color='darkgreen',
                bbox=dict(facecolor="white", edgecolor="none", boxstyle="round,pad=0.2")
            )
            texts.append(text)

    # Use adjust_text to prevent overlaps
    adjust_text(
        texts, 
        arrowprops=dict(arrowstyle="->", color='gray', lw=0.5),  # Optional arrows for clarity
        only_move={'points': 'y', 'text': 'xy'},
        expand_points=(1.2, 1.4),
        force_text=(0.5, 1)
    )

    plt.tight_layout()
    plt.savefig(f"mutations_per_position_{input_file}.pdf", format="pdf")
    plt.close()
    print(f"Saved mutation prevalence plot to 'mutations_per_position_{input_file}.jpg'")

def extract_mutations_per_sequence(input_file, file_format, use_reference):
    aln = AlignIO.read(input_file, file_format)

    mutation_data = []
    sequence_ids = []

    if use_reference:
        for y in list(aln):
            for x in range(len(aln[0].seq)):
                if str((aln[0].seq)[x].upper()) != str((y.seq)[x].upper()):
                    sequence_ids.append(y.id)
                    mutation_data.append("%s%d%s," % (str((aln[0].seq)[x]), int(x + 1), str((y.seq)[x])))
    else:
        for y in list(aln):
            for x in range(len(aln[0].seq)):
                cc = Counter(str(aln[:, x].upper()))
                cc = cc.most_common()
                if str(cc[0][0].upper()) != str((y.seq)[x].upper()):
                    sequence_ids.append(y.id)
                    mutation_data.append("%s%d%s," % (str(cc[0][0]), int(x + 1), str((y.seq)[x])))

    save_mutations_per_sequence(sequence_ids, mutation_data, input_file)

def save_mutations_per_sequence(sequence_ids, mutation_data, input_file):
    df = pd.DataFrame({"Seq_ID": sequence_ids, "mutation": mutation_data})
    df_grouped = df.groupby(['Seq_ID']).sum()
    mutation_counts = df_grouped.mutation.value_counts()

    df_grouped.to_csv(f"mutations_per_seq_{input_file}.csv")
    mutation_counts.to_csv(f"mutations_combination_freq_{input_file}.csv")
    
    print(f"Saved mutation data to 'mutations_per_seq_{input_file}.csv'")
    print(f"Saved mutation combination frequency to 'mutations_combination_freq_{input_file}.csv'")

def main():
    parser = argparse.ArgumentParser(description="Extract conserved sequences and analyze mutations.")
    parser.add_argument("-i", "--input", required=True, help="Input alignment file name.")
    parser.add_argument("-f", "--format", required=True, help="Format of the alignment file (e.g., clustal, fasta, phylip, stockholm).")
    parser.add_argument("-r", "--reference", action="store_true", help="Use the first sequence as the reference.")
    args = parser.parse_args()

    extract_conserved_sequence(args.input, args.format, args.reference)
    extract_mutations_per_sequence(args.input, args.format, args.reference)

if __name__ == "__main__":
    main()

