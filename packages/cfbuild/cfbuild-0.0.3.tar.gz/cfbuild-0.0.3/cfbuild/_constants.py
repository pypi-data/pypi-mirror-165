# MISCELLANEOUS CONSTANTS ############################################################################################

WARNING_MESSAGE = '!!!CHANGE ME!!! - '

STANDARD_NAME_TABLE_LOCATION = 'cf-standard-name-table.xml'

CONVENTION_VERSIONS = ['CF-1.9', 'ACDD-1.3']

CF_FEATURE_TYPES = ['point', 'timeSeries', 'trajectory', 'profile', 'timeSeriesProfile', 'trajectoryProfile']

DATA_TYPES = ['uint8', 'uint16', 'uint32', 'ufloat32', 'ufloat64', 'int8', 'int16',
              'int32', 'float32', 'float64', 'str', 'char', '|S1', '|S2']

CELL_METHODS_VALUES = ['point', 'sum', 'maximum', 'maximum_absolute_value', 'median', 'mid_range', 'minimum',
                       'minimum_absolute_value', 'mean', 'mean_absolute_value', 'mean_of_upper_decile', 'mode',
                       'range', 'root_mean_square', 'standard_deviation', 'sum_of_squares', 'variance']

OPENDAP_RESERVED_KEYWORDS = ['alias', 'array', 'attributes', 'byte', 'dataset', 'error', 'float32', 'float64',
                             'grid', 'int16', 'int32', 'maps', 'sequence', 'string', 'structure', 'uint16', 'uint32',
                             'url', 'code', 'message', 'program_type', 'program']

LIST_OF_VARIABLE_NAMES = ['Time Coordinate', 'Z Coordinate', 'Y Coordinate', 'X Coordinate', 'Coordinate',
                          'Auxiliary Coordinate', 'Scalar Coordinate', 'Grid Mapping Variable', 'Domain Variable',
                          'Boundary Variable', 'Cell Measures Variable', 'Georeferenced Data Variable',
                          'Data Variable', 'Ancillary Data Variable', 'Unknown']

VARIABLE_TYPE_INDICATORS = {
    'C': 'Coordinate',
    'T': 'Time Coordinate',
    'X': 'X Coordinate',
    'Y': 'Y Coordinate',
    'Z': 'Z Coordinate',
    'AC': 'Auxiliary Coordinate',
    'GD': 'Georeferenced Data Variable',
    'D': 'Data Variable',
    'AD': 'Ancillary Data Variable',
    'S': 'Scalar Coordinate',
    'G': 'Grid Mapping Variable',
    'DO': 'Domain Variable',
    'B': 'Boundary Variable',
    'CM': 'Cell Measures Variable',
    'U': 'Unknown'
}

# GLOBAL ATTRIBUTES ##################################################################################################

ACDD_ATTRIBUTES_REQUIRED = {
    'title': WARNING_MESSAGE + 'A succinct description of what is in the dataset',
    'summary': WARNING_MESSAGE + 'A paragraph describing the dataset, analogous to an abstract for a paper',
    'keywords': WARNING_MESSAGE + 'A comma-seperated list of key words and/or phrases',
    'Conventions': 'ACDD'
    }

ACDD_ATTRIBUTES_RECOMMENDED = {
    'id': WARNING_MESSAGE + 'An identifier for the data set, provided by and unique within its naming authority',
    'naming_authority': WARNING_MESSAGE + 'The organization that provides the initial id (see above) for the dataset',
    'history': WARNING_MESSAGE + 'Provides an audit trail for modifications to the original data',
    'source':  WARNING_MESSAGE + 'The method of production of the original data',  # Duplicate with CF
    'processing_level':  WARNING_MESSAGE + 'A textual description of the processing (or quality control)'
                                           ' level of the data',
    'comment':  WARNING_MESSAGE + 'Miscellaneous information about the data, not captured elsewhere',  # Duplicate with CF
    'acknowledgement':  WARNING_MESSAGE + 'TA place to acknowledge various types of support for the project that'
                                          ' produced this data',
    'license':  WARNING_MESSAGE + 'Provide the URL to a standard or specific license, enter \'Freely Distributed\' or '
                                  '\'None\', or describe any restrictions to data access and distribution in free text',
    'standard_name_vocabulary': 'CF Standard Name Table (v79, 19 March 2022)',
    'date_created':  '',  # set to today WARNING_MESSAGE + 'The date on which this version of the data was created',
    'creator_name':  WARNING_MESSAGE + 'The name of the person (or other creator type specified by the creator_type '
                                       'attribute) principally responsible for creating this data',
    'creator_email':  WARNING_MESSAGE + 'The email address of the person (or other creator type specified by the '
                                        'creator_type attribute) principally responsible for creating this data',
    'creator_url':  WARNING_MESSAGE + '	The URL of the person (or other creator type specified by the creator_type '
                                      'attribute) principally responsible for creating this data',
    'institution':  WARNING_MESSAGE + 'The name of the institution principally responsible for originating this data. '
                                      'This attribute is recommended by the CF convention',  # Duplicate with CF
    'project':  WARNING_MESSAGE + 'The name of the project(s) principally responsible for originating this data',
    'publisher_name':  WARNING_MESSAGE + 'The name of the person (or other entity specified by the publisher_type '
                                         'attribute) responsible for publishing the data file or product to users, '
                                         'with its current metadata and format',
    'publisher_email':  WARNING_MESSAGE + 'The email address of the person (or other entity specified by the '
                                          'publisher_type attribute) responsible for publishing the data file or '
                                          'product to users, with its current metadata and format',
    'publisher_url':  WARNING_MESSAGE + 'The URL of the person (or other entity specified by the publisher_type '
                                        'attribute) responsible for publishing the data file or product to users, with '
                                        'its current metadata and format',
    # these attributes only make sence if the file only has one domain
    # 'geospatial_bounds':  WARNING_MESSAGE + 'TDescribes the datas 2D or 3D geospatial extent in OGCs Well-Known Text (WKT) Geometry format (reference the OGC Simple Feature Access (SFA) specification)',
    # 'geospatial_bounds_crs':  WARNING_MESSAGE + 'The coordinate reference system (CRS) of the point coordinates in the geospatial_bounds attribute',
    # 'geospatial_bounds_vertical_crs':  WARNING_MESSAGE + 'The vertical coordinate reference system (CRS) for the Z axis of the point coordinates in the geospatial_bounds attribute',
    # 'geospatial_lat_min':  WARNING_MESSAGE + 'Describes a simple lower latitude limit; may be part of a 2- or 3-dimensional bounding region', # Set from dimensional data????
    # 'geospatial_lat_max':  WARNING_MESSAGE + 'Describes a simple upper latitude limit; may be part of a 2- or 3-dimensional bounding region', # Set from dimensional data????
    # 'geospatial_lon_min':  WARNING_MESSAGE + 'Describes a simple longitude limit; may be part of a 2- or 3-dimensional bounding region', # Set from dimensional data????
    # 'geospatial_lon_max':  WARNING_MESSAGE + 'TDescribes a simple longitude limit; may be part of a 2- or 3-dimensional bounding region', # Set from dimensional data????
    # 'geospatial_vertical_min':  WARNING_MESSAGE + 'Describes the numerically smaller vertical limit; may be part of a 2- or 3-dimensional bounding region',
    # 'geospatial_vertical_max':  WARNING_MESSAGE + 'Describes the numerically larger vertical limit; may be part of a 2- or 3-dimensional bounding region',
    # 'geospatial_vertical_positive':  WARNING_MESSAGE + 'One of \'up\' or \'down\'', # Mirrors CF positive variable attribute
    # 'time_coverage_start':  WARNING_MESSAGE + 'Describes the time of the first data point in the data set', # Set from dimensional data????
    # 'time_coverage_end':  WARNING_MESSAGE + 'Describes the time of the last data point in the data set', # Set from dimensional data????
    # 'time_coverage_duration':  WARNING_MESSAGE + 'Describes the duration of the data set', # Set from dimensional data????
    # 'time_coverage_resolution':  WARNING_MESSAGE + 'Describes the targeted time period between each value in the data set'
    }

ACDD_ATTRIBUTES_SUGGESTED = {
    'creator_type': WARNING_MESSAGE + 'Specifies type of creator with one of the following: "person", "group", '
                                      '"institution", or "position"',  # Defailt: person???
    'creator_institution': WARNING_MESSAGE + 'The institution of the creator; should uniquely identify the creators '
                                             'institution',
    'publisher_type': WARNING_MESSAGE + 'a comma-seperated list of key words and/or phrases',
    'publisher_institution': WARNING_MESSAGE + 'The institution that presented the data file or equivalent product '
                                               'to users',
    'program': WARNING_MESSAGE + 'The overarching program(s) of which the dataset is a part',
    'contributor_name': WARNING_MESSAGE + 'The name of any individuals, projects, or institutions that contributed '
                                          'to the creation of this data',
    'contributor_role': WARNING_MESSAGE + 'The role of any individuals, projects, or institutions that contributed '
                                          'to the creation of this data'
    
    # these attributes only make sence if the file only has one domain
    # 'geospatial_lat_units': WARNING_MESSAGE + 'Units for the latitude axis described in "geospatial_lat_min" and "geospatial_lat_max" attributes',
    # 'geospatial_lat_resolution': WARNING_MESSAGE + 'Information about the targeted spacing of points in latitude',
    # 'geospatial_lon_units': WARNING_MESSAGE + 'Units for the longitude axis described in "geospatial_lon_min" and "geospatial_lon_max" attributes',
    # 'geospatial_lon_resolution': WARNING_MESSAGE + 'Information about the targeted spacing of points in longitude',
    # 'geospatial_vertical_units': WARNING_MESSAGE + 'Units for the vertical axis described in "geospatial_vertical_min" and "geospatial_vertical_max" attributes',
    # 'geospatial_vertical_resolution': WARNING_MESSAGE + 'Information about the targeted vertical spacing of points',
    # ---------------------------------------------------------------
    # 'date_modified': WARNING_MESSAGE + 'The date on which the data was last modified. Note that this applies just to the data, not the metadata',
    # 'date_issued': WARNING_MESSAGE + 'The date on which this data (including all modifications) was formally issued (i.e., made available to a wider audience)',
    # 'date_metadata_modified': '', # set as today WARNING_MESSAGE + 'The date on which the metadata was last modified', 
    # 'product_version': WARNING_MESSAGE + 'Version identifier of the data file or product as assigned by the data creator',
    # 'keywords_vocabulary': WARNING_MESSAGE + 'If you are using a controlled vocabulary for the words/phrases in your "keywords" attribute, this is the unique name or identifier of the vocabulary from which keywords are taken',
    # 'platform': WARNING_MESSAGE + 'Name of the platform(s) that supported the sensor data used to create this data set or product',
    # 'platform_vocabulary': WARNING_MESSAGE + 'Controlled vocabulary for the names used in the "platform" attribute',
    # 'instrument': WARNING_MESSAGE + 'Name of the contributing instrument(s) or sensor(s) used to create this data set or product',
    # 'instrument_vocabulary': WARNING_MESSAGE + 'Controlled vocabulary for the names used in the "instrument" attribute',
    # 'cdm_data_type': '', # set to specific type WARNING_MESSAGE + 'The data type, as derived from Unidatas Common Data Model Scientific Data types and understood by THREDDS',
    # 'metadata_link': WARNING_MESSAGE + 'A URL that gives the location of more complete metadata',
    # 'references': WARNING_MESSAGE + 'Published or web-based references that describe the data or methods used to produce it' #Duplicate with CF
    }

ACDD_VARIABLE_ATTRIBUTES = {
    'coverage_content_type': 'An ISO 19115-1 code to indicate the source of the data (image, thematicClassification, '
                             'physicalMeasurement, auxiliaryInformation, qualityInformation, referenceInformation, '
                             'modelResult, or coordinate)'
    }

CF_GLOBAL_ATTRIBUTES = {
    'title': WARNING_MESSAGE + 'a succinct description of what is in the dataset',
    'institution': WARNING_MESSAGE + 'specifies where the original data was produced',
    'source': WARNING_MESSAGE + 'the method of production of the original data',
    'history': WARNING_MESSAGE + 'documentation of any modifications to the original data',
    'references': WARNING_MESSAGE + 'published or web based sorces that document the data or how it was produced',
    'comment': WARNING_MESSAGE + 'miscellaneous information about the data or methods used to produce it',
    'external_variables': WARNING_MESSAGE + 'variables which are named in the attributes of the file but are not '
                                            'contained in the file',
    'featureType': WARNING_MESSAGE + 'Specifies the type of data in the file/group. Set as \'point\', \'timeSeries\','
                                     ' \'trajectory\', \'profile\', \'featureType\', \'timeSeriesProfile\', or '
                                     '\'trajectoryProfile\'',
    'Conventions': 'CF-1.8, ACDD-1.3'
    }

CF_GROUP_ATTRIBUTES = {
    'title': WARNING_MESSAGE + 'a succinct description of what is in the dataset',
    'history': WARNING_MESSAGE + 'documentation of any modifications to the original data'
    }

GLOBAL_ATTRIBUTES = {
    'ACDD_ATTRIBUTES_REQUIRED': ACDD_ATTRIBUTES_REQUIRED,
    'ACDD_ATTRIBUTES_RECOMMENDED': ACDD_ATTRIBUTES_RECOMMENDED,
    'ACDD_ATTRIBUTES_SUGGESTED': ACDD_ATTRIBUTES_SUGGESTED,
    'ACDD_VARIABLE_ATTRIBUTES': ACDD_VARIABLE_ATTRIBUTES,
    'CF_GLOBAL_ATTRIBUTES': CF_GLOBAL_ATTRIBUTES,
    'CF_GROUP_ATTRIBUTES': CF_GROUP_ATTRIBUTES,
}

# VARIABLE ATTRIBUTES #################################################################################################

CF_ALL_COORDINATE_VARIABLE_ATTRIBUTES = {
    'long_name': WARNING_MESSAGE + 'A descriptive name that indicates a variable\'s content',
    'units': WARNING_MESSAGE + 'Units of a variables content',
    'comment': WARNING_MESSAGE + 'Miscellaneous information about the data or methods used to produce it',
    'valid_range': WARNING_MESSAGE + 'Smallest and largest valid values of a variable',
    'actual_range': WARNING_MESSAGE + 'The smallest and the largest valid nonmissing values occurring in the variable',
    '_FillValue': WARNING_MESSAGE + 'A value used to represent missing or undefined data. Allowed for auxiliary '
                                    'coordinate variables but not allowed for coordinate variables',
    
    # a COORDINATE_VARIABLE:
    # 'cf_role': ['timeseries_id', 'profile_id', 'trajectory_id'], # 'Identifies the roles of variables that identify features in discrete sampling geometries',
    # 'climatology': WARNING_MESSAGE + 'Identifies a climatology variable',
    # 'bounds': WARNING_MESSAGE + 'Identifies a boundary variable',
    # 'compress': WARNING_MESSAGE + 'Records dimensions which have been compressed by gathering',
    # 'computed_standard_name': WARNING_MESSAGE + 'Indicates the standard name, from the standard name table, of the computed vertical coordinate values, computed according to the formula in the definition',
    # 'formula_terms': WARNING_MESSAGE + 'Identifies variables that correspond to the terms in a formula',
    # 'add_offset': WARNING_MESSAGE + 'If present for a variable, this number is to be added to the data after it is read by an application. If both scale_factor and add_offset attributes are present, the data are first scaled before the offset is added. In cases where there is a strong constraint on dataset size, it is allowed to pack the coordinate variables (using add_offset and/or scale_factor), but this is not recommended in general', # not for all variables
    # 'geometry': WARNING_MESSAGE + 'Identifies a variable that defines geometry',
    # 'nodes': WARNING_MESSAGE + 'Identifies a coordinate node variable',
    
    }

CF_T_COORDINATE_VARIABLE_ATTRIBUTES = {
    'standard_name': 'time',
    'axis': 'T',
    'calendar': 'standard'
    # ADD THESE ATTRIBUTES BASED ON THE CALENDER SCHEDULE
    # 'leap_month': WARNING_MESSAGE + 'Specifies which month is lengthened by a day in leap years for a user defined calendar',
    # 'leap_year': WARNING_MESSAGE + 'Provides an example of a leap year for a user defined calendar. It is assumed that all years that differ from this year by a multiple of four are also leap years',
    # 'month_lengths': WARNING_MESSAGE + 'Specifies the length of each month in a non-leap year for a user defined calendar'
    }

CF_X_COORDINATE_VARIABLE_ATTRIBUTES = {
    'standard_name': 'longitude',
    'axis': 'X'
    }

CF_Y_COORDINATE_VARIABLE_ATTRIBUTES = {
    'standard_name': 'latitude',
    'axis': 'Y'
    }

CF_Z_COORDINATE_VARIABLE_ATTRIBUTES = {
    'standard_name': 'height',
    'axis': 'Z',
    'positive': 'up'
    }

CF_AUXILIARY_COORDINATE_VARIABLE_ATTRIBUTES = {
    '_FillValue': WARNING_MESSAGE + 'A value used to represent missing or undefined data. Allowed for auxiliary '
                                    'coordinate variables but not allowed for coordinate variables',
    'missing_value': WARNING_MESSAGE + 'A value or values used to represent missing or undefined data. Allowed for '
                                       'auxiliary coordinate variables but not allowed for coordinate variables.'
    # 'scale_factor': WARNING_MESSAGE + 'If present for a variable, the data are to be multiplied by this factor after the data are read by an application. See also the add_offset attribute. In cases where there is a strong constraint on dataset size, it is allowed to pack the coordinate variables (using add_offset and/or scale_factor), but this is not recommended in general',
    }

CF_DATA_VARIABLE_ATTRIBUTES = {
    'long_name': WARNING_MESSAGE + 'A descriptive name that indicates a variable\'s content',
    'standard_name': WARNING_MESSAGE + 'A standard name that references a description of a variable\'s content in the '
                                       'standard name table',  # Standardized
    'units': WARNING_MESSAGE + 'Units of a variables content',
    'institution': WARNING_MESSAGE + 'Where the original data was produced',
    'references': WARNING_MESSAGE + 'References that describe the data or methods used to produce it',
    'source': WARNING_MESSAGE + 'Method of production of the original data',
    'valid_range': WARNING_MESSAGE + 'Smallest and largest valid values of a variable',
    'actual_range': WARNING_MESSAGE + 'The smallest and the largest valid nonmissing values occurring in the variable',
    '_FillValue': WARNING_MESSAGE + 'The fill value for the data array',
    'missing_value': WARNING_MESSAGE + 'A value or values used to represent missing or undefined data. Allowed for '
                                       'auxiliary coordinate variables but not allowed for coordinate variables.'

    # 'cell_methods': WARNING_MESSAGE + 'Records the method used to derive data that represents cell values',
    # 'cell_measures': WARNING_MESSAGE + 'Identifies variables that contain cell areas or volumes',
    # 'add_offset': WARNING_MESSAGE + 'If present for a variable, this number is to be added to the data after it is read by an application. If both scale_factor and add_offset attributes are present, the data are first scaled before the offset is added. In cases where there is a strong constraint on dataset size, it is allowed to pack the coordinate variables (using add_offset and/or scale_factor), but this is not recommended in general', # not for all variables
    # 'scale_factor': WARNING_MESSAGE + 'If present for a variable, the data are to be multiplied by this factor after the data are read by an application. See also the add_offset attribute. In cases where there is a strong constraint on dataset size, it is allowed to pack the coordinate variables (using add_offset and/or scale_factor), but this is not recommended in general',# not for all variables
    # 'ancillary_variables': WARNING_MESSAGE + 'Identifies a variable that contains closely associated data, e.g., the measurement uncertainties of instrument data',
    # 'standard_error_multiplier': WARNING_MESSAGE + 'If a data variable with a standard_name modifier of standard_error has this attribute, it indicates that the values are the stated multiple of one standard error',
    
    # 'geometry': WARNING_MESSAGE + 'Identifies a variable that defines geometry',
    # 'grid_mapping': WARNING_MESSAGE + 'Identifies a variable that defines a grid mapping',
    # 'coordinate_interpolation': WARNING_MESSAGE + 'Indicates that coordinates have been compressed by sampling and identifies the tie point coordinate variables and their associated interpolation variables',
    # 'coordinates': WARNING_MESSAGE + 'Identifies auxiliary coordinate variables, label variables, and alternate coordinate variables',

    # 'flag_masks': WARNING_MESSAGE + 'Provides a list of bit fields expressing Boolean or enumerated flags',
    # 'flag_meanings': WARNING_MESSAGE + 'Use in conjunction with flag_values to provide descriptive words or phrases for each flag value. If multi-word phrases are used to describe the flag values, then the words within a phrase should be connected with underscores',
    # 'flag_values': WARNING_MESSAGE + 'Provides a list of the flag values. Use in conjunction with flag_meanings',
    }

CF_GEODATA_VARIABLE_ATTRIBUTES = CF_DATA_VARIABLE_ATTRIBUTES

ANCILLARY_VARIABLE_ATTRIBUTE = CF_DATA_VARIABLE_ATTRIBUTES

SCALAR_VARIABLE_ATTRIBUTES = {}

CF_DOMAIN_VARIABLE_ATTRIBUTES = {
    'long_name': WARNING_MESSAGE + 'A descriptive name that indicates a variable\'s content',
    'geometry': WARNING_MESSAGE + 'Identifies a variable that defines geometry',
    'cell_measures': WARNING_MESSAGE + 'Identifies variables that contain cell areas or volumes',
    'coordinate_interpolation': WARNING_MESSAGE + 'Indicates that coordinates have been compressed by sampling and '
                                                  'identifies the tie point coordinate variables and their associated '
                                                  'interpolation variables',
    'coordinates': WARNING_MESSAGE + 'Identifies auxiliary coordinate variables, label variables, and alternate '
                                     'coordinate variables',
    'grid_mapping': WARNING_MESSAGE + 'Identifies a variable that defines a grid mapping',
    'dimensions': WARNING_MESSAGE + 'Identifies the dimensions that define a domain variable'
    }

CF_GEOMETRY_CONTAINER_VARIABLE_ATTRIBUTES = {
    'geometry_type': WARNING_MESSAGE + 'Indicates the type of geometry present',
    'coordinates': WARNING_MESSAGE + 'Identifies auxiliary coordinate variables, label variables, and alternate '
                                     'coordinate variables',
    'grid_mapping': WARNING_MESSAGE + 'Identifies a variable that defines a grid mapping',
    'interior_ring': WARNING_MESSAGE + 'Identifies a variable that indicates if polygon parts are interior rings '
                                       '(i.e., holes) or not',
    'node_coordinates': WARNING_MESSAGE + 'Identifies variables that contain geometry node coordinates',
    'node_count': WARNING_MESSAGE + 'Identifies a variable indicating the count of nodes per geometry',
    'part_node_count': WARNING_MESSAGE + 'Identifies a variable providing the count of nodes per geometry part',
    }

BOUNDARY_VARIABLE_ATTRIBUTES = {}

CELL_METHODS_VARIABLE_ATTRIBUTE = {}

UNDEFINED_VARIABLE_ATTRIBUTE = {}

CF_OTHER_ATTRIBUTES = {
    'instance_dimension': WARNING_MESSAGE + 'An attribute which identifies an index variable and names the instance '
                                            'dimension to which it applies. The index variable indicates that the '
                                            'indexed ragged array representation is being used for a collection of '
                                            'features.',
    'sample_dimension': WARNING_MESSAGE + 'An attribute which identifies a count variable and names the sample '
                                          'dimension to which it applies. The count variable indicates that the '
                                          'contiguous ragged array representation is being used for a collection '
                                          'of features.',
    }

CF_DATA_TYPE_ATTRIBUTES = {
    VARIABLE_TYPE_INDICATORS['C']: CF_ALL_COORDINATE_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['T']: CF_T_COORDINATE_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['X']: CF_X_COORDINATE_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['Y']: CF_Y_COORDINATE_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['Z']: CF_Z_COORDINATE_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['AC']: CF_AUXILIARY_COORDINATE_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['GD']: CF_GEODATA_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['D']: CF_DATA_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['AD']: ANCILLARY_VARIABLE_ATTRIBUTE,
    VARIABLE_TYPE_INDICATORS['S']: SCALAR_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['G']: CF_GEOMETRY_CONTAINER_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['DO']: CF_DOMAIN_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['B']: BOUNDARY_VARIABLE_ATTRIBUTES,
    VARIABLE_TYPE_INDICATORS['CM']: CELL_METHODS_VARIABLE_ATTRIBUTE,
    VARIABLE_TYPE_INDICATORS['U']: UNDEFINED_VARIABLE_ATTRIBUTE
}

# SPECIFIED UNITS AND STANDARD NAMES ##################################################################################

UNITS = {
    'degrees_north': VARIABLE_TYPE_INDICATORS['Y'],
    'degree_north': VARIABLE_TYPE_INDICATORS['Y'],
    'degree_N': VARIABLE_TYPE_INDICATORS['Y'],
    'degrees_N': VARIABLE_TYPE_INDICATORS['Y'],
    'degreeN': VARIABLE_TYPE_INDICATORS['Y'],
    'degreesN': VARIABLE_TYPE_INDICATORS['Y'],
    'degrees_east': VARIABLE_TYPE_INDICATORS['X'],
    'degree_east': VARIABLE_TYPE_INDICATORS['X'],
    'degree_E': VARIABLE_TYPE_INDICATORS['X'],
    'degrees_E': VARIABLE_TYPE_INDICATORS['X'],
    'degreeE': VARIABLE_TYPE_INDICATORS['X'],
    'degreesE': VARIABLE_TYPE_INDICATORS['X']
    }

STANDARD_NAMES = {
    'grid_latitude': VARIABLE_TYPE_INDICATORS['Y'],
    'latitude': VARIABLE_TYPE_INDICATORS['Y'],
    'projection_y_angular_coordinate': VARIABLE_TYPE_INDICATORS['Y'],
    'projection_y_coordinate': VARIABLE_TYPE_INDICATORS['Y'],
    'grid_longitude': VARIABLE_TYPE_INDICATORS['X'],
    'longitude': VARIABLE_TYPE_INDICATORS['X'],
    'projection_x_angular_coordinate': VARIABLE_TYPE_INDICATORS['X'],
    'projection_x_coordinate': VARIABLE_TYPE_INDICATORS['X'],
    'altitude': VARIABLE_TYPE_INDICATORS['Z'],
    'height': VARIABLE_TYPE_INDICATORS['Z'],
    'time': VARIABLE_TYPE_INDICATORS['T']
    }

# GRID MAPPING VARIABLE #############################################################################################

GRID_MAPPING_NAMES = {
    'albers_conical_equal_area': {
        'map_parameters': ['standard_parallel', 'longitude_of_central_meridian', 'latitude_of_projection_origin',
                           {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'azimuthal_equidistant': {
        'map_parameters': ['longitude_of_projection_origin', 'latitude_of_projection_origin', {'false_easting': 0},
                           {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'geostationary': {
        'map_parameters': ['longitude_of_central_meridian', 'latitude_of_projection_origin', 'perspective_point_height',
                           {'sweep_angle_axis': ['x', 'y']}, {'fixed_angle_axis': ['x', 'y']}, {'false_easting': 0},
                           {'false_northing': 0}],
        'map_coordinates': ['pprojection_x_angular_coordinate', 'projection_y_angular_coordinate']},
    'lambert_azimuthal_equal_area': {
        'map_parameters': ['longitude_of_projection_origin', 'latitude_of_projection_origin', {'false_easting': 0},
                           {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'lambert_conformal_conic': {
        'map_parameters': ['standard_parallel', 'longitude_of_central_meridian', 'latitude_of_projection_origin',
                           {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'lambert_cylindrical_equal_area': {
        'map_parameters': ['longitude_of_central_meridian', 'standard_parallel', {'false_easting': 0},
                           {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'latitude_longitude': {
        'map_parameters': None,
        'map_coordinates': ['longitude', 'latitude']},
    'mercator': {
        'map_parameters': ['longitude_of_projection_origin', ['standard_parallel', 'scale_factor_at_projection_origin'],
                           {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'oblique_mercator': {
        'map_parameters': ['azimuth_of_central_line', 'latitude_of_projection_origin', 'longitude_of_projection_origin',
                           'scale_factor_at_projection_origin', {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'orthographic': {
        'map_parameters': ['longitude_of_projection_origin', 'latitude_of_projection_origin', {'false_easting': 0},
                           {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'polar_stereographic': {
        'map_parameters': ['straight_vertical_longitude_from_pole', {'latitude_of_projection_origin': [90, -90]},
                           ['standard_parallel', 'scale_factor_at_projection_origin'], {'false_easting': 0},
                           {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'rotated_latitude_longitude': {
        'map_parameters': ['grid_north_pole_latitude', 'grid_north_pole_longitude', {'north_pole_grid_longitude': 0}],
        'map_coordinates': ['grid_latitude', 'grid_longitude']},
    'sinusoidal': {
        'map_parameters': ['longitude_of_projection_origin', {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'stereographic': {
        'map_parameters': ['longitude_of_projection_origin', 'latitude_of_projection_origin',
                           'scale_factor_at_projection_origin', {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'transverse_mercator': {
        'map_parameters': ['scale_factor_at_central_meridian', 'longitude_of_central_meridian',
                           'latitude_of_projection_origin', {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']},
    'vertical_perspective': {
        'map_parameters': ['latitude_of_projection_origin', 'longitude_of_projection_origin',
                           'perspective_point_height', {'false_easting': 0}, {'false_northing': 0}],
        'map_coordinates': ['projection_x_coordinate', 'projection_y_coordinate']}
    }

GRID_MAPPING_OPTIONAL_ATTRIBUTES = ['crs_wkt', 'earth_radius', 'geographic_crs_name', 'geoid_name',
                                    'geopotential_datum_name', 'horizontal_datum_name', 'prime_meridian_name',
                                    'projected_crs_name', 'towgs84']

ELLIPSOID_AND_PRIME_MERIDIAN = ['earth_redius', 'inverse_flattening', 'longitude_of_prime_meridian',
                                'reference_ellipsoid_name', 'semi_major_axis', 'semi_minor_axis']
