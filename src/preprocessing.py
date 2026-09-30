import json
import csv
from pathlib import Path

from PIL import Image


# xBD damage classes
CLASS_NAMES = {
    "no-damage": 0,
    "minor-damage": 1,
    "major-damage": 2,
    "destroyed": 3,
}

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def find_image(image_dir, image_name):
    """
    Find an image using the exact filename or different image extensions.
    """
    exact = image_dir / image_name

    if exact.exists():
        return exact

    stem = Path(image_name).stem

    for ext in IMAGE_EXTENSIONS:
        candidate = image_dir / f"{stem}{ext}"
        if candidate.exists():
            return candidate

    return None


def get_polygon_points(feature):
    """
    Extract polygon coordinates from an xBD GeoJSON feature.
    """

    geometry = feature.get("geometry", {})

    if not geometry:
        return []

    coordinates = geometry.get("coordinates", [])

    if not coordinates:
        return []

    geometry_type = geometry.get("type")

    if geometry_type == "Polygon":
        return coordinates[0]

    if geometry_type == "MultiPolygon":
        return coordinates[0][0]

    return []


def crop_polygon(image, points, padding=5):
    """
    Crop a rectangular region around a building polygon.

    xBD polygon coordinates are generally pixel coordinates.
    """

    if not points:
        return None

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    left = max(0, int(min(xs)) - padding)
    top = max(0, int(min(ys)) - padding)
    right = min(image.width, int(max(xs)) + padding)
    bottom = min(image.height, int(max(ys)) + padding)

    if right <= left or bottom <= top:
        return None

    return image.crop((left, top, right, bottom))


def process_label_file(label_file, image_dir, output_dir, writer):
    """
    Process one xBD label JSON file.

    Each building becomes one training sample.
    """

    with open(label_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    image_name = label_file.stem + ".png"

    image_path = find_image(image_dir, image_name)

    if image_path is None:
        print(f"Image not found for: {label_file.name}")
        return 0

    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Could not open {image_path}: {e}")
        return 0

    features = data.get("features", [])

    count = 0

    for index, feature in enumerate(features):

        properties = feature.get("properties", {})

        damage_type = properties.get("subtype")

        if damage_type not in CLASS_NAMES:
            continue

        points = get_polygon_points(feature)

        crop = crop_polygon(image, points)

        if crop is None:
            continue

        # Ignore extremely small crops
        if crop.width < 10 or crop.height < 10:
            continue

        crop_name = f"{label_file.stem}_{index}.jpg"

        crop_path = output_dir / crop_name

        crop.save(crop_path, quality=95)

        writer.writerow([
            crop_name,
            damage_type,
            CLASS_NAMES[damage_type],
            str(image_path),
            label_file.stem,
        ])

        count += 1

    return count


def process_dataset(raw_dir, processed_dir):
    """
    Process an xBD dataset.

    Expected general structure:

        raw_dir/
            train/
                images/
                labels/

    The function searches recursively, so minor differences
    in folder organization are tolerated.
    """

    raw_dir = Path(raw_dir)
    processed_dir = Path(processed_dir)

    image_output_dir = processed_dir / "images"

    image_output_dir.mkdir(parents=True, exist_ok=True)

    labels_csv = processed_dir / "labels.csv"

    label_files = list(raw_dir.rglob("*.json"))

    print(f"Found {len(label_files)} JSON files.")

    total_samples = 0

    with open(labels_csv, "w", newline="", encoding="utf-8") as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow([
            "image",
            "damage_class",
            "label",
            "source_image",
            "scene",
        ])

        for i, label_file in enumerate(label_files, start=1):

            # Look for the closest images directory
            possible_image_dirs = [
                label_file.parent.parent / "images",
                label_file.parent / "images",
                raw_dir / "images",
            ]

            image_dir = None

            for directory in possible_image_dirs:
                if directory.exists():
                    image_dir = directory
                    break

            if image_dir is None:
                # Search recursively for images
                image_candidates = list(raw_dir.rglob(
                    f"{label_file.stem}.png"
                ))

                if image_candidates:
                    image_dir = image_candidates[0].parent

            if image_dir is None:
                print(f"No image directory found for {label_file}")
                continue

            samples = process_label_file(
                label_file,
                image_dir,
                image_output_dir,
                writer,
            )

            total_samples += samples

            if i % 100 == 0:
                print(
                    f"Processed {i}/{len(label_files)} label files | "
                    f"Samples: {total_samples}"
                )

    print("\nPreprocessing complete.")
    print(f"Total building samples: {total_samples}")
    print(f"Labels saved to: {labels_csv}")


if __name__ == "__main__":

    RAW_DATA_DIR = Path("data/raw/xbd")

    PROCESSED_DATA_DIR = Path("data/processed")

    process_dataset(
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
    )