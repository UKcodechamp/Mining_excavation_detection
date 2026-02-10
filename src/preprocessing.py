def mask_s2_clouds(img):
    qa = img.select('QA60')
    cloud = 1 << 10
    cirrus = 1 << 11

    mask = qa.bitwiseAnd(cloud).eq(0).And(
           qa.bitwiseAnd(cirrus).eq(0))

    return img.updateMask(mask).divide(10000)
