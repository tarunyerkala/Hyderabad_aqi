import folium

# Create Hyderabad base map
my_map = folium.Map(location=[17.3850, 78.4867], zoom_start=11)

# Function to get marker color based on AQI
def get_aqi_color(aqi):
    if aqi <= 50:
        return "green"
    elif aqi <= 100:
        return "lightgreen"
    elif aqi <= 150:
        return "orange"
    else:
        return "red"

# Locations with AQI
locations = [
    # ===== Schools =====
    ("Delhi Public School Khajaguda", 17.4173, 78.3618, "School", 95),
    ("Oakridge International School Gachibowli", 17.4482, 78.3725, "School", 88),
    ("Nasr School Banjara Hills", 17.4165, 78.4560, "School", 102),
    ("St Ann's School Mehdipatnam", 17.3950, 78.4570, "School", 85),
    ("Kendriya Vidyalaya Begumpet", 17.4447, 78.4661, "School", 110),
    ("Chirec International School", 17.4490, 78.3350, "School", 92),
    ("Johnson Grammar School Nacharam", 17.3940, 78.5540, "School", 120),

    # ===== Universities / Hubs =====
    ("Osmania University", 17.4065, 78.5281, "University", 150),
    ("JNTU Hyderabad", 17.4933, 78.3915, "University", 135),
    ("HITEC City Financial District", 17.4433, 78.3810, "IT Hub", 125),
    ("Begumpet Airport Area", 17.4530, 78.4680, "IT Hub", 130),

    # ===== Dumpyards =====
    ("Jawaharnagar Dump Yard", 17.4280, 78.4550, "Dump Yard", 180),
    ("Mehdipatnam Dump Area", 17.3920, 78.4410, "Dump Yard", 165),
    ("Kukatpally Dump Spot", 17.4925, 78.3930, "Dump Yard", 170),
    ("Autonagar Dump Yard", 17.3354, 78.5446, "Dump Yard", 175),

    # ===== Industrial Zones =====
    ("Jeedimetla Industrial Area", 17.4840, 78.4550, "Industrial", 160),
    ("Patancheru Industrial Area", 17.4800, 78.2500, "Industrial", 185),
    ("Nacharam Industrial Area", 17.3830, 78.5560, "Industrial", 150),
    ("Balanagar Industrial Zone", 17.4670, 78.4680, "Industrial", 155),
    ("Kattedan Industrial Area", 17.3470, 78.4280, "Industrial", 165),
]

# Add markers to map
for name, lat, lon, place_type, aqi in locations:

    popup_html = f"""
    <div style="
    font-family:Arial;
    width:180px;
    text-align:center;
    ">
        <h4 style="margin:5px;color:#222;">{name}</h4>
        <p style="font-size:13px;color:#666;margin:4px;">Type: {place_type}</p>
        <p style="font-size:13px;margin:4px;">AQI: <b style="color:#d9534f;">{aqi}</b></p>
        <a href="details.html?name={name}&type={place_type}&aqi={aqi}&lat={lat}&lon={lon}" target="_blank"
        style="
        display:block;
        margin-top:8px;
        padding:8px;
        background:#28a745;
        color:white;
        text-decoration:none;
        border-radius:6px;
        font-weight:bold;
        ">
        View Full Details
        </a>
    </div>
    """

    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=250),
        icon=folium.Icon(color=get_aqi_color(aqi))
    ).add_to(my_map)

# Details page overlay
details_page = """
<div id="detailsPage" style="
display:none;
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:white;
z-index:9999;
font-family:Arial;
padding:40px;
">
<h1 id="d_name"></h1>
<div style="font-size:20px;margin-top:20px;">
<p><b>Type:</b> <span id="d_type"></span></p>
<p><b>AQI:</b> <span id="d_aqi"></span></p>
<p><b>Latitude:</b> <span id="d_lat"></span></p>
<p><b>Longitude:</b> <span id="d_lon"></span></p>
</div>
<button onclick="closeDetails()"
style="margin-top:30px;padding:10px 20px;background:red;color:white;border:none;border-radius:6px;">
Back to Map
</button>
</div>

<script>
function openDetails(name,type,aqi,lat,lon){
    document.getElementById("detailsPage").style.display="block";
    document.getElementById("d_name").innerHTML=name;
    document.getElementById("d_type").innerHTML=type;
    document.getElementById("d_aqi").innerHTML=aqi;
    document.getElementById("d_lat").innerHTML=lat;
    document.getElementById("d_lon").innerHTML=lon;
}
function closeDetails(){
    document.getElementById("detailsPage").style.display="none";
}
</script>
"""

# AQI Legend overlay
aqi_legend = """
<div style="
position: fixed;
bottom: 50px;
left: 50px;
width: 200px;
background-color: white;
border:2px solid grey;
z-index:9999;
font-size:14px;
padding: 10px;
border-radius:7px;
">
<b>AQI Legend</b><br>
<span style="color:green">●</span> 0–50 (Good)<br>
<span style="color:lightgreen">●</span> 51–100 (Moderate)<br>
<span style="color:orange">●</span> 101–150 (Sensitive)<br>
<span style="color:red">●</span> 151+ (Unhealthy)
</div>
"""

# Add overlays to map
my_map.get_root().html.add_child(folium.Element(details_page))
my_map.get_root().html.add_child(folium.Element(aqi_legend))

# Save map
my_map.save("map.html")
print("Map saved to map.html")