# toil_strelka
[![github badge][github_badge]][github_base]
[![travis badge][travis_badge]][travis_base]
[![codecov badge][codecov_badge]][codecov_base]
[![docker badge][docker_badge]][docker_base]
[![code formatting][black_badge]][black_base]

Toil implementation of [Strelka2][strelka] SNV Caller

## Usage

This package uses docker to manage its dependencies, there are 2 ways of using it:

1. Running the [container][docker_base] in single machine mode without [`--batchSystem`] support:

        # using docker
        docker run -it papaemmelab/toil_strelka --help

        # using singularity
        singularity run docker://papaemmelab/toil_strelka --help

1. Installing the python package from [pypi][pypi_base] and passing the container as a flag:

        # install package
        pip install toil_strelka

        # run with docker
        toil_strelka [TOIL-OPTIONS] [PIPELINE-OPTIONS]
            --docker papaemmelab/toil_strelka
            --volumes <local path> <container path>
            --batchSystem LSF

        # run with singularity
        toil_strelka [TOIL-OPTIONS] [PIPELINE-OPTIONS]
            --singularity docker://papaemmelab/toil_strelka
            --volumes <local path> <container path>
            --batchSystem LSF

See [docker2singularity] if you want to use a [singularity] image instead of using the `docker://` prefix. If you want to run toil_strelka without a Docker/Singularity image, make sure {.../manta_installation_folder/bin} and {.../strelka_installation_folder/bin} are in the PATH.

## Example

        toil_strelka \
            --singularity {singularity image} \
            --volumes /ifs /ifs \
            --workDir {recommend using $TMP_DIR} \
            jobstore \
            --stats \
            --disableCaching \
            --realTimeLogging \
            --batchSystem CustomLSF \
            --writeLogs {outdir}/logs_toil \
            --logFile {outdir}/head_job.toil \
            --logLevel "INFO" \
            --sequencing_method TGD \
            --normal {normal bam} \
            --tumor {tumor bam} \
            --outdir {outdir} \
            --reference {reference fasta file} \
            --bed {bed file}

## Additional Options

| Option         | Default | Notes                                     |
| -------------- | ------- | ----------------------------------------- |
| --manta_jobs   | 2       | Number of Manta jobs to run in parallel   |
| --strelka_jobs | 2       | Number of Strelka jobs to run in parallel |
| --germline     | False   | Flag to call somatic or germline variants (pass only --normal, not --tumor) |

## Pipeline

As provided in Strelka docs:

![strelka pipeline diagram](workflow.png 'Pipeline')

## Contributing

Contributions are welcome, and they are greatly appreciated, check our [contributing guidelines](.github/CONTRIBUTING.md)!

## Credits

This package was created using [Cookiecutter] and the
[papaemmelab/cookiecutter-toil] project template.

<!-- References -->
[strelka]: https://github.com/Illumina/strelka
[singularity]: http://singularity.lbl.gov/
[docker2singularity]: https://github.com/singularityware/docker2singularity
[cookiecutter]: https://github.com/audreyr/cookiecutter
[papaemmelab/cookiecutter-toil]: https://github.com/papaemmelab/cookiecutter-toil
[docker2singularity]: https://github.com/singularityware/docker2singularity
[`--batchSystem`]: http://toil.readthedocs.io/en/latest/developingWorkflows/batchSystem.html?highlight=BatchSystem

<!-- Badges -->
[codecov_badge]: https://codecov.io/gh/papaemmelab/toil_strelka/branch/master/graph/badge.svg
[codecov_base]: https://codecov.io/gh/papaemmelab/toil_strelka
[docker_base]: https://hub.docker.com/r/papaemmelab/toil_strelka
[docker_badge]: https://img.shields.io/badge/docker%20build-automated-yellow
[pypi_badge]: https://img.shields.io/pypi/v/toil_strelka.svg
[pypi_base]: https://pypi.python.org/pypi/toil_strelka
[travis_badge]: https://app.travis-ci.com/papaemmelab/toil_strelka.svg?token=P6GGbmdLPwysz69FFv2X&branch=master
[travis_base]: https://app.travis-ci.com/papaemmelab/toil_strelka
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_base]: https://github.com/ambv/black
[github_badge]: https://img.shields.io/badge/version-v1.0.7-blue
[github_base]: https://github.com/papaemmelab/toil_strelka/releases/tag/v1.0.7

