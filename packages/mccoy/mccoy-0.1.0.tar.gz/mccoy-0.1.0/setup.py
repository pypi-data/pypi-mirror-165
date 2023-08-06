# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mccoy', 'mccoy.workflow.scripts']

package_data = \
{'': ['*'],
 'mccoy': ['config/*',
           'profiles/local/*',
           'profiles/slurm/*',
           'workflow/*',
           'workflow/envs/*',
           'workflow/report/*',
           'workflow/rules/*']}

install_requires = \
['snakemake>=7.5.0,<8.0.0', 'tqdm>=4.64.0,<5.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['mccoy = mccoy.main:app']}

setup_kwargs = {
    'name': 'mccoy',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Current workflow\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/smutch/mccoy/main.svg)](https://results.pre-commit.ci/latest/github/smutch/mccoy/main)\n[![docs](https://github.com/smutch/mccoy/actions/workflows/docs.yaml/badge.svg?event=push)](https://github.com/smutch/mccoy/actions/workflows/docs.yaml)\n\n\nThis will be updated as pieces are developed and modified.\n\n```mermaid\n%%{init: { \'theme\':\'neutral\' } }%%\nflowchart TB\n    sources[(fasta files)]\n    sources --> combine --> MSA\n    click combine href "https://github.com/smutch/mccoy/blob/main/mccoy/workflow/rules/combine.smk"\n\n    MSA[multiple sequence alignment<br/>-- MAFFT] --> QC\n    click MSA href "https://github.com/smutch/mccoy/blob/main/mccoy/workflow/rules/align.smk"\n\n    subgraph QC["Quality control"]\n        tree[L_max tree<br/>-- iqtree2] --> RTR[root-tip regression]\n        click tree href "https://github.com/smutch/mccoy/blob/main/mccoy/workflow/rules/tree.smk"\n        otherQC[other checks]\n    end\n\n    QC --> XML[Beast XML generation<br/>-- Wytamma\'s scripts + templates + FEAST] --> OnlineBEAST[run, pause & update BEAST analysis<br/>-- Online BEAST] .-> Beastiary[monitor running BEAST jobs<br/>-- Beastiary]\n    click XML href "https://github.com/smutch/mccoy/blob/main/mccoy/workflow/rules/beast.smk"\n    click OnlineBEAST href "https://github.com/Wytamma/online-beast"\n    click Beastiary href "https://github.com/Wytamma/beastiary"\n\n    classDef complete fill:#48b884;\n    class gisaid,GISAIDR,sources,combine,MSA,tree,RTR,XML complete;\n\n    classDef inProg fill:#cc8400;\n    class otherQC,OnlineBEAST inProg;\n```\n\n# Instructions\n\nEnsure you have [mamba](https://github.com/conda-forge/miniforge) (conda will work too, but mamba is strongly preferred), and [poetry](https://python-poetry.org) installed.\n\n## Step 1 - install the workflow\n\n```bash\npoetry install\n```\n\nTo start using McCoy, you can either spawn a new shell with the McCoy Poetry environment enabled:\n\n```bash\npoetry shell\n```\n\n**or** you can replace every instance of `mccoy` in the commands below with `poetry run mccoy`.\n\nThe workflow is being developed such that all required software will be automatically installed for each step of the pipeline in self-contained conda environments. These environments will be cached and reused whenever possible (all handled internally by snakemake), but if you want to remove them then they can be found in `.snakemake`.\n\n## Step 2 - Create a McCoy project\n\nFirst begin by creating a new McCoy project (called `test` in this example):\n\n```bash\nmccoy create test --reference resources/reference.fasta --template resources/templates/CoV_CE_fixed_clock_template.xml\n```\n\nThe `reference` and `template` options are required. At the moment we are distributing these reference and template files, however, once we reach v1.0, these will be removed and the useer will have to ensure they have appropriate reference and template files available.\n\nThe config for this project can be altered by editing the newly created file `test/config.yaml`.\n\n## Step 3 - Run the project!\n\nTo run the newly created project:\n\n```bash\nmccoy run test --data resources/omicron_test-original.fasta\n```\n\nAgain, the `data` option here is required. This command will create a new directory in `test/runs` with the workflow results and output.\n\n## Step 4 - Add new data\n\nSubsequent calls to `mccoy run` will result in a whole new run of the pipeline from start-to-finsh unless the `--inherit` or `--inherit-last` flags are used. See `mccoy run --help` for more information. Inheriting from a previous run will use the data and MCMC state as a starting point for the new data.\n\n```bash\nmccoy run test --data resources/omicron_test-extra.fasta --inherit-last\n```\n\nAs well as directly altering a project\'s `config.yaml`, config variables can be overridden on the command line. e.g.:\n```bash\nmccoy run --data resources/omicron_test-original.fasta --config align=\'{mafft: ["--6merpair", "--addfragments"]}\'\n```\n\nAny options passed to `mccoy run` that are not listed in `mccoy run --help` will be directly forwarded on to Snakemake. See `mccoy run --help-snakemake` for a list of all available options.\n',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
