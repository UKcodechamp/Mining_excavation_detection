import ee


def init_gee(project_id):
    ee.Initialize(project='transitional-proj')
print('EE OK')