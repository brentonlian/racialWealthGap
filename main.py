import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
import webbrowser
import tempfile

# Load data
d = pd.read_csv('allStats.csv', on_bad_lines='skip')
d = d.replace("%", "", regex=True).replace(",", "", regex=True).fillna("0")

blac = pd.read_csv('black.csv')
hispani = pd.read_csv('hispanic.csv')
asia = pd.read_csv('asian.csv')
american_india = pd.read_csv('native.csv')
multipl = pd.read_csv('multi.csv')

state = gpd.read_file("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json")

# Convert "Income" to numeric and handle non-numeric entries
d["Income"] = pd.to_numeric(d["Income"], errors="coerce")
blac["Income"] = pd.to_numeric(blac["Income"], errors="coerce")
hispani["Income"] = pd.to_numeric(hispani["Income"], errors="coerce")
asia["Income"] = pd.to_numeric(asia["Income"], errors="coerce")
american_india["Income"] = pd.to_numeric(american_india["Income"], errors="coerce")
multipl["Income"] = pd.to_numeric(multipl["Income"], errors="coerce")

# Merge dataframes
df = state.merge(d, left_on='NAME', right_on='State')
black = state.merge(blac, left_on='NAME', right_on='State')
hispanic = state.merge(hispani, left_on='NAME', right_on='State')
asian = state.merge(asia, left_on='NAME', right_on='State')
american_indian = state.merge(american_india, left_on='NAME', right_on='State')
multiple = state.merge(multipl, left_on='NAME', right_on='State')

# Ensure geometries are in the same coordinate system
state = state.to_crs(epsg=3857)
df = df.to_crs(epsg=3857)
black = black.to_crs(epsg=3857)
hispanic = hispanic.to_crs(epsg=3857)
asian = asian.to_crs(epsg=3857)
american_indian = american_indian.to_crs(epsg=3857)
multiple = multiple.to_crs(epsg=3857)

# Define a function to build the map
def buildmap(race):
    # Determine the appropriate dataframe
    if race == "none":
        selected_df = df
    elif race == "black":
        selected_df = black
    elif race == "hispanic":
        selected_df = hispanic
    elif race == "asian":
        selected_df = asian
    elif race == "american_indian":
        selected_df = american_indian
    elif race == "multiple":
        selected_df = multiple
    else:
        print(f"Invalid race category: {race}")
        return

    # Create the map
    m = folium.Map(location=[selected_df.geometry.centroid.y.mean(), selected_df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)

    # Determine color scale
    high = selected_df['Income'].max()
    low = selected_df['Income'].min()
    colormap = cm.LinearColormap(colors=['white', 'red'], vmin=low, vmax=high)

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
                  ).add_to(m)

    # Add colormap
    colormap.caption = "Income"
    colormap.add_to(m)

    # Save the map to a temporary HTML file and open it
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        m.save(f.name)
        webbrowser.open(f.name)

# Get user input
race = input('Enter none, black, hispanic, asian, american_indian, or multiple: ')

# Build the map based on user input
buildmap(race)
