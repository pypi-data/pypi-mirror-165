import socket
import threading
import select
import queue
import time
import pickle


def producer_get_connection(self):
    timeout_in_seconds = 0.1
    connection_dict = {}
    while self.signal:
        ready = select.select([self.producer_socket], [], [], timeout_in_seconds)
        if ready[0]:
            msg, client_address = self.producer_socket.recvfrom(1024)

            consumer_name = msg[0:20].decode('utf-8').strip(" ")
            consumer_request = msg[20:30].decode('utf-8').strip(" ")

            if consumer_request == "connect":
                if consumer_name in connection_dict:
                    old_client_address = connection_dict[consumer_name]
                    client_found = False
                    i = 0
                    while i < len(self.producer_client_list) and not client_found:
                        if self.producer_client_list[i] == old_client_address:
                            client_found = True
                            del self.producer_client_list[i]
                            print("deleted old address from consumer")
                        i += 1

                self.producer_client_list.append(client_address)
                respond_msg = "connection_success"
                respond_msg = pickle.dumps(respond_msg)
                self.producer_socket.sendto(respond_msg, client_address)
                connection_dict[consumer_name] = client_address
                if self.debug:
                    consumer_name = msg.decode('utf-8')
                    print(f"{consumer_name} connection established")

            if consumer_request == "disconnect":
                client_found = False
                i = 0
                while i < len(self.producer_client_list) and not client_found:
                    if self.producer_client_list[i] == client_address:
                        client_found = True
                        del self.producer_client_list[i]
                        print("disconnected consumer")
                    i += 1
                connection_dict.pop(consumer_name)
    self.producer_socket.close()
    self.socket_closed = True


def produce_alive_signal(self):
    while self.signal:
        pickle_msg = pickle.dumps("producer_alive")
        if len(self.producer_client_list):
            for i in range(len(self.producer_client_list)):
                self.producer_socket.sendto(pickle_msg, self.producer_client_list[i])
        time.sleep(0.2)


def consume_message_receiver(self):
    timeout_in_seconds = 0.5
    alive_timer = time.time()
    consumer_name = f"{self.name:<{20}}".encode('utf-8')
    con_dis = "connect"
    connect = f"{con_dis:<{10}}".encode('utf-8')
    message = consumer_name + connect

    while self.signal:
        consume_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        consume_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)
        consume_socket.sendto(message, (self.ip, self.port))
        ready = select.select([consume_socket], [], [], timeout_in_seconds)
        if ready[0]:
            msg, _ = consume_socket.recvfrom(65535)
            connection_status = pickle.loads(msg)
            #connection_status = msg[0:20].decode('utf-8').strip(" ")
            self.connection = True
            if connection_status == "connection_success":
                if self.debug:
                    print("successfully connected to producer")
            else:
                raise ValueError(connection_status)
        else:
            consume_socket.close()

        while self.signal and self.connection:
            ready = select.select([consume_socket], [], [], timeout_in_seconds)
            if ready[0]:
                msg, _ = consume_socket.recvfrom(65535)
                decoded_msg = pickle.loads(msg)

                if decoded_msg == "producer_alive":
                    alive_timer = time.time()
                else:
                    if not self.buffer:
                        if not self.msg_receive_queue.empty():
                            remove_old_data = self.msg_receive_queue.get()

                    self.msg_receive_queue.put(decoded_msg)
            else:
                if time.time() > alive_timer + 0.5:
                    self.connection = False
                    if not self.reconnect:
                        raise ConnectionError("Connection to producer timeout")

    if self.connection:
        con_dis = "disconnect"
        connect = f"{con_dis:<{10}}".encode('utf-8')
        disconnect_msg = consumer_name + connect
        consume_socket.sendto(disconnect_msg, (self.ip, self.port))
        consume_socket.close()
    self.socket_closed = True


class Produce(threading.Thread):
    def __init__(self, ip, port, debug=False):
        threading.Thread.__init__(self)
        self.signal = True
        self.ip = ip
        self.port = port
        self.producer_client_list = []
        self.debug = debug
        self.socket_closed = False

        self.producer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.producer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65535)
        socket_address = (self.ip, self.port)
        self.producer_socket.bind(socket_address)

        t_transmitter = threading.Thread(target=producer_get_connection, args=(self,))
        t_transmitter.daemon = True
        t_transmitter.start()

        t_alive = threading.Thread(target=produce_alive_signal, args=(self,))
        t_alive.daemon = True
        t_alive.start()

    def send_message(self, msg):
        pickle_msg = pickle.dumps(msg)
        if len(self.producer_client_list):
            for i in range(len(self.producer_client_list)):
                self.producer_socket.sendto(pickle_msg, self.producer_client_list[i])

    def close(self):
        self.signal = False
        while not self.socket_closed:
            time.sleep(0.1)


class Consume(threading.Thread):

    def __init__(self, consumer_name, ip, port, reconnect=True, blocking=True, buffer=False, debug=False):
        threading.Thread.__init__(self)
        self.signal = True
        self.ip = ip
        self.port = port
        self.name = consumer_name
        self.connection = False
        self.reconnect = reconnect
        self.blocking = blocking
        self.buffer = buffer
        self.test_queue = queue.Queue()
        self.debug = debug
        self.socket_closed = False
        self.msg_blocking = False

        t1 = threading.Thread(target=consume_message_receiver, args=(self,))
        t1.daemon = True
        t1.start()

        self.msg_receive_queue = queue.Queue()

    def get_msg(self):
        msg = None
        message = False
        self.msg_blocking = False

        if self.blocking:
            while self.signal and not message:
                try:
                    msg = self.msg_receive_queue.get(timeout=0.5)
                    message = True

                except:
                    pass
            self.msg_blocking = False
        else:
            if not self.msg_receive_queue.empty():
                msg = self.msg_receive_queue.get()
        return msg

    def close(self):
        self.signal = False
        while not self.socket_closed and self.msg_blocking:
            time.sleep(0.1)

