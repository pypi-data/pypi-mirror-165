import csv
import os.path

from opencmiss.utils.zinc.field import create_field_finite_element, find_or_create_field_stored_string, find_or_create_field_group
from opencmiss.zinc.context import Context
from opencmiss.zinc.field import Field
from opencmiss.zinc.status import OK as ZINC_OK

from opencmiss.importer.base import valid
from opencmiss.importer.errors import OpenCMISSImportInvalidInputs, OpenCMISSImportUnknownParameter, OpenCMISSImportColonManometryError
from opencmiss.utils.zinc.general import ChangeManager


def import_data_into_region(region, inputs):
    if type(inputs) == list and len(inputs) == 1:
        inputs = inputs[0]

    if not valid(inputs, parameters("input")):
        raise OpenCMISSImportInvalidInputs(f"Invalid input given to importer: {identifier()}")

    manometry_data = inputs
    field_module = region.getFieldmodule()

    with ChangeManager(field_module):
        with open(manometry_data) as f:
            csv_reader = csv.reader(f)
            first_row = True
            try:
                for row in csv_reader:
                    heading = row.pop(0)
                    if first_row and heading != 'Time':
                        raise OpenCMISSImportColonManometryError("Colon manometry file is not valid.")

                    if heading == 'Time':
                        first_row = False
                        times = [float(t) for t in row]
                    else:
                        values = row[:]
                        _create_node(field_module, heading, times, values)
            except UnicodeDecodeError:
                raise OpenCMISSImportColonManometryError("Colon manometry file is not valid.")
            except ValueError:
                raise OpenCMISSImportColonManometryError("Colon manometry file is not valid.")


def import_data(inputs, output_directory):
    output = None

    context = Context("Manometry")
    region = context.getDefaultRegion()

    import_data_into_region(region, inputs)

    # Inputs has already been validated by this point so it is safe to use.
    filename_parts = os.path.splitext(os.path.basename(inputs))
    output_exf = os.path.join(output_directory, filename_parts[0] + ".exf")
    result = region.writeFile(output_exf)
    if result == ZINC_OK:
        output = output_exf

    return output


def _create_node(field_module, name, times, values):
    pressure_field = field_module.findFieldByName("pressure")
    if not pressure_field.isValid():
        pressure_field = create_field_finite_element(field_module, "pressure", 1, type_coordinate=False)
    name_field = find_or_create_field_stored_string(field_module, "marker_name")
    data_points = field_module.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_DATAPOINTS)

    group_field = find_or_create_field_group(field_module, "marker")
    node_group_field = group_field.getFieldNodeGroup(data_points)
    if not node_group_field.isValid():
        node_group_field = group_field.createFieldNodeGroup(data_points)

    data_template = data_points.createNodetemplate()
    data_template.defineField(pressure_field)
    data_template.defineField(name_field)

    time_sequence = field_module.getMatchingTimesequence(times)

    data_template.setTimesequence(pressure_field, time_sequence)

    field_cache = field_module.createFieldcache()
    node = data_points.createNode(-1, data_template)

    nodeset_group = node_group_field.getNodesetGroup()
    nodeset_group.addNode(node)
    field_cache.setNode(node)
    name_field.assignString(field_cache, name)
    for index, value in enumerate(values):
        current_time = float(times[index])
        field_cache.setTime(current_time)
        pressure_field.assignReal(field_cache, float(value))


def identifier():
    return "ColonManometry"


def parameters(parameter_name=None):
    importer_parameters = {
        "version": "0.1.0",
        "id": identifier(),
        "title": "Colon manometry",
        "description":
            "Colon manometry importer is for data listed in a comma separated values file."
            " The first row is time, and subsequent rows are sensor location and the associated values.",
        "input": {
            "mimetype": "text/csv",
        },
        "output": {
            "mimetype": "text/x.vnd.abi.exf+plain",
        }
    }

    if parameter_name is not None:
        if parameter_name in importer_parameters:
            return importer_parameters[parameter_name]
        else:
            raise OpenCMISSImportUnknownParameter(f"Importer '{identifier()}' does not have parameter: {parameter_name}")

    return importer_parameters
