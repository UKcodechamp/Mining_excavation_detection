import ee


def compute_percentiles(years, aoi, ref_samples, annual_s2_composite):

    indices = ['NDVI', 'MNDWI', 'BSI', 'BU', 'BAEI']
    percentiles_by_year = {}

    for year in years:

        img = annual_s2_composite(year, aoi)

        # Sample image at reference points
        samples = img.select(indices).sampleRegions(
            collection=ref_samples,
            properties=['class'],   # your label column
            scale=10
        )

        thresholds = {}

        for idx in indices:

            # Pit samples (class = 1)
            pit_samples = samples.filter(ee.Filter.eq('class', 1))

            pit_90 = pit_samples.reduceColumns(
                ee.Reducer.percentile([90]),
                selectors=[idx]
            ).get('p90')

            # Non-pit samples (class = 0)
            nonpit_samples = samples.filter(ee.Filter.eq('class', 0))

            nonpit_10 = nonpit_samples.reduceColumns(
                ee.Reducer.percentile([10]),
                selectors=[idx]
            ).get('p10')

            thresholds[idx] = {
                'pit_90': pit_90.getInfo(),
                'nonpit_10': nonpit_10.getInfo()
            }

        percentiles_by_year[year] = thresholds

    return percentiles_by_year



def compute_summary_thresholds(percentiles_by_year, years):

    indices = ['NDVI', 'MNDWI', 'BSI', 'BU', 'BAEI']

    average_thresholds = {}
    conservative_thresholds = {}

    for idx in indices:

        pit_vals = [percentiles_by_year[y][idx]['pit_90'] for y in years]
        nonpit_vals = [percentiles_by_year[y][idx]['nonpit_10'] for y in years]

        # Average
        average_thresholds[idx] = {
            'pit_90': sum(pit_vals) / len(pit_vals),
            'nonpit_10': sum(nonpit_vals) / len(nonpit_vals)
        }

        # Conservative
        conservative_thresholds[idx] = {
            'pit_90': max(pit_vals),
            'nonpit_10': min(nonpit_vals)
        }

    return average_thresholds, conservative_thresholds
