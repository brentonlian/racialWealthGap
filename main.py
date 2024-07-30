import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
import webbrowser
import os
import tkinter as tk
from tkinter import ttk

# Load the CSV files
d = pd.read_csv('allStats.csv', on_bad_lines='skip', delimiter=',', quotechar='"', skipinitialspace=True)
d = d.replace("%", "", regex=True).replace(",", "", regex=True).fillna("0")
race = pd.read_csv('ageData.csv', delimiter=',', quotechar='"', skipinitialspace=True)
gender = pd.read_csv('genderData.csv', delimiter=',', quotechar='"', skipinitialspace=True)
age = pd.read_csv('raceData.csv', delimiter=',', quotechar='"', skipinitialspace=True)

# Load the GeoJSON file
state = gpd.read_file("states.json")

# Merge the dataframes
df = state.merge(d, left_on='NAME', right_on='State')
race = state.merge(race, left_on='NAME', right_on='State')
gender = state.merge(gender, left_on='NAME', right_on='State')
age = state.merge(age, left_on='NAME', right_on='State')


# Convert the 'Income' column to int
df = df.astype({"Income": int})
race = race.astype({"Income": int})
gender = gender.astype({"Income": int})
age = age.astype({"Income": int})


# Function to build the map
def buildmap(cat):
    if cat == "none":
        df_projected = df.to_crs(epsg=3857)
        centroid = df_projected.geometry.centroid.to_crs(epsg=4326)
        m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=5)
        folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
        fg = folium.FeatureGroup(name="Income", show=True)
        folium.GeoJson(df, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple'])
                       ).add_to(fg)
        fg.add_to(m)
    elif cat == 'race':
        race_projected = race.to_crs(epsg=3857)
        centroid = race_projected.geometry.centroid.to_crs(epsg=4326)
        m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=5)
        folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
        fg = folium.FeatureGroup(name="Income", show=True)
        high = int(df['Income'].max())
        low = int(df['Income'].min())
        colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
        style_function = lambda x: {
            'fillColor': colormap(x['properties']["Income"]),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.45,
            'opacity': 0.4,
            'nan_fill_color': 'purple'
        }
        folium.GeoJson(black, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'gender':
        gender_projected = hispanic.to_crs(epsg=3857)
        centroid = gender_projected.geometry.centroid.to_crs(epsg=4326)
        m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=5)
        folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
        fg = folium.FeatureGroup(name="Income", show=True)
        high = int(df['Income'].max())
        low = int(df['Income'].min())
        colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
        style_function = lambda x: {
            'fillColor': colormap(x['properties']["Income"]),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.45,
            'opacity': 0.4,
            'nan_fill_color': 'purple'
        }
        folium.GeoJson(hispanic, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'age':
        asian_projected = age.to_crs(epsg=3857)
        centroid = age_projected.geometry.centroid.to_crs(epsg=4326)
        m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=5)
        folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
        fg = folium.FeatureGroup(name="Income", show=True)
        high = int(df['Income'].max())
        low = int(df['Income'].min())
        colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
        style_function = lambda x: {
            'fillColor': colormap(x['properties']["Income"]),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.45,
            'opacity': 0.4,
            'nan_fill_color': 'purple'
        }
        folium.GeoJson(asian, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)

    # Save the map to an HTML file and open it in a web browser
    map_file = 'income_map.html'
    m.save(map_file)
    webbrowser.open('file://' + os.path.realpath(map_file))


# BUild blank map
buildmap("none")
# Function to be called when the button is clicked
def on_button_click():
    selected_race = race_var.get()
    buildmap(selected_race)

# Create the main window
root = tk.Tk()
root.title("Income Map Generator")

# Create a label
label = tk.Label(root, text="Select race:")
label.pack(pady=10)

# Create a dropdown menu
race_var = tk.StringVar()
race_options = ["none", "black", "hispanic", "asian", "american_indian", "multiple"]
race_menu = ttk.Combobox(root, textvariable=race_var, values=race_options)
race_menu.current(0)
race_menu.pack(pady=10)

# Create a button to generate the map
button = tk.Button(root, text="Generate Map", command=on_button_click)
button.pack(pady=20)

# Run the application
root.mainloop()
