# ⚡ Dehradun Supply Chain Optimization (MST-Based)

This project visualizes and optimizes the power supply distribution across Dehradun using **Minimum Spanning Tree (MST)** algorithms — **Kruskal's** and **Prim's** — within a Django web application featuring interactive map support and detailed graph analysis.

---

## 🚀 Features

- 🌍 **Interactive Map UI** using **Leaflet.js** to select areas in Dehradun.
- 🧠 **MST Algorithm Implementation**: Choose between Kruskal's or Prim's algorithm.
- 📊 **Cost & Distance Calculation** using the **Haversine formula**.
- 🖼️ **Graphical Visualization** of MST using **NetworkX** and **Matplotlib**.
- 🗺️ **Map Visualization** with directional edges and live MST overlay.
- 🔁 **Dynamic Area Data Fetching** via **OpenStreetMap (Overpass API)**.

---

## 🛠️ Tech Stack

| Technology      | Usage                                |
|-----------------|--------------------------------------|
| Django          | Web framework and backend logic      |
| Leaflet.js      | Frontend map visualization           |
| NetworkX        | Graph structure and MST generation   |
| Matplotlib      | Graph image plotting                 |
| HTML/CSS/JS     | Interactive frontend + UI styling    |
| OpenStreetMap   | Area data & coordinates              |
| SQLite          | Default lightweight database (Django)|

---

## 📌 How It Works

### 1. Area Selection
- Users select **substations or regions** on the map of Dehradun.
- Area coordinates are fetched dynamically using **Overpass API** from **OpenStreetMap**.

### 2. Edge Generation
- For every selected area pair, the **Haversine formula** calculates the distance.
- **Cost** is calculated using:  
  `cost = distance_in_km × 1000`

### 3. Algorithm Choice
Users can choose either:
- 🔺 **Kruskal’s Algorithm** – Greedy method that sorts all edges by weight and connects without forming cycles.
- 🔹 **Prim’s Algorithm** – Starts from one node and grows the MST by picking the shortest edge to a new node.

### 4. MST Generation
- MST is built based on the selected algorithm.
- **Total cost and distance** are calculated and displayed.

### 5. Visualization
- 📈 **Static Graph** using **NetworkX + Matplotlib**
- 🗺️ **Dynamic Leaflet Map** with color-coded MST overlay and directional arrows

---

## 🧪 Sample Screenshots (To Be Added)

| Feature           | Preview                        |
|------------------|---------------------------------|
| Map Selection     | ✅ Area markers and selection UI |
| Algorithm Page    | ✅ Table of distances + selection |
| Results Page      | ✅ MST graph + interactive map  |

---

## 📁 Folder Structure

mst_project/
├── templates/
│ ├── home.html
│ ├── map_selection.html
│ ├── algorithm_selection.html
│ └── results.html
├── static/
├── views.py
├── urls.py
├── algorithms.py
├── settings.py
├── asgi.py / wsgi.py
└── db.sqlite3


---

## 🧩 Algorithms Used

### 🔺 Kruskal’s Algorithm
- Sort all edges by weight
- Add the smallest edge if it doesn't form a cycle
- Uses **Union-Find**
- **Time Complexity:** `O(E log E)`

### 🔹 Prim’s Algorithm
- Start from any node
- Add the smallest edge connecting to a new node
- Uses **Min Heap (Priority Queue)**
- **Time Complexity:** `O(E log V)`

---

## ✅ How to Run Locally

```bash
# Clone the repo
git clone https://github.com/Anishu-Raj/MST-Supply-Chain-Optimization.git
cd MST-Supply-Chain-Optimization

# Create a virtual environment
python -m venv env
# Activate it
env\Scripts\activate  # On Windows
# OR
source env/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver

Then open http://127.0.0.1:8000/ in your browser.

```
## Future Improvements
**✅ Add real-time GIS data support**

**✅ User authentication and session save**

**✅ Export MST network as CSV/JSON**

**✅ Upload datasets for multiple cities**

## 🙌 Credits
**🧠 MST Algorithms: Custom Python logic in algorithms.py**

**🌍 Map UI: Leaflet.js**

**📊 Graph Rendering: NetworkX + Matplotlib**

**🗺️ Geolocation Data: OpenStreetMap Overpass API**


---
## Sample Screenshots![Screenshot (1134)](https://github.com/user-attachments/assets/fa04aeab-9075-43d1-95f9-4f99519a87f6)
## map selction![Screenshot (1135)](https://github.com/user-attachments/assets/a2c82ac3-ce7e-47e2-a41d-4ef613ceeb02)
## Algorithm selection![Screenshot (1136)](https://github.com/user-attachments/assets/85331722-a64e-49b3-818c-da3e57184cd1) ![Screenshot (1137)](https://github.com/user-attachments/assets/1e99cdbe-cad9-4dba-bff8-df4c84a1e027)
## Result page![Screenshot (1138)](https://github.com/user-attachments/assets/dfce9339-d21b-40f6-9d90-61c36d626e8a) ![Screenshot (1140)](https://github.com/user-attachments/assets/88146fa4-09f6-4f05-b317-50888c465eab)
![Screenshot (1139)](https://github.com/user-attachments/assets/8866a9ba-a6de-4c55-849b-c34b6e81ddbe)





