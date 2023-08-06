"""Data generation for ts-NN."""

import logging
import time
import warnings
from typing import Tuple

import numpy as np
from tensorflow.keras.utils import Sequence

logging.Formatter.converter = time.gmtime
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
warnings.filterwarnings("ignore")


class DataGenerator(Sequence):
    """Generate data for NN model."""

    def __init__(
        self, params: dict, data: dict, shuffle: bool = True, mode: str = "train"
    ):
        """Initialize DataGenerator object."""
        self.indexes = None
        self.shuffle = shuffle
        self.mode = mode

        self.batch_size = params["nn_batch_size"]
        self.dim = data["df_n_vars"]

        self.list_IDs = data[f"df_{mode}"].index
        self.data_source_regr = data[f"df_{mode}"]
        self.data_source_target = data[f"label_{mode}"]

        self.on_epoch_end()

    def __len__(self) -> int:
        """Denote the number of batches per epoch."""
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index: int) -> Tuple[np.array, np.array]:
        """Generate one batch of data.

        Args:
            index (int): batch index

        Returns:
            Tuple[np.array, np.array]: Batch of data and respective classes
        """
        # Generate indexes of the batch
        indexes = self.indexes[
            index * self.batch_size : (index + 1) * self.batch_size  # noqa: E203
        ]

        # Find list of IDs
        list_IDs_temp = self.list_IDs[indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        """Update indexes after each epoch."""
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp: list) -> Tuple[np.array, np.array]:
        """Generate data containing batch_size samples.

        Args:
            list_IDs_temp (list): list of user IDs to include in current batch

        Returns:
            Tuple[np.array, np.array]: Batch of data and respective classes
        """
        X = self.data_source_regr.iloc[list_IDs_temp].values
        y = self.data_source_target.iloc[list_IDs_temp].values

        return X, y
