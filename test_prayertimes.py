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
from prayertimes import TextFormatter, TimeService


class TextFormatterTest(unittest.TestCase):

  def setUp(self):
    self.sample_text = "sample"
    self.formatted_text = TextFormatter(self.sample_text)

  def test_instance(self):
    self.assertIsInstance(self.formatted_text, TextFormatter)

  def test_get(self):
    self.assertTrue(hasattr(self.formatted_text, 'get'))
    self.assertEqual(self.formatted_text.get(), self.sample_text)

  def test_highlight(self):
    self.assertTrue(hasattr(self.formatted_text, 'highlight'))
    highlighted_text = self.formatted_text.highlight().get()
    self.assertIn('href=#', highlighted_text)

  def test_small(self):
    self.assertTrue(hasattr(self.formatted_text, 'small'))
    small_text = self.formatted_text.small().get()
    self.assertIn('size=12', small_text)

  def test_monospace(self):
    self.assertTrue(hasattr(self.formatted_text, 'monospace'))
    monospace_text = self.formatted_text.monospace().get()
    self.assertIn('font=Monaco', monospace_text)

  def test_combo(self):
    combo_text = self.formatted_text.highlight().small().monospace().get()
    self.assertIn('font=Monaco', combo_text)
    self.assertIn('size=12', combo_text)
    self.assertIn('href=#', combo_text)
    self.assertNotEqual('sample', combo_text)


class TimeServiceTest(unittest.TestCase):

  def setUp(self):
    self.timing = TimeService()
    
  def test_total_hours(self):
    self.assertRaises(TypeError, TimeService.total_hours, 'a' )
    self.assertRaises( ValueError, TimeService.total_hours, -1 )
    
    self.assertEqual( 0, TimeService.total_hours(seconds=0) )
    self.assertEqual( 0, TimeService.total_hours(seconds=1) )
    self.assertEqual( 0, TimeService.total_hours(seconds=3599) )
    self.assertEqual( 1, TimeService.total_hours(seconds=3600) )
    self.assertEqual( 1, TimeService.total_hours(seconds=3601) )
    self.assertEqual( 2, TimeService.total_hours(seconds=7200) )

  def test_total_minutes(self):
    self.assertEqual( 0, TimeService.total_minutes(seconds=0) )
    self.assertEqual( 0, TimeService.total_minutes(seconds=59) )
    self.assertEqual( 1, TimeService.total_minutes(seconds=60) )
    self.assertEqual( 2, TimeService.total_minutes(seconds=120) )
    self.assertEqual( 0, TimeService.total_minutes(seconds=3600) )