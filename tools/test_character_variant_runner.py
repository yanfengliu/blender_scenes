"""Exercise output protection, bounded failure cleanup and immutable input checks."""
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from export_character_variant import run


class ExportOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix='character_variant_test_')
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.source = self.root/'dressed.blend'
        self.source.write_bytes(b'original dressed source')
        self.args = SimpleNamespace(input=self.source, output_dir=self.root/'fresh',
                                    blender='unused', base=self.root/'base.obj', samples=128, size=1600, timeout=1)

    def test_rejects_source_directory_and_existing_variants_before_launch(self):
        for directory in (self.root, self.root/'existing'):
            directory.mkdir(exist_ok=True)
            (directory/'unclothed.blend').write_bytes(b'prior result')
            self.args.output_dir = directory
            with patch('export_character_variant.subprocess.Popen') as launch:
                with self.assertRaisesRegex(ValueError, 'fresh output'):
                    run(self.args)
                launch.assert_not_called()
            self.assertEqual((directory/'unclothed.blend').read_bytes(), b'prior result')

    def test_timeout_closes_owned_job_and_retains_failure_log(self):
        process = Mock(pid=123, returncode=None)
        process.poll.return_value = None
        process.wait.side_effect = subprocess.TimeoutExpired('owned test process', 1)
        with patch('build_sailor_character.WindowsJob'), patch('build_sailor_character.close_owned_process') as close, \
             patch('export_character_variant.subprocess.Popen', return_value=process), \
             patch('export_character_variant.time.monotonic', side_effect=[0, 0, 2]):
            with self.assertRaisesRegex(TimeoutError, 'exceeded 1s'):
                run(self.args)
            self.assertIs(close.call_args.args[0], process)
        self.assertTrue((self.args.output_dir/'export.log').exists())
        self.assertEqual(self.source.read_bytes(), b'original dressed source')

    def test_failed_process_still_checks_source_hash_after_cleanup(self):
        process = Mock(pid=123, returncode=1)
        process.poll.return_value = 1
        def launch(*args, **kwargs):
            self.source.write_bytes(b'negative control: changed during failed launch')
            return process
        with patch('build_sailor_character.WindowsJob'), patch('build_sailor_character.close_owned_process') as close, \
             patch('export_character_variant.subprocess.Popen', side_effect=launch):
            with self.assertRaisesRegex(AssertionError, 'including failure cleanup'):
                run(self.args)
            close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
