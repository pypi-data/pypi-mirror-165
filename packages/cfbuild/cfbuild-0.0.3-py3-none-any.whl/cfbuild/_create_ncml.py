from lxml import etree
from datetime import datetime

from ._constants import GLOBAL_ATTRIBUTES
from ._constants import DATA_TYPES, CONVENTION_VERSIONS, CF_DATA_TYPE_ATTRIBUTES, VARIABLE_TYPE_INDICATORS
from ._variable_identification import sort_and_merge_attribute_lists, sort_variables
from ._attribute_values import _check_attribute_values, _check_spatial_variables, _determine_global_attributes_for_given_conventions, _check_variable
from ._ncml_comments import GLOBAL_ATTRIBUTES, DIMENSIONS, DATA_TYPE_WARNING, VARIABLE_COMMENTS


def create_ncml(ds):
    def add_attribute(element, name, value, last_attribute, indent_level: int = 1):
        attribute_element = etree.SubElement(element, 'attribute', name=str(name), value=str(value))
        if last_attribute:
            attribute_element.tail = '\n\n' + '\t' * indent_level
        else:
            attribute_element.tail = '\n' + '\t' * indent_level

    def add_group_attributes(group, group_element, required_attributes, indent_level):
        merged_attributes = sort_and_merge_attribute_lists(required_attributes, group.attributes)

        for index, attribute in enumerate(merged_attributes):
            name = attribute
            value = merged_attributes[attribute]

            if index + 1 < len(merged_attributes):
                last_attribute = False
            else:
                last_attribute = True

            add_attribute(group_element, name, value, last_attribute, indent_level)

    def _determine_variable_attributes(variable, variable_element, indent_level):
        variable_type = variable.variable_type

        required_attributes = {}

        if variable_type == VARIABLE_TYPE_INDICATORS['C'] or variable_type == VARIABLE_TYPE_INDICATORS['T'] or\
                variable_type == VARIABLE_TYPE_INDICATORS['X'] or variable_type == VARIABLE_TYPE_INDICATORS['Y'] or\
                variable_type == VARIABLE_TYPE_INDICATORS['Z']:
            required_attributes = sort_and_merge_attribute_lists(required_attributes,
                                                                 CF_DATA_TYPE_ATTRIBUTES[VARIABLE_TYPE_INDICATORS['C']])

        required_attributes = sort_and_merge_attribute_lists(required_attributes, CF_DATA_TYPE_ATTRIBUTES[variable_type])

        current_variable_attributes = {}
        for attribute in variable.attributes:
            current_variable_attributes[attribute] = variable.attributes[attribute]

        merged_attributes = sort_and_merge_attribute_lists(required_attributes, current_variable_attributes)

        try:
            variable_values = ds.dataset.variables[variable.name][:]
        except Exception as e:
            variable_values = None
            print(e)

        merged_attributes = _check_attribute_values(merged_attributes, variable, ds.standard_name_table, variable_values)

        for index, attribute in enumerate(merged_attributes):
            reduce_indent = False
            if index + 1 >= len(merged_attributes):
                if isinstance(merged_attributes[attribute], dict):
                    reduce_indent = True
                else:
                    indent_level -= 1
                    reduce_indent = False

            if isinstance(merged_attributes[attribute], dict):
                xml_comment = etree.Comment(merged_attributes[attribute]['comment'])
                xml_comment.tail = '\n' + '\t' * indent_level
                variable_element.append(xml_comment)

                if reduce_indent:
                    indent_level -= 1

                name = attribute
                value = merged_attributes[attribute]['value']
                add_attribute(variable_element, name, value, False, indent_level)
            else:
                name = attribute
                value = merged_attributes[attribute]
                add_attribute(variable_element, name, value, False, indent_level)

    def iterate_group(group, group_element, top_level: bool = False, conventions: list = CONVENTION_VERSIONS,
                      indent_level: int = 0):
        if top_level:
            if 'Conventions' in group.attributes:
                if ',' in group.attributes['Conventions']:
                    current_conventions = group.attributes['Conventions'].split(',')
                else:
                    current_conventions = group.attributes['Conventions'].split(' ')
            else:
                current_conventions = []

            required_attributes = _determine_global_attributes_for_given_conventions(conventions, current_conventions, group)
        else:
            required_attributes = {GLOBAL_ATTRIBUTES['CF_GROUP_ATTRIBUTES']}

        add_group_attributes(group, group_element, required_attributes, indent_level)

        xml_comment = etree.Comment(DIMENSIONS)
        xml_comment.tail = '\n' + '\t' * indent_level
        group_element.append(xml_comment)

        for index, dimension in enumerate(group.dimensions):
            dimension_element = etree.SubElement(group_element, 'dimension', name=dimension.name,
                                                 length=str(dimension.length))
            if index + 1 < len(group.dimensions):
                dimension_element.tail = '\n' + '\t' * indent_level
            else:
                dimension_element.tail = '\n\n' + '\t' * indent_level
                xml_comment = etree.Comment(VARIABLE_COMMENTS[VARIABLE_TYPE_INDICATORS['T']])
                xml_comment.tail = '\n\t'
                group_element.append(xml_comment)

        variable_ordered_dictionary = sort_variables(group.variables)
        warning_list = _check_spatial_variables(variable_ordered_dictionary)

        for warning in warning_list:
            xml_comment = etree.Comment(warning)
            xml_comment.tail = '\n' + '\t' * (indent_level + 1)
            group_element.append(xml_comment)

        for index, variable in enumerate(variable_ordered_dictionary):

            warning_list = _check_variable(variable)

            for warning in warning_list:
                xml_comment = etree.Comment(warning)
                xml_comment.tail = '\n' + '\t' * (indent_level + 1)
                group_element.append(xml_comment)

            if str(variable.data_type) not in DATA_TYPES:
                xml_comment = etree.Comment(DATA_TYPE_WARNING[0] + variable.data_type + DATA_TYPE_WARNING[1])
                xml_comment.tail = '\n' + '\t' * (indent_level + 1)
                group_element.append(xml_comment)

            variable_element = etree.SubElement(group_element, 'variable', name=str(variable.name),
                                                type=str(variable.data_type),
                                                shape=str(variable.dimensions),
                                                variable_type=str(variable.variable_type))
            variable_element.text = '\n' + '\t' * (indent_level + 1)

            if index + 1 < len(variable_ordered_dictionary):
                if variable_ordered_dictionary[index + 1].variable_type != variable.variable_type:
                    variable_element.tail = '\n\n' + '\t' * indent_level
                    variable_comment = VARIABLE_COMMENTS[variable_ordered_dictionary[index + 1].variable_type]

                    xml_comment = etree.Comment(variable_comment)
                    xml_comment.tail = '\n\t'
                    group_element.append(xml_comment)

                else:
                    variable_element.tail = '\n' + '\t' * indent_level
            else:
                variable_element.tail = '\n'

            _determine_variable_attributes(variable, variable_element, indent_level + 1)

        if len(group.groups) > 0:
            for group in ds.groups:
                group_element = etree.SubElement(root, group.name)
                iterate_group(group, group_element, False, conventions, indent_level + 1)

    root = etree.Element('netcdf', xmlns='http://www.unidata.ucar.edu/namespaces/netcdf/ncml-2.2',
                         location=ds.read_filepath)
    root.text = '\n\t'

    comment = etree.Comment(GLOBAL_ATTRIBUTES)
    comment.tail = '\n\t'
    root.append(comment)

    iterate_group(ds, root, True, ds.conventions, 1)

    tree = etree.ElementTree(root)
    return tree
