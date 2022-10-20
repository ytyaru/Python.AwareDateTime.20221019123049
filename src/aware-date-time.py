import datetime
class AwareDateTime:
    @classmethod # タイムゾーン付きであるか否か
    def is_aware(cls, dt: datetime.datetime): return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None
    @classmethod # nativeならawareなUTC標準時に変換して返す
    def to_aware(cls, dt: datetime.datetime): return dt if cls.is_aware(dt) else dt.astimezone(tz=datetime.timezone.utc)
    @classmethod # awareならnativeに変換して返す
    def to_native(cls, dt: datetime.datetime): # タイムゾーンを付与したawareなローカル時刻にする(tzinfo=Noneでなく)
        dt2 = cls.to_utc(dt) + (datetime.timedelta(seconds=cls.native_tz()) * -1)
        return datetime.datetime.fromisoformat(f"{dt2:%Y-%m-%dT%H:%M:%S}{cls.native_tz_iso()}")
    @classmethod # nativeならawareなUTC標準時に変換して返す
    def to_utc(cls, dt: datetime.datetime): return dt.astimezone(tz=datetime.timezone.utc)
    @classmethod # UTC標準時との時差を秒単位で返す
    def offset(cls, dt: datetime.datetime): return cls.offset(dt.astimezone()) if dt.tzinfo is None else dt.tzinfo.utcoffset(dt).seconds
    @classmethod # システムのタイムゾーンを秒数で返す
    def native_tz(cls): return cls.offset(datetime.datetime.now())
    @classmethod # 指定した秒数をISO-8601形式のタイムゾーンで返す
    def tz_iso(cls, seconds):
        minutes = seconds // 60
        h = minutes // 60
        m = minutes - (h * 60)
        s = seconds % 60
        return f"{'+' if 0 <= seconds else '-'}{h:02}:{m:02}{'' if 0 == s else ':'+str(s).zfill(2)}"
    @classmethod # システムのタイムゾーンをISO8601形式で返す
    def native_tz_iso(cls): return cls.tz_iso(cls.offset(datetime.datetime.now()))
    @classmethod # awareでUTC標準時な現在日時を返す
    def now(cls): return datetime.datetime.now(datetime.timezone.utc)
    @classmethod  # return:'yyyy-MM-ddTHH:mm:ssZ' UTC標準時
    def from_isoz(cls, s: str): return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
    @classmethod # s='yyyy-MM-ddTHH:mm:ssZ' UTC標準時
    def to_isoz(cls, dt: datetime.datetime): return f"{cls.to_utc(dt):%Y-%m-%dT%H:%M:%SZ}"
    @classmethod # s='yyyy-MM-dd HH:mm:ss' + UTC標準時
    def from_sqlite(cls, s: str): return datetime.datetime.fromisoformat(s.replace(' ', 'T') + '+00:00')
    @classmethod # return:'yyyy-MM-dd HH:mm:ss' + UTC標準時
    def to_sqlite(cls, dt: datetime.datetime): return f"{cls.to_utc(dt):%Y-%m-%d %H:%M:%S}"

