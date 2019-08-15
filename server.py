import socket
import select
import time
import re


class HTTPServer():
    URL_REGEX = re.compile(b'GET ([^ ]+) HTTP/\d.\d')
    URL_REWRITE = {}

    def __init__(self, ip, port, timeout=5, max_request=10000, listen=200):
        self.socket = socket.socket()
        self.socket.bind((ip, port))
        self.socket.listen(listen)
        self.socket.setblocking(False)
        self.timeout = timeout
        self.max_request = max_request
        self.listen = listen

    def serve(self):
        s = self.socket
        connect_data = [None] * 10000
        timeout_data = []
        timeout = self.timeout
        max_request = self.max_request
        listen = self.listen
        while True:
            now = time.time()
            read_conns = [connect_data[i[1]][3] for i in timeout_data] + [s]
#            try:
#                write_conns = [connect_data[i[1]][3] for i in timeout_data if connect_data[i[1]][2]]
#            except TypeError:
#                print(timeout_data)
#                print(read_conns)
#                exit()
            if read_conns:
                reading, _, _ = select.select(read_conns, [], [], timeout)
            else:
                reading, writing = [], []
            for conn in reading:
                fileno = conn.fileno()
                if fileno == s.fileno():
                    try:
                        new, caddr = s.accept()
                        new_fileno = new.fileno()
                        connect_data[new_fileno] = [now, b'', b'', new]
                        timeout_data.append((now + timeout, new_fileno))
                        if len(timeout_data) % 10 == 0:
                            print('New connection:', caddr, 'total',
                                  len(timeout_data), 'connections')
                    except OSError as error:
                        print(error)  # Ran out of sockets for some reason
#                        now += 0.5  # Make oldist ones time out
                    continue
                i = connect_data[fileno]
                try:
                    data = conn.recv(max_request)
                except ConnectionResetError:
                    print('CRE')
                    connect_data[fileno] = None
                    for pos, d in enumerate(timeout_data):
                        if d[1] == fileno:
                            del timeout_data[pos]
                            break
                    continue
                i[1] += data
                if not data or len(i[1]) > max_request:
                    connect_data[fileno] = None
                    for pos, d in enumerate(timeout_data):
                        if d[1] == fileno:
                            del timeout_data[pos]
                            break
                elif i[1].endswith(b'\r\n\r\n') or i[1].endswith(b'\n\n'):
                    headers = self.parse_request(i[1])
                    if isinstance(headers, dict):
                        print('New request @ %s total %s connections' % (
                            headers[b'URL'], len(timeout_data)))
                        code, headers, data = self.generate_response(caddr,
                                                                     headers)
                        response = [b'HTTP/1.0 %s' % code]
                        for key in headers:
                            response.append(b'%s: %s' % (key, headers[key]))
                        response.append(b'')
                        response.append(data)
                        conn.sendall(b'\r\n'.join(response))
                        connect_data[fileno] = None
                        for pos, d in enumerate(timeout_data):
                            if d[1] == fileno:
                                del timeout_data[pos]
                                break
                        conn.close()
                    else:
                        print('Invalid request', i[1])
                        connect_data[fileno] = None
                        for pos, d in enumerate(timeout_data):
                            if d[1] == fileno:
                                del timeout_data[pos]
                                break
                        conn.close()
#            for conn in writing:
#                fileno = conn.fileno()
#                i = connect_data[fileno]
#                if i is None:
#                    for pos, d in enumerate(timeout_data):
#                        if d[1] == fileno:
#                            del timeout_data[pos]
#                            break
#                    continue
#                amount = conn.send(i[2])
#                if amount < len(i[2]):
#                    i[2] = i[2][amount:]
#                else:
#                    connect_data[fileno] = None
#                    for pos, d in enumerate(timeout_data):
#                        if d[1] == fileno:
#                            del timeout_data[pos]
#                            break
#                    conn.close()
            i = 0
            tlen = len(timeout_data)
            while tlen > i and timeout_data[i][0] < now:
                try:
                    connect_data[timeout_data[i][1]][3].close()
                    connect_data[timeout_data[i][1]] = None
                except KeyError:
                    pass
                i += 1
            if i > 0:
                del timeout_data[:i]

    def parse_request(self, request):
        try:
            url_data, *lines = request.splitlines()[:-1]
            url_match = self.URL_REGEX.match(url_data)
            if url_match:
                headers = {b'URL': self.URL_REWRITE.get(url_match.group(1),
                                                        url_match.group(1))}
                for i in lines:
                    key, *data = i.split(b': ')
                    data = b': '.join(data)
                    headers[key] = data
                return headers
        except ValueError:
            pass

    def generate_response(self, caddr, headers):
        code = b'200 OK'
        headers = {b'Server': b'PyServer/0.1',
                   b'Content-Type': b'text/html'}
        data = b'This is the default function for HTTPServer'
        return code, headers, data
