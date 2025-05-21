from django.shortcuts import render, redirect
import json
import requests 
from .algorithms import kruskal, prim
from django.http import JsonResponse
from math import radians, sin, cos, sqrt, atan2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import io
import base64

# Initialize with default areas but allow additions
AREA_COORDINATES = {}

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points 
    on the Earth's surface using the Haversine formula.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    # Earth radius in kilometers
    R = 6371.0088
    distance = R * c
    
    return distance

def load_dehradun_areas():
    """Fetch Dehradun areas from OpenStreetMap or other API"""
    global AREA_COORDINATES
    try:
        # Example using Overpass API for OpenStreetMap
        overpass_url = "https://overpass-api.de/api/interpreter"
        query = """
        [out:json];
        area["name"="Dehradun"]->.searchArea;
        (
          node["place"~"suburb|neighbourhood|quarter|village|town"](area.searchArea);
          way["place"~"suburb|neighbourhood|quarter|village|town"](area.searchArea);
          relation["place"~"suburb|neighbourhood|quarter|village|town"](area.searchArea);
          node["name"~".",i](area.searchArea)(if: t["place"]);
          way["name"~".",i](area.searchArea)(if: t["place"]);
          relation["name"~".",i](area.searchArea)(if: t["place"]);
        );
        out center;
        """
        response = requests.get(overpass_url, params={'data': query})
        data = response.json()
        AREA_COORDINATES = {}  # Clear existing areas
        for element in data['elements']:
            name = element.get('tags', {}).get('name', '')
            if name:
                if 'center' in element:
                    AREA_COORDINATES[name] = {
                        'lat': element['center']['lat'],
                        'lng': element['center']['lon']
                    }
                elif 'lat' in element:
                    AREA_COORDINATES[name] = {
                        'lat': element['lat'],
                        'lng': element['lon']
                    }
        # Add some important landmarks if they're missing
        important_areas = {
            'ISBT': {'lat': 30.3165, 'lng': 78.0322},
            'Clock Tower': {'lat': 30.3181, 'lng': 78.0295},
            'Rajpur': {'lat': 30.3946, 'lng': 78.0964},
            'Premnagar': {'lat': 30.3465, 'lng': 78.0398},
            'Ballupur': {'lat': 30.3338, 'lng': 78.0425},
            'Raipur': {'lat': 30.3536, 'lng': 78.0678},
            'Sahastradhara': {'lat': 30.3832, 'lng': 78.1161},
            'Mussoorie Road': {'lat': 30.3356, 'lng': 78.0625}
        }
        for area, coords in important_areas.items():
            if area not in AREA_COORDINATES:
                AREA_COORDINATES[area] = coords
                
    except Exception as e:
        print(f"Error loading areas: {e}")
        # Fallback to some default areas
        AREA_COORDINATES = important_areas.copy()

# Load areas when the module is imported
load_dehradun_areas()

def home(request):
    return render(request, 'home.html')

def map_selection(request):
    if request.method == 'POST':
        selected_areas = request.POST.get('selected_areas', '').split(',')
        selected_areas = [area.strip() for area in selected_areas if area.strip()]
        request.session['selected_areas'] = selected_areas
        request.session['area_coordinates'] = AREA_COORDINATES
        
        if len(selected_areas) >= 2:
            edges = []
            for i in range(len(selected_areas)):
                for j in range(i+1, len(selected_areas)):
                    area1 = selected_areas[i]
                    area2 = selected_areas[j]
                    coord1 = AREA_COORDINATES[area1]
                    coord2 = AREA_COORDINATES[area2]
                    
                    distance_km = round(haversine(
                        coord1['lat'], coord1['lng'],
                        coord2['lat'], coord2['lng']
                    ), 2)
                    
                    cost = distance_km * 1000  # Cost in meters
                    edges.append((area1, area2, distance_km, cost))
            
            request.session['edges'] = edges
            return redirect('algorithm_selection')
        return redirect('map_selection')
    
    return render(request, 'map_selection.html', {
        'AREA_COORDINATES_json': json.dumps(AREA_COORDINATES)
    })

def algorithm_selection(request):
    print("\n=== algorithm_selection view ===")
    print("Session data on entry:", request.session.keys())
    
    if 'selected_areas' not in request.session or 'edges' not in request.session:
        print("Missing session data, redirecting to map_selection")
        return redirect('map_selection')
    
    if request.method == 'POST':
        print("POST data:", request.POST)
        algorithm = request.POST.get('algorithm')
        if algorithm in ['kruskal', 'prim']:
            print(f"Selected algorithm: {algorithm}")
            request.session['algorithm'] = algorithm
            request.session.modified = True  # Force session save
            print("Session after setting algorithm:", request.session.keys())
            return redirect('show_results')
        else:
            print("Invalid algorithm selected")
            return render(request, 'algorithm_selection.html', {
                'selected_areas': request.session['selected_areas'],
                'edges': request.session['edges'],
                'error': 'Please select a valid algorithm'
            })
    
    print("Rendering algorithm selection page")
    return render(request, 'algorithm_selection.html', {
        'selected_areas': request.session['selected_areas'],
        'edges': request.session['edges']
    })

def show_results(request):
    print("\n=== show_results view ===")
    print("Session data:", request.session.keys())
    
    selected_areas = request.session.get('selected_areas', [])
    algorithm = request.session.get('algorithm', '')
    edges = request.session.get('edges', [])
    
    print(f"Selected areas: {selected_areas}")
    print(f"Algorithm: {algorithm}")
    print(f"Edges count: {len(edges)}")
    
    if not selected_areas or algorithm not in ['kruskal', 'prim'] or not edges:
        print("Missing required data, redirecting to map_selection")
        return redirect('map_selection')
    
    try:
        # For algorithms, use (u, v, cost)
        algorithm_edges = [(u, v, cost) for u, v, dist, cost in edges]
        
        if algorithm == 'kruskal':
            result, total_cost = kruskal(selected_areas, algorithm_edges)
        else:
            result, total_cost = prim(selected_areas, algorithm_edges)
            
        print("MST calculation successful")
        print(f"Result edges: {result}")
        print(f"Total cost: {total_cost}")
            
        # For visualization, use (u, v, distance)
        display_edges = []
        for u, v, cost in result:
            for x, y, d, c in edges:
                if {u, v} == {x, y}:
                    display_edges.append((x, y, d, c))
                    break
        
        # For visualization, use (u, v, distance)
        visualization_edges = [(u, v, dist) for u, v, dist, cost in edges]
        
        # Create graph visualization
        graph_img = create_graph_visualization(
            selected_areas, 
            visualization_edges, 
            [(u, v, dist) for u, v, dist, cost in display_edges],  # MST edges with distance
            algorithm
        )

        total_distance = sum(d for _, _, d, _ in display_edges)
        
        print("Rendering results page")
        return render(request, 'results.html', {
            'algorithm': algorithm,
            'total_distance': total_distance,
            'total_cost': total_cost,
            'selected_areas': selected_areas,
            'selected_areas_json': json.dumps(selected_areas),
            'area_coordinates_json': json.dumps(request.session.get('area_coordinates', {})),
            'mst_edges_json': json.dumps([{'from': u, 'to': v, 'distance': d, 'cost': c} 
                                         for u, v, d, c in display_edges]),
            'all_edges_json': json.dumps(edges),
            'graph_img': graph_img,
            'display_edges': display_edges
        })
        
    except Exception as e:
        print(f"Error in show_results: {e}")
        return redirect('map_selection')

def create_graph_visualization(areas, all_edges, mst_edges, algorithm):
    """Create a matplotlib graph visualization of the MST"""
    plt.figure(figsize=(8,6))
    G = nx.Graph()
    
    # Add all nodes
    G.add_nodes_from(areas)
    
    # Add all edges (light gray)
    for u, v, w in all_edges:
        G.add_edge(u, v, weight=w, color='lightgray', width=1)
    
    # Add MST edges (highlighted)
    for u, v, w in mst_edges:
        if G.has_edge(u, v):
            if algorithm == 'kruskal':
                G.edges[u, v].update({
                    'color': '#e74c3c',  # Red for Kruskal
                    'style': 'solid',
                    'width': 3
                })
            else:
                G.edges[u, v].update({
                    'color': '#3498db',  # Blue for Prim
                    'style': 'solid',
                    'width': 3
                })
    
    # Position nodes using spring layout
    pos = nx.spring_layout(G, seed=42, k=0.5)
    
    # Draw all edges first
    edges = G.edges()
    colors = [G[u][v]['color'] for u, v in edges]
    widths = [G[u][v]['width'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, width=widths)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    
    # Draw edge labels
    edge_labels = {(u, v): f"{w:.1f}" for u, v, w in mst_edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    
    plt.title(f"Minimum Spanning Tree ({algorithm.capitalize()}'s Algorithm)")
    plt.axis('off')
    
    # Save to a temporary buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    
    # Encode as base64 for HTML
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{image_base64}"

def refresh_areas(request):
    """API endpoint to refresh areas from OSM"""
    try:
        load_dehradun_areas()
        return JsonResponse({
            'status': 'success',
            'area_count': len(AREA_COORDINATES)
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)