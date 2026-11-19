
import time

from src.genome_parser import parse_fasta, chunk_sequence
from src.alignment import find_off_targets


def main():

    file_path = "data/mock_genome.fasta"

    guide = "ATGCGTAC"

    print("================================")
    print("         GENEWEAVER")
    print("================================")

    print("\nReading FASTA file...")

    sequences = parse_fasta(file_path)

    genome = "".join(sequences)

    print("Genome loaded successfully!")
    print("Genome length:", len(genome))

    print("\nDividing genome into chunks...")

    chunks = chunk_sequence(genome, 20)

    print("Total chunks:", len(chunks))

    print("\nRunning CPU alignment...")

    start_time = time.perf_counter()

    results = find_off_targets(genome, guide)

    end_time = time.perf_counter()

    execution_time = end_time - start_time

    print("\nCPU ALIGNMENT RESULTS")

    print("Guide sequence:", guide)
    print("Potential matches:", len(results))
    print("Execution time:", execution_time, "seconds")

    print("\nFirst few matches:")

    for position, mismatches in results[:10]:

        print(
            "Position:", position,
            "| Mismatches:", mismatches
        )


if __name__ == "__main__":
    main()
