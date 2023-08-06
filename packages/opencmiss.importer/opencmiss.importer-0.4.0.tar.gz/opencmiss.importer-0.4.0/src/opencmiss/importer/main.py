import argparse
import importlib
import os.path
import pkgutil
import sys

from opencmiss.importer import ragpdata
from opencmiss.importer import colonhrm
import opencmiss.importer as imp
from opencmiss.importer.errors import OpenCMISSImportError


def _is_importer_module(mod):
    if hasattr(mod, 'identifier') and hasattr(mod, 'import_data') and hasattr(mod, 'import_data_into_region') and hasattr(mod, 'parameters'):
        return True
    return False


def available_importers():
    pkgpath = os.path.dirname(imp.__file__)
    package_names = [name for _, name, _ in pkgutil.iter_modules([pkgpath])]
    importers = []
    for name in package_names:
        t = importlib.import_module(f'opencmiss.importer.{name}')
        if _is_importer_module(t):
            importers.append(t.identifier())
    return importers


def import_data(importer, inputs, working_directory):
    t = importlib.import_module(f'opencmiss.importer.{importer.lower()}')
    if _is_importer_module(t):
        return t.import_data(inputs, working_directory)

    raise OpenCMISSImportError(f"Unknown importer: {importer}")


def import_parameters(importer):
    t = importlib.import_module(f'opencmiss.importer.{importer.lower()}')
    if _is_importer_module(t):
        return t.parameters()

    raise OpenCMISSImportError(f"Unknown importer: {importer}")


def main():
    parser = argparse.ArgumentParser(description='Import data into OpenCMISS-Zinc.')
    parser.add_argument("-o", "--output", default=os.curdir, help='output directory, default is the current directory.')
    parser.add_argument("-l", "--list", help="list available importers", action='store_true')
    subparsers = parser.add_subparsers(dest="importer", help="types of importer")

    ragp_parser = subparsers.add_parser(ragpdata.identifier())
    ragp_parser.add_argument("mbf_xml_file", nargs=1, help="MBF XML marker file.")
    ragp_parser.add_argument("csv_file", nargs=1, help="CSV file of gene, marker name, value matrix.")

    hrm_parser = subparsers.add_parser(colonhrm.identifier())
    hrm_parser.add_argument("colon_hrm_file", help="Colon HRM tab separated values file.")

    args = parser.parse_args()

    if args.list:
        print("Available importers:")
        for id_ in available_importers():
            print(f" - {id_}")
    else:
        if args.output and not os.path.isdir(args.output):
            sys.exit(1)

        inputs = []
        if args.importer == ragpdata.identifier():
            inputs.extend(args.mbf_xml_file)
            inputs.extend(args.csv_file)
        elif args.importer == colonhrm.identifier():
            inputs.extend(args.colon_hrm_file)

        import_data(args.importer, inputs, args.output)


if __name__ == "__main__":
    main()
