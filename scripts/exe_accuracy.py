import os 
import ee
import pandas as pd
from src.gee_init import init_gee
from src.detection import compute_final_mask
from src.accuracy import compute_accuracy
from config.settings import *
from config.thresholds import DEFAULT

init_gee(PROJECT_ID)

aoi = ee.FeatureCollection(AOI_asset)
ref = ee.FeatureCollection(ref_samples)

# ---- Compute detection mask ----
mask = compute_final_mask(
    years, aoi, DEFAULT, persistence
)

# ---- Accuracy metrics ----
metrics = compute_accuracy(mask, ref)

# ---- Build tabular row ----
row = {
    "AOI": "AOI1",
    "Case": "DEFAULT",
    "OA": metrics["OA"],
    "PA_nonpit": metrics["PA_nonpit"],
    "PA_pit": metrics["PA_pit"],
    "UA_nonpit": metrics["UA_nonpit"],
    "UA_pit": metrics["UA_pit"],
    "F1_nonpit": metrics["F1_nonpit"],
    "F1_pit": metrics["F1_pit"]
}

df = pd.DataFrame([row])

# ---- Export CSV ----
os.makedirs("outputs", exist_ok=True)
out_path = "outputs/accuracy_table_aoi1.csv"
df.to_csv(out_path, index=False)

print(f"Accuracy table exported → {out_path}")


