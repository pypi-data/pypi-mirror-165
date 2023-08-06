# cbmi_utils

Utility package for common features at CBMI. Further Information can be found in the [Wiki](https://gitlab.htw-berlin.de/baumapa/cbmi-utils/-/wikis/home).

## Install
```
pip install cbmi-utils
```

## Usage
Example PyTorch Layer Import
```
from cbmi_utils.pytorch.layers import Reshape
```

## New Release Procedure
- commit your changes on the dev branch and push to dev
- increase version number in `setup.py` and commit with message `increase version number` and push to dev
- merge to master and push
- on the gitlab-page create new tag
  - Tag Name: `0.X.XX`
  - Message: `new version 0.X.XX`
  - Release Notes: `<your actual changes>`
