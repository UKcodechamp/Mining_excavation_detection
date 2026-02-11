import ee
import os
import csv

from src.gee_init import init_gee
from src.composites import annual_s2_composite
from src.calibration import compute_percentiles, compute_summary_thresholds

from config.settings import *
from config.thresholds import DEFAULT


init_gee(PROJECT_ID)

aoi = ee.FeatureCollection(AOI_asset)


ref_samples = ee.FeatureCollection(ref_samples)

print("Reference samples loaded.")


# Compute yearly percentiles

percentiles_by_year = compute_percentiles(
    years,
    aoi,
    ref_samples,
    annual_s2_composite
)


# Compute average + conservative(min/max)

average_thresholds, conservative_thresholds = compute_summary_thresholds(
    percentiles_by_year,
    years
)


# Prepare output folder

output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)

csv_path = os.path.join(output_folder, "index_threshold_statistics.csv")


# Export CSV

with open(csv_path, mode="w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Type", "Year", "Index", "Pit_90", "NonPit_10"
    ])

    # Yearly values
    for year in years:
        for idx, vals in percentiles_by_year[year].items():
            writer.writerow([
                "Yearly",
                year,
                idx,
                vals["pit_90"],
                vals["nonpit_10"]
            ])

    # Average values
    for idx, vals in average_thresholds.items():
        writer.writerow([
            "Average",
            "All",
            idx,
            vals["pit_90"],
            vals["nonpit_10"]
        ])

    # Conservative values
    for idx, vals in conservative_thresholds.items():
        writer.writerow([
            "Conservative(min/max)",
            "All",
            idx,
            vals["pit_90"],
            vals["nonpit_10"]
        ])

print(f"\nExport completed successfully.")
print(f"Saved to: {csv_path}")
