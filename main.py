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

# Function to merge data with state geometries
def merge_data(demographic_key):
    data = pd.read_csv(demographic_data[demographic_key])
    return state.merge(data, left_on='NAME', right_on='State')

# Create data for each demographic
data_frames = {key: merge_data(key) for key in demographic_data}

# Set pandas display options for better viewing
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth', 199)

# Function to build the map based on the selected demographic
def buildmap(demographic):
    df = data_frames[demographic]
    m = folium.Map(location=[df.geometry.centroid.y.mean(), df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)

    fg = folium.FeatureGroup(name="Income", show=True)
    high = int(df['Income'].max())
    low = int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
    colormap.caption = "Income"
    colormap.add_to(m)

    style_function = lambda x: {
        'fillColor': colormap(x['properties']["Income"]),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.45,
        'opacity': 0.4,
        'nan_fill_color': 'purple'
    }

    folium.GeoJson(df, style_function=style_function,
                   tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Hawaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                   ).add_to(fg)
    fg.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    return m

# Example usage
race = input('Enter one of the following categories: fifteen-twentyfour, twentyfive-fortyfour, fortyfive-sixtyfour, sixtyfive+, asian, black, female, hispanic, male, multi, native, white: ')
buildmap(race)
