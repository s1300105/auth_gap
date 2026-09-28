CASES = [
    # controls
    "localhost", "127.0.0.1", "localhost:8080", "[::1]:8080", "user:pw@localhost", "localhost:pw@evil.example",
    "http://localhost:8080", "localhost.", "evil.example",
    # IPv6 special ranges that Python's is_private includes
    "[::ffff:8.8.8.8]", "[::ffff:8.8.8.8]:443", "::ffff:8.8.8.8", "user@[::ffff:8.8.8.8]",
    "[2002:808:808::1]", "[2002:808:808::1]:80",        # 6to4 of 8.8.8.8
    "[2001:0:4136:e378:8000:63bf:3fff:fdd2]",           # Teredo
    "[64:ff9b::808:808]", "[64:ff9b:1::808:808]",       # NAT64 well-known / local-use
    "[2001:db8::1]", "[fec0::1]", "[100::1]",
    "[fe80::1%eth0]", "[fe80::1%25eth0]", "fe80::1%eth0",
    "[::1%@evil.example]",
    # IPv4 special
    "0.0.0.0", "0", "0.0.0.0:8000", "192.0.2.1", "198.51.100.7", "203.0.113.9", "198.18.0.1", "240.0.0.1",
    "100.64.0.1", "169.254.169.254", "192.0.0.9", "192.0.0.10", "255.255.255.255",
    # numeric forms that clients resolve through inet_aton
    "2130706433", "0x7f000001", "0177.0.0.1", "127.1", "0x7f.1", "010.0.0.1",
    "127.0.0.1.", "10.0.0.1.",
    # names
    "LOCALHOST", "localhost..", "localhost.evil.com", "evil.com.localhost", "printer.local", "localhost.:8080",
    "xn--localhost", "ｌｏｃａｌｈｏｓｔ",  # fullwidth localhost
    "local​host",
    # userinfo / odd chars
    "evil.example@localhost", "localhost@evil.example", "a@b@localhost", "evil.example%40localhost",
    "localhost evil.example", "evil.example .localhost", "localhost\t@evil.example", "evil.example\t@localhost",
    "localhost\\@evil.example",
    # schemes / full URLs left unsplit
    "unix:///var/run/docker.sock", "http+unix://%2Fvar%2Frun%2Fdocker.sock", "file://localhost",
    "http://[::1", "http://[v1.fe80::a+en1]",
    # whitespace
    " localhost", "localhost ", "\nlocalhost",
]
