import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm

# Load the CSV files
d = pd.read_csv('allStats.csv', on_bad_lines='skip')
d = d.replace("%", "", regex=True).replace(",", "", regex=True).fillna("0")
blac = pd.read_csv('blackStats.csv')
hispani = pd.read_csv('hispanicStats.csv')
asia = pd.read_csv('asianStats.csv')
american_india = pd.read_csv('americanIndianStats.csv')
multipl = pd.read_csv('multipleStats.csv')

# Load the GeoJSON file
state = gpd.read_file("states.json")

# Merge the dataframes
df = state.merge(d, left_on='NAME', right_on='State')
black = state.merge(blac, left_on='NAME', right_on='State')
hispanic = state.merge(hispani, left_on='NAME', right_on='State')
asian = state.merge(asia, left_on='NAME', right_on='State')
american_indian = state.merge(american_india, left_on='NAME', right_on='State')
multiple = state.merge(multipl, left_on='NAME', right_on='State')

# Convert the 'Income' column to int
df = df.astype({"Income": int})
black = black.astype({"Income": int})
hispanic = hispanic.astype({"Income": int})
asian = asian.astype({"Income": int})
american_indian = american_indian.astype({"Income": int})
multiple = multiple.astype({"Income": int})

# Function to build the map
def buildmap(race):
    if race == "none":
        df_projected = df.to_crs(epsg=3857)
        centroid = df_projected.geometry.centroid.to_crs(epsg=4326)
        m = folium.Map(location=[centroid.y.mean(), centroid.x.mean()], zoom_start=5)
        folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
        fg = folium.FeatureGroup(name="Income", show=True)
        folium.GeoJson(df, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple'])
                       ).add_to(fg)
        fg.add_to(m)
        return m

    if race == 'black':
        black_projected = black.to_crs(epsg=3857)
        centroid = black_projected.geometry.centroid.to_crs(epsg=4326)
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
        return m

    if race == 'hispanic':
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
        return m

    if race == 'asian':
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
        return m

    if race == 'american_indian':
        american_indian_projected = american_indian.to_crs(epsg=3857)
        centroid = american_indian_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(american_indian, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
        return m

    if race == 'multiple':
        multiple_projected = multiple.to_crs(epsg=3857)
        centroid = multiple_projected.geometry.centroid.to_crs(epsg=4326)
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
        folium.GeoJson(multiple, style_function=style_function, tooltip=folium.GeoJsonTooltip(fields=['Income', 'State', 'White', 'Black', 'Hispanic', 'Asian', 'American Indian', 'Native Haiwaiian', 'Multiple', 'Minority', 'Location', 'Wealth'])
                       ).add_to(fg)
        fg.add_to(m)
        colormap.caption = "Income"
        colormap.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
        return m

# Get user input for race and build the map
race = input('Enter none, black, hispanic, asian, american_indian, or multiple: ')
buildmap(race)
