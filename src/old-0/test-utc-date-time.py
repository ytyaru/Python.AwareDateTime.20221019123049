#!/usr/bin/env python3
# coding: utf8
import unittest
import importlib  
UtcDateTime = importlib.import_module('utc-date-time').UtcDateTime 
import datetime, zoneinfo # <=3.9
import os
class TestUtcDateTime(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    def test_to_utc(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
        self.assertEqual(None, dt.tzinfo)
        actual = UtcDateTime.to_utc(dt)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual(datetime.datetime.fromisoformat('1999-12-31T15:00:00+00:00'), actual)
    def test_now(self):
        self.assertEqual(datetime.datetime, type(UtcDateTime.now()))
        self.assertEqual(datetime.timezone.utc, UtcDateTime.now().tzinfo)
    def test_from_isoz(self):
        actual = UtcDateTime.from_isoz('2000-01-01T00:00:00Z')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_isoz(self):
        actual = UtcDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01T00:00:00Z', actual)
    def test_to_isoz_from_tokyo_00(self):
        actual = UtcDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual('1999-12-31T15:00:00Z', actual)
    def test_to_isoz_from_tokyo_12(self):
        actual = UtcDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T12:00:00+09:00'))
        self.assertEqual('2000-01-01T03:00:00Z', actual)
    def test_from_sqlite(self):
        actual = UtcDateTime.from_sqlite('2000-01-01 00:00:00')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_sqlite_from_utc(self):
        actual = UtcDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01 00:00:00', actual)
    def test_to_sqlite_from_tokyo_00(self):
        actual = UtcDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual('1999-12-31 15:00:00', actual)
    def test_to_sqlite_from_tokyo_12(self):
        actual = UtcDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T12:00:00+09:00'))
        self.assertEqual('2000-01-01 03:00:00', actual)


if __name__ == '__main__':
    unittest.main()
