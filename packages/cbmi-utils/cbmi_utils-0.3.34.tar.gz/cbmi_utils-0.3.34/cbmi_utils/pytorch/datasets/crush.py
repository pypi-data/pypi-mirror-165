from pathlib import Path
from typing import Callable, Optional

from torch.utils.data import Dataset
from torchvision.io import read_image, ImageReadMode

import warnings
from .h5_dataset import H5Dataset


class Crush(Dataset):
    def __init__(self, root: str, class_to_idx: dict, tissue='*', zoom: int = 0, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None, scale: bool = False):
        self.transform = transform
        self.target_transform = target_transform
        self.scale = scale

        # -- fetch all samples from the specified path
        samples = sorted(Path(root).glob(f'{tissue}/*/{zoom}/patches/*.png'))
        self.samples = [s.__str__() for s in samples]  # convert PosixPath to strings

        # -- filter the whole list by dict keys
        self.samples = [s for s in self.samples if s.split('/')[-1].split('_')[0] in class_to_idx.keys()]

        # -- create targets
        self.targets = [class_to_idx[target.split('/')[-1].split('_')[0]] for target in self.samples]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image = read_image(self.samples[idx], mode=ImageReadMode.RGB)
        label = self.targets[idx]

        if self.scale:
            image = image.div(255)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)

        return image, label


def crush_cg_crush_void_tumor(root='/data/ldap/histopathologic/original_read_only/Crush/Patches', zoom: int = 0, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None, scale: bool = False):
    # Filter function
    class_to_idx = {
        "Crush": 0,
        "Crush-void": 0,
        "Tumor": 1
    }

    return Crush(root, class_to_idx, tissue='CG', zoom=zoom, transform=transform, target_transform=target_transform, scale=scale)


def crush_cm_crush_void_tumor(root='/data/ldap/histopathologic/original_read_only/Crush/Patches', zoom: int = 0, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None, scale: bool = False):
    # Filter function
    class_to_idx = {
        "Crush": 0,
        "Crush-void": 0,
        "Tumor": 1
    }

    return Crush(root, class_to_idx, tissue='CM', zoom=zoom, transform=transform, target_transform=target_transform, scale=scale)


def crush_crush_void_tumor(root='/data/ldap/histopathologic/original_read_only/Crush/Patches', zoom: int = 0, transform: Optional[Callable] = None, target_transform: Optional[Callable] = None, scale: bool = False):
    # Filter function
    class_to_idx = {
        "Crush": 0,
        "Crush-void": 0,
        "Tumor": 1
    }

    return Crush(root, class_to_idx, tissue='CM', zoom=zoom, transform=transform, target_transform=target_transform, scale=scale)


class Crush96x96(H5Dataset):
    """
    Data and further information can be found at TODO
    """

    def __init__(self, root: str, sub_set: str, transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        warnings.filterwarnings("default", category=DeprecationWarning)
        warnings.warn("Crush96x96 is depricated and will be removed from avocado soon. Use the ", DeprecationWarning)
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(data_path=Path(root) / f'{sub_set}.h5',
                         data_key='image',
                         target_path=Path(
                             root) / f'{sub_set}.h5',
                         target_key='label',
                         transform=transform,
                         transform_target=transform_target,
                         num_samples=num_samples)

        self.classes = ['C', 'T']  # C=crush and T=tumor

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        return cls('/data/ldap/histopathologic/processed_read_only/Crush_96', sub_set, transform, transform_target, num_samples=num_samples)

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.9031, 0.6317, 0.7814]
        std = [0.1185, 0.1722, 0.1203]
        return mean, std
