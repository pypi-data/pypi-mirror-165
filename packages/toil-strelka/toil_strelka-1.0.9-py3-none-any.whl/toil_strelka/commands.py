"""toil_strelka commands."""

from os.path import join
import glob
import gzip
import os
import shutil
import subprocess

from toil_container import ContainerArgumentParser
from toil_container import ContainerJob
import click

from toil_strelka import __version__
from toil_strelka import validators
from toil_strelka.utils import remove_folder_content


class BaseJob(ContainerJob):

    """A job base class that inherits from `ContainerJob`."""

    def __init__(self, options=None, *args, **kwargs):
        """
        Set variables that will be used in later steps.

        Arguments:
            options (object): an `argparse.Namespace` object with toil options.
            args (list): positional arguments to be passed to `toil.job.Job`.
            kwargs (dict): key word arguments to be passed to `toil.job.Job`.
        """
        runtime = kwargs.pop("runtime", 90)
        memory = kwargs.pop("memory", "4G")

        self._mem = memory
        self.manta_outdir = os.path.join(options.outdir, "manta")
        self.strelka_outdir = os.path.join(options.outdir, "strelka")

        if not os.path.exists(self.strelka_outdir):
            os.makedirs(self.strelka_outdir)

        # Create manta working directory
        if not options.germline:
            if not os.path.exists(self.manta_outdir):
                os.makedirs(self.manta_outdir)

        super().__init__(
            options=options, runtime=runtime, memory=memory, *args, **kwargs
        )

    def add_version_to_vcfs(self, vcfs):
        """Add version to vcfs."""
        for vcf in vcfs:
            self.add_version(vcf)
            self.call(["tabix", "-p", "vcf", "-f", vcf])

    def add_version(self, in_vcf):
        """
        Add toil_strelka version in the output vcf header.

        Args:
            in_vcf (String): Path to the input file.
        """
        self.call(["bgzip", "-d", in_vcf])
        self.call(
            [
                "sed",
                "-i",
                f"2i ##toil_strelka={__version__}",
                in_vcf.split(".gz")[0],
            ]
        )
        self.call(["bgzip", in_vcf.split(".gz")[0]])


class MantaConfig(BaseJob):
    def run(self, fileStore):
        """Configure manta."""
        config_cmd = [
                "configManta.py",
                "--normalBam",
                self.options.normal,
                "--tumorBam",
                self.options.tumor,
                "--referenceFasta",
                self.options.reference,
                "--runDir",
                self.manta_outdir,
                "--callRegions",
                self.options.bed,
            ]

        if self.options.manta_config:
            config_cmd += ["--config", self.options.manta_config]

        self.call(config_cmd)

class MantaRun(BaseJob):
    def run(self, fileStore):
        """Excecute manta."""
        # If rerun, we need to clean the workspace first
        workspace = join(self.manta_outdir, "workspace")
        if len(os.listdir(workspace)):
            remove_folder_content(workspace)

        self.call(
            [
                "python2",
                join(self.manta_outdir, "runWorkflow.py"),
                "-m",
                "local",
                "-j",
                self.options.manta_jobs,
                "-g",
                self._mem.strip("G"),
            ]
        )

        # add pipeline version to vcf
        self.add_version_to_vcfs(
            glob.glob(join(self.manta_outdir, "results", "variants", "*.vcf.gz"))
        )


class StrelkaConfig(BaseJob):
    def run(self, fileStore):
        """Configure strelka."""
        if self.options.germline:
            workflow = "configureStrelkaGermlineWorkflow.py"
        else:
            workflow = "configureStrelkaSomaticWorkflow.py"

        config_cmd = [
            workflow,
            "--referenceFasta",
            self.options.reference,
            "--callRegions",
            self.options.bed,
            "--runDir",
            self.strelka_outdir,
        ]

        if self.options.strelka_config:
            config_cmd += ["--config", self.options.strelka_config]

        if self.options.germline:
            config_cmd += ["--bam", self.options.normal]

        else:
            indel_candidates = join(
                self.manta_outdir, "results", "variants", "candidateSmallIndels.vcf.gz"
            )

            config_cmd += [
                "--normalBam",
                self.options.normal,
                "--tumorBam",
                self.options.tumor,
                "--indelCandidates",
                indel_candidates,
            ]

        if self.options.sequencing_method in ["WES", "TGD"]:
            config_cmd.extend(["--exome"])

        self.call(config_cmd)


class StrelkaRun(BaseJob):
    def run(self, fileStore):
        """Executre strelka."""
        # If rerun, we need to clean the workspace first
        workspace = join(self.strelka_outdir, "workspace")
        if len(os.listdir(workspace)):
            remove_folder_content(workspace)

        self.call(
            [
                "python2",
                join(self.strelka_outdir, "runWorkflow.py"),
                "-m",
                "local",
                "-j",
                self.options.strelka_jobs,
                "-g",
                self._mem.strip("G"),
            ]
        )

        # Add pipeline version to vcf
        self.add_version_to_vcfs(
            glob.glob(join(self.strelka_outdir, "results", "variants", "*.vcf.gz"))
        )


class SplitGermlineVariants(BaseJob):

    """A job class to split files by SNVs and indels."""

    def run(self, fileStore):
        """Run merge for vcf files."""
        outdir = join(self.strelka_outdir, "results", "variants")
        variants_raw_file = join(outdir, "variants.vcf.gz")
        variants_file = join(outdir, "variants.vcf")
        snvs_file = join(outdir, "snvs.vcf")
        indels_file = join(outdir, "indels.vcf")

        # Normalize and realign indels and split multi-allelic rows.
        self.call(
            [
                "bcftools",
                "norm",
                "-m",
                "-",
                "--fasta-ref",
                self.options.reference,
                "--output",
                variants_file,
                variants_raw_file,
            ]
        )

        os.remove(variants_raw_file)
        self.call(["bgzip", "-f", variants_file])
        variants_file += ".gz"
        self.call(["tabix", "-fp", "vcf", variants_file])

        # Split variants
        with gzip.open(variants_file, "rt") as variants, open(
            snvs_file, "wt", encoding="utf-8"
        ) as snvs, open(indels_file, "wt", encoding="utf-8") as indels:
            for line in variants:
                if line.startswith("#"):
                    snvs.write(line)
                    indels.write(line)
                elif "CIGAR=" in line:
                    indels.write(line)
                else:
                    snvs.write(line)

        self.call(["bgzip", snvs_file])
        self.call(["bgzip", indels_file])
        self.call(["tabix", "-fp", "vcf", snvs_file + ".gz"])
        self.call(["tabix", "-fp", "vcf", indels_file + ".gz"])


class CleanUp(BaseJob):
    def run(self, fileStore):
        """Clean up intermediate files."""
        for i in [self.manta_outdir, self.strelka_outdir]:
            shutil.rmtree(join(i, "workspace"), ignore_errors=True)


def run_toil(options):
    """Toil implementation for toil_strelka."""
    # memory requested here must be below the memory available by docker
    run_kwargs = dict(options=options, memory=options.memory, runtime=options.runtime)

    # setup jobs
    if not options.germline:
        manta_config_node = MantaConfig(options=options)
        manta_run_node = MantaRun(cores=options.manta_jobs, **run_kwargs)
    else:
        strelka_split_node = SplitGermlineVariants(options=options)

    strelka_config_node = StrelkaConfig(options=options)
    strelka_run_node = StrelkaRun(cores=options.strelka_jobs, **run_kwargs)
    clean_up_node = CleanUp(options=options)

    # build DAG
    if options.germline:
        head_node = strelka_config_node
        strelka_config_node.addFollowOn(strelka_run_node)
        strelka_run_node.addFollowOn(strelka_split_node)
        strelka_split_node.addFollowOn(clean_up_node)

    else:
        head_node = manta_config_node
        manta_config_node.addFollowOn(manta_run_node)
        manta_run_node.addFollowOn(strelka_config_node)
        strelka_config_node.addFollowOn(strelka_run_node)
        strelka_run_node.addFollowOn(clean_up_node)

    # Run workflow
    ContainerJob.Runner.startToil(head_node, options)


def get_parser():
    """Get pipeline configuration using toil's."""
    parser = ContainerArgumentParser(
        version=__version__, description="toil_strelka pipeline"
    )

    settings = parser.add_argument_group("strelka arguments")

    settings.add_argument(
        "--normal",
        help="Path of normal bam file.",
        required=True,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--tumor",
        help="Path of tumor bam file.",
        required=False,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--outdir",
        help="Output directory",
        required=True,
        type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    )

    settings.add_argument(
        "--reference",
        help="Reference .fasta",
        required=True,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--bed",
        help="bed file of the TGD panel",
        required=True,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--sequencing_method",
        required=True,
        help="one of {WGS, WES, TGD}",
        type=click.Choice(["WGS", "WES", "TGD"]),
    )

    settings.add_argument(
        "--manta_jobs",
        required=False,
        default="2",
        help="number of parallel jobs to run in manta",
    )

    settings.add_argument(
        "--manta_config",
        help="Custom Manta configuration",
        required=False,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--strelka_jobs",
        required=False,
        default="2",
        help="number of parallel jobs to run in strelka",
    )

    settings.add_argument(
        "--strelka_config",
        help="Custom Strelka configuration",
        required=False,
        type=click.Path(file_okay=True, readable=True, resolve_path=True),
    )

    settings.add_argument(
        "--germline",
        required=False,
        action="store_true",
        help="True if to run germline workflow (default: False)",
    )

    settings.add_argument(
        "--runtime",
        help="runtime for strelka and manta jobs",
        default=None,
        required=False,
    )

    settings.add_argument(
        "--memory",
        help="memory for strelka and manta jobs",
        default="32G",
    )

    return parser


def process_parsed_options(options):
    """Perform validations and add post parsing attributes to `options`."""
    if options.writeLogs is not None:
        subprocess.check_call(["mkdir", "-p", options.writeLogs])
    return options


def main():
    """Parse options and run toil."""
    options = get_parser().parse_args()

    # Check if required executables are in the PATH
    if not (options.docker or options.singularity):  # pragma: no cover
        validators.validate_programs_exist(
            [
                "configManta.py",
                "configureStrelkaSomaticWorkflow.py",
                "configureStrelkaGermlineWorkflow.py",
            ]
        )

    if not options.germline and not options.tumor:  # pragma: no cover
        msg = "Tumor bam file (--tumor) is needed for somatic variant calling."
        raise click.UsageError(msg)

    options = process_parsed_options(options=options)
    run_toil(options=options)


if __name__ == "__main__":
    main()  # pragma: no cover
