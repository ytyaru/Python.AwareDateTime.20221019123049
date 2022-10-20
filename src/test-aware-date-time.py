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
    def test_is_native_true(self):
        self.assertTrue(AwareDateTime.is_native(datetime.datetime.now()))
    def test_is_native_false(self):
        self.assertFalse(AwareDateTime.is_native(datetime.datetime.now(datetime.timezone.utc)))
    def test_is_aware_true(self):
        self.assertTrue(AwareDateTime.is_aware(datetime.datetime.now(datetime.timezone.utc)))
    def test_is_aware_false(self):
        self.assertFalse(AwareDateTime.is_aware(datetime.datetime.now()))
    def test_to_utc_native(self):
        actual = AwareDateTime.to_utc(datetime.datetime.fromisoformat('2000-01-01T00:00:00'))
        #actual = AwareDateTime.to_utc(datetime.datetime.now())
        if actual.tzinfo == datetime.timezone(datetime.timedelta(seconds=32400)):
            self.assertEqual(datetime.timezone.utc, actual.tzinfo)
            self.assertEqual("1999-12-31T15:00:00+0000", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
            self.assertEqual(15, actual.hour)
            self.assertEqual(0, actual.minute)
            self.assertEqual(0, actual.second)
            self.assertEqual(31, actual.day)
            self.assertEqual(12, actual.month)
            self.assertEqual(1999, actual.year)
    def test_to_utc_utc(self):
        #actual = AwareDateTime.to_utc(datetime.datetime.now(datetime.timezone.utc))
        actual = AwareDateTime.to_utc(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual("2000-01-01T00:00:00+0000", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
        self.assertEqual(0, actual.hour)
        self.assertEqual(0, actual.minute)
        self.assertEqual(0, actual.second)
        self.assertEqual(1, actual.day)
        self.assertEqual(1, actual.month)
        self.assertEqual(2000, actual.year)
    def test_to_utc_tokyo(self):
        actual = AwareDateTime.to_utc(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual("1999-12-31T15:00:00+0000", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
        self.assertEqual(15, actual.hour)
        self.assertEqual(0, actual.minute)
        self.assertEqual(0, actual.second)
        self.assertEqual(31, actual.day)
        self.assertEqual(12, actual.month)
        self.assertEqual(1999, actual.year)
    def test_to_local_utc(self):
        actual = AwareDateTime.to_local(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        if datetime.datetime.now().tzinfo == datetime.timezone(datetime.timedelta(seconds=32400)):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
    def test_to_local_tokyo(self):
        actual = AwareDateTime.to_local(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        if datetime.datetime.now().tzinfo == datetime.timezone(datetime.timedelta(seconds=32400)):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
    def test_to_local_native(self):
        actual = AwareDateTime.to_local(datetime.datetime.fromisoformat('2000-01-01T00:00:00'))
        if datetime.datetime.now().tzinfo == datetime.timezone(datetime.timedelta(seconds=32400)):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
    def test_to_tz_tokyo_utc(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'), 
            datetime.timezone.utc)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual("1999-12-31T15:00:00+0000", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
    def test_to_tz_tokyo_native(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'), 
            None)
        #self.assertEqual(None, actual.tzinfo)
        self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400), 'JST'), actual.tzinfo)
        self.assertEqual("2000-01-01T00:00:00+0900", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
    def test_to_tz_tokyo_tokyo(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'), 
            datetime.timezone(datetime.timedelta(seconds=32400)))
        self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
        self.assertEqual("2000-01-01T00:00:00+0900", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
    def test_to_tz_utc_tokyo(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), 
            datetime.timezone(datetime.timedelta(seconds=32400)))
        self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
        self.assertEqual("2000-01-01T09:00:00+0900", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
    def test_to_tz_utc_native(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), 
            None)
        if datetime.datetime.now().tzinfo == datetime.timezone(datetime.timedelta(seconds=32400)):
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
            self.assertEqual("2000-01-01T09:00:00+0900", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
    def test_to_tz_native_tokyo_timedelta(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00'), 
            datetime.timezone(datetime.timedelta(seconds=32400)))
        if datetime.datetime.now().tzinfo == datetime.timezone(datetime.timedelta(seconds=32400)):
            #self.assertEqual(datetime.timedelta(seconds=32400), actual.tzinfo)
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400), 'JST'), actual.tzinfo)
            self.assertEqual(datetime.timezone, type(actual.tzinfo))
            self.assertEqual(32400, actual.tzinfo.utcoffset(actual).seconds)
            self.assertEqual("2000-01-01T09:00:00+0900", f"{actual:%Y-%m-%dT%H:%M:%S%z}")
    def test_to_tz_native_tokyo_zoneinfo(self):
        actual = AwareDateTime.to_tz(
            datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), 
            zoneinfo.ZoneInfo('Asia/Tokyo'))
        self.assertEqual(zoneinfo.ZoneInfo('Asia/Tokyo'), actual.tzinfo)
        self.assertEqual(zoneinfo.ZoneInfo, type(actual.tzinfo))
        self.assertEqual(32400, actual.tzinfo.utcoffset(actual).seconds)
        









    """
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
        #self.assertEqual(None, AwareDateTime.to_native(dt).tzinfo)
        if 32400 == AwareDateTime.offset(datetime.datetime.now()):
            actual = AwareDateTime.to_native(dt)
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
            self.assertEqual(9, actual.hour)
            self.assertEqual(0, actual.minute)
            self.assertEqual(0, actual.second)
            self.assertEqual(1, actual.day)
            self.assertEqual(1, actual.month)
            self.assertEqual(2000, actual.year)
    def test_to_native_from_aware_as_tokyo(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00')
        self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), dt.tzinfo)
        #self.assertEqual(None, AwareDateTime.to_native(dt).tzinfo)
        if 32400 == AwareDateTime.offset(datetime.datetime.now()):
            actual = AwareDateTime.to_native(dt)
            self.assertEqual(datetime.timezone(datetime.timedelta(seconds=32400)), actual.tzinfo)
            self.assertEqual(0, actual.hour)
            self.assertEqual(0, actual.minute)
            self.assertEqual(0, actual.second)
            self.assertEqual(1, actual.day)
            self.assertEqual(1, actual.month)
            self.assertEqual(2000, actual.year)
    def test_to_utc(self):
        dt = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
        self.assertEqual(None, dt.tzinfo)
        actual = AwareDateTime.to_utc(dt)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
        self.assertEqual(datetime.datetime.fromisoformat('1999-12-31T15:00:00+00:00'), actual)
        #self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
    def test_offset_utc(self):
        self.assertEqual(0, AwareDateTime.offset(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00')))
    def test_offset_tokyo(self):
        self.assertEqual(32400, AwareDateTime.offset(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00')))
    def test_offset_native(self):
        native = datetime.datetime.now()
        expected = native.astimezone().tzinfo.utcoffset(native).seconds
        self.assertEqual(expected, AwareDateTime.offset(datetime.datetime.fromisoformat('2000-01-01T00:00:00')))
    def test_tz_iso_0000(self):
        self.assertEqual('+00:00', AwareDateTime.tz_iso(0))
    def test_tz_iso_0900(self):
        self.assertEqual('+09:00', AwareDateTime.tz_iso(32400))
    def test_tz_iso_0900(self):
        self.assertEqual('-09:00', AwareDateTime.tz_iso(-32400))
    def test_tz_iso_0900(self):
        self.assertEqual('+09:01:30', AwareDateTime.tz_iso(32490))
    def test_native_tz_iso(self):
        if 32400 == AwareDateTime.offset(datetime.datetime.now()):
            self.assertEqual('+09:00', AwareDateTime.native_tz_iso())
    def test_now(self):
        self.assertEqual(datetime.datetime, type(AwareDateTime.now()))
        self.assertEqual(datetime.timezone.utc, AwareDateTime.now().tzinfo)
    def test_from_isoz(self):
        actual = AwareDateTime.from_isoz('2000-01-01T00:00:00Z')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_isoz(self):
        actual = AwareDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01T00:00:00Z', actual)
    def test_to_isoz_from_tokyo_00(self):
        actual = AwareDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual('1999-12-31T15:00:00Z', actual)
    def test_to_isoz_from_tokyo_12(self):
        actual = AwareDateTime.to_isoz(datetime.datetime.fromisoformat('2000-01-01T12:00:00+09:00'))
        self.assertEqual('2000-01-01T03:00:00Z', actual)
    def test_from_sqlite(self):
        actual = AwareDateTime.from_sqlite('2000-01-01 00:00:00')
        self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
        self.assertEqual(datetime.timezone.utc, actual.tzinfo)
    def test_to_sqlite_from_utc(self):
        actual = AwareDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'))
        self.assertEqual('2000-01-01 00:00:00', actual)
    def test_to_sqlite_from_tokyo_00(self):
        actual = AwareDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00'))
        self.assertEqual('1999-12-31 15:00:00', actual)
    def test_to_sqlite_from_tokyo_12(self):
        actual = AwareDateTime.to_sqlite(datetime.datetime.fromisoformat('2000-01-01T12:00:00+09:00'))
        self.assertEqual('2000-01-01 03:00:00', actual)
    """


if __name__ == '__main__':
    unittest.main()
