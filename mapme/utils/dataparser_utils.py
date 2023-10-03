import pandas
import json
import pdb
from branca.colormap import linear
from .class_objects import *
import branca.colormap as cm
import matplotlib.cm as mpl_cm
import math
import logging
import pandas
from .datastructures import HexTree

"""
The DataFormatter class role is to take Data in whatever format x and reformat it to fit a GeoJson object. There are a few criteria, before this can be fulfilled.
A GeoJson object, as the name implies, specifies a geological location of an object. There are different kinds of GeoJson Objects. Polygons,Multipolygons, Linesting, Points and Multipoints
FeatureCollections etc.
"""

class DataFormatter:
    logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    LAT_ALIAS = ('Latitude', 'latitude', 'Lat', 'lat', 'Loclatitude','locLatitude')
    LON_ALIAS = ('Longitude', 'longitude', 'Lon', 'lon', 'Loclongitude','locLongitude')
    RSRP_FEATURES_NAMES = ('cellinfo_0_rsrp','lte_0_rsrp','density') # This can later be removed or changes based on user Request, but for testing this is currently required
    CELL_FEATURE_NAMES = ('distance','az')
    @staticmethod
    def jsonToGeoObject(data, source='linktaster'):
        jsonData = json.dumps(data)
        jsonData = json.loads(jsonData)
        geojson = {
            'type': 'FeatureCollection',
            'features': []
        }
        """
        A LOGIC STILL NEEDS TO BE IMPLEMENTED TO CHECK THE SOURCE OF THE DATA
        """

        if source == 'linktaster':
            if 'Entries' in jsonData: # Case1: Objects are stored as nested entries within a key
                objectData = jsonData['Entries']
                return DataFormatter.formatGeoJSONLinktaster(objectData,nested=True)
            else: # Case2: Objects are stored as documents
                objectData = jsonData
                return DataFormatter.formatGeoJSONLinktaster(objectData,nested=False) # might have to rename this function later on


        elif source == 'qualipoc':
            objectData = jsonData['']
            for key, value in objectData:
                DataFormatter.formatGeoJSONQualipoc(jsonData)

        elif source == 'generic':
            objectData = jsonData['']  # To be done
            for key, value in objectData:
                DataFormatter.formatGeoJSONGeneric(jsonData)

        return geojson

    @staticmethod
    def formatGeoJSONGeneric(data):
        print()

    #Might have to rename this function later on
    @staticmethod
    def formatGeoJSONLinktaster(data,nested):

        circle_markers = []
        hexagon_markers = HexTree() # Hexagon Markers will be stored in binary trees, to quickly update the variables.

        #Create a colormap <-- This should  be changed later based on user input
        colormap = cm.LinearColormap(
        colors=mpl_cm.viridis.colors,
        vmin=-120,
        vmax=-75
        )
        if nested:
            for entry in data:
                try:
                    # Extract location data using LAT_ALIAS and LON_ALIAS
                    location = DataFormatter.extractLocation(entry)
                    # Create properties dictionary with all other keys
                    properties = DataFormatter.extractProperties(entry)
                    lat, lon = location

                    feature = None
                    feature_tag = None
                    for feature_name in DataFormatter.RSRP_FEATURES_NAMES:
                        if feature_name in properties:
                            feature = properties[feature_name]
                            feature_tag = feature_name
                            break
                    if feature is not None and location[0] is not None:
                        radius = 15  # Adjust the radius as needed
                        # Create a dictionary representing the circle marker information
                        color = colormap(feature)

                        circle_marker = CircleMarker(lat,lon,radius,feature_tag,feature,color)
                        circle_markers.append(circle_marker.circle_marker_info)
                        #Hexagons are some aggregation of circleMarkers (we bin data)
                        hexagon_marker = HexagonMarker(lon,lat,properties,color,feature = feature_tag)
                        curr_hex = hexagon_markers.get(hexagon_marker.hex_info['hex_id']) # Search the Binary tree for an already Existing Hex Element with the given ID

                        if curr_hex is not None:
                            hexagon_marker.update(curr_hex.hex_info['feature_sum'])
                            logging.info(f'Updated HexagonMarker with hex_id: {hexagon_marker.hex_info["hex_id"]}')
                        else:
                            hexagon_markers.insert(hexagon_marker)
                            logging.info(f'Added HexagonMarker with hex_id: {hexagon_marker.hex_info["hex_id"]}')

                    else:
                        # Log that first_rsrp_value is invalid
                        logging.error(f'Invalid first_rsrp_value: {feature}')
                except Exception as e:
                    # Log any other exceptions that may occur
                    logging.error(f'Error processing entry: {e}')

            geoObjects = {}
            geoObjects['CircleMarkers'] = circle_markers
            geoObjects['HexagonMarkers'] = hexagon_markers.inorder_traversal()#Inorder Traversal,because hexagon_markers is a tree
        else:
            try:
                # Extract location data using LAT_ALIAS and LON_ALIAS
                location = DataFormatter.extractLocation(data)
                # Create properties dictionary with all other keys
                properties = DataFormatter.extractProperties(data)
                lat, lon = location

                feature = None
                feature_tag = None
                for feature_name in DataFormatter.CELL_FEATURE_NAMES: # This part of the code is just for testing and needs to be changed dynamicaly at some point
                    if feature_name in properties:
                        feature = properties[feature_name]
                        feature_tag = feature_name
                        break

                for feature_name in DataFormatter.RSRP_FEATURES_NAMES: # This part of the code is just for testing and needs to be changed dynamicaly at some point
                    if feature_name in properties:
                        feature = properties[feature_name]
                        feature_tag = feature_name
                        break

                if feature is not None and location[0] is not None:
                    radius = 15  # Adjust the radius as needed
                    # Create a dictionary representing the circle marker information
                    color = colormap(feature)

                    circle_marker = CircleMarker(lat,lon,radius,feature_tag,feature,color)
                    circle_markers.append(circle_marker.circle_marker_info)
                    #Hexagons are some aggregation of circleMarkers (we bin data)
                    hexagon_marker = HexagonMarker(lon,lat,properties,color,feature = feature_tag)
                    curr_hex = hexagon_markers.get(hexagon_marker.hex_info['hex_id']) # Search the Binary tree for an already Existing Hex Element with the given ID

                    if curr_hex is not None:
                        hexagon_marker.update(curr_hex.hex_info['feature_sum'])
                        logging.info(f'Updated HexagonMarker with hex_id: {hexagon_marker.hex_info["hex_id"]}')
                    else:
                        hexagon_markers.insert(hexagon_marker)
                        logging.info(f'Added HexagonMarker with hex_id: {hexagon_marker.hex_info["hex_id"]}')

                else:
                    # Log that first_rsrp_value is invalid
                    logging.error(f'Invalid first_rsrp_value: {feature}')
            except Exception as e:
                # Log any other exceptions that may occur
                logging.error(f'Error processing entry: {e}')

            geoObjects = {}
            geoObjects['CircleMarkers'] = circle_markers
            geoObjects['HexagonMarkers'] = hexagon_markers.inorder_traversal()#Inorder Traversal,because hexagon_markers is a tree
        return geoObjects
    

    @staticmethod
    def formatGeoJSONQualipoc(data):
        print()

    @staticmethod
    def extractLocation(object):
        return DataFormatter.findCoordinates(object)

    @staticmethod
    def findCoordinates(object):
        latitude,longitude = None,None
        if isinstance(object, dict):
            latitude, longitude = DataFormatter.traverseNestedDict(object, latitude, longitude)
        elif isinstance(object, list):
            latitude, longitude = DataFormatter.traverseNestedList(object, latitude, longitude)
        return latitude, longitude
        
    
    @staticmethod
    def traverseNestedDict(object, latitude, longitude):
        for key, value in object.items():
            if key in DataFormatter.LAT_ALIAS:
                latitude = value
            if key in DataFormatter.LON_ALIAS:
                longitude = value

            if latitude is not None and longitude is not None:
                return latitude, longitude

            if isinstance(value, dict):
                latitude, longitude = DataFormatter.traverseNestedDict(value, latitude, longitude)
            elif isinstance(value, list):
                latitude, longitude = DataFormatter.traverseNestedList(value, latitude, longitude)
        return latitude, longitude

    @staticmethod
    def traverseNestedList(object, latitude, longitude):
        for item in object:
            if isinstance(item, dict):
                latitude, longitude = DataFormatter.traverseNestedDict(item, latitude, longitude)
        return latitude, longitude


    def extractNestedProperties(data):
        properties = {}
        for key, value in data.items():
            if isinstance(value, dict):
                # If the value is a dictionary, recursively extract its properties
                nested_properties = DataFormatter.extractNestedProperties(value)
                properties.update(nested_properties)
            elif isinstance(value, list):
                # If the value is a list, iterate through its elements and add them individually
                for i, item in enumerate(value):
                    item_properties = DataFormatter.extractProperties(item)
                    for item_key, item_value in item_properties.items():
                        properties[f"{key}_{i}_{item_key}"] = item_value
            else:
                properties[key] = value
        return properties
    
    @staticmethod
    def extractProperties(data):
        properties = {}
        for key, value in data.items():
            if key not in DataFormatter.LAT_ALIAS + DataFormatter.LON_ALIAS:
                if isinstance(value, dict):
                    # If the value is a dictionary, recursively extract its properties
                    nested_properties = DataFormatter.extractNestedProperties(value)
                    properties.update(nested_properties)
                elif isinstance(value, list):
                    # If the value is a list, iterate through its elements and add them individually
                    for i, item in enumerate(value):
                        item_properties = DataFormatter.extractProperties(item)
                        for item_key, item_value in item_properties.items():
                            properties[f"{key}_{i}_{item_key}"] = item_value
                else:
                    properties[key] = value
        return properties

class DataTraverser():
    def function():
        print()



    



            














            





















