from pathlib import Path
from PIL import Image, ImageDraw
import csv
import random


IMAGE_DIR = Path("data/processed/images")
CSV_FILE = Path("data/processed/labels.csv")

CLASSES = {
    "no-damage": 0,
    "minor-damage": 1,
    "major-damage": 2,
    "destroyed": 3
}


def generate_synthetic_dataset(images_per_class=500):
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    random.seed(42)

    rows = []

    for class_name, label in CLASSES.items():

        for i in range(images_per_class):

            image = Image.new(
                "RGB",
                (224, 224),
                (
                    random.randint(80, 180),
                    random.randint(80, 180),
                    random.randint(80, 180)
                )
            )

            draw = ImageDraw.Draw(image)

            x1, y1 = 35, 35
            x2, y2 = 190, 190

            # Building
            draw.rectangle(
                [x1, y1, x2, y2],
                fill=(170, 170, 170),
                outline=(240, 240, 240),
                width=3
            )

            # Damage patterns
            if class_name == "no-damage":

                for _ in range(3):
                    x = random.randint(50, 170)
                    y = random.randint(50, 170)

                    draw.rectangle(
                        [x, y, x + 12, y + 12],
                        fill=(200, 200, 200)
                    )

            elif class_name == "minor-damage":

                for _ in range(8):
                    x = random.randint(45, 175)
                    y = random.randint(45, 175)

                    draw.rectangle(
                        [x, y, x + 10, y + 10],
                        fill=(110, 80, 60)
                    )

            elif class_name == "major-damage":

                for _ in range(20):
                    x = random.randint(40, 180)
                    y = random.randint(40, 180)

                    draw.rectangle(
                        [x, y, x + 12, y + 12],
                        fill=(75, 50, 40)
                    )

                for _ in range(5):
                    x = random.randint(50, 160)
                    y = random.randint(50, 160)

                    draw.line(
                        [(x, y), (x + 30, y + 25)],
                        fill=(40, 30, 25),
                        width=3
                    )

            elif class_name == "destroyed":

                draw.rectangle(
                    [x1, y1, x2, y2],
                    fill=(80, 70, 60)
                )

                for _ in range(50):
                    x = random.randint(30, 185)
                    y = random.randint(30, 185)
                    size = random.randint(5, 18)

                    draw.rectangle(
                        [x, y, x + size, y + size],
                        fill=(
                            random.randint(30, 100),
                            random.randint(25, 80),
                            random.randint(20, 60)
                        )
                    )

            filename = f"{class_name}_{i:04d}.jpg"

            image.save(
                IMAGE_DIR / filename,
                quality=95
            )

            rows.append([
                filename,
                label,
                class_name,
                "synthetic_scene",
                "synthetic"
            ])

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "image",
            "label",
            "damage_class",
            "source_image",
            "scene"
        ])

        writer.writerows(rows)

    print("Synthetic dataset created successfully.")
    print("Total images:", len(rows))
    print("Images:", IMAGE_DIR)
    print("Labels:", CSV_FILE)


if __name__ == "__main__":
    generate_synthetic_dataset()