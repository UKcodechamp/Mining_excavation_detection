def add_indices(img):
    ndvi = img.normalizedDifference(['B8','B4']).rename('NDVI')
    mndwi = img.normalizedDifference(['B3','B11']).rename('MNDWI')

    bsi = img.expression(
        '((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))',
        {
            'B11': img.select('B11'),
            'B4': img.select('B4'),
            'B8': img.select('B8'),
            'B2': img.select('B2')
        }
    ).rename('BSI')

    baei = img.expression(
        '((RED + 0.3) - (NIR + SWIR1)) / ((RED + 0.3) + (NIR + SWIR1))',
        {
            'RED': img.select('B4'),
            'NIR': img.select('B8'),
            'SWIR1': img.select('B11')
        }
    ).rename('BAEI')

    ndbi = img.normalizedDifference(['B11','B8']).rename('NDBI')
    cbi = ndbi.subtract(ndvi).rename('CBI')

    return img.addBands([ndvi, mndwi, bsi, baei, cbi])
