# Project Name

Template

## Objective of this project

to be used as a template
## Development

### Dependencies

Our chosen dependency manager is miniconda.

To create a conda environment from the dependencies file `environment.yml`, run the following command:

```sh
conda env create -f environment.yml
```

Please use miniconda as your python environment managers. Anaconda has some issues in resolving the packages
https://docs.conda.io/en/latest/miniconda.html

To update the conda environment `template` with the dependencies file `environment.yml`:

```sh
conda activate template
conda env update --file environment.yml --prune
```

### Unit tests and linting

```sh
tox
```

equivalent to

```sh
tox -e py37
tox -e flake8
```

### Git Flow

Git branches are managed by [git-flow](https://github.com/petervanderdoes/gitflow-avh).

Initialize git flow in your repository:

```
$ git flow init

Which branch should be used for bringing forth production releases?
   - develop
   - feature/ACG-448-daily-ingest
   - main
Branch name for production releases: [main]

Which branch should be used for integration of the "next release"?
   - develop
   - feature/ACG-448-daily-ingest
Branch name for "next release" development: [develop]

How to name your supporting branch prefixes?
Feature branches? [feature/]
Bugfix branches? [bugfix/]
Release branches? [release/]
Hotfix branches? [hotfix/]
Support branches? [support/]
Version tag prefix? []
```

Then when you are ready to develop a feature, use `git flow start <feature_name>` for example:

```
$ git flow feature start ACG-452-tests-code-hygiene
M       README.md
Switched to a new branch 'feature/ACG-452-tests-code-hygiene'

Summary of actions:
- A new branch 'feature/ACG-452-tests-code-hygiene' was created, based on 'develop'
- You are now on branch 'feature/ACG-452-tests-code-hygiene'
```

