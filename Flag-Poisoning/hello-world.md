
# Hello World | Flag Poisoning CTF 
Bonjour à tous et à toute, aujourd'hui nous allons voir un challlenge du ctf private de [Flag Poisoning](https://flag-poisoning.fr).

![](https://i.ibb.co/MhcJ20w/hello-word.png)

Il s'agit du dernier crackme.
## Annalyse
Nous allons tout de suite procéder à une annalyse : 



    raphgui@Ret2Mint:~$ checksec --file=hello-world
    [*] '/home/raphgui/hello-world'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
Le binaire possède comme protection PIE qui va faire que à chaque lancement le programme aura ses adresses de fonction qui changeront


    raphgui@Ret2Mint:~$ file hello-world hello-world:
    ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=2ff8d69cea4901f4e01a0b6c906c18ee29af0e72, for GNU/Linux 3.2.0, not stripped
   On fait directement un file pour avoir des informations sur le binaire.
   On sait qu'il n'est pas strippé et que c'est du 64 bit.
### IDA
On va à présent le lancer dans [**IDA**](https://hex-rays.com/ida-free/) pour avoir une représentation du binaire. 

![](https://i.ibb.co/Bjw8ZG0/ida1.png)

Nous allons regarder le pseudo code :

  ```c
  int __cdecl main(int argc, const char **argv, const char **envp)
{
  char *v3; // rax
  char s2[38]; // [rsp+0h] [rbp-80h] BYREF
  char v6[10]; // [rsp+26h] [rbp-5Ah] BYREF
  char s1[26]; // [rsp+30h] [rbp-50h] BYREF
  char needle[6]; // [rsp+4Ah] [rbp-36h] BYREF
  char s[34]; // [rsp+50h] [rbp-30h] BYREF
  char v10[7]; // [rsp+72h] [rbp-Eh]
  char v11[3]; // [rsp+79h] [rbp-7h] BYREF
  int i; // [rsp+7Ch] [rbp-4h]

  v10[0] = 26;
  v10[1] = 16;
  v10[2] = 31;
  v10[3] = 31;
  v10[4] = 6;
  v10[5] = 54;
  v10[6] = 1;
  qmemcpy(v11, "DZR", sizeof(v11));
  puts("Hello. What's your name?");
  if ( fgets(s, 24, stdin) )
    s[strlen(s) - 1] = 0;
  else
    printf("\nFail to read the input stream");
  printf("Hi there, %s !\n\n", s);
  strcpy(needle, "nqzva");
  ces(13LL, needle);
  v3 = strstr(s, needle);
  if ( v3 )
  {
    puts("OH ! You Have an unread message ");
    printf("Please , type your SuperSecret Password : ");
    if ( fgets(s1, 24, stdin) )
      s1[strlen(s1) - 1] = 0;
    else
      printf("\nFail to read the input stream");
    qmemcpy(v6, "HelloWorld", sizeof(v6));
    for ( i = 0; i <= 9; ++i )
      s2[i] = v6[i] ^ v10[i];
    s2[i + 1] = 0;
    if ( strlen(s1) == 10 && !strcmp(s1, s2) )
      LODWORD(v3) = printf("\nGG , you can validate the challenge \n(Format : flag{username:password})");
    else
      LODWORD(v3) = printf("\nInvalid Password");
  }
  return (int)v3;
}
```
## Première Étape
On peut  voir le déroulement du programme, on va s'intéresser à la fonction strstr. Si on fait un man de cette fonction :

       char *strstr(const char *haystack, const char *needle);
Elle prend deux chaines de caractère comme argument.
Si nous mettons un breakpoint sur le strstr, nous pourrons alors voir les éléments qu'il aura en mémoire  avec gdb : 
```Assembly
    strstr@plt (
    $rdi = 0x007fffffffdd90 → "aaaaaaaaaaaa",
    $rsi = 0x007fffffffdd8a → 0x6161006e696d6461 ("admin"?),
    $rdx = 0x007fffffffdd8a → 0x6161006e696d6461 ("admin"?)
    )
 ```

Nous savons à présent que le nom d'utilisateur est "**admin**".
Cela va nous permettre de débloquer la seconde vérification, celle du mot de passe.

## Seconde Étape

Nous allons lire la seconde partie du code, nous allons avoir un **fgets** qui va prendre une entrée utilisateur et qui va mettre ce qui la obtenue dans **s1**.

La ligne qui va nous intéresser à présent est la condition pour avoir le flag :

<code>if ( strlen(s1) == 10 && !strcmp(s1, s2)) </code>

On sait qu'il faut que notre entrée utilisateur soit égale à 10. Si cette condition n'est pas respecté, il va direct jump sur **"Invalid Password**".
Il ne va pas tester la seconde condition.
Nous n'avons plus qu'a faire comme toute à l'heure, mettre un breakpoint sur strcmp :

           int strcmp(const char *s1, const char *s2);

Nous allons alors pouvoir voir ce qu'il a en mémoire avec gdb :
```Assembly
strcmp@plt (
   $rdi = 0x007fffffffdd70 → "1234567890",
   $rsi = 0x007fffffffdd40 → "Russian666",
   $rdx = 0x007fffffffdd40 → "Russian666"
)
```
On peut voir le mot de passe apparaître.

## Conclusion
C'était un challenge assez sympa. Il est encore disponible sur leur CTFd si certains veulent le faire. Il demande certaine notion en reverse. Je recommande !!

Le flag est "**flag{fait-frr}**".

Thanks for Reading :" )

