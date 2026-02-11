import ee
import os
import json

def export_polygons(mask, aoi, min_area_ha, name, folder="outputs"):
    polys = mask.reduceToVectors(
        geometry=aoi.geometry(),
        scale=20,
        geometryType='polygon',
        eightConnected=True,
        maxPixels=1e13,
        tileScale=4
    )

    def add_area(f):
        return f.set(
            'area_ha',
            f.geometry().area(ee.ErrorMargin(1)).divide(10000)
        )

    polys = polys.map(add_area)
    polys = polys.filter(ee.Filter.gte('area_ha', min_area_ha))

    #task = ee.batch.Export.table.toDrive(
     #   collection=polys,
      #  description=name,
      #  folder=folder,
       # fileNamePrefix=name,
       # fileFormat='GeoJSON'
    #)
    #task.start()

    # -----------------------------------
    # Create local output folder
    # -----------------------------------
    os.makedirs(folder, exist_ok=True)

    output_path = os.path.join(folder, f"{name}.geojson")

    # -----------------------------------
    # Download to local machine
    # -----------------------------------
    geojson = polys.getInfo()

    with open(output_path, "w") as f:
        json.dump(geojson, f)

    print(f"Polygons saved to: {output_path}")
    return polys
