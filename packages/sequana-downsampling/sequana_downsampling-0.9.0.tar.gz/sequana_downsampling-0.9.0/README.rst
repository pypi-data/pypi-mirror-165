

.. image:: https://badge.fury.io/py/sequana-downsampling.svg
     :target: https://pypi.python.org/pypi/sequana_downsampling

.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg
    :target: http://joss.theoj.org/papers/10.21105/joss.00352
    :alt: JOSS (journal of open source software) DOI

.. image:: https://github.com/sequana/downsampling/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/downsampling/actions/workflows/main.yaml 


This is is the **downsampling** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ project

:Overview: downsample NGS data sets
:Input: a set of FastQ or FASTA files 
:Output: a set of downsampled files
:Status: production
:Citation(sequana): Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352
:Citation(pipeline): 
    .. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4047837.svg
       :target: https://doi.org/10.5281/zenodo.4047837



Installation
~~~~~~~~~~~~

You must install Sequana first::

    pip install sequana

Then, just install this package::

    pip install sequana_downsampling


Usage
~~~~~

::

    sequana_downsampling --help
    sequana_downsampling --input-directory DATAPATHH
    sequana_downsampling --downsampling-method random --downsampling-max-entries 100
    sequana_downsampling --downsampling-method random_pct --downsampling-percent 10 --downsampling-input-format fasta --input-pattern "whatever*fasta"

Note that the current implementation handles fastq files (zipped or not) and
fasta files (uncompressed only)


This creates a directory with the pipeline and configuration file. You will then need 
to execute the pipeline::

    cd downsampling
    sh downsampling.sh  # for a local run

This launch a snakemake pipeline. If you are familiar with snakemake, you can 
retrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::

    snakemake -s downsampling.rules -c config.yaml --cores 4 --stats stats.txt

Or use `sequanix <https://sequana.readthedocs.io/en/master/sequanix.html>`_ interface.

Examples of a set of FastQ zipped files in the current directory:


    sequana_downsampling --run --downsampling-method random_pct 
    cd downsampling
    make clean

This will create a directory called **downsampling**, and randomly select 10% of
the input reads for each file with extension .fastq.gz in the current directory.
Since **-run** is used, the pipeline is executed automatically. The following
commands will enter into the directory and called a Makefile. This will clean
the directory for temporary files.

Requirements
~~~~~~~~~~~~

This pipelines requires the following executable(s):

- sequana
- pigz

.. .. image:: https://raw.githubusercontent.com/sequana/downsampling/master/sequana_pipelines/downsampling/dag.png


Details
~~~~~~~~~

This pipeline runs **downsampling** in parallel on the input fastq or fasta files (paired or not). If paired, the one-to-one mapping is conserved.

It can take as input a set of FastQ files, or FastA files. by
default, the pipeline with randomly select 1000 entries from each input files.
You can increase this number using --downsampling-max-entries option. If you
prefer to select a percentage of the entries instead, you can change the
downsamping method as follows::

    --downsampling-method random_pct

and change the value if needed (default is 10%)::

    --downsampling-percent 20

Note that input FastQ can be gzipped. Output files are gzipped. FastA input
files must be compressed for now



Rules and configuration details
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/downsampling/master/sequana_pipelines/downsampling/config.yaml>`_
to be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. 


Changelog
~~~~~~~~~

========= ====================================================================
Version   Description
========= ====================================================================
0.8.5     * cope with R1/R2 paired data properly. Improved make file
0.8.4     * add missing MANIFEST to include missing requirements.txt
0.8.3     * comply with new API from sequana_pipetools 0.2.4
0.8.2     * add a --run option to execute the pipeline directly
0.8.1     * fix input and N in the random selection
0.8.0     **First release.**
========= ====================================================================


