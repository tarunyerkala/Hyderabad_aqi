import folium

# Create Hyderabad base map
my_map = folium.Map(location=[17.3850, 78.4867], zoom_start=11)

# ======================
# AQI COLOR FUNCTION
# ======================
def get_aqi_color(aqi):
    if aqi <= 50:
        return "green"
    elif aqi <= 100:
        return "lightgreen"
    elif aqi <= 150:
        return "orange"
    else:
        return "red"

# ======================
# LOCATION DATA (10 Total)
# ======================
locations = [
    ("Osmania University", 17.4065, 78.5281, "University", 180),
    ("Jawaharnagar Dump Yard", 17.5373, 78.5838, "Dump Yard", 180),

    ("JNTU Hyderabad", 17.4933, 78.3915, "College", 140),
    ("Kukatpally Dump Yard", 17.4925, 78.3930, "Dump Yard", 140),

    ("Delhi Public School Khajaguda", 17.4173, 78.3618, "School", 95),
    ("Khajaguda Dump Area", 17.4165, 78.3635, "Dump Yard", 95),

    ("Kendriya Vidyalaya LB Nagar", 17.3491, 78.5585, "School", 165),
    ("Autonagar Dump Yard", 17.3354, 78.5446, "Dump Yard", 165),

    ("St Ann's College Mehdipatnam", 17.3956, 78.4390, "College", 85),
    ("Mehdipatnam Dump Site", 17.3920, 78.4410, "Dump Yard", 85),
]

# ======================
# ADD MARKERS
# ======================
for name, lat, lon, place_type, aqi in locations:
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>{name}</b><br>Type: {place_type}<br>AQI: {aqi}",
        icon=folium.Icon(color=get_aqi_color(aqi))
    ).add_to(my_map)

# ======================
# ADD LEGEND
# ======================
legend_html = """
<div style="
position: fixed; 
bottom: 50px; left: 50px; width: 200px; height: 150px; 
background-color: white; 
border:2px solid grey; z-index:9999; font-size:14px;
padding: 10px;
">
<b>AQI Legend</b><br>
<span style="color:green">●</span> 0–50 (Good)<br>
<span style="color:lightgreen">●</span> 51–100 (Moderate)<br>
<span style="color:orange">●</span> 101–150 (Unhealthy for Sensitive)<br>
<span style="color:red">●</span> 151+ (Unhealthy)<br>
</div>
"""

my_map.get_root().html.add_child(folium.Element(legend_html))

# ======================
# SAVE MAP
# ======================
my_map.save("map.html")

print("Map created with 10 locations and legend!")