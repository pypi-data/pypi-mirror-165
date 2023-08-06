import importlib.resources
import geopandas as gpd


def get_countries():
    with importlib.resources.open_text("get_coordinates.boundaries", "world_countries.geojson") as countries:
        gdf = gpd.read_file(countries)
    return gdf
