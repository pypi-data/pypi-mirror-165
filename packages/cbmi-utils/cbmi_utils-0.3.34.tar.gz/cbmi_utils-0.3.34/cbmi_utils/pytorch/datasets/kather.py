from pathlib import Path
from typing import Callable, Optional
from .h5_dataset import H5Dataset
from torchvision.datasets import ImageFolder
import warnings


class Kather96x96(H5Dataset):
    """
    Kather dataset, more information can be found at https://zenodo.org/record/1214456
    """

    def __init__(self, root: str, sub_set: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(data_path=Path(root) / f'{sub_set}.h5',
                         data_key='image',
                         target_path=Path(root) / f'{sub_set}.h5',
                         target_key='label',
                         transform=transform,
                         transform_target=transform_target,
                         num_samples=num_samples)

        warnings.warn("Kather96x96 is deprecated and will be removed, use Kather instead or one of the given instanciation functions", DeprecationWarning)

        self.classes = ['ADI', 'BACK', 'DEB', 'LYM', 'MUC', 'MUS', 'NORM', 'STR', 'TUM']

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        return cls('/data/ldap/histopathologic/processed_read_only/kather/h5/96/norm_split0.9_old', sub_set, transform, transform_target, num_samples=num_samples)

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.7359, 0.5805, 0.7014]
        std = [0.2154, 0.2781, 0.2226]
        return mean, std


class Kather224x224(H5Dataset):
    """
    Kather dataset, more information can be found at https://zenodo.org/record/1214456
    """

    def __init__(self, root: str, sub_set: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(data_path=Path(root) / f'{sub_set}.h5',
                         data_key='image',
                         target_path=Path(root) / f'{sub_set}.h5',
                         target_key='label',
                         transform=transform,
                         transform_target=transform_target,
                         num_samples=num_samples)

        warnings.warn("Kather96x96 is deprecated and will be removed, use Kather instead or one of the given instanciation functions", DeprecationWarning)

        self.classes = ['ADI', 'BACK', 'DEB', 'LYM', 'MUC', 'MUS', 'NORM', 'STR', 'TUM']

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        if sub_set in ('train', 'valid'):
            return cls(root='/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm_split0.9_old', sub_set=sub_set, transform=transform, num_samples=num_samples)
        elif sub_set == "test":
            return cls(root='/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm', sub_set='test', transform=transform)
        else:
            raise AttributeError(f"No such sub set {sub_set}")

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.7357, 0.5804, 0.7013]
        std = [0.2261, 0.2857, 0.2297]
        return mean, std


class Kather(H5Dataset):
    """
    Kather dataset, more information can be found at https://zenodo.org/record/1214456
    """

    def __init__(self, root: str, sub_set: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(data_path=Path(root) / f'{sub_set}.h5',
                         data_key='image',
                         target_path=Path(root) / f'{sub_set}.h5',
                         target_key='label',
                         transform=transform,
                         transform_target=transform_target,
                         num_samples=num_samples)

        self.classes = ['ADI', 'BACK', 'DEB', 'LYM', 'MUC', 'MUS', 'NORM', 'STR', 'TUM']

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.7357, 0.5804, 0.7013]
        std = [0.2261, 0.2857, 0.2297]
        return mean, std


# -- H5 loader
def kather_h5_224_norm(sub_set='train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
    assert sub_set in ('train', 'test'), f"'sub_set' needs to be 'train' or 'test' for that set, not {sub_set} is no valid sub set."
    return Kather('/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm', sub_set, transform, transform_target, num_samples)


def kather_h5_224_norm_split_90_10(sub_set="train", transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
    assert sub_set in ("train", "valid", "test")

    if sub_set in ("train", "valid"):
        return Kather("/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm_split0.9", sub_set, transform, transform_target, num_samples)
    else:
        return Kather("/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm", "test", transform, transform_target, num_samples)


def kather_h5_224_norm_split_old(sub_set="train", transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
    assert sub_set in ("train", "valid", "test")

    if sub_set in ("train", "valid"):
        return Kather("/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm_split0.9_old", sub_set, transform, transform_target, num_samples)
    else:
        return Kather("/data/ldap/histopathologic/processed_read_only/kather/h5/224/norm", "test", transform, transform_target, num_samples)


def kather_h5_96_norm_split_old(sub_set="train", transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
    assert sub_set in ("train", "valid", "test")
    return Kather("/data/ldap/histopathologic/processed_read_only/kather/h5/96/norm_split0.9_old", sub_set, transform, transform_target, num_samples)


# -- ImageFolder loader
def kather_if_224_norm(sub_set="train", transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
    assert sub_set in ("train", "test"), f"'sub_set' needs to be 'train' or 'test' for that set, not {sub_set} is no valid sub set."

    folder_path = {
        "train": "/data/ldap/histopathologic/original_read_only/Kather/NCT-CRC-HE-100K",
        "test": "/data/ldap/histopathologic/original_read_only/Kather/CRC-VAL-HE-7K"
    }

    return ImageFolder(folder_path[sub_set], transform, transform_target)
