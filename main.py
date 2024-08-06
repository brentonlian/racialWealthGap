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

# Validate geometries
df = df[df.is_valid]
black = black[black.is_valid]
hispanic = hispanic[hispanic.is_valid]
asian = asian[asian.is_valid]
american_indian = american_indian[american_indian.is_valid]
multiple = multiple[multiple.is_valid]

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

    # Debug: Print sample data
    print("Sample Data:")
    print(selected_df[['State', 'Income']].head())

    # Drop rows with missing income data
    selected_df = selected_df.dropna(subset=['Income'])
    selected_df = selected_df[selected_df['Income'] > 0]  # Filter out zero incomes

    # Debug: Check for non-zero income values
    if selected_df.empty:
        print("No data available with non-zero Income for the selected category.")
        return

    # Debug: Check geometries
    if selected_df.empty or selected_df.geometry.is_empty.any():
        print("Warning: Some geometries are missing or empty.")
        return

    # Create the map
    m = folium.Map(location=[selected_df.geometry.centroid.y.mean(), selected_df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)

    # Determine color scale
    high = selected_df['Income'].max()
    low = selected_df['Income'].min()

    # Debug: Print min and max income
    print(f"Min Income: {low}, Max Income: {high}")

    colormap = cm.LinearColormap(colors=['white', 'red'], vmin=low, vmax=high)

    # Define style function
    def style_function(x):
        # Debug: Print the properties being passed to style function
        income_value = x['properties']["Income"]
        print(f"Styling {x['properties']['State']} with Income: {income_value}")
        return {
            'fillColor': colormap(income_value) if pd.notnull(income_value) else 'purple',
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7 if pd.notnull(income_value) else 0,  # Ensure fillOpacity is used
            'opacity': 0.4
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

#testing geometries
import geopandas as gpd
import matplotlib.pyplot as plt

# Export DataFrame to CSV
df.to_csv('df_full.csv', index=False)
black.to_csv('black_full.csv', index=False)
hispanic.to_csv('hispanic_full.csv', index=False)
asian.to_csv('asian_full.csv', index=False)
american_indian.to_csv('american_indian_full.csv', index=False)
multiple.to_csv('multiple_full.csv', index=False)


