# Unpackme [300] 

Aujourd'hui nous allons voir un challenge du Pico CTF. C'est un challenge
de reverse engineering. Nous avons alors juste un binaire et comme consigne  : "Can you get the flag?".

## Analyse du binaire

On a notre binaire qui se nomme unpackme-upx. Son nom est assez explicite, il s'agit d'un binaire packé avec [UPX](https://upx.github.io/).
Nous allons alors essayé de récuperer des informations sur le binaire :
```bash
raphgui@Ret2Mint ~/Documents> file unpackme-upx 
unpackme-upx: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, no section header
```
On va utiliser [DIE](https://github.com/horsicq/Detect-It-Easy), pour avoir un analyse plus approfondie.
  
![DIE](https://i.ibb.co/qCf2Sfh/upx-die.png)

On retrouve donc notre UPX, on a la version ainsi que la façon dont il a été packé.

## Unpacking

Pour l'unpack ça va être très simple, car UPX propose un option d'unpack tels que :

```bash
raphgui@Ret2Mint:~$ upx
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2018
UPX 3.95        Markus Oberhumer, Laszlo Molnar & John Reiser   Aug 26th 2018

Usage: upx [-123456789dlthVL] [-qvfk] [-o file] file..

Commands:
  -1     compress faster                   -9    compress better
  -d     decompress                        -l    list compressed file
  -t     test compressed file              -V    display version number
  -h     give more help                    -L    display software license
Options:
  -q     be quiet                          -v    be verbose
  -oFILE write output to 'FILE'
  -f     force compression of suspicious files
  -k     keep backup files
file..   executables to (de)compress

Type 'upx --help' for more detailed help.

UPX comes with ABSOLUTELY NO WARRANTY; for details visit https://upx.github.io
```

Nous n'avons plus qu'a faire un **"upx -d < binaire >"** :

```bash
raphgui@Ret2Mint:~/Documents$ upx -d unpackme-upx 
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2018
UPX 3.95        Markus Oberhumer, Laszlo Molnar & John Reiser   Aug 26th 2018

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
   1002408 <-    379116   37.82%   linux/amd64   unpackme-upx

Unpacked 1 file.
```

##  Get a flag 
Nous avons désormais notre binaire unpacké, plus qu'a le reverse. On le lance dans IDA.
	![enter image description here](https://i.ibb.co/hYjfGvx/ida-unpack.png)Nous avons alors notre code en assembleur. On peut voir les fonctions de libc (scanf, puts..)
Nous pouvons voir un saut conditionelle (*jnz*) qui saute sur la fonction "Mauvais Pass".
Nous n'avons plus qu'a modifier le saut :

```assembly
jz     short loc_401F42
```
Nous allons directement sauter sur good passord et avoir notre flag.

## Conclusion 

Voici notre flag :
 

    raphgui@Ret2Mint:~/Documents$ ./unpackme-upx What's my favorite number? pass
    picoCTF{up><_m3_f7w_5769b54e}
Ce challenge était assez cool, je le conseil.
Merci d'avoir lu <3
