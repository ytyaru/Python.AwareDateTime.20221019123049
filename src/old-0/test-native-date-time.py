#!/usr/bin/env python3
# coding: utf8
import unittest
import importlib
NativeDateTime = importlib.import_module('native-date-time').NativeDateTime 
AwareDateTime = importlib.import_module('aware-date-time').AwareDateTime 
import datetime, zoneinfo # <=3.9
import os
class TestNativeDateTime(unittest.TestCase):
    def setUp(self): pass
    def tearDown(self): pass
    def test_from_ymdhms(self):
        actual = NativeDateTime.from_ymdhms('2000-01-01 00:00:00') 
        if 32400 == AwareDateTime.offset(datetime.datetime.now()):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
            self.assertEqual(0, actual.hour)
            self.assertEqual(0, actual.minute)
            self.assertEqual(0, actual.second)
            self.assertEqual(1, actual.day)
            self.assertEqual(1, actual.month)
            self.assertEqual(2000, actual.year)
    def test_from_iso_utc(self):
        actual = NativeDateTime.from_iso('2000-01-01T00:00:00+00:00')
        if 32400 == AwareDateTime.offset(datetime.datetime.now()):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
            self.assertEqual(15, actual.hour)
            self.assertEqual(0, actual.minute)
            self.assertEqual(0, actual.second)
            self.assertEqual(31, actual.day)
            self.assertEqual(12, actual.month)
            self.assertEqual(1999, actual.year)
    def test_from_iso_tokyo(self):
        actual = NativeDateTime.from_iso('2000-01-01T00:00:00+09:00')
        print(actual)
        print(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        if 32400 == AwareDateTime.offset(datetime.datetime.now()):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
            self.assertEqual(0, actual.hour)
            self.assertEqual(0, actual.minute)
            self.assertEqual(0, actual.second)
            self.assertEqual(1, actual.day)
            self.assertEqual(1, actual.month)
            self.assertEqual(2000, actual.year)
    """
    def test_(self):
    def test_(self):
    def test_(self):
    def test_(self):
    def test_(self):
    def test_to_utc(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
        self.assertEqual(None, dt.tzinfo)
        actual = NativeDateTime.to_utc(dt)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual(datetime.datetime.fromisoformat('1999-12-31T15:00:00+00:00'), actual)
    def test_now(self):
        self.assertEqual(datetime.datetime, type(NativeDateTime.now()))
        self.assertEqual(datetime.timezone.utc, NativeDateTime.now().tzinfo)
    def test_from_isoz(self):
        actual = NativeDateTime.from_isoz('2000-01-01T00:00:00Z')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_isoz(self):
        actual = NativeDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01T00:00:00Z', actual)
    def test_to_isoz_from_tokyo_00(self):
        actual = NativeDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual('1999-12-31T15:00:00Z', actual)
    def test_to_isoz_from_tokyo_12(self):
        actual = NativeDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T12:00:00+09:00'))
        self.assertEqual('2000-01-01T03:00:00Z', actual)
    def test_from_sqlite(self):
        actual = NativeDateTime.from_sqlite('2000-01-01 00:00:00')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_sqlite_from_utc(self):
        actual = NativeDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01 00:00:00', actual)
    def test_to_sqlite_from_tokyo_00(self):
        actual = NativeDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual('1999-12-31 15:00:00', actual)
    def test_to_sqlite_from_tokyo_12(self):
        actual = NativeDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T12:00:00+09:00'))
        self.assertEqual('2000-01-01 03:00:00', actual)
    """


if __name__ == '__main__':
    unittest.main()
