# тулсу которая ломает шифрование на xor е
import requests

xor = lambda A, B: bytes([a^b for a, b in zip(A, B)])

URL = "https://t-capybit-kdot8z7j.spbctf.org"

print("[.] Регистрация короткого имени пользователя")
res = requests.post(f"{URL}/register", data={"username": "qwe"}, allow_redirects=False)
short_cook = res.cookies['session']
print(f"[*] Короткое куки: {short_cook}")

print("[.] Регистрация длиного имени пользователя")
res = requests.post(f"{URL}/register", data={"username": "q"*100}, allow_redirects=False)
long_cook = res.cookies['session']
print(f"[*] Длинное куки: {long_cook}")

cipherstream = xor(b''.fromhex(long_cook), b"q"*300)
plaintext = xor(b''.fromhex(short_cook), cipherstream)
print(f"[*] Декодированый куки: {plaintext}")

patched = plaintext.replace(b'"role": "user"', b'"role": "root"')
# Дополнительные изменения раскодированых куки
new_cook = xor(patched, cipherstream).hex()
print(f"[*] Повторно зашифрованный куки: {new_cook}")

res = requests.get(f"{URL}/funds", cookies={"session": new_cook})
print(f"[*] result: {res.text}")