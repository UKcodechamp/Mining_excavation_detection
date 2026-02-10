import ee
from src.composites import annual_s2_composite

def pit_mask(img, t):
    return (
        img.select('NDVI').lt(t['NDVI_MAX'])
        .And(img.select('BSI').gt(t['BSI_MIN']))
        .And(img.select('MNDWI').lt(t['MNDWI_MAX']))
        .And(img.select('CBI').lt(t['CBI_MAX']))
        .And(img.select('BAEI').lt(t['BAEI_MAX']))
    ).rename('pit')


def compute_final_mask(years, aoi, thresholds, persistence):
    masks = []

    for y in years:
        img = annual_s2_composite(y, aoi)
        masks.append(pit_mask(img, thresholds))

    P = ee.ImageCollection(masks).sum()
    return P.gte(persistence).selfMask()
