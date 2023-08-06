Python code for working with [the data](https://cls-gitlab.phil.uni-wuerzburg.de/spp-cls-data-exchange/spp-cls_annotationtables_data)
of the DFG-funded [SPP Computational Literary Studies](https://dfg-spp-cls.github.io/).

- **sppcls.py**: the [sppcls](https://pypi.org/project/sppcls/) Python
  module to access the data:
  - blocking:
  ```python
  from sppcls import sppcls
  df = sppcls.load_df(work="test", projects=["project"])
  print(df.describe())
  ```
  - non blocking: 
  ```python
  from sppcls import sppcls
  df = await sppcls.load_df_async(work="test", projects=["project"])
  print(df.describe())
  ```

## Installation

### PyPI

`pip install sppcls`

### From source

Setup an virtual environment, if necessary:

```sh
python3 -m venv env
source env/bin/activate
```

Install dependencies:

```sh
pip install -r requirements.txt
python -m spacy download de_core_news_lg
```

## Usage

### tokenise.py

```sh
python tokenise.py path_to_input_txt path_to_output_folder
```

TODO: fix character offset to be byte instead

### check.py
