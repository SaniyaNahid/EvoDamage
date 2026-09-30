import json
import time

from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim

from torch.utils.data import DataLoader

from torchvision import models

from dataset import (
    DamageDataset,
    get_train_transform,
    get_validation_transform,
)


NUM_CLASSES = 4

BATCH_SIZE = 32

NUM_EPOCHS = 10

LEARNING_RATE = 0.0001


CLASS_NAMES = [
    "no-damage",
    "minor-damage",
    "major-damage",
    "destroyed",
]


def create_model():

    model = models.resnet18(
        weights=models.ResNet18_Weights.DEFAULT
    )

    # Freeze backbone initially
    for parameter in model.parameters():
        parameter.requires_grad = False

    # Replace final layer
    model.fc = nn.Linear(
        model.fc.in_features,
        NUM_CLASSES,
    )

    return model


def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    device,
):

    model.train()

    running_loss = 0.0

    correct = 0

    total = 0

    for images, labels in loader:

        images = images.to(device)

        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item() * images.size(0)

        predictions = outputs.argmax(dim=1)

        correct += (predictions == labels).sum().item()

        total += labels.size(0)

    epoch_loss = running_loss / total

    epoch_accuracy = correct / total

    return epoch_loss, epoch_accuracy


def validate(
    model,
    loader,
    criterion,
    device,
):

    model.eval()

    running_loss = 0.0

    correct = 0

    total = 0

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(device)

            labels = labels.to(device)

            outputs = model(images)

            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)

            predictions = outputs.argmax(dim=1)

            correct += (predictions == labels).sum().item()

            total += labels.size(0)

    loss = running_loss / total

    accuracy = correct / total

    return loss, accuracy


def main():

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Using device:", device)

    train_csv = Path("data/splits/train.csv")

    val_csv = Path("data/splits/val.csv")

    image_dir = Path("data/processed/images")

    train_dataset = DamageDataset(
        train_csv,
        image_dir,
        get_train_transform(),
    )

    val_dataset = DamageDataset(
        val_csv,
        image_dir,
        get_validation_transform(),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
    )

    model = create_model()

    model = model.to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(
        model.fc.parameters(),
        lr=LEARNING_RATE,
    )

    best_val_accuracy = 0.0

    history = []

    Path("models").mkdir(exist_ok=True)

    Path("outputs/metrics").mkdir(
        parents=True,
        exist_ok=True,
    )

    for epoch in range(NUM_EPOCHS):

        start_time = time.time()

        train_loss, train_accuracy = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
        )

        val_loss, val_accuracy = validate(
            model,
            val_loader,
            criterion,
            device,
        )

        elapsed = time.time() - start_time

        print(
            f"Epoch {epoch + 1}/{NUM_EPOCHS} | "
            f"Train Loss: {train_loss:.4f} | "
            f"Train Acc: {train_accuracy:.4f} | "
            f"Val Loss: {val_loss:.4f} | "
            f"Val Acc: {val_accuracy:.4f} | "
            f"Time: {elapsed:.1f}s"
        )

        history.append({
            "epoch": epoch + 1,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "val_loss": val_loss,
            "val_accuracy": val_accuracy,
        })

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            torch.save(
                model.state_dict(),
                "models/damage_model.pth",
            )

            print("Best model saved.")

    with open(
        "outputs/metrics/training_history.json",
        "w",
    ) as f:

        json.dump(
            history,
            f,
            indent=4,
        )

    print("\nTraining complete.")
    print(
        f"Best validation accuracy: "
        f"{best_val_accuracy:.4f}"
    )


if __name__ == "__main__":
    main()