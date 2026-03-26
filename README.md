# 🛰️ Sand & Gravel Pit Detection using Sentinel-2

A rule-based remote sensing workflow to detect **sand and gravel pits (exposed soil / spoil surfaces)** using **Sentinel-2 satellite imagery**, with a focus on reducing false detections from visually similar land cover types.

---

##  Project Overview

Detecting mining excavations from satellite data is challenging because many land surfaces appear similar to exposed soil, including:

* Freshly ploughed agricultural fields
* Construction sites
* Stockpiles
* Bright natural soils
* Shoreline exposures

This project introduces a **multi-year persistence-based approach**, where only areas that consistently behave like pits across multiple years are considered valid detections.

---

##  Objective

The goal is to:

> Identify **persistent exposed soil areas** (potential mining pits) while filtering out **temporary or seasonal changes**.

Instead of full time-series analysis, a simplified **3–4 year comparison** is used to keep the workflow computationally efficient and suitable for academic purposes.

---

##  Study Area (AOI)

* Defined using `AOI.gpkg`
* Recommended size: **~8–10 km × 8–10 km**
* Should include:

  * Water bodies (for testing exclusion)
  * Agricultural land (confusing class)
  * Bright/exposed surfaces (target)

---

##  Data

* **Source:** Sentinel-2 (Google Earth Engine)
* **Temporal Coverage:** Typically 3–4 years (e.g., 2022–2025)
* **Preprocessing:**

  * Cloud & shadow masking
  * Seasonal composite (May–September)
  * Median pixel aggregation

---

##  Spectral Indices Used
<img width="999" height="444" alt="image" src="https://github.com/user-attachments/assets/430a8b80-aac1-413f-9000-4f974eff0d4e" />



##  Methodology

### 1. Annual Feature Extraction

For each selected year:

* Generate Sentinel-2 composite
* Compute NDVI, NDWI/MNDWI, and BSI

---

### 2. Pit Candidate Mask (Per Year)

A pixel is classified as a **pit candidate (1)** if:

* NDVI is **low**
* BSI is **high**
* Pixel is **not water**

Otherwise:

```
mask_y(x) ∈ {0,1}
```

---

### 3. Threshold Calibration

Thresholds are defined using:

* Orthophoto interpretation
* Sample points:

  * Known pits (positive class)
  * Confusing surfaces (negative class)

---

### 4. Multi-Year Persistence Analysis

The key idea:

```
P(x) = Σ mask_y(x)
```

Where:

* `P(x)` = number of years pixel is detected as pit
* `mask_y(x)` = 0 or 1 for each year

---

### 5. Final Detection Rule

* `P(x) = 1` → likely temporary (e.g., ploughing)
* `P(x) ≥ 2` → **persistent → likely pit**

Final output:

```
P(x) ≥ 2
```

---

### 6. Vectorization & Filtering

* Convert raster mask to polygons
* Apply minimum area filter:

> Recommended threshold: **0.1 ha**

* Optional:

  * Remove built-up areas
  * Exclude known industrial zones


---

## Validation

Validation is performed using **orthophotos**:

### Classes:

* **1 → Pits**
* **0 → Confusing objects**

  * Ploughing
  * Construction
  * Bright soils
  * Shorelines

---

###  Metrics:

* Overall Accuracy (OA)
* Producer Accuracy (PA)
* User Accuracy (UA)
* Confusion Matrix

---

###  Error Analysis

Typical errors include:

* **False Positives**

  * Ploughed fields
  * Construction areas

* **Possible Improvements**

  * Stricter thresholds
  * Higher persistence (P ≥ 3)
  * Larger minimum area filter
  * Built-up masking

---
##  Code Inputs/Outputs

### Inputs
* PROJECT_ID = 'transitional-proj'
* AOI_asset = 'projects/transitional-proj/assets/proj_aoi'
* ref_samples = 'projects/transitional-proj/assets/valid_samp'
* years = [2022, 2023, 2024, 2025]
* persistence = 2
* min_area_ha = 0.3
### Outputs
* Accuracy_table.csv
* Index_threshold_statistics.csv
* Detected_pits_polygon_layer.geojson


##  How to Run

###  1. Check Python Version

```bash
py -3.11 --version
```

---

###  2. Create Virtual Environment

```bash
python -m venv minenv
```

---

###  3. Activate Environment (PowerShell)

```powershell
.\minenv\Scripts\Activate.ps1
```

---

###   4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

###   5. Authenticate Google Earth Engine

```bash
earthengine authenticate
```

---

###   6. Run the Scripts

```bash
python -m scripts.exe_detection
```

---

## 📂 Project Structure

```
├── config/                 # Configuration files (AOI, parameters)
├── scripts/                # Processing scripts
├── src/                    # Functions (Modular approach)
├── requirements.txt        # Dependencies
├── AOI.gpkg                # Area of Interest
└── README.md
```


---

## 📜 License

This project is for academic and research purposes.

---

##  Author

**Umara Kazmi**
MSc Remote Sensing / Geospatial Analysis

---
