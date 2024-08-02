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
fifteen = pd.read_csv('15-24.csv', delimiter=',', quotechar='"', skipinitialspace=True)
twentyfive = pd.read_csv('25-44.csv', delimiter=',', quotechar='"', skipinitialspace=True)
fourtyfive = pd.read_csv('45-64.csv', delimiter=',', quotechar='"', skipinitialspace=True)
sixtyfive = pd.read_csv('65+.csv', delimiter=',', quotechar='"', skipinitialspace=True)
asian = pd.read_csv('asian.csv', delimiter=',', quotechar='"', skipinitialspace=True)
black = pd.read_csv('black.csv', delimiter=',', quotechar='"', skipinitialspace=True)
female = pd.read_csv('female.csv', delimiter=',', quotechar='"', skipinitialspace=True)
hispanic = pd.read_csv('hispanic.csv', delimiter=',', quotechar='"', skipinitialspace=True)
male = pd.read_csv('male.csv', delimiter=',', quotechar='"', skipinitialspace=True)
multi = pd.read_csv('multi.csv', delimiter=',', quotechar='"', skipinitialspace=True)
native = pd.read_csv('native.csv', delimiter=',', quotechar='"', skipinitialspace=True)
white = pd.read_csv('white.csv', delimiter=',', quotechar='"', skipinitialspace=True)


# Load the GeoJSON file
state = gpd.read_file("states.json")

# Merge the dataframes
df = state.merge(d, left_on='NAME', right_on='State')
fifteen = state.merge(fifteen, left_on='NAME', right_on='State')
twentyfive = state.merge(twentyfive, left_on='NAME', right_on='State')
fourtyfive = state.merge(fourtyfive, left_on='NAME', right_on='State')
sixtyfive = state.merge(sixtyfive, left_on='NAME', right_on='State')
asian = state.merge(asian, left_on='NAME', right_on='State')
black = state.merge(black, left_on='NAME', right_on='State')
female = state.merge(female, left_on='NAME', right_on='State')
hispanic = state.merge(hispanic, left_on='NAME', right_on='State')
male = state.merge(male, left_on='NAME', right_on='State')
multi = state.merge(multi, left_on='NAME', right_on='State')
native = state.merge(native, left_on='NAME', right_on='State')
white = state.merge(white, left_on='NAME', right_on='State')




# Convert the 'Income' column to int
df = df.astype({"Income": int})
fifteen = fifteen.astype({"Income": int})
twentyfive = twentyfive.astype({"Income": int})
fourtyfive = fourtyfive.astype({"Income": int})
sixtyfive = sixtyfive.astype({"Income": int})
asian = asian.astype({"Income": int})
black = black.astype({"Income": int})
female = female.astype({"Income": int})
hispanic = hispanic.astype({"Income": int})
male = male.astype({"Income": int})
multi = multi.astype({"Income": int})
native = native.astype({"Income": int})
white = white.astype({"Income": int})


# Function to build the map
def buildmap(cat):
    if cat == 'none':
        df_projected = df.to_crs(epsg=3857)
        centroid = df_projected.geometry.centroid.to_crs(epsg=4326)
        m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=5)
        folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
        fg = folium.FeatureGroup(name="Income", show=True)
        folium.GeoJson(df, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple'])
                       ).add_to(fg)
        fg.add_to(m)
    elif cat == 'fifteen':
        fifteen_projected = fifteen.to_crs(epsg=3857)
        centroid = fifteen_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(fifteen, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'twentyfive':
        twentyfive_projected = twentyfive.to_crs(epsg=3857)
        centroid = twentyfive_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(twentyfive, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'fourtyfive':
        fourtyfive_projected = fourtyfive.to_crs(epsg=3857)
        centroid = fourtyfive_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(fourtyfive, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'sixtyfive':
        sixtyfive_projected = sixtyfive.to_crs(epsg=3857)
        centroid = sixtyfive_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(sixtyfive, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'asian':
        asian_projected = asian.to_crs(epsg=3857)
        centroid = asian_projected.geometry.centroid.to_crs(epsg=4326)
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
    elif cat == 'black':
        black_projected = black.to_crs(epsg=3857)
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
        folium.GeoJson(black, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'female':
        female_projected = female.to_crs(epsg=3857)
        centroid = female_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(female, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'hispanic':
        hispanic_projected = hispanic.to_crs(epsg=3857)
        centroid = hispanic_projected.geometry.centroid.to_crs(epsg=4326)
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
    elif cat == 'male':
        male_projected = male.to_crs(epsg=3857)
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
        folium.GeoJson(male, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'multi':
        multi_projected = multi.to_crs(epsg=3857)
        centroid = multi_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(multi, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'native':
        native_projected = native.to_crs(epsg=3857)
        centroid = native_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(native, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
    elif cat == 'white':
        white_projected = white.to_crs(epsg=3857)
        centroid = white_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(white, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)

    # Save the map to an HTML file and open it in a web browser
    map_file = 'income_map.html'
    m.save(map_file)
    webbrowser.open('file://' + os.path.realpath(map_file))


# Build blank map
buildmap("none")
# Function to be called when the button is clicked
def on_button_click():
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)
    selected_demo = dem_var
    buildmap(selected_demo)

# Create the main window
root = tk.Tk()
root.title("Income Map Generator")

# Create a label
label = tk.Label(root, text="Select demography:")
label.pack(pady=10)

# Create a dropdown menu
dem_var = tk.StringVar()
dem_options = ["none", "15-24", "25-44", "45-64", "65+", "asian", "black", "female", "hispanic", "male", "multi", "native", "white"]
dem_menu = ttk.Combobox(root, textvariable=dem_var, values=dem_options)
dem_menu.current(0)
dem_menu.pack(pady=10)

# Create a button to generate the map
button = tk.Button(root, text="Generate Map", command=on_button_click)
button.pack(pady=20)

# Run the application
root.mainloop()
