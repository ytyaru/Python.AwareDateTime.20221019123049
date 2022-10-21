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
    @classmethod # UTC標準時からの時差を返す（指定した日時のタイムゾーンを秒数で返す）
    def tz_sec(cls, dt: datetime.datetime): return cls.tz_sec(dt.astimezone()) if cls.is_native(dt) else dt.tzinfo.utcoffset(dt).seconds
    @classmethod # UTC標準時からの時差を返す（指定した日時のタイムゾーンを+00:00テキストで返す）
    def tz_iso(cls, dt: datetime.datetime):
        seconds = cls.tz_sec(dt)
        minutes = seconds // 60
        h = minutes // 60
        m = minutes - (h * 60)
        s = seconds % 60
        return f"{'+' if 0 <= seconds else '-'}{h:02}:{m:02}{'' if 0 == s else ':'+str(s).zfill(2)}"

