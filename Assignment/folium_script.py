import pandas as pd
import geopandas as gpd
import folium

lon, lat = -6.4112091, 54.620593

zoom_start = 8

tiles = 'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}.png'
attr =  ('&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
)

folium.Map(location=[lat, lon], tiles=tiles, attr=attr, zoom_start=zoom_start)

lgd = gpd.read_file('data_files/LGD2012.shp')

m = lgd.explore('Population', cmap = 'viridis')

df = pd.read_csv('data_files/emergencydepartments.csv')

eds = gpd.GeoDataFrame(df[['Name','Address']],
                       geometry = gpd.points_from_xy(df['X'],df['Y']),
                       crs='epsg:4326')

eds.explore('Name',
            m=m,
            marker_type='marker',
            popup=True,
            legend=False,
            )

travel = pd.read_csv('data_files/LGD2012.csv')

merged = lgd.merge(travel,left_on = 'LGDCode',right_on = 'LGDCode')

m = merged.explore('RouteLength_km',
                   cmap = 'plasma',
                   legend_kwds = {'caption': 'Distance to nearest Emergency Department (km)'}
                  )

eds_args = {
    'm': m,
    'marker_type': 'marker',
    'popup': True,
    'legend': False,
    'marker_kwds': {'icon': folium.Icon(color='blue',icon='square-h',prefix='fa')}
}

eds.explore('Name',**eds_args)

m

m.save('NI_EmgDept.html')