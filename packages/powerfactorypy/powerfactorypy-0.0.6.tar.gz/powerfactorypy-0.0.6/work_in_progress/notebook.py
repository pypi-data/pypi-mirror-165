# %%
%load_ext autoreload
%autoreload 2
import sys
sys.path.append(r'C:\Program Files\DIgSILENT\PowerFactory 2022 SP1\Python\3.10')
import powerfactory as powerfactory

sys.path.insert(0,r'D:\User\seberlein\Code\powerfactorypy\src')
import powerfactorypy 

import time
import statistics
from re import sub
from os import path as os_path
from collections.abc import Iterable

app = powerfactory.GetApplication()
pfbi = powerfactorypy.PFBaseInterface(app)
pfbi.app.Show()
pfbi.app.ActivateProject(r'\seberlein\powfacpy\powfacpy_tests')

# %%
terminal_1 = pfbi.get_obj(r"Network Model\Network Data\Grid\Terminal HV 1")
print(terminal_1)
assert isinstance(terminal_1,powerfactory.DataObject)
# %% 
project_folder = pfbi.app.GetActiveProject()
terminal_1 = pfbi.get_obj(r"Network Model\Network Data\Grid\Terminal HV 1",project_folder)

time_with_folder = []
time_without_folder = []
for i in range(9):
    start = time.perf_counter()
    terminal_1 = pfbi.get_obj(r"Ntwork Model\Network Data\Grid\Terminal HV 1",project_folder)
    time_with_folder.append(time.perf_counter() - start)

    start = time.perf_counter()
    terminal_1 = pfbi.get_obj(r"Network Model\Network Data\Grid\Terminal HV 1")
    time_without_folder.append(time.perf_counter() - start)

print(statistics.mean(time_with_folder))
print(statistics.mean(time_without_folder))
# %% 
# pfbi.set_attr("Library\Dynamic Models\Linear_interpolation",{"sTitle":1})
pfbi.set_attr("Library\Dynamic Models\Linear_interpolation",
    {"sTitle":"Dummy title","desc":["Dummy description"]})
# %%
# pfbi.get_attr("Library\Dynamic Models\Linear_interpolation",["sTile","desc"])
pfbi.get_attr("Library\Dynamic Models\Linear_interpolation",["sTitle","desc"])
# %%
pfbi.get_obj(r"\Library\Dynamic Models\Linear_interpolation")
# %%
project_folder = pfbi.app.GetActiveProject()
powerfactorypy.PFStringManipuilation.delete_classes(str(project_folder))
# %%
pfbi.create_by_path("Library\Dynamic Models\dummy.BlkDef")
# %%
pfbi.create_by_path(4)
# %%
pfbi.create_in_folder(r"Library\Dynamic Models","dummy2.BlkDef")
pfbi.create_in_folder(r"Library\Dynamic Models",2)
# %%
contents1 = pfbi.get_from_folder(r"Network Model\Network Data\Grid\Voltage source ctrl")
contents2 = pfbi.get_from_folder(r"Network Model\Network Data\Grid\Voltage source ctrl",
    obj_name="Angle")
# %%
folder = r"Network Model\Network Data"
terminals = pfbi.get_from_folder(folder, obj_name="*.ElmTerm", attr="uknom", 
    attr_lambda=lambda x : x==110, include_subfolders=True)
len(terminals)

dsl_obj_angle = pfbi.get_from_folder(r"Network Model\Network Data\Grid\Voltage source ctrl",
    obj_name="Angle")
len(dsl_obj_angle)  

# %%   
folder = r"Network Model\Network Data\Grid"
terminals = pfbi.get_from_folder(folder, obj_name="*.ElmTerm")

mv_terminals = pfbi.get_by_attribute(terminals,"uknom",lambda x:x > 100)
print(len(terminals))
print(len(mv_terminals))
# 
# %%
folder = "Library\Dynamic Models\TestDelete"
pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")
pfbi.delete_obj_from_folder(folder,"dummy_to_be_deleted*")
objects_in_folder = pfbi.get_from_folder(folder)
print(len(objects_in_folder))

pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")
pfbi.delete_obj_from_folder(folder,"dummy_to_be_deleted_1.BlkDef")
objects_in_folder = pfbi.get_from_folder(folder)
print(len(objects_in_folder))

pfbi.create_in_folder(folder,"dummy_to_be_deleted_1.BlkDef")
pfbi.create_in_folder(folder,"dummy_to_be_deleted_2.BlkDef")
pfbi.delete_obj_from_folder("Library\Dynamic Models","dummy_to_be_deleted*",include_subfolders=True)

# pfbi.delete_obj_from_folder(folder,"dummy_to_be_deleted_1.BlkDef",error_when_nonexistent=True)
# %%
obj_to_be_copied = r"Library\Dynamic Models\Linear_interpolation"
folder_copy_to = r"Library\Dynamic Models\TestCopy"
pfbi.delete_obj_from_folder(folder_copy_to,"*",error_when_nonexistent=False)
pfbi.copy_obj(obj_to_be_copied,folder_copy_to)
pfbi.copy_obj(obj_to_be_copied,folder_copy_to,new_name="dummy_new_name")

pfbi.copy_obj(r"wrong_name",folder_copy_to,new_name="dummy_new_name")

# %%
folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
folder_copy_to = r"Library\Dynamic Models\TestCopyMultiple"
pfbi.copy_multiple_objects(folder_copy_from,folder_copy_to)

pfbi.delete_obj_from_folder(folder_copy_to,"*",error_when_nonexistent=False)
objects_to_copy = pfbi.get_from_folder(folder_copy_from)
pfbi.copy_multiple_objects(objects_to_copy,folder_copy_to)
# %%
project_folder = pfbi.app.GetActiveProject()
a = project_folder.GetChildren(1,r"Network Model\Network Data\Grid\*.ElmTerm",1)
print(a)
len(a)
# %%
pfbi.get_obj(r"Network Model\Network Data\Grid\*.ElmTerm",
    condition=lambda x: getattr(x,"ukno") > 20 and getattr(x,"uknom") < 100)

# %%
pfbi.get_obj(r"Network Model\Network Data\Grid\*.ElmTerm",
    condition=lambda x: getattr(x,"uknom") < 0)   
# %%
pfbi.get_obj(r"Network Model\Network Data\Grid\*.ElmTerm",
    condition=lambda x: getattr(x,"uknom") < 200)   

# %%
folder = r"Network Model\Network Data"
terminals = pfbi.get_from_folder(folder, obj_name="*.ElmTerm", error_if_non_existent=False,
    condition=lambda x: getattr(x,"uknom") < "100" and getattr(x,"uknom") > 0, include_subfolders=True)    
print(terminals)
len(terminals)
# %%
folder = r"Network Model\Network Data"
terminals = pfbi.get_from_folder(folder, obj_name="*.ElmTerm",  
    condition=lambda x : getattr(x,"uknom")==110, include_subfolders=True)
# %%
project = pfbi.get_obj("powerfactorypy_base",parent_folder="user")
type(project)
#%%
lib = app.GetGlobalLibrary()
lib.GetContents("Types") 
#%%
pfbi.path_exists("abc",parent="abc",return_info=True)
#%%
pfbi.get_obj(r"\Network Data\*.ElmTerm",parent_folder="Network Model",
    include_subfolders=True) 
#%%
parent_folder = pfbi.get_first_level_folder("user")    
# %%
folder = pfbi.get_obj(r"Network Model\Network Data")[0]
type(folder)
isinstance(folder, powerfactory.DataObject)
# %%
pfbi.handle_single_pf_object_input_or_path_string([folder])
# %%
pfbi.handle_single_pf_object_input_or_path_string(r"Network Model\Network Data")
# %%
folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
folder_copy_to = r"Library\Dynamic Models\TestCopyMultiple"

pfbi.delete_obj("*",parent_folder=folder_copy_to,error_if_non_existent=False)
copied_objects = pfbi.copy_obj("*",folder_copy_to,parent_folder=folder_copy_from)
len(copied_objects)
# %%
pfbi.delete_obj("*",parent_folder=folder_copy_to,error_if_non_existent=False)
folder_copy_from = pfbi.get_obj(r"Library\Dynamic Models\TestDummyFolder")[0]
folder_copy_to = pfbi.get_obj(r"Library\Dynamic Models\TestCopyMultiple")[0]
copied_objects = pfbi.copy_obj("*",folder_copy_to,parent_folder = folder_copy_from)
assert len(copied_objects) == 2

# %%
objects_to_copy = pfbi.get_obj("*",parent_folder=folder_copy_from)
copied_objects = pfbi.copy_obj(objects_to_copy,folder_copy_to,overwrite=False)
assert len(copied_objects) == 2
all_objects = pfbi.get_obj("*",parent_folder=folder_copy_to)
len(all_objects)
# %%
folder_copy_from = r"Library\Dynamic Models\TestDummyFolder"
folder_copy_to = r"Library\Dynamic Models\TestCopy"
pfbi.delete_obj("*",parent_folder=folder_copy_to,error_if_non_existent=False)
object_to_copy = pfbi.get_single_obj("dummy.*",parent_folder=folder_copy_from)
copied_object=pfbi.copy_single_obj(object_to_copy,folder_copy_to,overwrite=True)
# %%
pfbi.delete_obj("*",parent_folder=folder_copy_to,error_if_non_existent=False)
copied_object=pfbi.copy_single_obj(object_to_copy,folder_copy_to,overwrite=False)
# %%
pfbi.delete_obj("*",parent_folder=folder_copy_to,error_if_non_existent=False)
copied_object=pfbi.copy_single_obj("dummy.*",folder_copy_to,overwrite=False,
    parent_folder=folder_copy_from)
# %%
copied_object=pfbi.copy_single_obj("dummy.*",folder_copy_to,overwrite=False,
    parent_folder=folder_copy_from,new_name="new_dummy_name")
# %%
obj_to_copy = pfbi.get_single_obj("dummy2.*",parent_folder=folder_copy_from)
copied_object=pfbi.copy_single_obj(obj_to_copy,folder_copy_to,overwrite=True)   
# %%
copied_object=pfbi.copy_single_obj(obj_to_copy,folder_copy_to,overwrite=False,
    parent_folder=folder_copy_from,new_name="new_dummy_name")   
# %%
dsl_obj_lin_interp = pfbi.get_single_obj(r"Library\Dynamic Models\Linear_interpolation")
pfbi.set_attr(r"Network Model\Network Data\Grid\Voltage source ctrl\Angle",{"typ_id":dsl_obj_lin_interp})
pfbi.set_attr(r"Network Model\Network Data\Grid\Voltage source ctrl\Frequency",{"typ_id":dsl_obj_lin_interp})
pfbi.set_attr(r"Network Model\Network Data\Grid\Voltage source ctrl\Magnitude",{"typ_id":dsl_obj_lin_interp})
# %%
pf_sim = powerfactorypy.PFDynSimInterface(app)

# %%
pf_sim = powerfactorypy.PFDynSimInterface(app)
pf_sim.export_to_csv()
# %%
import pandas
df = pandas.read_csv('results.csv', header=[0,1])
df[df.columns[0][0],df.columns[0][1]]
# %%
with open('results.csv', "r") as f:
    f.readline()
    f.readline()

import csv
with open('results.csv', "w") as f:
    writer = csv.writer(f)
    writer.writerow("a")

# %%
import time

# pf_sim.initialize_and_run_sim()

start = time.process_time() 
pf_sim.export_to_csv()
print(time.process_time() - start)


# %%
# %%
import os
with open("results.csv") as read_file, open("results.csv.temp", "w") as write_file:
    full_paths = read_file.readline().split(",")
    variables = read_file.readline().split(",")
    for col,path in enumerate(full_paths):
        if col > 0:
            formated_path = powerfactorypy.PFStringManipuilation.format_full_path(path,pf_sim)
            variable_name = variables[col].split(" ", 1)[0][1:] 
            row = row + formated_path + "\\" + variable_name + ","
        else:
            row = "Time,"
    write_file.write(row+"\n")
    while row:
        row = read_file.readline()
        write_file.write(row)
os.replace("results.csv.temp","results.csv")   



# %%
%matplotlib qt

from matplotlib import pyplot
pyplot.figure()
pf_plot = powerfactorypy.PFPlotInterface(app)
powerfactorypy.PFPlotInterface.pyplot_from_csv(
    "results.csv",
    [r"Network Model\Network Data\Grid\AC Voltage Source\s:u0",
     r"Network Model\Network Data\Grid\AC Voltage Source\m:Qsum:bus1"]) 
pyplot.xlabel("t [s]")

pyplot.figure()
powerfactorypy.PFPlotInterface.pyplot_from_csv(
    "results.csv",
    [r"Network Model\Network Data\Grid\AC Voltage Source\s:u0",
     r"Network Model\Network Data\Grid\AC Voltage Source\m:Psum:bus1"])

# %%
comRes = pf_sim.app.GetFromStudyCase("ComRes")
all_calc = pf_sim.app.GetFromStudyCase("All calculations.ElmRes")
comRes.SetAttribute("resultobj",[all_calc])

# %% 
pf_plot = powerfactorypy.PFPlotInterface(app)
all_calc = pf_plot.app.GetFromStudyCase("All calculations.ElmRes")
pf_plot.set_active_plot("Test plot 1", "Test page")
pf_plot.plot(r"Network Model\Network Data\Grid\AC Voltage Source","m:Psum:bus1",results_obj=all_calc)
pf_plot.plot(r"Network Model\Network Data\Grid\AC Voltage Source","m:Qsum:bus1")
pf_plot.set_active_plot("Test plot 2", "Test page")
pf_plot.plot(r"Network Model\Network Data\Grid\AC Voltage Source","s:u0")

pf_plot.set_active_plot("Test plot 1", "Test page 2")
pf_plot.plot(r"Network Model\Network Data\Grid\AC Voltage Source","m:Psum:bus1")
pf_plot.plot(r"Network Model\Network Data\Grid\AC Voltage Source","m:Qsum:bus1")

# %%
source_study_case = r"Study Cases\Study Case 1"
target_study_cases = [r"Study Cases\Study Case 2", r"Study Cases\Study Case 3"]
source_study_case = pf_plot.handle_single_pf_object_or_path_input(source_study_case)
source_graphics_board = pf_plot.get_single_obj("Graphics Board",parent_folder=source_study_case)

for target_study_case in target_study_cases:
    target_study_case = pf_plot.handle_single_pf_object_or_path_input(target_study_case)
    target_graphics_board = pf_plot.get_single_obj("Graphics Board",parent_folder=target_study_case)
    pf_plot.delete_obj("*",parent_folder=target_graphics_board,error_if_non_existent=False)
    pf_plot.copy_obj("*",target_folder=target_graphics_board,overwrite=True,condition=None,
        parent_folder=source_graphics_board)

# %%
source_study_case = r"Study Cases\Study Case 1"
target_study_cases = [r"Study Cases\Study Case 1",r"Study Cases\Study Case 2", r"Study Cases\Study Case 3"]
pf_plot = powerfactorypy.PFPlotInterface(app)
pf_plot.copy_graphics_board_content(source_study_case,target_study_cases,
    obj_to_copy="*.GrpPage",clear_target_graphics_board=True)

# %%
source_study_case = r"Study Cases\Study Case 1"
pf_plot = powerfactorypy.PFPlotInterface(app)
pf_plot.copy_graphics_board_content_to_all_study_cases(source_study_case)

# %%
pfplot = powerfactorypy.PFPlotInterface(app)

study_cases = pfplot.get_obj(r"Study Cases\Study Case*.IntCase")
pfplot.set_active_plot("Test plot 1", "Test page")
plot_obj = r"Network Model\Network Data\Grid\AC Voltage Source"
plot_var = "m:Psum:bus1"
for study_case in study_cases:
    results_obj = pf_plot.get_single_obj("All calculations",
        parent_folder=study_case)
    pf_plot.plot(plot_obj,plot_var,result_obj=results_obj)  

# %%
results_objects = pfplot.get_multiple_obj_from_similar_sub_directories(
    r"Study Cases\Study Case*.IntCase","All calculations")   

study_case = pfplot.create_in_folder("Study Cases","Comparison.IntCase",overwrite=True)
study_case.Activate()    
pfplot.get_or_create_graphics_board()
pfplot.set_active_plot("Test plot 1", "Test page")

# %%

# %%
study_case.Deactivate()
study_case = pfplot.create_in_folder("Study Cases","Comparison.IntCase",overwrite=True)
study_case.Activate()
# %%
grb = pfplot.get_or_create_graphics_board()
grb.Show()
# %%
pfplot.set_active_plot("Test plot 1", "Test")


# %%
data_series = pfplot.get_data_series_of_active_plot()
data_series.ClearCurves()
# %%

pfplot.clear_plot_pages()
pfplot.set_active_plot("Test plot 1", "Test")
results_objects = pfplot.get_multiple_obj_from_similar_sub_directories(
    r"Study Cases\Study Case*.IntCase","All calculations") 
plot_obj = r"Network Model\Network Data\Grid\AC Voltage Source"
plot_var = "m:Psum:bus1"    
for results_obj in results_objects:
    pfplot.plot(plot_obj,plot_var,result_obj=results_obj)          

# %%
pfplot.get_multiple_obj_from_similar_sub_directories(
    r"Study Cases\Study Case*.IntCase","All calculations")

# %%
case.Deactivate()
case.Delete()
pfplot = powerfactorypy.PFPlotInterface(app)
active_project = app.GetActiveProject()
study_cases_folder = active_project.GetContents("Study Cases")[0]
case = study_cases_folder.CreateObject("IntCase","Test")
case.Activate()
grb = pfplot.app.GetGraphicsBoard()   
grb = case.CreateObject("SetDesktop","Graphics Board")
grb.Show()
page = grb.GetPage("Test",1,"GrpPage")
page.GetOrInsertCurvePlot("Test")

# %%
pfplot = powerfactorypy.PFPlotInterface(app)
pfsim = powerfactorypy.PFDynSimInterface(app)
pfsim.activate_study_case(r"Study Cases\test_plot_interface\Study Case 1")
# pfsim.initialize_and_run_sim()
pfplot.set_active_plot("test_plot 1","test_plot_interface 1")
pfplot.plot(r"Network Model\Network Data\Grid\AC Voltage Source",
    ["s:u0","m:Qsum:bus1"])

# %%

pfcs = powerfactorypy.PFCaseStudies(app)
params = {"p":r"Network Model\Network Data\Grid\General Load HV\plini",
"q":r"Network Model\Network Data\Grid\General Load HV\qlini",
"u":r"Network Model\Network Data\Grid\Terminal HV 2\uknom"
}

delimiter = "|"
param_value_string = ""
for parname,path_with_par in params.items():
    value = pfcs.get_attr_by_path(path_with_par)
    param_value_string += parname + "=" + str(value) + delimiter
param_value_string = param_value_string[:-1]
print(param_value_string)

# %%
pfcs = powerfactorypy.PFCaseStudies(app)
params = {"p":r"Network Model\Network Data\Grid\General Load HV\plini",
"q":r"Network Model\Network Data\Grid\General Load HV\qlini",
"u":r"Network Model\Network Data\Grid\Terminal HV 2\uknom"
}
pfcs.get_parameter_value_string(params)

# %%
pfcs = powerfactorypy.PFCaseStudies(app)
# invalid characters :*?=",\~|(LF)(CR)!
parameter_values = {
    "p HV load":[0, 1, 2, 3],
    "q HV load":[-2, -1, 1, 2],
}
parameter_paths = {
    "p HV load":r"Network Model\Network Data\Grid\General Load HV\plini",
    "q HV load":r"Network Model\Network Data\Grid\General Load HV\qlini",
}
active_grids = [
    r"Network Model\Network Data\Grid",
    r"Network Model\Network Data\Grid",
    r"Network Model\Network Data\Grid",
    r"Network Model\Network Data\Grid"
]

delimiter = " "
parent_folder_study_cases = r"Study Cases\test_case_studies"
parent_folder_scenarios = r"Network Model\Operation Scenarios\test_case_studies"
parent_folder_variations = r"Network Model\Variations\test_case_studies"
parent_folder_operation_scenarios = r"Network Model\Operation Scenarios\test_case_studies"
number_of_cases = len(next(iter(parameter_values.values())))
for case_num in range(number_of_cases):
    parameter_values_string = ""
    for parameter,value in parameter_values.items():
        parameter_values_string += parameter + "_" + str(value[case_num]) + delimiter
    parameter_values_string = parameter_values_string[:-1]    
    study_case_obj = pfcs.create_in_folder(parent_folder_study_cases,
        parameter_values_string+".IntCase")
    study_case_obj.Activate()
    if isinstance(active_grids,(list,tuple)):
        for grids in active_grids:
            if not isinstance(grids,(list,tuple)):
                grids = [grids]
            for grid in grids:
                grid = pfcs.handle_single_pf_object_or_path_input(grid)
                grid.Activate()
    else:
        grid = pfcs.handle_single_pf_object_or_path_input(active_grids)
        grid.Activate()             
    scenario_obj = pfcs.create_in_folder(parent_folder_scenarios,
        parameter_values_string+".IntScenario")
    scenario_obj.Activate()
    variation_obj = pfcs.create_in_folder(parent_folder_variations,
        parameter_values_string+".IntScheme")
    variation_obj.NewStage(parameter_values_string,0,1)
    variation_obj.Activate()
    for parameter,value in parameter_values.items():
        pfcs.set_attr_by_path(parameter_paths[parameter],value[case_num])
    scenario_obj.Save()
# %% 
pfcs.delete_obj(r"Study Cases\test_case_studies\p HV load_0 q HV load_-2(1)")    
# %%
pf_cases = powerfactorypy.PFStudyCases(app)
pf_cases.parameter_values = {
    "p HV load":[1, 2, 1, 2],
    "q HV load":[-1, -1, 1, 1],
}
pf_cases.parameter_paths = {
    "p HV load":r"Network Model\Network Data\Grid\General Load HV\plini",
    "q HV load":r"Network Model\Network Data\Grid\General Load HV\qlini",
}
pf_cases.active_grids = r"Network Model\Network Data\test_case_studies\Grid 1"

pf_cases.delimiter = " "
pf_cases.parent_folder_study_cases = r"Study Cases\test_case_studies"
pf_cases.parent_folder_scenarios = r"Network Model\Operation Scenarios\test_case_studies"
pf_cases.parent_folder_variations = r"Network Model\Variations\test_case_studies"
pf_cases.delete_obj("*",
    parent_folder = pf_cases.parent_folder_study_cases,error_if_non_existent=False)
pf_cases.delete_obj("*",parent_folder =pf_cases.parent_folder_scenarios,
    error_if_non_existent=False)
pf_cases.delete_obj("*",parent_folder =pf_cases.parent_folder_variations,
    error_if_non_existent=False)
pf_cases.hierarchy = ["q HV load"]
pf_cases.create_cases()

# %%
selected_cases = pf_cases.get_study_cases({"p HV load": lambda x: x == 2})
selected_cases[0].Activate()
selected_cases[1].Activate()
# %%
pfbi = powerfactorypy.PFBaseInterface(app)
pfbi.create_directory(r"test1\test2",
    parent_folder=r"Study Cases\test_case_studies")
# %%
pfbi.create_directory(r"test1\test2\test3\test4",
    parent_folder=r"Study Cases\test_case_studies")
pfbi.delete_obj("test1",parent_folder=r"Study Cases\test_case_studies")
# %%
pf_cases = powerfactorypy.PFStudyCases(app)
pf_cases.parameter_values = {
    "p HV load":[1, 2, 1, 2, 1, 2, 1, 2,],
    "q HV load":[-1, -1, 1, 1,-1, -1, 1, 1,],
    "control": ["A","A","A","A","B","B","B","B",]
}
pf_cases.parameter_paths = {
    "p HV load":r"Network Model\Network Data\Grid\General Load HV\plini",
    "q HV load":r"Network Model\Network Data\Grid\General Load HV\qlini",
}
pf_cases.active_grids = [
    [r"Network Model\Network Data\test_case_studies\Grid 1",
    r"Network Model\Network Data\test_case_studies\Grid 2"],
    [r"Network Model\Network Data\test_case_studies\Grid 1"],
    r"Network Model\Network Data\test_case_studies\Grid 1",
    [r"Network Model\Network Data\test_case_studies\Grid 1",
    r"Network Model\Network Data\test_case_studies\Grid 2"],
    r"Network Model\Network Data\test_case_studies\Grid 2",
    r"Network Model\Network Data\test_case_studies\Grid 2",
    r"Network Model\Network Data\test_case_studies\Grid 2",
    r"Network Model\Network Data\test_case_studies\Grid 2",
]

pf_cases.delimiter = " "
pf_cases.parent_folder_study_cases = r"Study Cases\test_case_studies"
pf_cases.parent_folder_scenarios = r"Network Model\Operation Scenarios\test_case_studies"
pf_cases.parent_folder_variations = r"Network Model\Variations\test_case_studies"
pf_cases.delete_obj("*",
    parent_folder = pf_cases.parent_folder_study_cases,error_if_non_existent=False)
pf_cases.delete_obj("*",parent_folder =pf_cases.parent_folder_scenarios,
    error_if_non_existent=False)
pf_cases.delete_obj("*",parent_folder =pf_cases.parent_folder_variations,
    error_if_non_existent=False)
pf_cases.hierarchy = ["control","q HV load"]
pf_cases.add_variation_to_each_case = True
pf_cases.create_cases()

# %%
pf_plots = powerfactorypy.PFPlotInterface(app)
pf_sim = powerfactorypy.PFDynSimInterface(app)
for case_num,study_case_obj in enumerate(pf_cases.study_cases):
    
    study_case_obj.Activate()
    # Set controller parameter
    dsl_controller_obj = r"Network Model\Network Data\test_case_studies\Grid 2\WECC WT Control System Type 4A\REEC_A Electrical Control Model"
    if pf_cases.get_value_of_parameter_for_case("control",case_num) == "A":
        pf_cases.set_attr(dsl_controller_obj,{"PfFlag":0}) 
        pf_cases.set_attr(dsl_controller_obj,{"VFlag":1}) 
    elif pf_cases.get_value_of_parameter_for_case("control",case_num) == "B":
        pf_cases.set_attr(dsl_controller_obj,{"PfFlag":1}) 
        pf_cases.set_attr(dsl_controller_obj,{"VFlag":0}) 
    # Plot
    pf_plots.clear_plot_pages()
    pf_plots.set_active_plot("Reactive current","WPP")
    pf_plots.plot(dsl_controller_obj,"s:Iqcmd")
    # Simulate   
    pf_sim.initialize_and_run_sim() 
      

# %%
