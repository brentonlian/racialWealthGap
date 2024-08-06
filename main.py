import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
import webbrowser
import tempfile
import tkinter as tk
from tkinter import ttk

# Load data
d = pd.read_csv('allStats.csv', on_bad_lines='skip')
d = d.replace("%", "", regex=True).replace(",", "", regex=True).fillna("0")

blac = pd.read_csv('black.csv')
hispani = pd.read_csv('hispanic.csv')
asia = pd.read_csv('asian.csv')
american_india = pd.read_csv('native.csv')
multipl = pd.read_csv('multi.csv')

state = gpd.read_file("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json")

# Merge dataframes
df = state.merge(d, left_on='NAME', right_on='State')
black = state.merge(blac, left_on='NAME', right_on='State')
hispanic = state.merge(hispani, left_on='NAME', right_on='State')
asian = state.merge(asia, left_on='NAME', right_on='State')
american_indian = state.merge(american_india, left_on='NAME', right_on='State')
multiple = state.merge(multipl, left_on='NAME', right_on='State')

# Set types to integer
df = df.astype({"Income": int})
black = black.astype({"Income": int})
hispanic = hispanic.astype({"Income": int})
asian = asian.astype({"Income": int})
american_indian = american_indian.astype({"Income": int})
multiple = multiple.astype({"Income": int})

# Define a function to build the map
def buildmap(demography):
    # Determine the appropriate dataframe
    if demography == "none":
        selected_df = df
    elif demography == "black":
        selected_df = black
    elif demography == "hispanic":
        selected_df = hispanic
    elif demography == "asian":
        selected_df = asian
    elif demography == "american_indian":
        selected_df = american_indian
    elif demography == "multiple":
        selected_df = multiple
    else:
        print(f"Invalid category: {demography}")
        return

    # Create the map
    m = folium.Map(location=[selected_df.geometry.centroid.y.mean(), selected_df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)

    # Determine color scale
    high = selected_df['Income'].max()
    low = selected_df['Income'].min()
    colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
    colormap

    # Define style function
    style_function = lambda x: {
        'fillColor': colormap(x['properties']["Income"]),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.45,
        'opacity': 0.4,
        'nan_fill_color': 'purple'
    }

    # Add GeoJson layer
    folium.GeoJson(selected_df, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State'])
                  ).add_to(fg)
    fg.add_to(m)

    # Add colormap
    colormap.caption = "Income"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    # Save and open map
    m.save('map.html')
    webbrowser.open('map.html')

# Define a function for the GUI
def on_generate_map():
    demography = demographic_selection.get()
    buildmap(demography)

# Create the GUI
root = tk.Tk()
root.title("Demographic Map Generator")

# Label
label = ttk.Label(root, text="Select Demographic Category:")
label.pack(pady=10)

# Dropdown menu
demographic_selection = ttk.Combobox(root, values=["none", "black", "hispanic", "asian", "american_indian", "multiple"])
demographic_selection.current(0)
demographic_selection.pack(pady=10)

# Button
generate_button = ttk.Button(root, text="Generate Map", command=on_generate_map)
generate_button.pack(pady=20)

# Run the GUI
root.mainloop()
