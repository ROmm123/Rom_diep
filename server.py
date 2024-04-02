import socket
import threading

# Define the handle_client function

def print_data(data):
    # Process received data
    '''
    z_info, rectangle_info = data.split(",")
    # Process circle info
    circle_data = circle_info.split()
    circle_center_x = float(circle_data[1])
    circle_center_y = float(circle_data[2])
    circle_radius = float(circle_data[3])
    print("circle_x :" + str(circle_center_x) + " circle_y :" + str(circle_center_y) + " circle_radius :" + str(circle_radius))

    # Process rectangle info
    rectangle_data = rectangle_info.split()
    rect_center_x = float(rectangle_data[1])
    rect_center_y = float(rectangle_data[2])
    rect_width = float(rectangle_data[3])
    rect_height = float(rectangle_data[4])
    rotation_angle = float(rectangle_data[5])
    print("rect_x:" + str(rect_center_x) + " rect_y :" + str(rect_center_y) + " rect_width :" + str(rect_width) + " rect_height: "
          + str(rect_height) + " rotation_angle: " + str(rotation_angle))
'''


def handle_client(client_socket, client_number):
    print("entered thread")
    while True:
        data = client_socket.recv(2048).decode("utf-8")
        print_data(data)
        #print("data: " + data)
        if not data:
            print(f"Client {client_number} disconnected.")
            client_socket.close()
            break
        #print(f"Received position from client {client_number}: {data}")
        # Forward data to the other client
        num ='0'
        if len(clients) > 1:

            other_client_socket = clients[1 - client_number]
            other_client_socket.send(data.encode("utf-8"))
            #print("packet is sent")
        else:
            print ("ho yeah")
            num_data = num.encode()
            client_socket.send(num_data)
            #print ("sent!")
# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 10008))
server_socket.listen(5)
print("Server listening ")

# Initialize the clients list
clients = []
clients_lock = threading.Lock()  # Create a lock for thread safety

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        with clients_lock:
            clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, len(clients) - 1))
        client_thread.start()

except KeyboardInterrupt:
    print("Server interrupted by user.")

finally:
    # Close all client sockets
    with clients_lock:
        for client_socket in clients:
            client_socket.close()

    # Close the server socket
    server_socket.close()
