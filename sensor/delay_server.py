import socket
import time


class DelayServer:
    def __init__(self, port=80, initial_delay=1.0, timeout=0.5):
        self.delay_s = initial_delay
        self.timeout = timeout
        self.port = port
        self.socket = None

    def start(self):
        s = socket.socket()
        s.bind(("0.0.0.0", self.port))
        s.listen(1)
        s.settimeout(self.timeout)
        self.socket = s

    def parse_request(self, request):
        try:
            if "GET /?delay=" in request:
                part = request.split("GET /?delay=")[1]
                val = part.split(" ")[0]
                return float(val)
        except:
            return None
        return None

    def build_page(self):
        return """\
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<body>
<h3>Sensor Read Delay</h3>
<form action="/" method="GET">
  <label>Delay (seconds):</label>
  <input type="text" name="delay">
  <input type="submit" value="Set">
</form>
<p>Current delay: %s seconds</p>
</body>
</html>
""" % self.delay_s

    def poll(self):
        try:
            conn, addr = self.socket.accept()
            req = conn.recv(1024).decode()

            new = self.parse_request(req)
            if new is not None:
                self.delay_s = new

            conn.send(self.build_page())
            conn.close()
        except:
            pass

    def get_delay(self):
        return self.delay_s


if __name__ == "__main__":
    print("Starting DelayServer self-test...")
    server = DelayServer(initial_delay=1.0)
    server.start()

    last = time.time()

    while True:
        server.poll()

        now = time.time()
        if now - last >= 2:
            last = now
            print("Current delay:", server.get_delay())
