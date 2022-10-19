from packaging import version
import sys, datetime
if version.parse("3.9") <= sys.version: import zoneinfo
class AwareDateTime:
    @classmethod
    def default_native_tz(cls): return zoneinfo.ZoneInfo('Asia/Tokyo') if version.parse("3.9") <= sys.version else JST()
    @classmethod
    def is_aware(cls, dt: datetime.datetime): # タイムゾーン付きであるか否か
        return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None
    @classmethod
    def to_aware(cls, dt: datetime.datetime): # nativeならawareなUTC標準時に変換して返す
        return dt if cls.is_aware(dt) else  dt.astimezone(tz=datetime.timezone.utc)
    @classmethod
    def to_native(cls, dt: datetime.datetime, tz=None): # awareならnativeに変換して返す
        return dt.astimezone(tz=cls.default_native_tz() if tz is None else tz).replace(tzinfo=None) if cls.is_aware(dt) else dt
    @classmethod
    def now(cls): # awareでUTC標準時な現在日時を返す
        return datetime.datetime.now(datetime.timezone.utc)
    @classmethod
    def from_sqlite(cls, s: str): # s='yyyy-MM-dd HH:mm:ss' + UTC標準時
        return datetime.datetime.fromisoformat(s.replace(' ', 'T') + '+00:00')
    @classmethod
    def to_sqlite(cls, dt: datetime.datetime): # return:'yyyy-MM-dd HH:mm:ss' + UTC標準時
        return f"{cls.to_aware(dt):%Y-%m-%d %H:%M:%S}"

