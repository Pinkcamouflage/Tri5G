"""
A Factory produces items, For instance GeoObjects.
"""
from .dataparser_utils import DataFormatter
import multiprocessing
import pdb

class Factory():

    def __init__(self,assembly_line_amount = 1):
        self.assembly_line_amount = assembly_line_amount

    """
        We then have the following Data
    """
    def produceGeoObjects(self,data_list):

        assembly_lines = multiprocessing.Pool(processes = self.assembly_line_amount)
        if len(data_list)>1: # case for multiple documents within a collection
            geo_structures = DataFormatter.jsonToGeoObject(data_list[0])

            for data in data_list[1:]:
                temp_geo_structure = DataFormatter.jsonToGeoObject(data) # Currently returns a dict Object, with lists of HexagonMarkers and CircleMarkers
                geo_structures = Factory.combineGeoStructures(geo_structures,temp_geo_structure)
        else: # Case for only one document within a collection
            geo_structures = DataFormatter.jsonToGeoObject(data_list[0]) 
        return geo_structures
    

    """
        combineGeoStructures, is reponsible for updating the list of geostructures after each documents data is converted
        within a collection.
    """
    @staticmethod
    def combineGeoStructures(structure1,structure2):
        new_structure = {}
        for key,value in structure1.items():
            if key in structure2:
                new_geo_object = structure1[key] + structure2[key]
                new_structure[key] = new_geo_object
        return new_structure







    