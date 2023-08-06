from typing import Any, Callable, Optional, Tuple
from pathlib import Path
from typing import Callable, Optional
from torch.utils.data import Dataset, random_split
import csv
import numpy as np
from PIL import Image
from torchvision import datasets

class MaiPatch(Dataset):
    """
    The final PHH3-Dataset from the MAI project.
    """
    def __init__(self,
                 root: str,
                 sub_set: str,
                 transform: Optional[Callable] = None,
                 transform_target: Optional[Callable] = None
                ):
        assert sub_set in ['train', 'valid', 'test']
        self.root = root
        if sub_set == 'train':
            path = f'{root}/MP.train.HTW.train'
        elif sub_set == 'valid':
            path = f'{root}/MP.train.HTW.validation'
        elif sub_set == 'test':
            path = f'{root}/MP.validation.HTW.test'
            
        self.ds = datasets.ImageFolder(root=path, transform=transform, target_transform=transform_target)
        self.classes = ['NoMitosis', 'Mitosis']

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None):
        return cls('/data/ldap/histopathologic/original_read_only/MAI-DS', sub_set, transform, transform_target)

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.86121925, 0.86814779, 0.88314296]
        std = [0.13475281, 0.10909398, 0.09926313]
        return mean, std
    
    def __len__(self) -> int:
        return len(self.ds)

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        return self.ds[index]
    