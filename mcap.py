import requests
import hashlib
import time

def uint8(n):
    u8 = 0
    for i in range(n):
        u8 += 1
        if u8 == 256:
            u8 = 0
    return u8

def s(e):
    n = len(e)
    t = [(255 & n) >> 0, (65280 & n) >> 8, (16711680 & n) >> 16, (4278190080 & n) >> 24, (0xff00000000 & n) >> 32, (0xff000000000 & n) >> 48, (0xff00000000000 & n) >> 56, int((0xff0000000000000 & n) >> 64)]
    return t + [ord(c) for c in e]

def score(e):
    t = 0
    n = 15
    while True:
        t += 256 ** (16 - (n + 1)) * uint8(e[n])
        n -= 1
        if not n >= 0:
            break
    return t

def stepped_generate_work(salt, string, difficulty_factor):
    u = salt + "".join(chr(n) for n in s(string))
    n = 340282366920938463463374607431768211455
    l = d = p = 0
    f = n - n / difficulty_factor
    while d < f:
        if p < 5000:
            l += 1
            e = hashlib.sha256((u + str(l)).encode()).digest()
            d = score(e)
            p += 1
        else:
            p = 0
    return {"result": str(d), "nonce": l}

def solve(sitekey, endpoint):
    r = requests.post(f"{endpoint}/api/v1/pow/config", json={
        "key": sitekey
    })
    start = time.time()
    try:
      config = r.json()
      t = stepped_generate_work(config["salt"], config["string"], config["difficulty_factor"])
    except:
        return r.text
    r = requests.post(f"{endpoint}/api/v1/pow/verify", json={
        "key":sitekey,
        "nonce":t["nonce"],
        "result":t["result"],
        "string": config["string"],
        "time":int((time.time()-start)*1000),
        "worker_type":"wasm"
    })
    if "token\":" in r.text:
        return r.json()["token"]
    else:
        return r.text
