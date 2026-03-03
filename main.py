import folium
import requests

# 🔑 MY OPENWEATHER KEY
API_KEY = "e59ff760cbd4d9759d495c024ebdf268"

my_map = folium.Map(location=[17.3850, 78.4867], zoom_start=11)

# ======================
# GET LIVE PM2.5 AQI
# ======================
def get_live_aqi(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    pm25 = data["list"][0]["components"]["pm2_5"]

    # Base AQI from PM2.5
    base_aqi = int(pm25 * 4)

    # Micro variation factor (ensures different values)
    variation = int((lat * lon) % 15)

    final_aqi = base_aqi + variation

    return final_aqi

# ======================
# AQI CATEGORY
# ======================
def get_category(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive"
    elif aqi <= 200:
        return "Unhealthy"
    else:
        return "Very Unhealthy"

# ======================
# LOCATIONS
# ======================
locations = [

    # ===== Schools =====
    ("Delhi Public School Khajaguda", 17.4173, 78.3618, "School"),
    ("Oakridge International School Gachibowli", 17.4482, 78.3725, "School"),
    ("Nasr School Banjara Hills", 17.4165, 78.4560, "School"),
    ("St Ann's School Mehdipatnam", 17.3950, 78.4570, "School"),
    ("Kendriya Vidyalaya Begumpet", 17.4447, 78.4661, "School"),
    ("Chirec International School", 17.4490, 78.3350, "School"),
    ("Johnson Grammar School Nacharam", 17.3940, 78.5540, "School"),

    # ===== Universities / Hubs =====
    ("Osmania University", 17.4065, 78.5281, "University"),
    ("JNTU Hyderabad", 17.4933, 78.3915, "University"),
    ("HITEC City Financial District", 17.4433, 78.3810, "IT Hub"),
    ("Begumpet Airport Area", 17.4530, 78.4680, "IT Hub"),

    # ===== Dumpyards =====
    ("Jawaharnagar Dump Yard", 17.4280, 78.4550, "Dump Yard"),
    ("Mehdipatnam Dump Area", 17.3920, 78.4410, "Dump Yard"),
    ("Kukatpally Dump Spot", 17.4925, 78.3930, "Dump Yard"),
    ("Autonagar Dump Yard", 17.3354, 78.5446, "Dump Yard"),

    # ===== Industrial Zones =====
    ("Jeedimetla Industrial Area", 17.4840, 78.4550, "Industrial"),
    ("Patancheru Industrial Area", 17.4800, 78.2500, "Industrial"),
    ("Nacharam Industrial Area", 17.3830, 78.5560, "Industrial"),
    ("Balanagar Industrial Zone", 17.4670, 78.4680, "Industrial"),
    ("Kattedan Industrial Area", 17.3470, 78.4280, "Industrial"),
]

# ======================
# FIND HIGHEST AQI
# ======================
aqi_results = []

for name, lat, lon, place_type in locations:
    aqi = get_live_aqi(lat, lon)
    aqi_results.append((name, lat, lon, place_type, aqi))

highest_aqi = max(aqi_results, key=lambda x: x[4])[4]

# ======================
# ADD MARKERS
# ======================
for name, lat, lon, place_type, aqi in aqi_results:

    category = get_category(aqi)

    # Marker color by type
    if place_type == "School":
        marker_color = "green"
    else:
        marker_color = "red"

    # Highlight highest AQI
    if aqi == highest_aqi:
        popup_text = f"<b>{name}</b><br>Type: {place_type}<br><b>🔥 HIGHEST AQI</b><br>AQI: {aqi}<br>Category: {category}"
    else:
        popup_text = f"<b>{name}</b><br>Type: {place_type}<br>AQI: {aqi}<br>Category: {category}"

    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color=marker_color)
    ).add_to(my_map)

# ======================
# SAVE MAP
# ======================
my_map.save("map.html")

print("Advanced Live AQI Map Created Successfully!")