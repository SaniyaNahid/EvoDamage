import pandas as pd
import torch

from pathlib import Path
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


CLASS_NAMES = [
    "no-damage",
    "minor-damage",
    "major-damage",
    "destroyed",
]


class DamageDataset(Dataset):

    def __init__(
        self,
        csv_file,
        image_dir,
        transform=None,
    ):

        self.data = pd.read_csv(csv_file)

        self.image_dir = Path(image_dir)

        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):

        row = self.data.iloc[index]

        image_path = self.image_dir / row["image"]

        image = Image.open(image_path).convert("RGB")

        label = int(row["label"])

        if self.transform:
            image = self.transform(image)

        return image, torch.tensor(label, dtype=torch.long)


def get_train_transform():

    return transforms.Compose([
        transforms.Resize((224, 224)),

        transforms.RandomHorizontalFlip(),

        transforms.RandomVerticalFlip(),

        transforms.RandomRotation(10),

        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2,
            saturation=0.2,
        ),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])


def get_validation_transform():

    return transforms.Compose([
        transforms.Resize((224, 224)),

        transforms.ToTensor(),

        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])