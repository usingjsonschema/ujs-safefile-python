"""
Unit tests for jsonsyntax.

Note that the read error (code = 3) is not tested since artificially
generating a read error (e.g. disabling read file permissions) is not
consistent across operating systems.
"""
from os import mkdir, rmdir, unlink
from os.path import exists
import pytest
from safefile import safefile

# at start, create temporary directory
def setup_module (module):
    mkdir ("tempdir")

# at end, remove temporary directory
def teardown_module (module):
    rmdir ("tempdir")

# convenience function to clean up all test files
def cleanup ():
    if exists ("test.txt.eph"):
        unlink ("test.txt.eph")
    if exists ("test.txt.rdy"):
        unlink ("test.txt.rdy")
    if exists ("test.txt"):
        unlink ("test.txt")
    if exists ("test.txt.bak"):
        unlink ("test.txt.bak")
    if exists ("test.txt.bk2"):
        unlink ("test.txt.bk2")

# convenience function to write a file
def writeFile (file, data):
    file = open (file, "w")
    file.write (data)
    file.close ()

class TestRead:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_no_error (self):
        writeFile ("test.txt", "test")
        safefile.readFile ("test.txt")

    def test_invalid_name (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.readFile (None)
        assert e.value.code == safefile.INVALID_NAME

    def test_does_not_exist (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.readFile ("nofile.json")
        assert e.value.code == safefile.DOES_NOT_EXIST

    def test_is_not_a_file (self, tmpdir):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.readFile ("tempdir")
        assert e.value.code == safefile.IS_NOT_A_FILE

class TestWrite:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_no_error (self, tmpdir):
        safefile.writeFile ("test.txt", "test")

    def test_invalid_name (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.writeFile (None, "test")
        assert e.value.code == safefile.INVALID_NAME

    def test_is_not_a_file (self, tmpdir):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.writeFile ("tempdir", "test")
        assert e.value.code == safefile.IS_NOT_A_FILE

class TestSafeGetState:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_normal (self):
        writeFile ("test.txt", "test")
        assert safefile.safeGetState ("test.txt") == safefile.SAFE_NORMAL

    def test_intervene (self):
        writeFile ("test.txt.eph", "test eph")
        assert safefile.safeGetState ("test.txt") == safefile.SAFE_INTERVENE

    def test_recoverable_ready (self):
        writeFile ("test.txt.rdy", "test rdy")
        assert safefile.safeGetState ("test.txt") == safefile.SAFE_RECOVERABLE

    def test_recoverable_backup (self):
        writeFile ("test.txt.bak", "test bak")
        assert safefile.safeGetState ("test.txt") == safefile.SAFE_RECOVERABLE

    def test_recoverable_tertiary (self):
        writeFile ("test.txt.bk2", "test bk2")
        assert safefile.safeGetState ("test.txt") == safefile.SAFE_RECOVERABLE

    def test_invalid_file_none (self):
        assert safefile.safeGetState (None) == safefile.INVALID_NAME

    def test_invalid_file_doesnt_exist (self):
        assert safefile.safeGetState ("nofile.txt") == safefile.DOES_NOT_EXIST

    def test_invalid_file_directory (self):
        assert safefile.safeGetState ("tempdir") == safefile.IS_NOT_A_FILE

class TestSafeRecover:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_invalid_file_none (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeRecover (None)
        assert e.value.code == safefile.INVALID_NAME

    def test_invalid_file_doesnt_exist (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeRecover ("nofile.txt")
        assert e.value.code == safefile.DOES_NOT_EXIST

    def test_invalid_file_directory (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeRecover ("tempdir")
        assert e.value.code == safefile.IS_NOT_A_FILE

    def test_base_file (self):
        writeFile ("test.txt", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_ephemeral_file (self):
        writeFile ("test.txt.eph", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == False
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_ready_file (self):
        writeFile ("test.txt.rdy", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_backup_file (self):
        writeFile ("test.txt.bak", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_tertiary_file (self):
        writeFile ("test.txt.bk2", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_ready_base_files (self):
        writeFile ("test.txt", "test")
        writeFile ("test.txt.rdy", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_backup_file (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt.bak", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_base_backup_file (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt", "test")
        writeFile ("test.txt.bak", "test")
        safefile.safeRecover ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

class TestSafeReadBasic:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_invalid_name (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeReadFile (None)
        assert e.value.code == safefile.INVALID_NAME

    def test_does_not_exist (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeReadFile ("nofile.json")
        assert e.value.code == safefile.DOES_NOT_EXIST

    def test_is_not_a_file (self, tmpdir):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeReadFile ("tempdir")
        assert e.value.code == safefile.IS_NOT_A_FILE

    def test_no_error (self):
        writeFile ("test.txt", "test")
        safefile.safeReadFile ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_recover_ready (self):
        writeFile ("test.txt.rdy", "test")
        safefile.safeReadFile ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

class TestSafeWriteBasic:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_invalid_name (self):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeReadFile (None)
        assert e.value.code == safefile.INVALID_NAME

    def test_is_not_a_file (self, tmpdir):
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeReadFile ("tempdir")
        assert e.value.code == safefile.IS_NOT_A_FILE

    def test_write_new_file (self):
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_write_file_exists (self):
        writeFile ("test.txt", "test")
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

class TestSafeReadRecoverable:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_only_ephemeral_file (self):
        writeFile ("test.txt.eph", "test")
        with pytest.raises (safefile.SafeFileError) as e:
            safefile.safeReadFile ("test.txt")
        assert e.value.code == safefile.DOES_NOT_EXIST
        assert exists ("test.txt.eph") == True
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == False
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_only_ready_file (self):
        writeFile ("test.txt.rdy", "test")
        safefile.safeReadFile ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_ready_and_base_files (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt", "test")
        safefile.safeReadFile ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_and_backup_files (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt.bak", "test")
        safefile.safeReadFile ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_and_base_and_backup_files (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt", "test")
        writeFile ("test.txt.bak", "test")
        safefile.safeReadFile ("test.txt")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

class TestSafeWriteRecoverable:
    # process before each test method
    def setup_method (self, method):
        pass

    # clean up after each test method
    def teardown_method (self, method):
        cleanup ()

    def test_only_ephemeral_file (self):
        writeFile ("test.txt.eph", "test")
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == False
        assert exists ("test.txt.bk2") == False

    def test_only_ready_file (self):
        writeFile ("test.txt.rdy", "test")
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_and_base_files (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt", "test")
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_and_backup_files (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt.bak", "test")
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False

    def test_ready_and_base_and_backup_files (self):
        writeFile ("test.txt.rdy", "test")
        writeFile ("test.txt", "test")
        writeFile ("test.txt.bak", "test")
        safefile.safeWriteFile ("test.txt", "test")
        assert exists ("test.txt.eph") == False
        assert exists ("test.txt.rdy") == False
        assert exists ("test.txt") == True
        assert exists ("test.txt.bak") == True
        assert exists ("test.txt.bk2") == False
