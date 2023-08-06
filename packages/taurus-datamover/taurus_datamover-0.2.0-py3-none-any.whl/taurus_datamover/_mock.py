from pathlib import Path
import tempfile
import os
import shutil

my_path = Path(__file__).parent


class MockCluster:
    def __init__(self, commands: list = [
                 'dtls', 'dtcp', 'dtmv'], dtwrapper: str = 'dtwrapper') -> None:
        self.source_path = my_path / 'mock_cluster_files'
        self.tempdir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.tempdir.name)
        self.bin_path = Path(self.tempdir.name) / 'bin'
        self.commands = commands
        self.dtwrapper_path = self.bin_path / dtwrapper
        self.scratch_path = self.temp_path / 'scratch'
        self.scratch_path.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        shutil.copytree(str(self.source_path), self.bin_path)
        for command in self.commands:
            os.symlink(
                self.dtwrapper_path, self.bin_path / command)
        return self

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        self.tempdir.cleanup()
