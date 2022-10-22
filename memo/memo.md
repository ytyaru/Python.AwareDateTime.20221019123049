タイムゾーンがない日時にタイムゾーンを付ける【Python】

　`aware`/`native`とかややこしいので、タイムゾーンをつけるクラスを作った。

<!-- more -->

# ブツ

* [リポジトリ][]

[リポジトリ]:https://github.com/ytyaru/Python.AwareDateTime.20221019123049
[DEMO]:https://ytyaru.github.io/Python.AwareDateTime.20221019123049/

## 実行

```sh
NAME='Python.AwareDateTime.20221019123049'
git clone https://github.com/ytyaru/$NAME
cd $NAME/src
./test-aware-date-time.py
```

# コード

```python
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
```

　欲しかったのは`if_native_to_local`。

メソッド|概要
--------|----
`if_native_to_local`|タイムゾーンがないときローカルのタイムゾーンとして解釈した日付型を返す
`if_native_to_utc`|タイムゾーンがないときUTCとして解釈した日付型を返す
`if_native_to_tz`|タイムゾーンがないとき指定したタイムゾーンとして解釈した日付型を返す

　`if_native_*`でない`to_*`系は強制的に変換する。でもタイムゾーンがある場合はそのまま使いたい場合もある。問題なのはタイムゾーンがない場合なので、それだけ変換するのが`if_native_*`系。

# 日時の基礎

　[datetime][]を使う。

[datetime]:https://docs.python.org/ja/3/library/datetime.html

　Pythonの日付はタイムゾーンがある場合とない場合がある。これが諸悪の根源。それぞれ以下のように呼ぶ。

呼び方|意味
------|----
`aware`|タイムゾーンがある日付型インスタンス
`native`|タイムゾーンがない日付型インスタンス

## 謎

　なぜ`native`なタイムゾーンなんてあるのかわからない。

　`native`（タイムゾーンがない日時型）があるせいでややこしくなる。私としてはタイムゾーンがないときは実行環境のタイムゾーンを付与して欲しかった。実際には`tzinfo`が`None`になる。なのに`astimezone()`では実行環境のタイムゾーンで計算されてそれを付与した日付型が返される。なんだかチグハグな印象。なぜ`native`なんて日付型があるのかわからない。

## Pythonの[datetime][]を確認する

```python
import datetime
```

aware
```python
aware = datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00')
assert aware.tzinfo == datetime.timezone.utc

aware = datetime.datetime.now(datetime.timezone.utc)
assert aware.tzinfo == datetime.timezone.utc
```

native
```python
native = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
assert native.tzinfo == None

native = datetime.datetime.now()
assert native.tzinfo == None
```

　タイムゾーンは`tzinfo`で取得する。基本的にはUTCとNoneの2パターン。

　タイムゾーンがないときは`tzinfo`が`None`になる。これをなくして実行環境に応じたタイムゾーンを付与したい。

　システムのタイムゾーン情報を取得する方法は以下。ネイティブ日時を`astimezone()`する。私の実行環境である日本`"Asia/Tokyo"`なら`+09:00`。秒で表すと`32400`。名前は`JST`。型は`timezone(timedelta)`。

```python
native.astimezone()
```
```python
datetime.datetime(2000, 1, 1, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400), 'JST'))
```
```python
assert native.astimezone().tzinfo == datetime.timezone(datetime.timedelta(seconds=32400))
```

　タイムゾーンを直接指定した日付テキストもある。

```python
tokyo = datetime.datetime.fromisoformat('2000-01-01T00:00:00+09:00')
assert tokyo.tzinfo == datetime.timezone(datetime.timedelta(seconds=32400))
```

　UTC標準時との時差を秒単位で取得するなら以下。32400秒＝9時間。

```python
tokyo.tzinfo.utcoffset(tokyo).seconds #=> 32400
```

　ネイティブ時刻からタイムゾーンを取得する。これがシステムのタイムゾーンである。

```python
native.astimezone().tzinfo.utcoffset(native).seconds #=>32400
```

　[datetime][]の`astimezone()`や`utcoffset()`を使うことでシステムのタイムゾーンを取得できた。あとはこれをセットした日付インスタンスを生成すればいい。けど、そこが難関。

　`astimezone()`には`tzinfo`が引数にある。なので取得した`32400`をここで指定できれば万事解決していた。が、残念ながら以下エラーが出る。

```python
native.astimezone(32400)
```
```sh
TypeError: tzinfo argument must be None or of a tzinfo subclass, not type 'int'
```

　`astimezone()`にセットできる`tzinfo`は次の3パターンである。

引数|意味
----|----
`None`|`aware`でなく`native`な日付になる。タイムゾーン情報がない。こいつを消す方法はよ
`datetime.timezone.utc`|UTC標準時
`zoneinfo.ZoneInfo('Asia/Tokyo')`|`+09:00`（Python3.9以降）
`datetime.datetime.now().astimezone().tzinfo`|ローカルのタイムゾーン

　こんなパターンやコードを覚えられるわけがない。長いし深い。

　そもそも問題なのはタイムゾーンがない日付。こいつの対処は以下3パターンのはず。というか、ふつうはローカル日時として解釈するはず。ただ、SQLite3はUTCとして解釈する。なので一応全パターン網羅できるようにした。

メソッド|概要
--------|----
`if_native_to_local`|タイムゾーンがないときローカルのタイムゾーンとして解釈した日付型を返す
`if_native_to_utc`|タイムゾーンがないときUTCとして解釈した日付型を返す
`if_native_to_tz`|タイムゾーンがないとき指定したタイムゾーンとして解釈した日付型を返す

