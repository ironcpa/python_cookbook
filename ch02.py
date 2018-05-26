from common_util import call_funcs
import re


# ====================================================
# 0201 splitting strings on any of multiple delimiters
# ----------------------------------------------------
def test_0201():
    line = 'asdf fjdk; afed, fjek,asdf,     foo'

    # \s가 따라오는 ;,\s 중 아무거나
    fields = re.split(r'[;,\s]\s*', line)
    print(fields)

    # () is capture group : 캡쳐그룹 사용 시 구분 결과에 포함됨
    #   - 어떤 구분자로 구분되었는지 확인에 유용
    fields = re.split(r'(;|,|\s)\s*', line)
    print(fields)
    #   - 구분자 모음을 활용할 수 있음
    values = fields[::2]
    delimeters = fields[1::2]
    reformed = ''.join(v + d for v, d in zip(values, delimeters))
    print(reformed)
    # (?:...) is non capture group : 그룹은 필요하지만 결과포함 안할때 사용
    fields = re.split(r'(?:;|,|\s)\s*', line)
    print(fields)


# ====================================================
# 0202 matching text at the start or end of a string
# ----------------------------------------------------
def test_0202():
    # startswith, endswith

    name = 'https:aaa.bbb.ccc/ddd'

    # tuple로 여러 매칭 조건 받을 수 있다.
    print(name.startswith(('http', 'https', 'ftp')))


# ====================================================
# 0203 matching strings using shell wildcard patterns
# ----------------------------------------------------
def test_0203():
    # fnmatch, fnmatchcase
    #  : unix style whildcard patterns
    #    파일명에 대한 와일드 카트 매칭 목적이지만
    #    용도만 맞으면 유사 패턴에 사용 가능
    from fnmatch import fnmatch, fnmatchcase

    # fnmatch : 시스템 기본 case-sensitivity 따름
    r = fnmatch('foo.txt', '*.txt')
    print(r)
    r = fnmatch('foo.txt', '?oo.txt')
    print(r)
    r = fnmatch('Dat45.csv', 'Dat[0-9]*')
    print(r)
    r = fnmatch('foo.txt', '*.TXT')
    print(r)  # unix: False, windows: True

    r = fnmatchcase('foo.txt', '*.TXT')
    print(r)  # 어디서나 False

    # file name 아니라도 유사한 패턴매칭에 사용하면 됨
    addresses = [
        '5412 N CLARK ST',
        '1060 W ADDISON ST',
        '1039 W GRANVILLE AVE',
        '2122 N CLARK ST',
        '4802 N BROADWAY',
    ]
    r = [addr for addr in addresses if fnmatchcase(addr, '* ST')]
    print(r)
    r = [addr for addr in addresses
         if fnmatchcase(addr, '54[0-9][0-9] *CLARK*')]
    print(r)


# ====================================================
# 0204 matching and searching for text patterns
# ----------------------------------------------------
def test_0204():
    # basic search with regex

    # basic example
    text = '11/27/2018'
    # use r'' for easy escape
    #  - r'' 방식   : r'\d+'
    #  - 일반문자열 : '\\d+'
    r = re.match(r'\d+/\d+/\d+', text)
    print(r)  # match object

    # if문으로 None 아닌지 체크
    if re.match(r'\d+/\d+/\d+', text):
        print('matched')

    # capture group : 검색 후 사후 처리 일부 수행 가능
    #  - group index에 주의 : 0번째는 기본 결과임!
    r = re.match(r'(\d+)/(\d+)/(\d+)', text)
    print(r)  # match object
    print(r.group(0))  # 기본 결과 : 전체 11/27/2018
    print(r.group(1))  # 그룹1 : 11
    print(r.group(2))  # 그룹2 : 27
    print(r.group(3))  # 그룹3 : 2018
    print(r.groups())  # ('11', '27', '2018')
    #  - 그룹 활용예
    month, day, year = r.groups()

    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
    # comple to reuse pattern
    datepattern = re.compile(r'(\d+)/(\d+)/(\d+)')
    # 모든 결과 찾을 때 findall()
    r = datepattern.findall(text)
    # findall 결과는 list : 각 원소는 groups() 결과와 같음
    print(r)  # [('11', '27', '2012'), ('3', '13', '2013')]
    # finditer : findall 결과를 list대신 match로 받고 싶을때
    for m in datepattern.finditer(text):
        print(m.groups())

    # 특정 문자열 exact match 찾을 때 : $ 붙이기(end marker)
    datepattern = re.compile(r'(\d+)/(\d+)/(\d+)$')
    r = datepattern.match('11/27/2018aefawefw')
    print(r)
    r = datepattern.match('11/27/2018')
    print(r)

    # for instant matching, use module level function
    #  - re.findall('patter', text)
    re.findall(r'(\d+)/(\d+)/(\d+)', text)


# ====================================================
# 0205 searching and replacing text
# ----------------------------------------------------
def test_0205():
    # replace a text
    # --------------

    # simple way : str.replace()
    text = 'yeah, but no, but yeah, but no, but yeah'
    r = text.replace('yeah', 'yep')
    print(r)

    # for complicated patterns : re.sub()
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
    #  - \1, \2, \3 ... is capture group
    r = re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text)
    print(r)  # Today is 2012-11-27. PyCon starts 2013-3-13.
    #  - same thing with pattern
    datepattern = re.compile(r'(\d+)/(\d+)/(\d+)')
    r = datepattern.sub(r'\3-\1-\2', text)
    print(r)

    # for more! complicated patterns : use callback function
    #  - callback function 은 match 객체를 받는 함수!
    def change_date(m):
        from calendar import month_abbr
        mon_name = month_abbr[int(m.group(1))]
        return '{} {} {}'.format(m.group(2), mon_name, m.group(3))
    r = datepattern.sub(change_date, text)
    print(r)

    # use subn() to get match counts
    r, n = datepattern.subn(r'\3-\1-\2', text)
    print(r, n)


# ====================================================
# 0206 searching and replacing case-insensitive text
# ----------------------------------------------------
def test_0206():
    # use re.IGNORECASE flag to ignore case

    text = 'UPPER PYTHON, lower python, Mixed Python'
    #  - findall 에 사용한 예
    r = re.findall('python', text, flags=re.IGNORECASE)
    print(r)  # ['PYTHON', 'python', 'Python']
    #  - sub 에 사용한 예
    r = re.sub('python', 'snake', text, flags=re.IGNORECASE)
    print(r)  # 'UPPER snake, lower snake, Mixed snake'

    #  - 함수를 이용해 sub 조건을 변경한 예
    def matchcase(word):  # 찾은 단어와 동일한 case 적용하기
        def replace(m):
            text = m.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.capitalize()
            else:
                return word
        return replace
    r = re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
    print(r)


# ====================================================
# 0207 longest vs shortest match pattern
# ----------------------------------------------------
def test_0207():
    # longest vs shortest match
    #  - regex 기본은 longest match 검색
    #  - shortest match 검색 방법도 있다
    #    - capture group에 * or + 뒤에 ? 를 사용한다. : *는 이런 패턴에 원래 들어가므로

    # longest match 예 : default
    p = re.compile(r'\"(.*)\"')
    t1 = 'Computer says "no."'
    r = p.findall(t1)
    print(r)  # no.
    t2 = 'Computer says "no." Phone says "yes."'
    r = p.findall(t2)
    print(r)  # "no." Phone says "yes." - 가장 바깥으로 확장된 검색이 됨!

    # shortes match : use ?
    p = re.compile(r'\"(.*?)\"')
    r = p.findall(t2)
    print(r)  # "no.", "yes."


# ====================================================
# 0208 multiline search pattern
# ----------------------------------------------------
def test_0208():
    # multi line search

    t1 = '/* this is a comment */'
    t2 = '''/* this is a \n
          multiline comment */'''

    # fail case
    p = re.compile(r'/\*(.*?)\*/')
    r = p.findall(t1)
    print(r)  # matched
    r = p.findall(t2)
    print(r)  # no match

    # success case
    #  - add newline math case
    #    - (?:) is non capture group
    p = re.compile(r'/\*((?:.|\n)*?)\*/')
    r = p.findall(t2)
    print(r)
    #  - or use re.DOTALL flag
    #    - it makes . match all charactors : including \n
    #    - 이 방법은 상황에 따라 다른 패턴과 충돌할 수 있다!
    p = re.compile(r'/\*(.*?)\*/', re.DOTALL)
    r = p.findall(t2)
    print(r)


# ====================================================
# 0209 normalize unicode
# ----------------------------------------------------
def test_0209():
    pass


# ====================================================
# 0210 unicode in pattern
# ----------------------------------------------------
def test_0210():
    pass


# ====================================================
# 0211 strip unwanted characters
# ----------------------------------------------------
def test_0211():
    #  - 양 끝단 제거 : str.strip() | lstrip() | rstrip()
    #  - 중간 제거 : str.replace(), re.sub('\s+', '', s)
    pass


# ====================================================
# 0213 normalize unicode
# ----------------------------------------------------
def test_0213():
    # align string
    #  - str.ljust, rjust, center

    s = 'Hellow World'

    r = s.ljust(20)
    print('[', r, ']')
    r = s.rjust(20)
    print('[', r, ']')
    r = s.center(20)
    print('[', r, ']')

    #  - decoration | padding
    r = s.ljust(20, '=')
    print('[', r, ']')
    r = s.center(20, '*')
    print('[', r, ']')

    #  - format function
    r = format(s, '>20')  # right
    print('[', r, ']')
    r = format(s, '<20')  # left
    print('[', r, ']')
    r = format(s, '^20')  # center
    print('[', r, ']')

    #  - format w/ padding
    r = format(s, '=>20')
    print('[', r, ']')

    #  - multiple fields str.format
    r = '{:>10s} {:>10s}'.format('hello', 'world')
    print('[', r, ']')


# ====================================================
# 0214 how to concat strings
# ----------------------------------------------------
def test_0214():
    # concat strings
    #  - use str.join()
    #  - use + operator or +=
    #  - use 단순 나열 for str lterals

    # literal 나열 예
    s = 'hello' 'world' 'hahaha'
    print(s)

    # pretty print w/ separator
    a, b, c = 'aaa', 'bbb', 'ccc'
    print(a, b, c, sep=':')


# ====================================================
# 0215 using variables in format string fields
# ----------------------------------------------------
def test_0215():
    # format 에서 변수명 사용하기
    #  - {변수명} : format(변수명=값}

    s = '{name} has {n} messages'

    r = s.format(name='Guido', n=37)
    print(r)

    # format_map : object의 field명과 format문자열 매칭
    class Info:
        def __init__(self, name, n):
            self.name = name
            self.n = n

    a = Info('Augie', 37)
    print(vars(a))  # vars() 는 현재 scope의 fields dict, vars(a)는 a의 fields
    r = s.format_map(vars(a))
    print(r)

    # format_map w/ missing match
    #  - use __missing__ function : missing as default
    class safesub(dict):
        def __missing__(self, key):
            return '{' + key + '}'
    v = {'name': 'Augie'}
    r = s.format_map(safesub(v))
    print(r)


# ====================================================
# 0216 text wrapping
# ----------------------------------------------------
def test_0216():
    import textwrap
    import os

    s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

    r = textwrap.fill(s, 70)
    print(r)

    # format w/ terminal size
    r = textwrap.fill(s, os.get_terminal_size().columns)
    print(r)


# ====================================================
# 0217 replace html tags
# ----------------------------------------------------
def test_0217():
    import html

    # html escape characters
    #  - use html.escape()
    s = 'Elements are written as "<tag>text</tag>".'
    print(s)
    e = html.escape(s)
    print(e)

    #  - ignore quotes on escape()
    e = html.escape(s, quote=False)
    print(e)


# ====================================================
# 0218 tokeizing text w/ composite pattern
# ----------------------------------------------------
def test_0218():
    text = 'foo = 23 + 42 * 10'

    # 조합될 단위 패턴을 만든다
    #  - 패턴명을 사용 : ?P<패턴명>
    NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
    NUM = r'(?P<NUM>\d+)'
    PLUS = r'(?P<PLUS>\+)'
    TIMES = r'(?P<TIMES>\*)'
    EQ = r'(?P<EQ>=)'
    WS = r'(?P<WS>\s)'

    # 단위패턴들로 조합패턴을 만든다
    #  - 조합 순서는 우선순위를 의미하므로 중요하다
    comp_pattern = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))
    #  - 중간에 매칭 안되면 중단된다, 즉 delimiter를 제외할 수 없다
    #    - 아래 패턴은 \s 만나면 중단된다
    #    - 단, genexp 등으로 간단히 filter 가공하여 사용할 수 있다
    # comp_pattern = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ]))

    # scatter 객체를 만든다
    scanner = comp_pattern.scanner('foo = 42')
    s = scanner.match()
    print(s)
    # scanner.match() 로 결과를 한 건 씩 얻는다
    #  - 패턴명 : lastgroup, 결과 : group()
    print("'{}', '{}'".format(s.lastgroup, s.group()))

    #  - 결과 나올때까지 실행한다
    s = scanner.match()
    while s:
        print("'{}', '{}'".format(s.lastgroup, s.group()))
        s = scanner.match()

    # 종합 예시
    scanner = comp_pattern.scanner(text)
    print("tokenize w/ scanner for '{}'".format(text))
    s = scanner.match()
    while s:
        print("\t'{}', '{}'".format(s.lastgroup, s.group()))
        s = scanner.match()

    # generator function 으로 정리한 예
    from collections import namedtuple
    Token = namedtuple('Token', ['type', 'value'])

    def generate_tokens(p, t):
        scanner = p.scanner(t)
        for m in iter(scanner.match, None):
            yield Token(m.lastgroup, m.group())  # generator

    #  - usage
    for tok in generate_tokens(comp_pattern, 'foo = 42'):
        print(tok)
    for n, t in generate_tokens(comp_pattern, 'foo = 42'):
        print("pattern={}: token='{}'".format(n, t))
    #  - 검출 제외 filtering : 단순 genexp
    tokens = (tok for tok in generate_tokens(comp_pattern, text)
              if tok.type != 'WS')
    for t in tokens:
        print(t)


# ====================================================
# 0219 나만의 프로그래밍 언어 구문 파서 만들기 : too long
# ----------------------------------------------------


# ====================================================
# 0220 about byte string
# ----------------------------------------------------
def test_0220():
    # byte string은 대부분의 str 함수가 적용된다
    #  - 대신 주어진 타입은 byte string 여야 함 : regex도 마찬가지
    b = b'Hello World'
    print(b[0:5])
    print(b.startswith(b'Hello'))
    # print(b.startswith('Hello'))  # type error!
    print(b.split())
    print(b.replace(b'Hello', b'Yello'))
    print(re.split(b'[:,]', b'FOO:BAR,SPAM'))
    #  - bytearray로 만들어도 동일하게 적용됨
    ba = bytearray(b)
    print(ba[0:5])  # 나머지 함수도 결과 같음

    # byte string 만의 특징들
    #  - 단위요소는 숫자로 나옴옴
    #  - format 함수 없음


def test_022001():
    # byte string to string
    b = b'Hello World'
    s = str(b, 'utf-8')
    print(b, s)


if __name__ == '__main__':
    call_funcs(vars(), lambda s: s.startswith('test_'))
