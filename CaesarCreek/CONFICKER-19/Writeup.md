# CONFICKER-19 (Caesar Creek Software — Reverse Engineering & Forensics)

![Challenge Screenshot](./conficker-19.png)

---

## Challenge Description
> We identified a compromised system on our network and captured the start of some communications from a rogue process. Can you help us figure out what it’s doing?

**Categories:** Reverse Engineering, Forensic  

**Files**
- `conficker-19.pcapng`  
  - sha256: `d1afb309dbea6508c6e2e3c5346cd24ac8f98da9e6342971342b2aa524231d59`  
- sha256: `e3b0c44298fc1c149afb4c8996fb92427ae41e4649b934ca495991b7852b855`

---

## My Process

### Step 1: Background Research
The first thing I did was look up **Conficker**. It’s a worm that exploited a buffer overflow in Windows, targeting the Windows Server service (used for sharing files and printers).

---

### Step 2: Inspecting the PCAP
I opened the provided `CONFICKER-19.pcapng` in **Wireshark**.  

- I noticed **TCP communication** between ports `1234` and `39280`.  
- Inside one packet stream, I saw an **ELF file header** (`7f 45 4c 46 02 01 01`) and references to shared objects like `AES_Encrypt`.  
- From this, I concluded that the payload was being transferred over TCP.

I used **Follow → Follow TCP Stream** in Wireshark to extract the raw binary and saved it as an ELF file. Running `readelf` on it in my Kali VM confirmed it was a valid executable.

---

### Step 3: Reverse Engineering the Payload
I loaded the ELF into **Ghidra** and examined the `main` function.  

- The code handled different commands:  
  - `S` → stop execution  
  - `P` → set a password for AES (ECB mode, no IV)  
  - `F` → request a file (e.g., `flag.txt`)  

- The interesting part:  
  - If no password was set, the payload just sent the file contents in plaintext.  
  - If a password was set, it **applied two layers of encryption**:  
    1. XOR loop over the first 16 bytes  
    2. AES-128 (ECB) with the key: `Prestidigitation`

In the PCAP, I saw the sequence where:
1. The client requested `flag.txt`  
2. The password was set with `P` = `Prestidigitation`  
3. The file was returned in encrypted form.

The final encrypted data appeared in the capture as:

```
e1dbfd6826a14f279fafe76982333070
a0595e10eec5ffd64cf3569eac102451
```

---

### Step 4: Writing the Decrypter
I wrote a Python script to reverse the logic:

```python
from Crypto.Cipher import AES
import binascii

# AES key
key = b'Prestidigitation'

# Ciphertext from the PCAP
block = binascii.unhexlify(
    'e1dbfd6826a14f279fafe76982333070'
    'a0595e10eec5ffd64cf3569eac102451'
)

# AES decryption (ECB mode)
aes = AES.new(key, AES.MODE_ECB)
decrypted = aes.decrypt(block)

string = ""
size = len(decrypted) - 1

# Undo the XOR layer
for i in range(0, size):
    string = (chr(decrypted[size - i] ^ decrypted[size - 1 - i])) + string

print(string)
```

---

### Step 5: Getting the Flag
Running this script printed the flag:

```
flag{CATS_CATS_ARE_NICE}
```

✅ Challenge solved.

---

## Lessons Learned
- PCAP analysis can hide entire binaries inside TCP streams.  
- Looking for ELF headers (`0x7f 45 4c 46`) is a great way to confirm payloads.  
- Layered encryption (XOR + AES) requires careful step-by-step reversal.  
- Always check for commands (`S`, `P`, `F`) — they often map directly to challenge behavior.  
