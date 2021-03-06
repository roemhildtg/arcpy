import arcpy

'''
    gets a field dict with defaults
'''
def get_field(input):
    output = {
        'name': input.get('name'),
        'type': input.get('type', 'TEXT'),
        'alias': input.get('alias', input.get('name')),
        'domain': input.get('domain', None),
        'length': input.get('length', None),
    }

    if not output['length'] and output['type'] == 'TEXT':
        output['length'] = 255

    return output
    


def add_field(table, field):
    field = get_field(field)
    print('Adding field {}<{}:{}> to {}'.format(field['name'], field['type'], field['length'], table))
    # AddField(in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
    arcpy.management.AddField(table, field['name'], field['type'], field_length=field['length'], field_alias=field['alias'], field_domain=field['domain'])

def add_fields(table, fields):
    print('Adding {} fields to {}'.format(len(fields), table))
    for field in fields:
        add_field(table, field)


def add_domain(workspace, name, options):
    print('create {} in {}...'.format(name, workspace))
    arcpy.management.CreateDomain(workspace, name, name, 'TEXT', 'CODED')
    for domain in options:
        print('Adding domain value {}'.format(domain['name']))
        arcpy.management.AddCodedValueToDomain(workspace, name, domain['name'], domain['alias'])

def add_table(workspace, name, fields, feature_class=False, geometry_type='POINT', spatial_reference=4326):
    print('Creating table {}'.format(name))
    if not arcpy.Exists(name):
        if feature_class:
            arcpy.management.CreateFeatureclass(workspace, name, geometry_type=geometry_type, spatial_reference=arcpy.SpatialReference(spatial_reference))
        else:
            arcpy.management.CreateTable(workspace, name)
    else:
        print('Table exists: {}'.format(name))

    field_names = [f.name for f in arcpy.ListFields(name)]

    if not 'globalid' in field_names:
        print('Adding global ids to {}'.format(name))
        arcpy.management.AddGlobalIDs(name)


    # print('Adding unique index to {}'.format(name))
    # arcpy.management.AddIndex(name, ['globalid'], "unique_globalid_{}".format(name), "UNIQUE", "ASCENDING")

    print('Adding fields to {}'.format(name))
    for f in fields:
        if f['name'] in field_names:
            print('Field exists and will not be added: {}'.format(f['name']))
            fields.remove(f)
    add_fields(name, fields)

def update_field(table, field):

    field = get_field(field)

    print('Updating field {}'.format(field['name']))
    # AlterField(in_table, field, {new_field_name}, {new_field_alias}, {field_type}, {field_length}, {field_is_nullable}, {clear_field_alias})
    arcpy.management.AlterField(table, field['name'], new_field_alias=field['alias'], field_type=field['type'], field_length=field['length'])