import pandas as pd
import geopandas as gpd
import folium

LGD2012 = gpd.read_file('data_files/LGD2012.shp')

df = pd.read_csv('data_files/emergencydepartments.csv')

eds = gpd.GeoDataFrame(df[['Name','Address','Town', 'Postcode','Phone', 'Trust', 'Website']],
                       geometry=gpd.points_from_xy(df['X'],df['Y']),
                       crs='epsg:29903')

eds.explore('Name',
            m=m,
            marker_type='marker',
            popup=True,
            legend=False,
            )

lgd_travel = pd.read_csv('data_files/LGD2012.csv')

lgd_merged = LGD2012.merge(lgd_travel, left_on='LGDCode', right_on='LGDCode')

m = lgd_merged.explore('RouteLength_km',
                   cmap='plasma',
                   legend_kwds={'caption': 'Distance to nearest Emergency Department (km)'}
                  )

eds_args = {
    'm': m,
    'marker_type': 'marker',
    'popup': True,
    'legend': False,
    'marker_kwds': {'icon': folium.Icon(color='blue', icon='square-h', prefix='fa')}
}

eds.explore('Name', **eds_args)

m

m.save('NI_EmgDept_test.html')