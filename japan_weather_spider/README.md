# Weather Spider

A spider to fetch historical weather information from
[Japan Meteorological Agency](https://www.data.jma.go.jp/obd/stats/etrn/view/daily_s1.php).

Just for fun.

P.S. Python's list duplication is a devil! If you do `l = [[]]*20` and then `l[0].append('hello')` you'll end up
getting `[['hello']]*20`! Cost me so much time!

P.P.S If anyone sees this and know how to solve please leave an issue or something:

Pycharm throws `ImportError: DLL load failed` when importing SSL. The reason I need SSL is that `requests` needs it when
performing `https` requests. Later I changed "https://" to "http://" as a workaround.

I added `weather1.py` for testing.

* OpenSSL is up-to-date
* I use Anaconda2
* Interpreter is selected but displays "non-zero exit code" when viewing libraries in PyCharm
* In Anaconda Prompt, Python Console, and Terminal (both as in PyCharm), SSL can be imported correctly
* Python 3.6.5
* PATH include `C:\<path>\Anaconda2\`, `C:\<path>\Anaconda2\Library\bin\`, `C:\<path>\Anaconda2\Scripts\`
* Didn't try reinstalling

If no one sees this... then let it just be a note for me.
