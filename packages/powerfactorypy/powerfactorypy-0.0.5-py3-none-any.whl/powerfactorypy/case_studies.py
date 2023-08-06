import sys
sys.path.insert(0,r'.\src')
import powerfactorypy

class PFCaseStudies(powerfactorypy.PFBaseInterface):
  language = powerfactorypy.PFBaseInterface.language

  def __init__(self,app):
    super().__init__(app)
    self.active_grids = None
    self.parameter_values = None
    self.parameter_paths = None
    self.delimiter = " "
    self.hierarchy = None
    # ToDo language
    self.parent_folder_study_cases = r"Study Cases"
    self.parent_folder_scenarios = r"Network Model"
    self.parent_folder_variations = r"Network Model"
    self.parent_folder_operation_scenarios = r"Network Model"

  def create_cases(self):
    number_of_cases = len(next(iter(self.parameter_values.values())))
    for case_num in range(number_of_cases):
      if self.hierarchy:
        folder_path = ""
        for par in self.hierarchy:
          folder_path += par + "_" + str(self.parameter_values[par][case_num]) + self.delimiter
        folder_path = folder_path[:-1]
      parameter_values_string = self.get_case_param_value_string(case_num) 
      self.create_study_cases_scenarios_variants(parameter_values_string,folder_path) 
      self.set_parameters(case_num)

  def get_case_param_value_string(self,case_num):
    parameter_values_string = ""
    for parameter,value in self.parameter_values.items():
      if parameter not in self.hierarchy:
        parameter_values_string += parameter + "_" + str(value[case_num]) + self.delimiter
    return parameter_values_string[:-1]

  def create_study_cases_scenarios_variants(self,parameter_values_string,folder_path): 
    if folder_path:
      parent_folder_path = self.parent_folder_study_cases + "\\" + folder_path
      print(parent_folder_path)
      if not self.path_exists(parent_folder_path):
        folder_names = parent_folder_path.split("\\")
        print(folder_names)
        path = ""
        for folder_name in folder_names:
          path += "\\" + folder_name
          print(path)
          if not self.path_exists(path[1:]):
            self.create_by_path(path + ".IntFolder") 
    parent_folder = self.get_single_obj(parent_folder_path)
    study_case_obj = self.create_in_folder(parent_folder,
      parameter_values_string+".IntCase")
    study_case_obj.Activate()
    self.activate_grids()            
    scenario_obj = self.create_in_folder(self.parent_folder_scenarios,
      parameter_values_string+".IntScenario")
    scenario_obj.Activate()
    variation_obj = self.create_in_folder(self.parent_folder_variations,
      parameter_values_string+".IntScheme")
    variation_obj.NewStage(parameter_values_string,0,1)
    variation_obj.Activate()

  def activate_grids(self):
    if isinstance(self.active_grids,(list,tuple)):
      for grids in self.active_grids:
        if not isinstance(grids,(list,tuple)):
            grids = [grids]
        for grid in grids:
            grid = self.handle_single_pf_object_or_path_input(grid)
            grid.Activate()
    else:
      grid = self.handle_single_pf_object_or_path_input(self.active_grids)
      grid.Activate() 

  def set_parameters(self,case_num):
    for parameter,value in self.parameter_values.items():
      self.set_attr_by_path(self.parameter_paths[parameter],value[case_num])  

