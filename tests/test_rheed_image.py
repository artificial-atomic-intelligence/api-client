
from pandas import DataFrame
import pytest
from atomicds import Client
from datetime import datetime
from unittest import mock
from .conftest import ResultIDs
from atomicds.results import RHEEDVideoResult, RHEEDImageResult
from PIL.Image import Image
from pandas import DataFrame

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def result(client: Client):
    results = client.get(data_ids=ResultIDs.rheed_image)
    return results[0] 

def test_get_plot(result: RHEEDImageResult):
    plot = result.get_plot()
    assert isinstance(plot, Image)

def test_get_laue(result: RHEEDImageResult):
    radius, (x, y)  = result.get_laue_zero_radius()
    assert isinstance(radius, float)
    assert isinstance(x, float)
    assert isinstance(y, float)

def test_get_dataframe(result: RHEEDImageResult):

    cols = {'node_id', 'centroid_0', 'centroid_1', 'specular_origin_0',
       'specular_origin_1', 'relative_centroid_0', 'relative_centroid_1',
       'intensity_centroid_0', 'intensity_centroid_1', 'area', 'fwhm_0',
       'fwhm_1', 'mask_rle', 'bbox_maxc', 'bbox_maxr', 'bbox_minc',
       'bbox_minr', 'distances', 'spot_area', 'mask_width', 'pattern_id',
       'mask_height', 'streak_area', 'eccentricity', 'bbox_intensity',
       'center_distance', 'roughness_metric', 'axis_major_length',
       'axis_minor_length', 'data_id'}

    df = result.get_pattern_dataframe() 
    assert isinstance(df, DataFrame) 
    assert not len(set(df.columns) - cols)

    df = result.get_pattern_dataframe(symmetrize=True) 
    assert isinstance(df, DataFrame) 
    assert not len(set(df.columns) - cols)

    df = result.get_pattern_dataframe(return_as_features=True) 
    assert isinstance(df, DataFrame) 
    assert len(df) == 1
