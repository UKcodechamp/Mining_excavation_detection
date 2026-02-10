import os
import ee
import pandas as pd
from src.gee_init import init_gee
from src.composites import annual_s2_composite
from src.calibration import compute_index_stats_by_class
from config.settings import *

init_gee(PROJECT_ID)

aoi = ee.FeatureCollection(AOI_asset).geometry()
ref = ee.FeatureCollection(ref_samples)

rows_class0 = []
rows_class1 = []

for year in years:
    img = annual_s2_composite(year, ee.FeatureCollection(AOI_asset).geometry())
    
    # Compute stats with 10m buffer
    stats = compute_index_stats_by_class(img, ref, buffer_m=10)

    for cls, indices in stats.items():
        target_list = rows_class0 if cls == 0 else rows_class1
        for idx, vals in indices.items():
            target_list.append({
                "Year": year,
                "Class": cls,
                "Index": idx,
                "Mean": vals["mean"],
                "StdDev": vals["stdDev"],
                "Min": vals["min"],
                "Max": vals["max"],
                "Median": vals["median"]
            })

# Convert to DataFrames
df0 = pd.DataFrame(rows_class0)
df1 = pd.DataFrame(rows_class1)

# Make output folder
os.makedirs("outputs", exist_ok=True)

# Save separate CSVs for each class
df0.to_csv("outputs/index_statistics_class0.csv", index=False)
df1.to_csv("outputs/index_statistics_class1.csv", index=False)

print("Class 0 stats → outputs/index_statistics_class0.csv")
print("Class 1 stats → outputs/index_statistics_class1.csv")
