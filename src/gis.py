import folium
import pandas as pd


DAMAGE_COLORS = {
    "no-damage": "green",
    "minor-damage": "orange",
    "major-damage": "red",
    "destroyed": "darkred",
}


def create_damage_map(data: pd.DataFrame):

    if data.empty:
        return folium.Map(
            location=[17.24, 78.43],
            zoom_start=13
        )

    center_lat = data["latitude"].mean()
    center_lon = data["longitude"].mean()

    damage_map = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=15,
        control_scale=True
    )

    for _, row in data.iterrows():

        damage = str(row["damage"]).lower()

        color = DAMAGE_COLORS.get(
            damage,
            "blue"
        )

        confidence = float(row["confidence"])

        popup_html = f"""
        <div style="font-family: Arial; width: 220px;">

            <h4 style="margin-bottom:10px;">
                🏢 {row['building_id']}
            </h4>

            <b>Damage:</b>
            {damage.replace("-", " ").title()}
            <br><br>

            <b>Confidence:</b>
            {confidence:.1%}
            <br><br>

            <b>Latitude:</b>
            {float(row['latitude']):.6f}
            <br>

            <b>Longitude:</b>
            {float(row['longitude']):.6f}

        </div>
        """

        folium.Marker(
            location=[
                float(row["latitude"]),
                float(row["longitude"])
            ],
            popup=folium.Popup(
                popup_html,
                max_width=300
            ),
            tooltip=(
                f"{row['building_id']} | "
                f"{damage.replace('-', ' ').title()}"
            ),
            icon=folium.Icon(
                color=color,
                icon="home",
                prefix="fa"
            )
        ).add_to(damage_map)

    return damage_map