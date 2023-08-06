from ._constants import UNITS, STANDARD_NAMES, LIST_OF_VARIABLE_NAMES, VARIABLE_TYPE_INDICATORS


def determine_variable_type(netCDF4_dataset):
    variables = netCDF4_dataset.variables
    variable_type_dict = {}
    
    for variable in variables:
        variable_type_dict[variable] = []
    
    for variable in variables:
        if len(variables[variable].dimensions) == 1 and variables[variable].dimensions[0] == variable:
            if hasattr(variables[variable], 'axis'):
                if variables[variable].axis == 'X':
                    if VARIABLE_TYPE_INDICATORS['X'] not in variable_type_dict[variable]:
                        variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['X'])
                elif variables[variable].axis == 'Y':
                    if VARIABLE_TYPE_INDICATORS['Y'] not in variable_type_dict[variable]:
                        variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['Y'])
                elif variables[variable].axis == 'Z':
                    if VARIABLE_TYPE_INDICATORS['Z'] not in variable_type_dict[variable]:
                        variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['Z'])
                elif variables[variable].axis == 'T':
                    if VARIABLE_TYPE_INDICATORS['T'] not in variable_type_dict[variable]:
                        variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['T'])
            elif hasattr(variables[variable], 'standard_name'):
                if variables[variable].standard_name in STANDARD_NAMES:
                    if STANDARD_NAMES[variables[variable].standard_name] not in variable_type_dict[variable]:
                        variable_type_dict[variable].append(STANDARD_NAMES[variables[variable].standard_name])
            elif hasattr(variables[variable], 'units'):
                if variables[variable].units in UNITS:
                    if UNITS[variables[variable].units] not in variable_type_dict[variable]:
                        variable_type_dict[variable].append(UNITS[variables[variable].units])
                elif 'since' in variables[variable].units:
                    variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['T'])
            if VARIABLE_TYPE_INDICATORS['X'] not in variable_type_dict[variable] and VARIABLE_TYPE_INDICATORS['Y'] \
                    not in variable_type_dict[variable] and VARIABLE_TYPE_INDICATORS['Z'] not in \
                    variable_type_dict[variable] and VARIABLE_TYPE_INDICATORS['T'] not in \
                    variable_type_dict[variable]:
                if VARIABLE_TYPE_INDICATORS['C'] not in variable_type_dict[variable]:
                    variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['C'])
        
        if 'dimensions' in variables[variable].ncattrs():
            if VARIABLE_TYPE_INDICATORS['DO'] not in variable_type_dict[variable]:
                variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['DO'])
        if hasattr(variables[variable], 'grid_mapping_name'):
            if VARIABLE_TYPE_INDICATORS['G'] not in variable_type_dict[variable]:
                variable_type_dict[variable].append(VARIABLE_TYPE_INDICATORS['G'])
            
        if hasattr(variables[variable], 'grid_mapping'):
            grid_mapping_variable = variables[variable].grid_mapping
            if grid_mapping_variable in variable_type_dict:
                if VARIABLE_TYPE_INDICATORS['G'] not in variable_type_dict[grid_mapping_variable]:
                    variable_type_dict[grid_mapping_variable].append(VARIABLE_TYPE_INDICATORS['G'])
            
        if hasattr(variables[variable], 'bounds'):
            boundary_variable = variables[variable].bounds
            if boundary_variable in variable_type_dict:
                if VARIABLE_TYPE_INDICATORS['B'] not in variable_type_dict[boundary_variable]:
                    variable_type_dict[boundary_variable].append(VARIABLE_TYPE_INDICATORS['B'])
            
        if hasattr(variables[variable], 'ancillary_variables'):
            ancillary_variable_list = variables[variable].ancillary_variables.split(' ')
            for ancillary_variable in ancillary_variable_list:
                if ancillary_variable in variable_type_dict:
                    if ancillary_variable in variable_type_dict:
                        if VARIABLE_TYPE_INDICATORS['AD'] not in variable_type_dict[ancillary_variable]:
                            variable_type_dict[ancillary_variable].append(VARIABLE_TYPE_INDICATORS['AD'])
        
        if hasattr(variables[variable], 'coordinates'):
            auxillary_variable_list = variables[variable].coordinates.split(' ')
            for auxillary_variable in auxillary_variable_list:
                if auxillary_variable in variable_type_dict:
                    if len(variables[auxillary_variable].dimensions) == 0:
                        if VARIABLE_TYPE_INDICATORS['S'] not in variable_type_dict[auxillary_variable]:
                            variable_type_dict[auxillary_variable].append(VARIABLE_TYPE_INDICATORS['S'])
                    elif auxillary_variable in variable_type_dict:
                        if auxillary_variable not in variables[auxillary_variable].dimensions:
                            if VARIABLE_TYPE_INDICATORS['AC'] not in variable_type_dict[auxillary_variable]:
                                variable_type_dict[auxillary_variable].append(VARIABLE_TYPE_INDICATORS['AC'])
            
        if hasattr(variables[variable], 'cell_measures'):
            cell_measures_string = variables[variable].cell_measures
            counter = 1
            
            for character in cell_measures_string:
                if character == ':' and cell_measures_string[counter] == ' ':
                    cell_measures_string = cell_measures_string[:counter] + cell_measures_string[counter + 1:]
                else:
                    counter += 1
                    
            cell_measures_list = cell_measures_string.split(' ')
            cell_measures_variable_list = []
            
            for cell_measures_pair in cell_measures_list:
                key_value = cell_measures_pair.split(':')
                cell_measures_variable_list.append(key_value[1])
            
            for cell_measures_variable in cell_measures_variable_list:
                if cell_measures_variable in variable_type_dict:
                    if VARIABLE_TYPE_INDICATORS['CM'] not in variable_type_dict[cell_measures_variable]:
                        variable_type_dict[cell_measures_variable].append(VARIABLE_TYPE_INDICATORS['CM'])
    
    for var_name in variable_type_dict:
        if len(variable_type_dict[var_name]) == 0:
            has_x_dim = False
            has_y_dim = False
            for dim in variables[var_name].dimensions:
                if dim in variable_type_dict:
                    if VARIABLE_TYPE_INDICATORS['X'] in variable_type_dict[dim]:
                        has_x_dim = True
                    elif VARIABLE_TYPE_INDICATORS['Y'] in variable_type_dict[dim]:
                        has_y_dim = True
            if has_x_dim and has_y_dim:
                if VARIABLE_TYPE_INDICATORS['GD'] not in variable_type_dict[var_name]:
                    variable_type_dict[var_name].append(VARIABLE_TYPE_INDICATORS['GD'])
            elif len(variables[var_name].dimensions) < 0:
                if VARIABLE_TYPE_INDICATORS['D'] not in variable_type_dict[var_name]:
                    variable_type_dict[var_name].append(VARIABLE_TYPE_INDICATORS['D'])
            else:
                variable_type_dict[var_name].append(VARIABLE_TYPE_INDICATORS['S'])
                
    return variable_type_dict        


def sort_and_merge_attribute_lists(requiered_attributes, secondary_attributes):
    for key in secondary_attributes:
        
        if key in requiered_attributes.keys():
            requiered_attributes.pop(key)
            
    return {**requiered_attributes, **secondary_attributes}


def sort_variables(variables):
    sorted_variable_list = []

    for type_indicator in LIST_OF_VARIABLE_NAMES:
        for variable in variables:
            if variable.variable_type == type_indicator:
                sorted_variable_list.append(variable)

    return sorted_variable_list
