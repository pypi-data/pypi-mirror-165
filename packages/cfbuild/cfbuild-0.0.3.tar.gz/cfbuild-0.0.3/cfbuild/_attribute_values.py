import numpy
import datetime

from cfunits import Units
from lxml import etree

from ._ncml_comments import UNITS_WARNING, STANDARD_NAME_WARNING, TEMPORAL_UNITS_WARNING, \
    OPENDAP_RESERVED_KEYWORDS_WARNING
from ._constants import CONVENTION_VERSIONS, WARNING_MESSAGE, GLOBAL_ATTRIBUTES, UNITS, OPENDAP_RESERVED_KEYWORDS, VARIABLE_TYPE_INDICATORS
from ._ncml_comments import ADD_GRID_MAPPING_VARIABLE


def _check_variable(variable):
    list_of_warnings = []
    if variable.name in OPENDAP_RESERVED_KEYWORDS:
        list_of_warnings.append(OPENDAP_RESERVED_KEYWORDS_WARNING)

    return list_of_warnings


def _check_attribute_values(merged_attributes, variable, standard_name_table, variable_values):
    if 'standard_name' in merged_attributes:
        tree = etree.parse(standard_name_table)
        root = tree.getroot()
        standard_name_element = root.findall('entry[@id="' + merged_attributes['standard_name'] + '"]')

        if merged_attributes['standard_name'] == 'latitude':
            if 'units' in merged_attributes:
                merged_attributes['units'] = 'degrees_north'
            if 'long_name' in merged_attributes:
                if WARNING_MESSAGE in merged_attributes['long_name']:
                    merged_attributes['long_name'] = 'Latitudinal Axis'

        elif merged_attributes['standard_name'] == 'longitude':
            if 'units' in merged_attributes:
                merged_attributes['units'] = 'degrees_east'
            if 'long_name' in merged_attributes:
                if WARNING_MESSAGE in merged_attributes['long_name']:
                    merged_attributes['long_name'] = 'Longitudinal Axis'

        elif merged_attributes['standard_name'] == 'time':
            if 'units' in merged_attributes:
                if WARNING_MESSAGE in merged_attributes['units']:
                    merged_attributes['units'] = {'value': '!!!CHANGE ME!!! - (temporal units) since (date)',
                                                  'comment': TEMPORAL_UNITS_WARNING}
            if 'long_name' in merged_attributes:
                if WARNING_MESSAGE in merged_attributes['long_name']:
                    merged_attributes['long_name'] = 'Temporal Axis'

        if len(standard_name_element) > 0:
            standard_name_element = standard_name_element[0]
            standard_units = standard_name_element.findall('canonical_units')

            if len(standard_units) > 0:
                standard_units = Units(standard_units[0].text)

                if 'units' in merged_attributes:
                    if not isinstance(merged_attributes['units'], dict):
                        units = Units(merged_attributes['units'])

                        if not standard_units.equivalent(units) and 'since' not in merged_attributes['units']:
                            if WARNING_MESSAGE not in merged_attributes['units']:
                                merged_attributes['units'] = {'value': str(units),
                                                              'comment': UNITS_WARNING[0] + str(units) +
                                                                         UNITS_WARNING[1] + str(standard_units) +
                                                                         UNITS_WARNING[2]}

        else:
            value = merged_attributes['standard_name']
            if WARNING_MESSAGE not in value:
                merged_attributes['standard_name'] = {'value': value,
                                                      'comment': STANDARD_NAME_WARNING[0] + value +
                                                                 STANDARD_NAME_WARNING[1]}


    if '_FillValue' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['_FillValue']
        else:
            if type(merged_attributes['_FillValue']) == str:
                if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
                    del merged_attributes['_FillValue']
                else:
                    if WARNING_MESSAGE in merged_attributes['_FillValue']:
                        merged_attributes['_FillValue'] = variable_values.fill_value

    if 'missing_value' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['missing_value']
        else:
            if type(merged_attributes['missing_value']) == str:
                if WARNING_MESSAGE in merged_attributes['missing_value']:
                    if '_FillValue' in merged_attributes:
                        merged_attributes['missing_value'] = merged_attributes['_FillValue']
                    else:
                        merged_attributes['missing_value'] = variable_values.fill_value

    if 'valid_min' in merged_attributes or 'valid_max' in merged_attributes:
        if 'valid_range' in merged_attributes:
            del merged_attributes['valid_range']

    elif 'valid_range' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['valid_range']
        else:
            if type(merged_attributes['valid_range']) == str:
                if WARNING_MESSAGE in merged_attributes['valid_range']:
                    data_type = variable.data_type
                    change_value = True

                    if numpy.issubdtype(data_type, numpy.integer):
                        data_type = 'int'
                    elif numpy.issubdtype(data_type, numpy.float):
                        data_type = 'float'
                    elif numpy.issubdtype(data_type, numpy.str):
                        data_type = 'str'
                    elif numpy.issubdtype(data_type, numpy.bool):
                        data_type = 'bool'
                    elif numpy.issubdtype(data_type, numpy.complex):
                        data_type = 'complex'
                    else:
                        data_type = 'unknown'

                    if '_FillValue' in merged_attributes:
                        fill_value = merged_attributes['_FillValue']
                    else:
                        fill_value = None

                    if data_type == 'int':
                        if isinstance(fill_value, str):
                            fill_value = int(fill_value)
                        if fill_value is None:
                            valid_min = numpy.iinfo(variable.data_type).min
                            valid_max = numpy.iinfo(variable.data_type).max
                        elif fill_value < 0:
                            valid_min = fill_value + 1
                            valid_max = numpy.iinfo(variable.data_type).max
                        elif fill_value >= 0:
                            valid_min = numpy.iinfo(variable.data_type).min
                            valid_max = fill_value - 1
                    elif data_type == 'float':
                        if isinstance(fill_value, str):
                            fill_value = float(fill_value)
                        if fill_value is None:
                            valid_min = numpy.finfo(variable.data_type).min
                            valid_max = numpy.finfo(variable.data_type).max
                        elif fill_value < 0:
                            valid_min = fill_value + 2 * numpy.finfo(variable.data_type).eps
                            valid_max = numpy.finfo(variable.data_type).max
                        elif fill_value >= 0:
                            valid_min = numpy.finfo(variable.data_type).min
                            valid_max = fill_value - 2 * numpy.finfo(variable.data_type).eps
                    else:
                        change_value = False
                        valid_max = None
                        valid_min = None

                    if change_value:
                        valid_range = [valid_min, valid_max]
                        merged_attributes['valid_range'] = valid_range

    if 'actual_range' in merged_attributes:
        if not isinstance(variable_values, numpy.ndarray) or len(variable_values.shape) <= 0:
            del merged_attributes['actual_range']
        else:
            if type(merged_attributes['actual_range']) == str:
                if WARNING_MESSAGE in merged_attributes['actual_range']:
                    actual_min = variable_values[:].min()
                    actual_max = variable_values[:].max()

                    merged_attributes['actual_range'] = [actual_min, actual_max]

    return merged_attributes


def _check_spatial_variables(variable_ordered_dictionary):
    spatial_list = []
    georeferenced_dict = {}
    warning_list = []
    list_of_domains = []
    named_variable_dict = {}

    for variable in variable_ordered_dictionary:
        named_variable_dict[variable.name] = variable
        condition_y = variable.variable_type == VARIABLE_TYPE_INDICATORS['Y']
        condition_x = variable.variable_type == VARIABLE_TYPE_INDICATORS['X']
        condition_g = variable.variable_type == VARIABLE_TYPE_INDICATORS['G']
        condition_gd = variable.variable_type == VARIABLE_TYPE_INDICATORS['GD']

        if condition_y or condition_x or condition_g or condition_gd:
            if condition_y or condition_x or condition_g:
                spatial_list.append(variable.name)
            elif condition_gd:
                georeferenced_dict[variable.name] = variable

    for variable_name in georeferenced_dict:
        variable = georeferenced_dict[variable_name]
        new_domain_list = []
        for dimension in variable.dimensions:
            if dimension in spatial_list:
                new_domain_list.append(dimension)
        if 'coordinates' in variable.attributes:
            for coordinate in variable.attributes['coordinates'].split(' '):
                if coordinate != '':
                    if coordinate in spatial_list:
                        if coordinate not in new_domain_list:
                            new_domain_list.append(coordinate)
        if 'grid_mapping' in variable.attributes:
            if variable.attributes['grid_mapping'] != '':
                if variable.attributes['grid_mapping'] in spatial_list:
                    if variable.attributes['grid_mapping'] not in new_domain_list:
                        new_domain_list.append(variable.attributes['grid_mapping'])

        if len(new_domain_list) > 0:
            new_domain_list.sort()
            if len(list_of_domains) == 0:
                list_of_domains.append(new_domain_list)
            else:
                if new_domain_list not in list_of_domains:
                    list_of_domains.append(new_domain_list)

    for domain in list_of_domains:
        has_lat = False
        has_lon = False
        has_grid_mapping = False
        has_proj_x = False
        has_proj_y = False

        for variable_name in domain:
            variable = named_variable_dict[variable_name]
            if variable.variable_type == VARIABLE_TYPE_INDICATORS['Y']:
                if 'standard_name' in variable.attributes:
                    if variable.attributes['standard_name'] == 'latitude' or variable.attributes[
                        'standard_name'] == 'grid_latitude':
                        has_lat = True
                    elif variable.attributes['standard_name'] == 'projection_y_coordinate' or variable.attributes[
                        'standard_name'] == 'projection_y_angular_coordinate':
                        has_proj_y = True
                elif 'units' in variable.attributes:
                    if variable.attributes['units'] in UNITS:
                        has_lat = True
                else:
                    has_proj_y = True
            elif variable.variable_type == VARIABLE_TYPE_INDICATORS['X']:
                if 'standard_name' in variable.attributes:
                    if variable.attributes['standard_name'] == 'longitude' or variable.attributes[
                        'standard_name'] == 'grid_longitude':
                        has_lon = True
                    elif variable.attributes['standard_name'] == 'projection_x_coordinate' or variable.attributes[
                        'standard_name'] == 'projection_x_angular_coordinate':
                        has_proj_x = True
                elif 'units' in variable.attributes:
                    if variable.attributes['units'] in UNITS:
                        has_lon = True
                else:
                    has_proj_x = True
            elif variable.variable_type == VARIABLE_TYPE_INDICATORS['G']:
                has_grid_mapping = True

        condition_1 = has_proj_y and has_proj_x
        condition_2 = not has_grid_mapping
        condition_3 = not has_lat and not has_lon
        if condition_1 and condition_2 and condition_3:
            warning_list.append(ADD_GRID_MAPPING_VARIABLE)

    return warning_list


def _determine_global_attributes_for_given_conventions(conventions, current_conventions, group):
    append_convention = True
    if CONVENTION_VERSIONS[0] in conventions and not CONVENTION_VERSIONS[1] in conventions:
        required_attributes = GLOBAL_ATTRIBUTES['CF_GLOBAL_ATTRIBUTES']

        for convention in current_conventions:

            if 'CF' in convention:
                list_index = current_conventions.index(convention)
                current_conventions = current_conventions[:list_index] + [
                    CONVENTION_VERSIONS[0]] + current_conventions[list_index + 1:]
                append_convention = False

        if append_convention:
            current_conventions.append(CONVENTION_VERSIONS[0])

        group.attributes['Conventions'] = ', '.join(current_conventions)

    elif CONVENTION_VERSIONS[1] in conventions and not CONVENTION_VERSIONS[0] in conventions:
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED']['date_created'] = datetime.now().strftime("%m/%d/%Y")
        required_attributes = {**GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_REQUIRED'],
                               **GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED'],
                               **GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_SUGGESTED']}

        for convention in current_conventions:

            if 'ACDD' in convention:
                list_index = current_conventions.index(convention)
                current_conventions = current_conventions[:list_index] + [
                    CONVENTION_VERSIONS[1]] + current_conventions[list_index + 1:]
                append_convention = False

        if append_convention:
            current_conventions.append(CONVENTION_VERSIONS[1])

        group.attributes['Conventions'] = ', '.join(current_conventions)

    else:
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_REQUIRED'].pop('title')
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_REQUIRED'].pop('Conventions')
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED'].pop('source')
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED'].pop('comment')
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED'].pop('institution')
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED']['date_created'] = datetime.now().strftime('%m/%d/%Y')
        GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_SUGGESTED']['date_metadata_modified'] = datetime.now().strftime('%m/%d/%Y')
        required_attributes = {**GLOBAL_ATTRIBUTES['CF_GLOBAL_ATTRIBUTES'],
                               **GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_REQUIRED'],
                               **GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_RECOMMENDED'],
                               **GLOBAL_ATTRIBUTES['ACDD_ATTRIBUTES_SUGGESTED']}

        for convention in current_conventions:
            if 'ACDD' in convention or 'CF' in convention:
                if 'ACDD' in convention:
                    list_index = current_conventions.index(convention)
                    current_conventions = current_conventions[:list_index] + [CONVENTION_VERSIONS[1]] + \
                                          current_conventions[list_index + 1:]
                    append_convention = True
                if 'CF' in convention:
                    list_index = current_conventions.index(convention)
                    current_conventions = current_conventions[:list_index] + [CONVENTION_VERSIONS[0]] + \
                                          current_conventions[list_index + 1:]
                    append_convention = True

        if append_convention:
            for convention in CONVENTION_VERSIONS:
                current_conventions.append(convention)

        group.attributes['Conventions'] = ', '.join(current_conventions)

    return required_attributes
