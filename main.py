import pandas as pd
import geopandas as gpd
import folium
import branca.colormap as cm
import webbrowser
import tkinter as tk
from tkinter import ttk

# Load data
d = pd.read_csv('allStats.csv', on_bad_lines='skip')
d = d.replace("%", "", regex=True).replace(",", "", regex=True).fillna("0")

# Load demographic data
blac = pd.read_csv('black.csv')
hispani = pd.read_csv('hispanic.csv')
asia = pd.read_csv('asian.csv')
american_india = pd.read_csv('american_indian.csv')
multipl = pd.read_csv('multi.csv')
whit = pd.read_csv('white.csv')
age_15_24 = pd.read_csv('15-24.csv')
age_25_44 = pd.read_csv('25-44.csv')
age_45_64 = pd.read_csv('45-64.csv')
age_65 = pd.read_csv('65+.csv')
female = pd.read_csv('female.csv')
male = pd.read_csv('male.csv')

# Load state data
state = gpd.read_file("https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json")

# Merge dataframes
df = state.merge(d, left_on='NAME', right_on='State')
black = state.merge(blac, left_on='NAME', right_on='State')
hispanic = state.merge(hispani, left_on='NAME', right_on='State')
asian = state.merge(asia, left_on='NAME', right_on='State')
american_indian = state.merge(american_india, left_on='NAME', right_on='State')
multiple = state.merge(multipl, left_on='NAME', right_on='State')
age_15_24 = state.merge(age_15_24, left_on='NAME', right_on='State')
age_25_44 = state.merge(age_25_44, left_on='NAME', right_on='State')
age_45_64 = state.merge(age_45_64, left_on='NAME', right_on='State')
age_65 = state.merge(age_65, left_on='NAME', right_on='State')
female = state.merge(female, left_on='NAME', right_on='State')
male = state.merge(male, left_on='NAME', right_on='State')
white = state.merge(whit, left_on='NAME', right_on='State')

# Set types to integer
df = df.astype({"Income": int})
Black = black.astype({"Income": int})
Hispanic = hispanic.astype({"Income": int})
Asian = asian.astype({"Income": int})
American_Indian = american_indian.astype({"Income": int})
Multiple = multiple.astype({"Income": int})
Age_15_24 = age_15_24.astype({"Income": int})
Age_25_44 = age_25_44.astype({"Income": int})
Age_45_64 = age_45_64.astype({"Income": int})
Age_65 = age_65.astype({"Income": int})
Female = female.astype({"Income": int})
Male = male.astype({"Income": int})
White = white.astype({"Income": int})

# Dictionary mapping user input to dataframes
demographics = {
    "15-24": Age_15_24,
    "25-44": Age_25_44,
    "45-64": Age_45_64,
    "65+": Age_65,
    "Female": Female,
    "Male": Male,
    "Black": Black,
    "Hispanic": Hispanic,
    "Asian": Asian,
    "American_Indian": American_Indian,
    "Multiple": Multiple,
    "White": White,
}

# Define a function to build the map
def buildmap(demography):
    # Determine the appropriate dataframe
    if demography == "none":
        selected_df = df
    elif demography in demographics:
        selected_df = demographics[demography]
    else:
        print(f"Invalid category: {demography}")
        return

    # Find the states with the highest and lowest income
    highest_income_state = selected_df.loc[selected_df['Income'].idxmax()]['NAME']
    highest_income_value = selected_df['Income'].max()
    lowest_income_state = selected_df.loc[selected_df['Income'].idxmin()]['NAME']
    lowest_income_value = selected_df['Income'].min()

    # Create the map
    m = folium.Map(location=[selected_df.geometry.centroid.y.mean(), selected_df.geometry.centroid.x.mean()], zoom_start=5)
    folium.TileLayer(tiles='openstreetmap', show=True, control=False, min_zoom=5).add_to(m)
    fg = folium.FeatureGroup(name="Income", show=True)
    
    # Determine color scale
    high = highest_income_value
    low = lowest_income_value
    colormap = cm.LinearColormap(colors=['white', 'red'], index=[low, high], vmin=low, vmax=high)
    
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

    # Add colormap with additional information
    colormap.caption = f"Lowest: {lowest_income_state} (${lowest_income_value})\nHighest: {highest_income_state} (${highest_income_value})"
    colormap.add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)

    # Save and open map
    m.save('map.html')
    webbrowser.open('map.html')

# Define the GUI
def on_main_category_change(event):
    main_category = combo_main_category.get()
    if main_category == "Age":
        subcategory_options = ["15-24", "25-44", "45-64", "65+"]
    elif main_category == "Gender":
        subcategory_options = ["Female", "Male"]
    elif main_category == "Race":
        subcategory_options = ["Black", "Hispanic", "Asian", "American_Indian", "Multiple", "White"]
    else:
        subcategory_options = []

    combo_subcategory['values'] = subcategory_options
    combo_subcategory.current(0)

def on_submit():
    selected_demography = combo_subcategory.get()
    buildmap(selected_demography)

root = tk.Tk()
root.title("Demographic Map Builder")

# Main category dropdown
label_main = ttk.Label(root, text="Select Main Category:")
label_main.grid(column=0, row=0, padx=10, pady=10)
combo_main_category = ttk.Combobox(root, values=["Age", "Gender", "Race"])
combo_main_category.grid(column=1, row=0, padx=10, pady=10)
combo_main_category.bind("<<ComboboxSelected>>", on_main_category_change)

# Subcategory dropdown
label_sub = ttk.Label(root, text="Select Subcategory:")
label_sub.grid(column=0, row=1, padx=10, pady=10)
combo_subcategory = ttk.Combobox(root)
combo_subcategory.grid(column=1, row=1, padx=10, pady=10)

# Submit button
submit_button = ttk.Button(root, text="Generate Map", command=on_submit)
submit_button.grid(column=0, row=2, columnspan=2, pady=10)

# Run the GUI loop
root.mainloop()
