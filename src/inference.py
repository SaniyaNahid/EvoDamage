from predict import predict_damage
from priority import calculate_priority


def assess_building(
    image_path,
    building_type="residential",
    occupancy=0,
    accessibility=1.0,
    distance_km=0.0
):
    """
    Complete EvoDamage assessment pipeline.

    Image
        ↓
    Damage prediction
        ↓
    Rescue priority
    """

    # Step 1: AI damage prediction
    prediction = predict_damage(image_path)

    # Step 2: Rescue priority
    priority = calculate_priority(
        prediction=prediction,
        building_type=building_type,
        occupancy=occupancy,
        accessibility=accessibility,
        distance_km=distance_km
    )

    # Step 3: Combine results
    result = {
        "damage_class": prediction["damage_class"],
        "confidence": prediction["confidence"],
        "damage_probabilities": prediction["damage_probabilities"],
        "inference_time_ms": prediction["inference_time_ms"],
        "priority_score": priority["priority_score"],
        "priority_level": priority["priority_level"],
        "building_type": priority["building_type"],
        "occupancy": priority["occupancy"],
        "accessibility": priority["accessibility"],
        "distance_km": priority["distance_km"]
    }

    return result


if __name__ == "__main__":

    image = "data/processed/images/major-damage_0000.jpg"

    result = assess_building(
        image_path=image,
        building_type="residential",
        occupancy=60,
        accessibility=0.4,
        distance_km=8
    )

    print("\nEvoDamage Complete Assessment")
    print("=============================")

    print("Damage Class     :", result["damage_class"])
    print("Confidence       :", f"{result['confidence'] * 100:.2f}%")
    print("Inference Time   :", f"{result['inference_time_ms']:.2f} ms")
    print("Priority Score   :", result["priority_score"])
    print("Priority Level   :", result["priority_level"])