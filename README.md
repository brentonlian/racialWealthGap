# Demographic Map Builder
# An example picture is included in examplepic.png

## Introduction
This Python based Demographic Map Builder allows users to view income disparities by state and demographic in the United States.

## Features
-Interactive map generation with Folium and GeoPandas.\
-Tooltips on hover for each state.\
-Multiple demographic categories.\
-User friendly Tkinter GUI and HTML map.\
-Color coded map.\
-Statistics for highest and lowest income and the corresponding state.

## Requirements
-Python 3\
-pandas\
-geopandas\
-folium\
-branca\
-tkinter

## Installation
1. Clone the repository from https://github.com/brentonlian/racialWealthGap
2. Navigate to the project directory with cd racialWealthGap
3. Install required packages with pip install -r requirements.txt

## Usage
1. Run main.py. A tkinter pop up should appear in around 3-5 seconds. 
2. Open the tkinter pop up and select a general category (race, gender, or age), then a specific category
3. A map will automatically be opened. If not, manually run map.html.
4. Choose the general category: Age, Race, or Gender
5. Then choose the corresponding subcategory.

## Sources
## allStats.csv
https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D
https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html
http://www.plantsgalore.com/plants/types/maps/00M-Map-US-Regions.htm

## State geometry
https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_500k.json

## Race 
https://www.dol.gov/agencies/ofccp/about/data/earnings/race-and-ethnicity

## Age
https://scholaroo.com/report/median-income-by-generation/


## Gender
https://www.dol.gov/agencies/ofccp/about/data/earnings/gender#NorthCarolina




