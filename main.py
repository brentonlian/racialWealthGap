import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
#https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D
#https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html
#https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.plantsgalore.com%2Fplants%2Ftypes%2Fmaps%2F00M-Map-US-Regions.htm&psig=AOvVaw28UZpZCYvUMKWnudXlS4i2&ust=1619404911103000&source=images&cd=vfe&ved=0CAkQjhxqFwoTCJiWncWvmPACFQAAAAAdAAAAABAf
#Above are the sources for demographics, income, and us regions


d=pd.read_csv('allStats.csv',on_bad_lines = 'skip')
d = d.replace("%","", regex=True).replace(",","", regex=True).fillna("0")
#d.head()
blac=pd.read_csv('black.csv')
hispani=pd.read_csv('hispanic.csv')
asia=pd.read_csv('asian.csv')
american_india=pd.read_csv('native.csv')
multipl=pd.read_csv('multi.csv')

state = gpd.read_file("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json")
#Above is the source for state geometries
state.head()
df=state.merge(d,left_on='NAME',right_on='State')
black=state.merge(blac,left_on='NAME',right_on='State')
hispanic=state.merge(hispani,left_on='NAME',right_on='State')
asian=state.merge(asia,left_on='NAME',right_on='State')
american_indian=state.merge(american_india,left_on='NAME',right_on='State')
multiple=state.merge(multipl,left_on='NAME',right_on='State')
#state.dropna()
#df.dropna()
#state.head()
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_colwidth', 199)
df.head()
df.dtypes
df = df.astype({"Income": int})
black = black.astype({"Income": int})
hispanic = hispanic.astype({"Income": int})
asian = asian.astype({"Income": int})
american_indian = american_indian.astype({"Income": int})
multiple= multiple.astype({"Income": int})
df.head()
#DRAFT
#
#
#
#
def buildmap(race):
  if race=="none":
    m = folium.Map(location=[df.geometry.centroid.y.mean(), df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    folium.GeoJson(df,tooltip=folium.GeoJsonTooltip(fields=['Income','State','White','Black','Hispanic','Asian','American Indian','Native Haiwaiian','Multiple'])
    ).add_to(fg)
    fg.add_to(m)
    m
  if race=='black':
    m = folium.Map(location=[black.geometry.centroid.y.mean(), black.geometry.centroid.x.mean()], zoom_start=5)
    #changed tiles none
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    high=int(df['Income'].max())
    low=int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white','red'],index=[low,high],vmin=low,vmax=high)
    colormap
    #skipped totals
    style_function=lambda x: {
      'fillColor': colormap(x['properties']["Income"]),
      'color': 'black',
      'weight': 1,
      'fillOpacity': 0.45,
      'weight': 1,
      'opacity':0.4,
      'nan_fill_color': 'purple'
      }
    folium.GeoJson(black,style_function=style_function,tooltip=folium.GeoJsonTooltip(fields=['Income','State','White','Black','Hispanic','Asian','American Indian','Native Haiwaiian','Multiple','Minority','Location','Wealth'])
    ).add_to(fg)
    fg.add_to(m)
    colormap.caption = "Income"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return(m)
  if race=='hispanic':
    m = folium.Map(location=[hispanic.geometry.centroid.y.mean(), hispanic.geometry.centroid.x.mean()], zoom_start=5)
    #changed tiles none
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    high=int(df['Income'].max())
    low=int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white','red'],index=[low,high],vmin=low,vmax=high)
    colormap
    #skipped totals
    style_function=lambda x: {
      'fillColor': colormap(x['properties']["Income"]),
      'color': 'black',
      'weight': 1,
      'fillOpacity': 0.45,
      'weight': 1,
      'opacity':0.4,
      'nan_fill_color': 'purple'
      }
    folium.GeoJson(hispanic,style_function=style_function,tooltip=folium.GeoJsonTooltip(fields=['Income','State','White','Black','Hispanic','Asian','American Indian','Native Haiwaiian','Multiple','Minority','Location','Wealth'])
    ).add_to(fg)
    fg.add_to(m)
    colormap.caption = "Income"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return(m)

  if race=='asian':
    m = folium.Map(location=[asian.geometry.centroid.y.mean(), asian.geometry.centroid.x.mean()], zoom_start=5)
    #changed tiles none
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    high=int(df['Income'].max())
    low=int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white','red'],index=[low,high],vmin=low,vmax=high)
    colormap
    #skipped totals
    style_function=lambda x: {
      'fillColor': colormap(x['properties']["Income"]),
      'color': 'black',
      'weight': 1,
      'fillOpacity': 0.45,
      'weight': 1,
      'opacity':0.4,
      'nan_fill_color': 'purple'
      }
    folium.GeoJson(asian,style_function=style_function,tooltip=folium.GeoJsonTooltip(fields=['Income','State','White','Black','Hispanic','Asian','American Indian','Native Haiwaiian','Multiple','Minority','Location','Wealth'])
    ).add_to(fg)
    fg.add_to(m)
    colormap.caption = "Income"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return(m)

  if race=='american_indian':
    m = folium.Map(location=[american_indian.geometry.centroid.y.mean(), american_indian.geometry.centroid.x.mean()], zoom_start=5)
    #changed tiles none
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    high=int(df['Income'].max())
    low=int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white','red'],index=[low,high],vmin=low,vmax=high)
    colormap
    #skipped totals
    style_function=lambda x: {
      'fillColor': colormap(x['properties']["Income"]),
      'color': 'black',
      'weight': 1,
      'fillOpacity': 0.45,
      'weight': 1,
      'opacity':0.4,
      'nan_fill_color': 'purple'
      }
    folium.GeoJson(american_indian,style_function=style_function,tooltip=folium.GeoJsonTooltip(fields=['Income','State','White','Black','Hispanic','Asian','American Indian','Native Haiwaiian','Multiple','Minority','Location','Wealth'])
    ).add_to(fg)
    fg.add_to(m)
    colormap.caption = "Income"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return(m)

  if race=='multiple':
    m = folium.Map(location=[multiple.geometry.centroid.y.mean(), multiple.geometry.centroid.x.mean()], zoom_start=5)
    #changed tiles none
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    high=int(df['Income'].max())
    low=int(df['Income'].min())
    colormap = cm.LinearColormap(colors=['white','red'],index=[low,high],vmin=low,vmax=high)
    colormap
    #skipped totals
    style_function=lambda x: {
      'fillColor': colormap(x['properties']["Income"]),
      'color': 'black',
      'weight': 1,
      'fillOpacity': 0.45,
      'weight': 1,
      'opacity':0.4,
      'nan_fill_color': 'purple'
      }
    folium.GeoJson(multiple,style_function=style_function,tooltip=folium.GeoJsonTooltip(fields=['Income','State','White','Black','Hispanic','Asian','American Indian','Native Haiwaiian','Multiple','Minority','Location','Wealth'])
    ).add_to(fg)
    fg.add_to(m)
    colormap.caption = "Income"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    return(m)

race=input('Enter none, black, hispanic, asian, american_indian, or multiple')
buildmap(race)
