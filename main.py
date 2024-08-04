import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

# Importing data
demographic_data = {
    'fifteen-twentyfour': '15-24.csv',
    'twentyfive-fortyfour': '25-44.csv',
    'fortyfive-sixtyfour': '45-64.csv',
    'sixtyfive+': '65+.csv',
    'asian': 'asian.csv',
    'black': 'black.csv',
    'female': 'female.csv',
    'hispanic': 'hispanic.csv',
    'male': 'male.csv',
    'multi': 'multi.csv',
    'native': 'native.csv',
    'white': 'white.csv',
}

# Load state geometries
state = gpd.read_file("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json")

# Reproject state geometries to a projected CRS (e.g., EPSG 3857)
state = state.to_crs(epsg=3857)

# Function to merge data with state geometries
def merge_data(demographic_key):
    data = pd.read_csv(demographic_data[demographic_key])
    # Debug: Print data columns
    print(f"Columns in {demographic_key} data:", data.columns)
    return state.merge(data, left_on='NAME', right_on='State')

# Create data for each demographic
data_frames = {key: merge_data(key) for key in demographic_data}

# Set pandas display options for better viewing
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth', 199)

# Function to build the map based on the selected demographic
# Function to build the map based on the selected demographic
def buildmap(demographic):
    global m  # Declare m as global
    df = data_frames[demographic]
    
    # Debug: Print merged dataframe columns and a sample of the data
    print("Merged dataframe columns:", df.columns)
    print("Sample data:", df.head())

    m = folium.Map(location=[df.geometry.centroid.y.mean(), df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)

    fg = folium.FeatureGroup(name="Income", show=True)
    high = int(df['Income'].max())
    low = int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
    colormap.caption = "Income"
    colormap.add_to(m)

    style_function = lambda x: {
        'fillColor': colormap(x['properties']["Income"]) if pd.notnull(x['properties']["Income"]) else 'gray',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.45,
        'opacity': 0.4
    }

    folium.GeoJson(df, style_function=style_function,
                   tooltip=folium.GeoJsonTooltip(fields=['Income', 'State'])
                   ).add_to(fg)
    fg.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

# Example usage
race = input('Enter one of the following categories: fifteen-twentyfour, twentyfive-fortyfour, fortyfive-sixtyfour, sixtyfive+, asian, black, female, hispanic, male, multi, native, white: ')
buildmap(race)

# Save the map to an HTML file and print the file path
output_file = 'map.html'
m.save(output_file)
print(f"Map saved to {output_file}. Open this file in a web browser to view the map.")
