from pathlib import Path
from typing import Callable, Optional

from .h5_dataset import H5Dataset


class LizardClassification(H5Dataset):
    """
    Data and further information can be found at https://arxiv.org/pdf/2108.11195.pdf.
    Neutrophil and Eosinophil classes are removed from this dataset, as they were to rare for training.
    """
    def __init__(
            self, root: str, sub_set: str, transform: Optional[Callable] = None,
            transform_target: Optional[Callable] = None, num_samples: int = 1
    ):
        assert sub_set in ['train', 'valid', 'test']

        super().__init__(
            data_path=Path(root) / f'{sub_set}.h5',
            data_key='image',
            target_path=Path(root) / f'{sub_set}.h5',
            target_key='label',
            transform=transform,
            transform_target=transform_target,
            num_samples=num_samples
        )

        # Neutrophil and Eosinophil classes are removed from this dataset, as they were to rare for training.
        self.classes = ['Epithelial', 'Lymphocyte', 'Plasma', 'Connective tissue']

    @classmethod
    def from_avocado(
            cls, sub_set: str = 'train', transform: Optional[Callable] = None,
            transform_target: Optional[Callable] = None, num_samples: int = 1
    ):
        return cls(
            '/data/ldap/histopathologic/processed_read_only/lizard_classification', sub_set, transform,
            transform_target, num_samples=num_samples
        )

    @staticmethod
    def normalization_values():
        # Calculated on the 'train' set
        mean = [0.64788544, 0.4870253,  0.68022424]
        std = [0.2539682,  0.22869842, 0.24064516]
        return mean, std
