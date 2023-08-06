# Garbáge

#### Design principles

1. Mix of crap code and tested, clean, utilities
2. Allow data scientists to work by writing crap vim scrips, use what they want from the framework
3. Unix philosophy of composition, but with piping jsonl around which admitted breaks some of ideas of pipes

#### How to write your own experiment

1. Make a config file that has fields: `name`, `reshaper`, `plotter`, `experiment_module`, `experiment_class`, at minimum
2. Make an experiment class that inherits from Experiment located `from naveen.experiment.experiment import Experiment`
2a. The`experiment_class` field is the name of the experiment's class and the module is the location w/in your repo
3. The class should implement `get_results -> List[dict]`
4. `$ experiment -c yourconfig.json -p src` where src is the top-level package for your project
e.g. `experiment -p src -c config/voss.json`

#### Example use

###### Get all urls for first two pages of allnurses.com
`pages -b 'https://allnurses.com/search/?&q=EHR&page=' -m 53 | stream  | urls  | pv -l > tmp/a` # get URLs from allnurses

###### Stream URLs from a list, run spacy to get the text of the pages into w2v format and print the processed text w/ jq
`cat test/fixtures/url_list.txt | stream | python demo_oneoffs/process_amazon_url.py | jq .processed`

#### Dev ops

- `cz c` to make commits using commitizen
- `make conda` to update the environment information based on `config/cookiecutter.yml`
- `conda create --clone cookiecutter --name nlp` to make a new env forking cookiecutter
- `.git/hooks/pre-commit` is committed as part of the repo. It will run tests before you commit and abort the commit if they fail.

#### Commands

- `make init` to get setup
- `make lint` to run linters
- `make test` to run the tests

#### Directories
- `config` experiment config files go here, as json or yaml
- `data` project data
- `docs` notes and markdown files for dendron
- `naveen` source files
- `results` experiment output files go here, usually as csv. Usually go into unix timestamped dirs with corresponding config files
- `scripts` one-off scripts
    + `scripts/reshapers` reshape data. By convention these Python scripts acccept two named arguments `--results_directory` and `--resultsfile`. They are assumed to run on `.csv` files. By convention they write results as `reshaped.csv`
    + `scripts/plotters` plot data. By convention these Python scripts acccept two named arguments `--results_directory` and `--results_file`.
- `tmp` use this directory for writing interim tmp files and such that don't need to get saved longterm. I also use this directory to save/move crap one-off code that may get turned into a script or class later.
