
class OpenCMISSImportError(Exception):
    pass


class OpenCMISSImportInvalidInputs(OpenCMISSImportError):
    pass


class OpenCMISSImportUnknownParameter(OpenCMISSImportError):
    pass


class OpenCMISSImportMBFXMLError(OpenCMISSImportError):
    pass


class OpenCMISSImportFileNotFoundError(OpenCMISSImportError):
    pass


class OpenCMISSImportGeneFileError(OpenCMISSImportError):
    pass


class OpenCMISSImportColonHRMError(OpenCMISSImportError):
    pass


class OpenCMISSImportColonManometryError(OpenCMISSImportError):
    pass


class OpenCMISSImportCellDensityError(OpenCMISSImportError):
    pass
