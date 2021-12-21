import socket
import pickle
import struct
import threading


port = 6000

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)


socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()

socket_list = [server_socket]
clients = {}
print("Listening at",socket_address)

def show_client(addr,client_socket):
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket: # if a client socket exists
			data = b""
			payload_size = struct.calcsize("Q")
			while True:
				while len(data) < payload_size:
					packet = client_socket.recv(4*1024) # 4K
					if not packet: break
					data+=packet
				packed_msg_size = data[:payload_size]
				data = data[payload_size:]
				msg_size = struct.unpack("Q",packed_msg_size)[0]
				
				while len(data) < msg_size:
					data += client_socket.recv(4*1024)

				frame_data = data[:msg_size]
				data  = data[msg_size:]

				frame = pickle.loads(frame_data)
				client_socket.sendall(frame)
                
				text  =  f"CLIENT: {addr}"
				print(text)
				#cv2.imshow(f"FROM {addr}",frame)

                
				#key = cv2.waitKey(1) & 0xFF
				#if key  == ord('q'):
				#	break   
			#client_socket.close()
	except Exception as e:
		print(f"CLINET {addr} DISCONNECTED")
		pass

		
while True:
	client_socket,addr = server_socket.accept()
	thread = threading.Thread(target=show_client, args=(addr,client_socket))
	thread.start()
	print("TOTAL CLIENTS ",threading.activeCount() - 1)