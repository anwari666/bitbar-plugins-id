import unittest
import importlib
import sys

# since the filename contains dot, we cannot import it directly
# and should do this instead
spec = importlib.util.spec_from_file_location(
    "prayertimes", "./prayertimes.1m.py")
module = importlib.util.module_from_spec(spec)
sys.modules["prayertimes"] = module
spec.loader.exec_module(module)

# now we can load the module called prayertimes
from prayertimes import TextFormatter


class TextFormatterTest(unittest.TestCase):

  def setUp(self):
    self.sampleText = "sample"
    self.textFormatter = TextFormatter(self.sampleText)

  def test_instance(self):
    self.assertIsInstance(self.textFormatter, TextFormatter)

  def test_get(self):
    self.assertTrue(hasattr(self.textFormatter, 'get'))
    self.assertEqual(self.textFormatter.get(), self.sampleText)

  def test_highlight(self):
    self.assertTrue(hasattr(self.textFormatter, 'highlight'))
    highlighted_text = self.textFormatter.highlight().get()
    self.assertIn('href=#', highlighted_text)

  def test_small(self):
    self.assertTrue(hasattr(self.textFormatter, 'small'))
    small_text = self.textFormatter.small().get()
    self.assertIn('size=12', small_text)

  def test_monospace(self):
    self.assertTrue(hasattr(self.textFormatter, 'monospace'))
    monospace_text = self.textFormatter.monospace().get()
    self.assertIn('font=Monaco', monospace_text)

  def test_combo(self):
    combo_text = self.textFormatter.highlight().small().monospace().get()
    self.assertIn('font=Monaco', combo_text)
    self.assertIn('size=12', combo_text)
    self.assertIn('href=#', combo_text)
    self.assertNotEqual('sample', combo_text)
