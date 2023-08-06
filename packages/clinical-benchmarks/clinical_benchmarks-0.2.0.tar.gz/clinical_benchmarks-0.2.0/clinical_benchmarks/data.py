"""Convenience classes for loading and working with datasets."""
import torch
import pandas as pd


class SimpleDataset(torch.utils.data.Dataset):
    def __init__(self, X: pd.DataFrame, y: pd.DataFrame):
        self.X = X
        self.y = y

    def __getitem__(self, idx):
        return torch.tensor(self.X.loc[idx]), self.y.loc[idx]

    def __len__(self):
        return self.X.shape[0]
