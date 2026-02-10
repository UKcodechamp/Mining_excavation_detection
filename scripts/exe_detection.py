import ee
from src.gee_init import init_gee
from src.detection import compute_final_mask
from config.settings import *
from config.thresholds import DEFAULT

init_gee(PROJECT_ID)

aoi = ee.FeatureCollection(AOI_asset)

mask = compute_final_mask(
    years, aoi, DEFAULT, persistence
)

print('Mask ready')
