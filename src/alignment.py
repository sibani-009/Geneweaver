
def find_off_targets(genome, guide, max_mismatches=2):

    results = []

    guide_length = len(guide)
    genome_length = len(genome)

    for start in range(genome_length - guide_length + 1):

        section = genome[start:start + guide_length]

        mismatches = 0

        for i in range(guide_length):

            if section[i] != guide[i]:
                mismatches += 1

        if mismatches <= max_mismatches:
            results.append((start, mismatches))

    return results
