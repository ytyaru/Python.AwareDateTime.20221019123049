import datetime, re
import importlib  
AwareDateTime = importlib.import_module('aware-date-time').AwareDateTime 
class NativeDateTime:
    @classmethod
    def _from_ymdhms(cls, s: str, tz)->datetime.datetime:
        if re.fullmatch(r'\d{4,}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', s):
            return datetime.datetime.fromisoformat(s.replace(' ', 'T') + tz)
        else: raise Error("書式エラーです。'yyyy-MM-dd HH:mm:ss' の書式にしてください。")
    @classmethod # 指定した日時にそのままシステムのタイムゾーンを付与する
    def from_ymdhms(cls, s: str)->datetime.datetime: return cls._from_ymdhms(s, AwareDateTime.native_tz_iso())
    @classmethod # datetime.fromisoformat()
    def from_iso(cls, s: str)->datetime.datetime: return AwareDateTime.to_native(datetime.datetime.fromisoformat(s))
    @classmethod # aware/native問わずシステムのタイムゾーンを付与する
    def from_datetime(cls, dt: datetime.datetime)->datetime.datetime: return AwareDateTime.to_native(dt)
    @classmethod # UTCとして解釈しシステムのタイムゾーンに変換する
    def from_sqlite(cls, s: str)->datetime.datetime: return cls.from_datetime(cls._from_ymdhms(s, '+00:00'))

