
from Bio import SeqIO


def parse_fasta(file_path):
    sequences = []

    for record in SeqIO.parse(file_path, "fasta"):
        dna_sequence = str(record.seq).upper()
        sequences.append(dna_sequence)

    return sequences


def chunk_sequence(sequence, chunk_size=20):
    chunks = []

    for start in range(0, len(sequence), chunk_size):
        chunk = sequence[start:start + chunk_size]
        chunks.append(chunk)

    return chunks
