from .safefile import readFile, writeFile, safeReadFile,\
    safeWriteFile, safeGetState, safeRecover, SafeFileError,\
    NO_ERROR, INVALID_NAME, DOES_NOT_EXIST, IS_NOT_A_FILE, READ_ERROR,\
    WRITE_ERROR, SAFE_NORMAL, SAFE_RECOVERABLE, SAFE_INTERVENE

__version__="0.1.0dev"
