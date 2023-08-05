import numpy
import json

from lxml import etree


def create_or_update_nc_file(ncml_object, final_netcdf4_dataset, original_dataset):
    def validate_json(json_data):
        try:
            json.loads(json_data)
        except ValueError:
            return False
        return True

    def parse_attribute_value(element):
        if validate_json(element.attrib['value']):
            if element.attrib['value'][0] == '[' and element.attrib['value'][-1] == ']':
                value_list = json.loads(element.attrib['value'])
                value = numpy.array(value_list)
            else:
                value = json.loads(element.attrib['value'])
        else:
            value = element.attrib['value']
        return value

    def get_attributes(xml_group):
        attribute_dictionary = {}

        for element in xml_group:
            if element.tag is not etree.Comment:
                if element.tag.split('}')[-1] == 'attribute':
                    value = parse_attribute_value(element)
                    attribute_dictionary[element.attrib['name']] = value

        return attribute_dictionary

    def add_attributes(xml_group, netcdf_element):
        attribute_dictionary = {}

        for element in xml_group:
            if element.tag is not etree.Comment:
                if element.tag.split('}')[-1] == 'attribute':
                    if element.attrib['name'] not in netcdf_element.ncattrs():
                        value = parse_attribute_value(element)
                        attribute_dictionary[element.attrib['name']] = value

        netcdf_element.setncatts(attribute_dictionary)
        return attribute_dictionary

    def iterate_group(xml_element, final_netcdf4_dataset_group, ncbuild_dataset_group, original_dataset_group):
        variable_dictionary = {}
        for ncbuild_variable in ncbuild_dataset_group.variables:
            variable_dictionary[ncbuild_variable.name] = ncbuild_variable

        for element in xml_element:

            if element.tag is not etree.Comment:
                if element.tag.split('}')[-1] == 'dimension':
                    if element.attrib['length'] == 'None' or element.attrib['length'] == 'unlimited':
                        dimension_size = None
                    elif element.attrib['length'].isdigit():
                        dimension_size = int(element.attrib['length'])
                    else:
                        print('error')
                        dimension_size = None

                    if element.attrib['name'] not in final_netcdf4_dataset_group.dimensions:
                        final_netcdf4_dataset_group.createDimension(dimname=element.attrib['name'], size=dimension_size)

                elif element.tag.split('}')[-1] == 'variable':
                    try:
                        variable_values = original_dataset_group.variables[element.attrib['name']][:]
                    except Exception as e:
                        print(e)

                    if element.attrib['name'] in final_netcdf4_dataset_group.variables:
                        attributes = add_attributes(element,
                                                    final_netcdf4_dataset_group.variables[element.attrib['name']])
                    else:
                        attributes = get_attributes(element)

                        if isinstance(variable_values, numpy.ndarray):
                            if '_FillValue' in attributes:
                                if isinstance(attributes['_FillValue'], str) or \
                                        isinstance(attributes['_FillValue'], bytes) or \
                                        isinstance(attributes['_FillValue'], bytearray):
                                    if validate_json(attributes['_FillValue']):
                                        fill_value = json.loads(attributes['_FillValue'])
                                    else:
                                        fill_value = attributes['_FillValue']
                                else:
                                    fill_value = attributes['_FillValue']
                            else:
                                fill_value = variable_values.fill_value

                            new_variable = final_netcdf4_dataset_group.createVariable(varname=element.attrib['name'],
                                                                                      datatype=element.attrib['type'],
                                                                                      dimensions=eval(
                                                                                          element.attrib['shape']),
                                                                                      fill_value=fill_value)

                            add_attributes(element, new_variable)

                            if element.attrib['type'] != str(variable_dictionary[element.attrib['name']].data_type):
                                new_variable[:] = variable_dictionary[element.attrib['name']]. \
                                    values.astype(str(element.attrib['type']))
                            else:
                                new_variable[:] = variable_values
                            # add_attributes(element, new_variable)

                elif element.tag.split('}')[-1] == 'group':
                    new_group = final_netcdf4_dataset_group.createGroup(groupname=element.attrib['name'])
                    iterate_group(element, new_group, original_dataset_group.groups[element.attrib['name']])

    tree = etree.parse(ncml_object.ncml_filepath)
    root = tree.getroot()
    ncbuild_dataset = ncml_object.dataset
    add_attributes(root, final_netcdf4_dataset)
    iterate_group(root, final_netcdf4_dataset, ncbuild_dataset, original_dataset)
