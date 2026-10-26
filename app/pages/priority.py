"""
EvoDamage - Rescue Priority Engine

Converts damage prediction + disaster context into
an actionable rescue priority score.

This module is independent of the ML model.
It accepts the output of predict_damage().
"""

# Damage severity weights
DAMAGE_WEIGHTS = {
    "no-damage": 0,
    "minor-damage": 25,
    "major-damage": 60,
    "destroyed": 90
}

# Building importance weights
BUILDING_WEIGHTS = {
    "residential": 50,
    "school": 80,
    "hospital": 100,
    "public": 70,
    "commercial": 40,
    "industrial": 30,
    "unknown": 30
}


def calculate_priority(
    prediction,
    building_type="residential",
    occupancy=0,
    accessibility=1.0,
    distance_km=0.0
):
    """
    Calculate rescue priority from damage prediction and context.

    Parameters
    ----------
    prediction : dict
        Output from predict_damage()

    building_type : str
        Type of building.

    occupancy : int
        Estimated number of people affected.

    accessibility : float
        Accessibility factor between 0 and 1.
        1.0 = easily accessible
        0.0 = inaccessible

    distance_km : float
        Distance of rescue team from location.

    Returns
    -------
    dict
        Priority score and explanation.
    """

    damage_class = prediction["damage_class"]
    confidence = prediction["confidence"]

    # --------------------------------------------------
    # 1. DAMAGE SEVERITY
    # --------------------------------------------------

    damage_score = DAMAGE_WEIGHTS.get(damage_class, 0)

    # --------------------------------------------------
    # 2. BUILDING IMPORTANCE
    # --------------------------------------------------

    building_type = building_type.lower()
    building_score = BUILDING_WEIGHTS.get(
        building_type,
        BUILDING_WEIGHTS["unknown"]
    )

    # --------------------------------------------------
    # 3. OCCUPANCY
    # --------------------------------------------------

    # Cap occupancy contribution at 100
    occupancy_score = min(occupancy / 100 * 100, 100)

    # --------------------------------------------------
    # 4. ACCESSIBILITY
    # --------------------------------------------------

    accessibility = max(0.0, min(accessibility, 1.0))

    # Lower accessibility = greater urgency
    accessibility_score = (1 - accessibility) * 100

    # --------------------------------------------------
    # 5. DISTANCE
    # --------------------------------------------------

    # Nearby locations are easier to reach.
    # Farther locations receive a larger urgency contribution.
    distance_score = min(distance_km / 20 * 100, 100)

    # --------------------------------------------------
    # 6. MODEL CONFIDENCE
    # --------------------------------------------------

    confidence = max(0.0, min(confidence, 1.0))

    # --------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------

    priority_score = (
        0.40 * damage_score +
        0.20 * building_score +
        0.20 * occupancy_score +
        0.10 * accessibility_score +
        0.10 * distance_score
    )

    # Confidence adjusts the score slightly
    priority_score *= (0.85 + 0.15 * confidence)

    priority_score = min(max(priority_score, 0), 100)

    # --------------------------------------------------
    # PRIORITY LEVEL
    # --------------------------------------------------

    if priority_score >= 75:
        priority_level = "CRITICAL"
    elif priority_score >= 50:
        priority_level = "HIGH"
    elif priority_score >= 25:
        priority_level = "MEDIUM"
    else:
        priority_level = "LOW"

    return {
        "priority_score": round(priority_score, 2),
        "priority_level": priority_level,
        "damage_class": damage_class,
        "model_confidence": round(confidence, 4),
        "building_type": building_type,
        "occupancy": occupancy,
        "accessibility": accessibility,
        "distance_km": distance_km
    }


if __name__ == "__main__":

    # Example ML prediction
    sample_prediction = {
        "damage_class": "major-damage",
        "confidence": 0.8165,
        "damage_probabilities": {
            "no-damage": 0.0466,
            "minor-damage": 0.0712,
            "major-damage": 0.8165,
            "destroyed": 0.0656
        },
        "inference_time_ms": 41.2
    }

    result = calculate_priority(
        prediction=sample_prediction,
        building_type="residential",
        occupancy=60,
        accessibility=0.4,
        distance_km=8
    )

    print("EvoDamage Rescue Priority")
    print("=========================")

    for key, value in result.items():
        print(f"{key}: {value}")