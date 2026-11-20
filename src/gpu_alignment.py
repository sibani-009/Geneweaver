
import numpy as np

try:
    from numba import cuda
    CUDA_AVAILABLE = cuda.is_available()
except Exception:
    CUDA_AVAILABLE = False


if CUDA_AVAILABLE:

    @cuda.jit
    def alignment_kernel(genome, guide, results):

        position = cuda.grid(1)

        if position < len(results):

            mismatches = 0

            for i in range(len(guide)):

                if genome[position + i] != guide[i]:
                    mismatches += 1

            results[position] = mismatches


def encode_sequence(sequence):

    mapping = {
        "A": 0,
        "T": 1,
        "G": 2,
        "C": 3
    }

    return np.array(
        [mapping[base] for base in sequence],
        dtype=np.int32
    )


def find_off_targets_gpu(genome, guide, max_mismatches=2):

    if not CUDA_AVAILABLE:
        print("CUDA GPU is not available.")
        return None

    if len(genome) < len(guide):
        return []

    genome_array = encode_sequence(genome)
    guide_array = encode_sequence(guide)

    total_positions = len(genome) - len(guide) + 1

    output = np.zeros(total_positions, dtype=np.int32)

    d_genome = cuda.to_device(genome_array)
    d_guide = cuda.to_device(guide_array)
    d_output = cuda.to_device(output)

    threads_per_block = 128

    blocks_per_grid = (
        total_positions + threads_per_block - 1
    ) // threads_per_block

    alignment_kernel[blocks_per_grid, threads_per_block](
        d_genome,
        d_guide,
        d_output
    )

    results_array = d_output.copy_to_host()

    results = []

    for position, mismatches in enumerate(results_array):

        if mismatches <= max_mismatches:
            results.append((position, int(mismatches)))

    return results
