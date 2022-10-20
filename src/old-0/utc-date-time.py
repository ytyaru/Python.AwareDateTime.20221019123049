#import sys, datetime, zoneinfo # <=3.9
import datetime
class UtcDateTime:
    @classmethod
    def to_utc(cls, dt: datetime.datetime): return dt.astimezone(tz=datetime.timezone.utc)
    @classmethod
    def now(cls): return datetime.datetime.now(datetime.timezone.utc)
    @classmethod  # s:'yyyy-MM-ddTHH:mm:ssZ' UTC標準時
    def from_isoz(cls, s: str): return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
    @classmethod # return 'yyyy-MM-ddTHH:mm:ssZ' UTC標準時
    def to_isoz(cls, dt: datetime.datetime): return f"{cls.to_utc(dt):%Y-%m-%dT%H:%M:%SZ}"
    @classmethod # s='yyyy-MM-dd HH:mm:ss' + UTC標準時
    def from_sqlite(cls, s: str): return datetime.datetime.fromisoformat(s.replace(' ', 'T') + '+00:00')
    @classmethod # return:'yyyy-MM-dd HH:mm:ss' + UTC標準時
    def to_sqlite(cls, dt: datetime.datetime): return f"{cls.to_utc(dt):%Y-%m-%d %H:%M:%S}"

