import datetime
class AwareDateTime:
    @classmethod # タイムゾーン付きでないか否か
    def is_native(cls, dt: datetime.datetime): return dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None
    @classmethod # タイムゾーン付きであるか否か
    def is_aware(cls, dt: datetime.datetime): return not cls.is_native(dt)
    @classmethod # UTC標準時に変換する
    def to_utc(cls, dt: datetime.datetime): return dt.astimezone(tz=datetime.timezone.utc)
    @classmethod # システムのローカル時に変換する
    def to_local(cls, dt: datetime.datetime): return dt.astimezone()
    @classmethod # 指定したタイムゾーン時に変換する
    def to_tz(cls, dt: datetime.datetime, tz): return dt.astimezone(tz=tz)
    @classmethod # タイムゾーンがないならシステムのローカル時に変換する
    def if_native_to_local(cls, dt: datetime.datetime): return cls.to_local(dt) if cls.is_native(dt) else dt
    @classmethod # タイムゾーンがないならUTC標準時に変換する
    def if_native_to_utc(cls, dt: datetime.datetime): return cls.to_utc(dt) if cls.is_native(dt) else dt
    @classmethod # 指定したタイムゾーン時に変換する。ネイティブならローカル時刻と解釈する
    def if_native_to_tz(cls, dt: datetime.datetime, tz): return cls.to_tz(dt, tz) if cls.is_native(dt) else dt

