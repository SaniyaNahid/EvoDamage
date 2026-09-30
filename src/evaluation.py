import json

from pathlib import Path

import matplotlib.pyplot as plt

import torch
import torch.nn as nn

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

from torch.utils.data import DataLoader

from torchvision import models

from dataset import (
    DamageDataset,
    get_validation_transform,
)


CLASS_NAMES = [
    "no-damage",
    "minor-damage",
    "major-damage",
    "destroyed",
]


def load_model(model_path):

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    model = models.resnet18(
        weights=None
    )

    model.fc = nn.Linear(
        model.fc.in_features,
        4,
    )

    model.load_state_dict(
        torch.load(
            model_path,
            map_location=device,
        )
    )

    model = model.to(device)

    model.eval()

    return model, device


def evaluate():

    test_csv = Path(
        "data/splits/test.csv"
    )

    image_dir = Path(
        "data/processed/images"
    )

    model_path = Path(
        "models/damage_model.pth"
    )

    dataset = DamageDataset(
        test_csv,
        image_dir,
        get_validation_transform(),
    )

    loader = DataLoader(
        dataset,
        batch_size=32,
        shuffle=False,
        num_workers=0,
    )

    model, device = load_model(
        model_path
    )

    all_labels = []

    all_predictions = []

    with torch.no_grad():

        for images, labels in loader:

            images = images.to(device)

            outputs = model(images)

            predictions = outputs.argmax(
                dim=1
            ).cpu().tolist()

            all_predictions.extend(
                predictions
            )

            all_labels.extend(
                labels.tolist()
            )

    accuracy = accuracy_score(
        all_labels,
        all_predictions,
    )

    precision = precision_score(
        all_labels,
        all_predictions,
        average="weighted",
        zero_division=0,
    )

    recall = recall_score(
        all_labels,
        all_predictions,
        average="weighted",
        zero_division=0,
    )

    f1 = f1_score(
        all_labels,
        all_predictions,
        average="weighted",
        zero_division=0,
    )

    print("\nEvaluation Results")
    print("==================")

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    report = classification_report(
        all_labels,
        all_predictions,
        target_names=CLASS_NAMES,
        zero_division=0,
    )

    print("\nClassification Report")
    print(report)

    output_dir = Path(
        "outputs/metrics"
    )

    plot_dir = Path(
        "outputs/plots"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    plot_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
    }

    with open(
        output_dir / "metrics.json",
        "w",
    ) as f:

        json.dump(
            metrics,
            f,
            indent=4,
        )

    with open(
        output_dir / "classification_report.txt",
        "w",
    ) as f:

        f.write(report)

    cm = confusion_matrix(
        all_labels,
        all_predictions,
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=CLASS_NAMES,
    )

    display.plot(
        xticks_rotation=45
    )

    plt.tight_layout()

    plt.savefig(
        plot_dir / "confusion_matrix.png"
    )

    plt.close()

    print(
        "\nEvaluation files saved."
    )


if __name__ == "__main__":
    evaluate()