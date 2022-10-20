タイムゾーン無しにタイムゾーンを付ける【Python】

　`aware`/`native`とかいうクソ概念をぶち殺す！

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
    @classmethod # タイムゾーン付きであるか否か
    def is_aware(cls, dt: datetime.datetime): return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None
    @classmethod # nativeならawareなUTC標準時に変換して返す
    def to_aware(cls, dt: datetime.datetime): return dt if cls.is_aware(dt) else dt.astimezone(tz=datetime.timezone.utc)
    @classmethod # awareならnativeに変換して返す
    def to_native(cls, dt: datetime.datetime, tz=None): # タイムゾーンを付与したawareなローカル時刻にする(tzinfo=Noneでなく)
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
```

# 日時の基礎

　[datetime][]を使う。

[datetime]:https://docs.python.org/ja/3/library/datetime.html

　Pythonの日付はタイムゾーンがある場合とない場合がある。これが諸悪の根源。それぞれ以下のように呼ぶ。

呼び方|意味
------|----
`aware`|タイムゾーンがある日付型インスタンス
`native`|タイムゾーンがない日付型インスタンス

　は？　ってなる。

## `aware`/`native`とかいうクソ概念

　`aware`/`native`の2種類があるせいで日付処理の複雑さが爆上がる。タイムゾーンは`tzinfo`で取得できるが`native`な日付型は`tzinfo`が`None`になる。PythonはNULL安全でないレガシー言語なので`None`とそうでない場合の条件分岐が大変。クソにクソが上塗りされてクソコードになる。

　というわけで`aware`/`native`の区別がない世界にしたい。すべての日付型はタイムゾーンをもっているようにしたい。今回はそれを実装した。

## Pythonの[datetime][]を確認する

```python
import datetime
aware = datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00')
native = datetime.datetime.fromisoformat('2000-01-01T00:00:00')
assert aware.tzinfo == datetime.timezone.utc
assert native.tzinfo == None
```

　タイムゾーンは`tzinfo`で取得する。基本的にはUTCとNoneの2パターン。

　タイムゾーンがないときは`tzinfo`が`None`になる。これをなくして実行環境に応じたタイムゾーンを付与したい。

　システムのタイムゾーン情報を取得する方法は以下。ネイティブ日時を`astimezone()`する。私の実行環境である日本`"Asia/Tokyo"`なら`+09:00`。秒で表すと`32400`。名前は`JST`。

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

　`astimezone()`には`tzinfo`が引数にある。なので取得した`32400`をここで指定できれば万事解決していた。が、残念ながら以下エラーが出る。なんでや！

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

　この方法には致命的な問題がある。実行環境のタイムゾーンが取得できないことだ。

　世界中のどこかで実行したとき、それぞれの地域に応じたタイムゾーンを取得したい。その問題を解決する方法がどこにもない。`None`はそもそもタイムゾーンがないし、`utc`はUTC標準時`+00:00`。`Asia/Tokyo`とかいう地域名のテキストは実行マシンごとに自分の地域名を取得できれば解決するのだが、そんな方法はどこにもないっぽい。そんなバカな……。

　というわけで、自分で工夫して作るしかなかった。

　先ほど取得したシステムのタイムゾーン（UTC標準時との時差`32400`秒）をうまいこと利用してタイムゾーンがない日付にそのシステムのタイムゾーンをセットしてやりたい。それが今回実装した`to_native(dt)`メソッド。

## nativeな日付にタイムゾーンをつける

```python
def to_native(cls, dt: datetime.datetime, tz=None):
    dt2 = cls.to_utc(dt) + (datetime.timedelta(seconds=cls.native_tz()) * -1)
    return datetime.datetime.fromisoformat(f"{dt2:%Y-%m-%dT%H:%M:%S}{cls.native_tz_iso()}")
```

　`to_native`の`native`はタイムゾーンがない日付のことではなく、単に現地時間のこと。もちろんタイムゾーン付き。ふつうはそう思うはず。私はそう思う。なので紛らわしいが`native`の名前を使った。

　`to_native()`は以下のようなメソッドを呼び出している。

```python
def to_utc(cls, dt: datetime.datetime): return dt.astimezone(tz=datetime.timezone.utc)
def native_tz(cls): return cls.offset(datetime.datetime.now())
def native_tz_iso(cls): return cls.tz_iso(cls.offset(datetime.datetime.now()))
def offset(cls, dt: datetime.datetime): return cls.offset(dt.astimezone()) if dt.tzinfo is None else dt.tzinfo.utcoffset(dt).seconds
```

　UTC標準時からの時差が取得できるので、それを起点にして頑張った。まず渡された日付をUTC日時に変換する。そこからシステムのタイムゾーン時差分だけ引く。その日付の年月日時分秒とシステムのタイムゾーン時差をISO8601形式にして`datetime.fromisoformat()`で日付型インスタンスを生成した。日付の計算はすべてPythonで実装済みのものを使うよう小細工を弄した。

# タイムゾーンがない`native`時刻が何のためにあるのかわからない

　`aware`だけでいいと思う。もう哀れとしか読めない。`native`は一体だれのためにあるのか理解できない。そのくせ内部では`astimezone()`でちゃんと計算できている様子。タイムゾーンの`tzinfo`は`None`なのにどういうこと？　って思う。内部にタイムゾーンがあるから計算できるはず。なら最初からタイムゾーンを指定しないときは自分の地域のタイムゾーンを指定してほしかった。そうすれば今回自分で実装する必要なかったのに。

# 時間ってなんだっけ？

　きっと`native`の存在理由はある。何か複雑な事情があるのだろう。

　時間はむずかしい。タイムゾーンだのサマータイムだの、時間というやつは政治の都合でコロコロ変えられてしまう面があるようだし。時間は絶対的なものでなく宗教みたいなものなのかもしれない。それともじつは地球の公転や自転の速さは微妙に変わったりしているのか？　時間とかいう概念がむずかしすぎる。

　そんな細かいことどうでもいいのだけど、きっちり決めないと定義できないし。偉い人に頑張ってもらうしかない。もっとアホでも使える簡単なのにしてほしい。

-----------------------------------------------------------------------










　だったらどうして最初からタイムゾーンを指定しないときは自分の地域のタイムゾーンを指定してほしいのだが。なぜ`None`にした？　たぶん手抜きしたのだろう。結局、自分で超頑張って調べて書かねばならなかった。





dt.tzinfo.utcoffset(dt).seconds #=> 32400

datetime.datetime.timezone.utcoffset(tokyo)




メソッド|概要
--------|----
`from_isoz(s)`|ISO-8601の末尾`Z`日時書式テキストから日付型インスタンスを返す
`to_isoz(dt)`|日付型インスタンスからISO-8601の末尾`Z`日時書式テキストを返す

メソッド|概要
--------|----
`from_sqlite(s)`|`yyyy-MM-dd HH:mm:ss`形式テキストをUTC標準時として解釈し日付型インスタンスを返す
`to_sqlite(dt)`|日付型インスタンスをUTC標準時にして`yyyy-MM-dd HH:mm:ss`形式テキストで返す


```python
def test_from_isoz(self):
    actual = AwareDateTime.from_isoz('2000-01-01T00:00:00Z')
    self.assertEqual(datetime.datetime.fromisoformat('2000-01-01T00:00:00+00:00'), actual)
    self.assertEqual(datetime.timezone.utc, actual.tzinfo)
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
```


