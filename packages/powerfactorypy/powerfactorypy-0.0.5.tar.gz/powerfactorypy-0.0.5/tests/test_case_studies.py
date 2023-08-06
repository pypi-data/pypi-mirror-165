import pytest
import sys
sys.path.insert(0,r'.\src')
import powerfactorypy 
import importlib
importlib.reload(powerfactorypy)

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfcs(pf_app):
    # Return PFPlotInterface instance and show app
    pfcs = powerfactorypy.PFPlotInterface(pf_app)
    return pfcs 

  