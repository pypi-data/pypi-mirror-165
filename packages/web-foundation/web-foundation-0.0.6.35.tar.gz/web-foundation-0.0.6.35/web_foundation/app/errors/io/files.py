from web_foundation.app.errors.application.application import ApplicationError


class SectionNotFound(ApplicationError):
    pass


class FileNotExist(ApplicationError):
    pass


class NothingToWrite(ApplicationError):
    pass


class OsIOError(ApplicationError):
    pass


class NestedFolderDetected(ApplicationError):
    pass
