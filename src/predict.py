import time

import torch
import torch.nn as nn

from PIL import Image

from torchvision import models, transforms


CLASS_NAMES = [
    "no-damage",
    "minor-damage",
    "major-damage",
    "destroyed",
]


DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


def load_model(model_path="models/damage_model.pth"):

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
            map_location=DEVICE,
        )
    )

    model = model.to(DEVICE)

    model.eval()

    return model


transform = transforms.Compose([
    transforms.Resize((224, 224)),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


def predict_damage(
    image,
    model_path="models/damage_model.pth",
):

    model = load_model(model_path)

    if not isinstance(image, Image.Image):
        image = Image.open(image)

    image = image.convert("RGB")

    input_tensor = transform(image)

    input_tensor = input_tensor.unsqueeze(0)

    input_tensor = input_tensor.to(DEVICE)

    start_time = time.perf_counter()

    with torch.no_grad():

        outputs = model(input_tensor)

        probabilities = torch.softmax(
            outputs,
            dim=1,
        )

    inference_time = (
        time.perf_counter() - start_time
    ) * 1000

    confidence, predicted_class = torch.max(
        probabilities,
        dim=1,
    )

    predicted_class = predicted_class.item()

    confidence = confidence.item()

    probability_values = probabilities[0].cpu().tolist()

    damage_probabilities = {
        CLASS_NAMES[i]: probability_values[i]
        for i in range(4)
    }

    return {
        "damage_class": CLASS_NAMES[predicted_class],

        "confidence": confidence,

        "damage_probabilities": damage_probabilities,

        "inference_time_ms": inference_time,
    }


if __name__ == "__main__":

    print("Prediction module ready.")