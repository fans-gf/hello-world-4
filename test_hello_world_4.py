import unittest

from hello_world_4 import hello


class TestHello(unittest.TestCase):
    def test_default_greeting(self):
        self.assertEqual(hello(), "Hello, world!")

    def test_named_greeting(self):
        self.assertEqual(hello("GitHub"), "Hello, GitHub!")

    def test_whitespace_is_trimmed(self):
        self.assertEqual(hello("  Ada  "), "Hello, Ada!")

    def test_empty_name_raises(self):
        with self.assertRaises(ValueError):
            hello("   ")


class TestMain(unittest.TestCase):
    def test_main_prints_default_greeting(self):
        import contextlib
        import io
        import runpy

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            runpy.run_module("hello_world_4", run_name="__main__")
        self.assertEqual(buffer.getvalue().strip(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
