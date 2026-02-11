import ee
from src.gee_init import init_gee
from src.detection import compute_final_mask
from src.vectorization import export_polygons
from config.settings import *
from config.thresholds import DEFAULT

init_gee(PROJECT_ID)

aoi = ee.FeatureCollection(AOI_asset)

mask = compute_final_mask(
    years, aoi, DEFAULT, persistence
)

export_polygons(
    mask,
    aoi,
    min_area_ha,
    'S2_Pits_AOI1_03',
    'outputs'
)
