#!/usr/bin/env python3
# coding: utf8
import unittest
import importlib  
AwareDateTime = importlib.import_module('aware-date-time').AwareDateTime 
import datetime, zoneinfo # <=3.9
import os
class TestAwareDateTime(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    def test_default_native_tz(self):
        self.assertEqual(zoneinfo.ZoneInfo('Asia/Tokyo'), AwareDateTime.default_native_tz())
    def test_is_aware_true(self):
        self.assertTrue(AwareDateTime.is_aware(datetime.datetime.now(datetime.timezone.utc)))
    def test_is_aware_false(self):
        self.assertFalse(AwareDateTime.is_aware(datetime.datetime.now()))
    def test_to_aware_from_native(self):
        dt = datetime.datetime.now()
        self.assertEqual(None, dt.tzinfo)
        self.assertEqual(datetime.timezone.utc, AwareDateTime.to_aware(dt).tzinfo)
    def test_to_aware_from_aware(self):
        dt = datetime.datetime.now(datetime.timezone.utc)
        self.assertEqual(datetime.timezone.utc, dt.tzinfo)
        self.assertEqual(datetime.timezone.utc, AwareDateTime.to_aware(dt).tzinfo)
    def test_to_aware_from_native_as(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
        self.assertEqual(None, dt.tzinfo)
        self.assertEqual(datetime.timezone.utc, AwareDateTime.to_aware(dt).tzinfo)
    def test_to_native_from_aware_as(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00')
        self.assertEqual(datetime.timezone.utc, dt.tzinfo)
        self.assertEqual(None, AwareDateTime.to_native(dt).tzinfo)
    def test_to_native_from_aware_as_tokyo(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00')
        self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), dt.tzinfo)
        self.assertEqual(None, AwareDateTime.to_native(dt).tzinfo)
    def test_to_utc(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
        self.assertEqual(None, dt.tzinfo)
        actual = AwareDateTime.to_utc(dt)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
    def test_now(self):
        self.assertEqual(datetime.datetime, type(AwareDateTime.now()))
        self.assertEqual(datetime.timezone.utc, AwareDateTime.now().tzinfo)
    def test_from_sqlite(self):
        actual = AwareDateTime.from_sqlite('2000-01-01 00:00:00')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_sqlite_from_utc(self):
        actual = AwareDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01 00:00:00', actual)





    """
    def test_to_aware_from_native_as(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00')
        #self.assertEqual(None, dt.tzinfo)
        self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), dt.tzinfo)
        print(dt)
        print(AwareDateTime.to_aware(dt))
        self.assertEqual(datetime.timezone.utc, AwareDateTime.to_aware(dt).tzinfo)
    def test_to_aware_from_aware_as(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00')
        self.assertEqual(datetime.timezone.utc, dt.tzinfo)
        self.assertEqual(datetime.timezone.utc, AwareDateTime.to_aware(dt).tzinfo)
    """
         
    """
    def test_default_native_tz(self):
        expected = zoneinfo.ZoneInfo('Asia/Tokyo') if version.parse("3.9") <= sys.version else JST()
        self.assertEqual(expected, AwareDateTime.default_native_tz())
    """
    """
    def test_error(self):
        with self.assertRaises(ValueError) as cm:
            Lib().error()
        self.assertEqual(cm.exception.args[0], 'This is a Error!!')
    """


if __name__ == '__main__':
    unittest.main()
