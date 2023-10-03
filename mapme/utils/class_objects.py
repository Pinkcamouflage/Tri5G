"""
The following file, will depict the Objects that folium has to render based on some given information
"""
from typing import Dict
import pdb
import  h3
import pdb

class GeoObject:
    def __init__(self,properties:Dict):
        self.properties = properties
        

class CircleMarker(GeoObject):

    def __init__(self,lon,lat,radius,feature,feature_val,color,fill = True,fill_opacity = 0.7):
        self.circle_marker_info = \
        {
        'location': [lon,lat],
        'radius': radius,
        'color': color,
        'fill': fill,
        'fill_color': color,
        'fill_opacity': fill_opacity,
        'popup': f'{feature}: {feature_val}'
        }

"""
The following class, works with the h3 module  I would advise anyone, to read the h3 documentation first to understand how the class works
A simple Overview:
*Create a h3 Hexagon grid with the  latitude and longitude and resolution
*The h3 object is saved as a hexID
*We can use this hexID to calculate binned datapoints etc, IE points within a hex share the same hexID on a given resolution
"""
class HexagonMarker(GeoObject):

    def __init__(self,lon,lat,properties,color,feature = 'lte_0_rsrp',fill_opacity = 0.4,resolution = 8):

        hexagon = h3.geo_to_h3(lat,lon,resolution)
        center_lat, center_lon = h3.h3_to_geo(hexagon)
        vertices = h3.h3_to_geo_boundary(hexagon)
        self.hex_info = {
            'hex_id': hexagon,
            'center': (center_lat, center_lon),
            'hexagon_vertices': vertices,
            'color': 'black',
            'fill_color': color,
            'fill_opacity':fill_opacity,
            'population':1,
            'feature_sum':properties[feature],
        }
        self.hex_info['feature_avg'] = float(self.hex_info['feature_sum'])/float(self.hex_info['population'])

        for key in properties:
            self.hex_info[key] = properties[key]

    def update(self,value):
        self.hex_info['population'] = float(self.hex_info['population'])+1 # Everytime we update te element, we increase the point density or population of the hexbin
        self.hex_info['feature_sum'] = float(self.hex_info['feature_sum']) + float(value)
        self.hex_info['feature_avg'] = float(self.hex_info['feature_sum'])/float(self.hex_info['population'])
        if self.hex_info['hex_id'] == '89639224413ffff':
            print(self.hex_info['population'])
            print(self.hex_info['feature_sum'])
            print(self.hex_info['feature_avg'])





















