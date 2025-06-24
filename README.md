<<<<<<< HEAD
"# MST-based Supply Network" 
Dehradun Supply Chain Optimization (MST-Based)
This project visualizes and optimizes the power supply distribution across Dehradun using Minimum Spanning Tree (MST) algorithms—Kruskal's and Prim's—within a Django web application featuring interactive map support and detailed graph analysis.

 Features:
  Interactive Map UI using Leaflet.js to select areas in Dehradun.

   MST Algorithm Implementation: Choose between Kruskal's or Prim's algorithm for optimal supply chain planning.
 
  Cost & Distance Calculation between all selected substations using the Haversine formula.

  Graphical Visualization of the MST using NetworkX and Matplotlib.

  Map Visualization of the Network with directional edges and real-time MST overlay.

   Dynamic Area Data Fetching via OpenStreetMap (Overpass API).

🛠️ Tech Stack
Technology	Usage
Django	Web framework and backend logic
Leaflet.js	Frontend map visualization
NetworkX	Graph structure and MST generation
Matplotlib	Graph image plotting
HTML/CSS/JS	Interactive frontend with dynamic UI
OpenStreetMap	Area data & coordinates
SQLite	Default database (via Django)

📌 How It Works
1. Area Selection
Users interact with a Leaflet map to select substations or regions within Dehradun.

Area coordinates are loaded via OpenStreetMap Overpass API.

2. Edge Generation
For each pair of selected areas, the Haversine distance is calculated.

Cost is computed as:
cost = distance_in_km * 1000

3. Algorithm Choice
Users choose either:

Kruskal’s Algorithm – Greedy approach using sorted edges.

Prim’s Algorithm – Expands from a starting node with the smallest edge.

4. MST Generation
MST is computed from selected edges.

Total distance and cost of the MST are calculated and displayed.

5. Visualization
📈 Static Graph: Generated using NetworkX and Matplotlib.

🗺️ Dynamic Map Overlay: Edges and nodes rendered on the map using Leaflet.js with directional arrows and color codes.

FOLDER STRUCTURE:
mst_project/
├── templates/                  # All HTML files
│   ├── home.html
│   ├── map_selection.html
│   ├── algorithm_selection.html
│   └── results.html
├── static/                     # Static files (CSS, JS, icons)
├── views.py                    # Django views
├── urls.py                     # URL routing
├── algorithms.py               # Kruskal & Prim logic
├── settings.py                 # Django configuration
├── asgi.py / wsgi.py           # Server interface
└── db.sqlite3                  # SQLite database


