from ._variable_identification import determine_variable_type
from ._constants import VARIABLE_TYPE_INDICATORS


def from_file(ncbuild_dataset): 
    def iterate_group(ncbuild_dataset_group, netcdf4_dataset_group, group_name):
        
        variable_type_dict = determine_variable_type(ncbuild_dataset.dataset)
        ncbuild_dataset.data_structure[group_name] = variable_type_dict
        
        file_attributes = netcdf4_dataset_group.__dict__
        
        for key in file_attributes.keys():
            ncbuild_dataset_group.attribute(key, file_attributes[key])
            
        for variable in netcdf4_dataset_group.variables:
            variable_name = variable
            variable_data_type = netcdf4_dataset_group.variables[variable].dtype
            variable_dimensions = netcdf4_dataset_group.variables[variable].dimensions

            if len(variable_type_dict[variable]) == 1:
                variable_type = variable_type_dict[variable][0]
            else:
                variable_type = VARIABLE_TYPE_INDICATORS['U']

                # variable_values = netcdf4_dataset_group.variables[variable][:]
            new_variable = ncbuild_dataset_group.variable(variable_name, variable_data_type,
                                                          variable_dimensions, variable_type)

            for key in netcdf4_dataset_group.variables[variable].__dict__:
                name = key
                value = str(netcdf4_dataset_group.variables[variable].__dict__[key])
                new_variable.attribute(name, value)
                
        for dimension in netcdf4_dataset_group.dimensions:
            dimension_name = dimension
            dimension_length = netcdf4_dataset_group.dimensions[dimension].size
                
            ncbuild_dataset_group.dimension(name=dimension_name, length=dimension_length)
            
        for group in netcdf4_dataset_group.groups:
            new_group = ncbuild_dataset_group.group(group)
            iterate_group(new_group, netcdf4_dataset_group[group], group.name)
            
    iterate_group(ncbuild_dataset, ncbuild_dataset.dataset, 'main_group')
