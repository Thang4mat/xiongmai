import threading
import time

a = '116.105.'
def ipgen():
	start_time = time.time()
	for i in range(1,256):
		ip = str(a) + str(i)
		for i in range(1,256):
			ip2 = ip + '.' + str(i)
			#for i in range(1,256):
				#ip3 = ip2 + '.' + str(i)

			file = open('list.txt', 'a')
			file.write(ip2 + '\n');
			file.close()

	print('\n''Done. Saved result to \'list.txt\'')
	print('\n''EXIT')
	print("--- %s seconds ---" % (time.time() - start_time))

t = threading.Thread(target=ipgen)
t.start()
