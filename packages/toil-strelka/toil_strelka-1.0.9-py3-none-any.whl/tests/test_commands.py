"""toil_strelka commands tests."""

from os.path import join

import gzip
import os

from toil_strelka import commands
from toil_strelka import __version__
from tests.utils import TEST

# Expected somatic calls
EXPECTED_SNP_1 = "2\t477\t.\tC\tA\t.\tPASS"
EXPECTED_SNP_2 = "2\t503\t.\tG\tT\t.\tPASS"
EXPECTED_INDEL_1 = "2\t529\t.\tG\tGT\t.\tPASS"
EXPECTED_INDEL_2 = "2\t123601\t.\tTG\tT\t.\tLowEVS"

# Expected germline calls
EXPECTED_VARIANT_1 = "2\t118418\t.\tA\tC\t2\tLowGQX"
EXPECTED_VARIANT_2 = "2\t118440\t.\tT\tC\t56\tLowGQX"
EXPECTED_VARIANT_3 = "2\t123513\t.\tT\tTG\t3070\tPASS"
EXPECTED_VARIANT_4 = "2\t123601\t.\tTG\tT\t3070\tPASS"


def get_variant_lines(content):
    """Count the number of variants."""
    return len([v for v in content.strip().split("\n") if not v.startswith("#")])


def test_run_somatic_toil(tmpdir):
    """Sample test for the main command."""
    outdir = tmpdir.strpath
    jobstore = join(outdir, "jobstore")
    reference = TEST["reference"]
    bedfile = TEST["bedfile"]
    normal = TEST["normal"]
    tumor = TEST["tumor"]
    manta_conf = TEST["manta_config"]
    strelka_conf = TEST["strelka_config"]
    args = [
        jobstore,
        "--stats",
        "--disableCaching",
        "--realTimeLogging",
        "--writeLogs",
        join(outdir, "logs_toil"),
        "--logFile",
        join(outdir, "head_job.toil"),
        "--logLevel",
        "INFO",
        "--sequencing_method",
        "TGD",
        "--normal",
        normal,
        "--tumor",
        tumor,
        "--outdir",
        outdir,
        "--reference",
        reference,
        "--bed",
        bedfile,
        "--manta_config",
        manta_conf,
        "--strelka_config",
        strelka_conf,
        "--memory",
        "4G",
    ]

    # Get and validate options.
    parser = commands.get_parser()
    options = parser.parse_args(args)
    options = commands.process_parsed_options(options)

    # Call pipeline
    commands.run_toil(options)

    # Check Manta files exist
    manta_SV = join(outdir, "manta", "results", "variants", "somaticSV.vcf.gz")

    with gzip.open(manta_SV, "rt") as f:
        content = f.read()
        assert f"##toil_strelka={__version__}\n" in content

    # Check if the output files are correct
    strelka_snvs = join(outdir, "strelka", "results", "variants", "somatic.snvs.vcf.gz")
    strelka_indels = join(
        outdir, "strelka", "results", "variants", "somatic.indels.vcf.gz"
    )

    with gzip.open(strelka_snvs, "rt") as f:
        content = f.read()
        assert EXPECTED_SNP_1 in content
        assert EXPECTED_SNP_2 in content
        assert f"##toil_strelka={__version__}\n" in content

    with gzip.open(strelka_indels, "rt") as f:
        content = f.read()
        assert EXPECTED_INDEL_1 in content
        assert EXPECTED_INDEL_2 in content
        assert f"##toil_strelka={__version__}\n" in content

    # Check if intermediate files are cleaned up
    assert not os.path.isdir(join(outdir, "manta", "workspace"))
    assert not os.path.isdir(join(outdir, "strelka", "workspace"))


def test_run_somatic_toil_no_conf(tmpdir):
    """Sample test for the main command."""
    outdir = tmpdir.strpath
    jobstore = join(outdir, "jobstore")
    reference = TEST["reference"]
    bedfile = TEST["bedfile"]
    normal = TEST["normal"]
    tumor = TEST["tumor"]
    args = [
        jobstore,
        "--stats",
        "--disableCaching",
        "--realTimeLogging",
        "--writeLogs",
        join(outdir, "logs_toil"),
        "--logFile",
        join(outdir, "head_job.toil"),
        "--logLevel",
        "INFO",
        "--sequencing_method",
        "TGD",
        "--normal",
        normal,
        "--tumor",
        tumor,
        "--outdir",
        outdir,
        "--reference",
        reference,
        "--bed",
        bedfile,
        "--memory",
        "4G",
    ]

    # Get and validate options.
    parser = commands.get_parser()
    options = parser.parse_args(args)
    options = commands.process_parsed_options(options)

    # Call pipeline
    commands.run_toil(options)

    # Check Manta files exist
    manta_SV = join(outdir, "manta", "results", "variants", "somaticSV.vcf.gz")

    with gzip.open(manta_SV, "rt") as f:
        content = f.read()
        assert f"##toil_strelka={__version__}\n" in content

    # Check if the output files are correct
    strelka_snvs = join(outdir, "strelka", "results", "variants", "somatic.snvs.vcf.gz")
    strelka_indels = join(
        outdir, "strelka", "results", "variants", "somatic.indels.vcf.gz"
    )

    with gzip.open(strelka_snvs, "rt") as f:
        content = f.read()
        assert EXPECTED_SNP_1 in content
        assert EXPECTED_SNP_2 in content
        assert f"##toil_strelka={__version__}\n" in content

    with gzip.open(strelka_indels, "rt") as f:
        content = f.read()
        assert EXPECTED_INDEL_1 in content
        assert EXPECTED_INDEL_2 in content
        assert f"##toil_strelka={__version__}\n" in content

    # Check if intermediate files are cleaned up
    assert not os.path.isdir(join(outdir, "manta", "workspace"))
    assert not os.path.isdir(join(outdir, "strelka", "workspace"))


def test_run_germline_toil(tmpdir):
    """Sample test for the main command."""
    outdir = tmpdir.strpath
    jobstore = join(outdir, "jobstore")
    reference = TEST["reference"]
    bedfile = TEST["bedfile"]
    normal = TEST["normal"]

    args = [
        jobstore,
        "--stats",
        "--disableCaching",
        "--realTimeLogging",
        "--writeLogs",
        join(outdir, "logs_toil"),
        "--logFile",
        join(outdir, "head_job.toil"),
        "--logLevel",
        "INFO",
        "--sequencing_method",
        "TGD",
        "--normal",
        normal,
        "--outdir",
        outdir,
        "--reference",
        reference,
        "--bed",
        bedfile,
        "--germline",
        "--memory",
        "4G",
    ]

    # Get and validate options.
    parser = commands.get_parser()
    options = parser.parse_args(args)
    options = commands.process_parsed_options(options)

    # Call pipeline
    commands.run_toil(options)

    # Check if the output files are correct
    strelka_outdir = join(outdir, "strelka", "results", "variants")
    strelka_variants = join(strelka_outdir, "variants.vcf.gz")

    with gzip.open(strelka_variants, "rt") as f:
        content = f.read()
        assert EXPECTED_VARIANT_1 in content
        assert EXPECTED_VARIANT_2 in content
        assert EXPECTED_VARIANT_3 in content
        assert EXPECTED_VARIANT_4 in content
        assert f"##toil_strelka={__version__}\n" in content

    variants_count = get_variant_lines(content)

    freebayes_snvs = join(strelka_outdir, "snvs.vcf.gz")
    with gzip.open(freebayes_snvs, "rt") as f:
        content = f.read()
        assert EXPECTED_VARIANT_1 in content
        assert EXPECTED_VARIANT_2 in content
        assert EXPECTED_VARIANT_3 not in content
        assert EXPECTED_VARIANT_4 not in content

    snvs_count = get_variant_lines(content)

    freebayes_indels = join(strelka_outdir, "indels.vcf.gz")
    with gzip.open(freebayes_indels, "rt") as f:
        content = f.read()
        assert EXPECTED_VARIANT_1 not in content
        assert EXPECTED_VARIANT_2 not in content
        assert EXPECTED_VARIANT_3 in content
        assert EXPECTED_VARIANT_4 in content

    indels_count = get_variant_lines(content)

    assert variants_count == snvs_count + indels_count
