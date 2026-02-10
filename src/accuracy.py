import ee

def compute_accuracy(mask, ref_samples):
    classified = mask.unmask(0).rename('classification')

    validation = classified.sampleRegions(
        collection=ref_samples,
        properties=['class'],
        scale=20,
        geometries=False
    )

    error_matrix = validation.errorMatrix(actual='class',predicted='classification')

    # ---- Basic metrics ----
    oa = error_matrix.accuracy()

    pa_list = error_matrix.producersAccuracy().toList()   # [[PA0], [PA1]]
    ua_list = error_matrix.consumersAccuracy().toList()   # [[UA0, UA1]]

    pa0 = ee.Number(ee.List(pa_list.get(0)).get(0))  # non-pit
    pa1 = ee.Number(ee.List(pa_list.get(1)).get(0))  # pit

    ua0 = ee.Number(ee.List(ua_list.get(0)).get(0))  # non-pit
    ua1 = ee.Number(ee.List(ua_list.get(0)).get(1))  # pit

    # ---- F1 score ----
    f1_nonpit = ee.Number(2).multiply(pa0).multiply(ua0).divide(pa0.add(ua0))
    f1_pit    = ee.Number(2).multiply(pa1).multiply(ua1).divide(pa1.add(ua1))

    # ---- Return client-side dict ----
    return {
        "OA": oa.getInfo(),
        "PA_nonpit": pa0.getInfo(),
        "PA_pit": pa1.getInfo(),
        "UA_nonpit": ua0.getInfo(),
        "UA_pit": ua1.getInfo(),
        "F1_nonpit": f1_nonpit.getInfo(),
        "F1_pit": f1_pit.getInfo()
    }

