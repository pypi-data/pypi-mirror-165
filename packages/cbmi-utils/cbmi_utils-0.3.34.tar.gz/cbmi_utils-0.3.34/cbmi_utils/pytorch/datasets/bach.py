from typing import Any, Callable, Optional, Tuple
from pathlib import Path
from typing import Callable, Optional
from torch.utils.data import Dataset, random_split
import csv
import numpy as np
from PIL import Image

class BACH(Dataset):
    """
    distribution of the classes on the train set: 1600, 1503,  985, 1600;
    validation set 243, 316, 327, 437 and test set 313, 314, 370, 426
    """
    def __init__(self,
                 root: str,
                 sub_set: str,
                 transform: Optional[Callable] = None,
                 transform_target: Optional[Callable] = None,
                 num_samples: int = 1):
        assert sub_set in ['train', 'valid', 'test']
        self.root = root
        if sub_set == 'train':
            csv_path = f'{root}/train_subset.csv'
        elif sub_set == 'valid':
            csv_path = f'{root}/validation.csv'
        elif sub_set == 'test':
            csv_path = f'{root}/test.csv'
        self.ds = []
        with open(csv_path, newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                self.ds.append(row)
        self.classes = ['Normal', 'Benign', 'in situ', 'Invasive']

    @classmethod
    def from_avocado(cls, sub_set: str = 'train', transform: Optional[Callable] = None, transform_target: Optional[Callable] = None, num_samples: int = 1):
        return cls('/data/ldap/histopathologic/processed_read_only/BACH', sub_set, transform, transform_target, num_samples=num_samples)

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.75476083, 0.60369028, 0.73111293]
        std = [0.13389589, 0.16942156, 0.12501291]
        return mean, std
    
    def __len__(self) -> int:
        return len(self.ds)

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        im = np.array(Image.open(self.root + '/' + self.ds[index][0])) / 255.
        label = int(self.ds[index][4])
        if label == -1:
            label = 0
        return im, label
    