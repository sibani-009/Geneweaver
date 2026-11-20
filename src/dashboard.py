
import asyncio

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, ProgressBar

from src.genome_parser import parse_fasta, chunk_sequence
from src.alignment import find_off_targets
from src.gpu_alignment import find_off_targets_gpu, CUDA_AVAILABLE


class GeneWeaverDashboard(App):

    def compose(self) -> ComposeResult:

        yield Header()

        yield Static(
            "GENEWEAVER - DNA ALIGNMENT ENGINE",
            id="heading"
        )

        yield Static("Starting...", id="status")

        yield ProgressBar(total=1, id="progress")

        yield Static("", id="results")

        yield Footer()

    async def on_mount(self):

        self.run_worker(self.process_genome())

    async def process_genome(self):

        status = self.query_one("#status", Static)
        progress = self.query_one("#progress", ProgressBar)
        results_widget = self.query_one("#results", Static)

        status.update("Reading FASTA file...")

        sequences = parse_fasta("data/mock_genome.fasta")

        genome = "".join(sequences)

        chunks = chunk_sequence(genome, 20)

        progress.update(total=len(chunks), progress=0)

        status.update("Processing genome chunks...")

        for number, chunk in enumerate(chunks, start=1):

            await asyncio.sleep(0.1)

            progress.update(progress=number)

        status.update("Running CPU alignment...")

        guide = "ATGCGTAC"

        cpu_results = find_off_targets(genome, guide)

        if CUDA_AVAILABLE:

            status.update("Running GPU alignment...")

            gpu_results = find_off_targets_gpu(genome, guide)

            gpu_message = f"GPU matches: {len(gpu_results)}"

        else:

            gpu_message = "GPU not available - CPU mode only."

        results_widget.update(
            f"Genome length: {len(genome)}\n"
            f"Total chunks: {len(chunks)}\n"
            f"CPU matches: {len(cpu_results)}\n"
            f"{gpu_message}\n"
            f"Guide sequence: {guide}"
        )

        status.update("Processing completed!")


if __name__ == "__main__":

    GeneWeaverDashboard().run()
