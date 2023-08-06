import pytest
import sys
sys.path.append(r'C:\Program Files\DIgSILENT\PowerFactory 2022 SP1\Python\3.10')
import powerfactory
sys.path.insert(0,r'.\src')
import powerfactorypy 
import importlib
importlib.reload(powerfactorypy)
from os import remove

from test_base_interface import pfbi, pf_app, activate_test_project

@pytest.fixture
def pfsim(pf_app):
    # Return PFDynSimInterface instance
    return powerfactorypy.PFDynSimInterface(pf_app)   

def test_export_to_csv(pfsim,activate_test_project):
    export_dir = r"D:\User\seberlein\Code\powerfactorypy\tests"
    file_name = "test_results"
    pfsim.add_results_variable(
        r"Network Model\Network Data\Grid\AC Voltage Source","m:Psum:bus1")    
    pfsim.initialize_and_run_sim()  

    pfsim.export_dir =  export_dir
    pfsim.export_to_csv() 
    remove(export_dir + "\\results.csv")

    pfsim.export_to_csv(dir=export_dir, file_name=file_name)
    remove(export_dir + "\\" + file_name + ".csv")

    results_obj = pfsim.get_single_obj(
        r"Study Cases\Study Case 1\All calculations")
    print(results_obj)
    pfsim.export_to_csv(results_obj=results_obj) 
    remove(export_dir + "\\results.csv")    

if __name__ == "__main__":
    pytest.main(([r"tests\test_dyn_sim_interface.py"]))