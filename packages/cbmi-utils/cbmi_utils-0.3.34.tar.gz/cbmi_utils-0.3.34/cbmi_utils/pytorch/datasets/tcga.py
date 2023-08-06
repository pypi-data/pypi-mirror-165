from pathlib import Path
from typing import Callable, Optional

from .h5_dataset import H5Dataset


TISSUE_TYPES = ['STAD', 'CRC_DX']
ALL_TISSUE_TYPES = ['all', *TISSUE_TYPES]


class TCGA(H5Dataset):
    """
    Data and further information can be found at https://zenodo.org/record/2530835
    """

    def __init__(
            self, root: Path, sub_set: str, transform: Optional[Callable] = None,
            transform_target: Optional[Callable] = None, num_samples: int = 1
    ):
        """
        Creates a new TCGA Dataset.
        """
        super().__init__(
            data_path=Path(root) / '{}.h5'.format(sub_set),
            data_key='image',
            target_path=Path(root) / '{}.h5'.format(sub_set),
            target_key='label',
            transform=transform,
            transform_target=transform_target,
            num_samples=num_samples
        )
        
        self.classes = ['MSS', 'MSIMUT']


def tcga_h5_224_split(
        sub_set: str, tissue_type: str = 'all', transform: Optional[Callable] = None,
        transform_target: Optional[Callable] = None, num_samples: int = 1
) -> TCGA:
    """
    This dataset consists of "train", "valid" and "test" dataset. The "valid" dataset is created by splitting 1/6 of the
    original "train" dataset.

    Args:
        sub_set: The sub_set to use. One of ["train", "valid", "test"]
        tissue_type: The tissue type to train on. One of ["all", "STAD", "CRC_DX"]. "all" combines all tissue types.
    """
    assert sub_set in ('train', 'valid', 'test')
    assert tissue_type in ALL_TISSUE_TYPES

    if sub_set in ('train', 'valid'):
        # in case of train or valid, we use the split dataset
        root = Path('/data/ldap/histopathologic/processed_read_only/TCGA/TOAD') / tissue_type / 'split'
    else:
        # in case of test, we use the normal dataset
        root = Path('/data/ldap/histopathologic/processed_read_only/TCGA/TOAD') / tissue_type
    return TCGA(
        root=root, sub_set=sub_set, transform=transform, transform_target=transform_target, num_samples=num_samples
    )


def tcga_h5_224_no_split(
        sub_set: str, tissue_type: str = 'all', transform: Optional[Callable] = None,
        transform_target: Optional[Callable] = None, num_samples: int = 1
) -> TCGA:
    """
    This dataset is only split into train and test dataset. Use "tcga_h5_224_split" in order to use "valid" dataset.

    Args:
        sub_set: The sub_set to use. One of ["train", "valid", "test"]
        tissue_type: The tissue type to train on. One of ["all", "STAD", "CRC_DX"]. "all" combines all tissue types.
    """
    assert sub_set in ('train', 'test'), '"tcga_h5_224" only supports "train" and "test" dataset. Use ' \
                                         '"tcga_h5_224_split" in order to use "valid" '
    assert tissue_type in ALL_TISSUE_TYPES
    root = Path('/data/ldap/histopathologic/processed_read_only/TCGA/TOAD') / tissue_type

    return TCGA(
        root=root, sub_set=sub_set, transform=transform, transform_target=transform_target, num_samples=num_samples
    )


def tcga_get_norm_values_split(tissue_type: str = 'all', sub_set: str = 'train'):
    """
    Returns the normalization values (mean, std) for the tcga split dataset.
    """
    if tissue_type == 'all':
        if sub_set == 'train':
            mean = [0.7455422, 0.52883655, 0.70516384]
            std = [0.15424888, 0.20247863, 0.14497302]
        elif sub_set == 'valid':
            mean = [0.7456962, 0.52919656, 0.7055899]
            std = [0.15419695, 0.20254336, 0.1447762]
        elif sub_set == 'test':
            mean = [0.7466583, 0.5304041, 0.70326054]
            std = [0.15270334, 0.20127273, 0.14331447]
        else:
            raise ValueError('unknown sub_set: "{}"'.format(sub_set))
    elif tissue_type == 'STAD':
        if sub_set == 'train':
            mean = [0.7634684, 0.54374254, 0.71698856]
            std = [0.15011676, 0.2008121, 0.14292231]
        elif sub_set == 'valid':
            mean = [0.7634385, 0.54307556, 0.71678466]
            std = [0.14998579, 0.20067562, 0.14286728]
        elif sub_set == 'test':
            mean = [0.7629462, 0.54384017, 0.7157198]
            std = [0.15086626, 0.20151193, 0.14315079]
        else:
            raise ValueError('unknown sub_set: "{}"'.format(sub_set))
    elif tissue_type == 'CRC_DX':
        if sub_set == 'train':
            mean = [0.72625715, 0.5129033, 0.6924695]
            std = [0.15628287, 0.20297064, 0.14583662]
        elif sub_set == 'valid':
            mean = [0.7265287, 0.51308644, 0.69268656]
            std = [0.15626888, 0.20299286, 0.14657238]
        elif sub_set == 'test':
            mean = [0.7272331, 0.514329, 0.688363]
            std = [0.15487206, 0.2009504, 0.14348038]
        else:
            raise ValueError('unknown sub_set: "{}"'.format(sub_set))
    else:
        raise ValueError('unknown tissue type: "{}"'.format(tissue_type))

    return mean, std
