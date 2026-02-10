import ee
from src.preprocessing import mask_s2_clouds
from src.indices import add_indices

def annual_s2_composite(year, aoi):
    start = ee.Date.fromYMD(year, 5, 1)
    end   = ee.Date.fromYMD(year, 9, 30)

    return (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .filterBounds(aoi)
        .filterDate(start, end)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
        .map(mask_s2_clouds)
        .map(add_indices)
        .median()
        .clip(aoi)
    )
