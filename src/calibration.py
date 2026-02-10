import ee

def compute_index_stats_by_class(image, ref_samples, index_bands=None, buffer_m=10):
    #"""
    #Compute mean, std, min, max, median of indices at reference points for each class (0, 1)
    #Args:
       # image: ee.Image with spectral indices
       # ref_samples: ee.FeatureCollection with 'class' property
       # index_bands: list of bands to compute stats
       # buffer_m: buffer around points in meters to include multiple pixels
   # Returns:
      #  stats_dict: {class: {band: {mean, stdDev, min, max, median}}}
   # """#
    if index_bands is None:
        index_bands = ["NDVI", "MNDWI", "BSI", "CBI", "BAEI"]

    image = image.select(index_bands)
    stats_dict = {}
    classes = [0, 1]

    for cls in classes:
        # Select points of this class
        cls_points = ref_samples.filter(ee.Filter.eq("class", cls))

        # Add buffer around each point
        cls_points_buffered = cls_points.map(lambda f: f.buffer(buffer_m))

        # Combine reducers
        reducer = (
            ee.Reducer.mean()
            .combine(ee.Reducer.stdDev(), sharedInputs=True)
            .combine(ee.Reducer.min(), sharedInputs=True)
            .combine(ee.Reducer.max(), sharedInputs=True)
            .combine(ee.Reducer.median(), sharedInputs=True)
        )

        # Reduce regions over buffered points
        stats = image.reduceRegions(
            collection=cls_points_buffered,
            reducer=reducer,
            scale=20
        )

        # Aggregate per-band stats across points
        cls_stats = {}
        for band in index_bands:
            band_mean = stats.aggregate_array(f"{band}_mean").getInfo()
            band_std = stats.aggregate_array(f"{band}_stdDev").getInfo()
            band_min = stats.aggregate_array(f"{band}_min").getInfo()
            band_max = stats.aggregate_array(f"{band}_max").getInfo()
            band_median = stats.aggregate_array(f"{band}_median").getInfo()

            cls_stats[band] = {
                "mean": sum(band_mean)/len(band_mean) if band_mean else None,
                "stdDev": sum(band_std)/len(band_std) if band_std else None,
                "min": min(band_min) if band_min else None,
                "max": max(band_max) if band_max else None,
                "median": sum(band_median)/len(band_median) if band_median else None
            }

        stats_dict[cls] = cls_stats

    return stats_dict
