# 🔐 AES Modes of Operation: The Complete Comparison

## 1. Quick Comparison Matrix

| Mode | Name | Security Level | Integrity? | Parallelizable? | Best Use Case |
| --- | --- | --- | --- | --- | --- |
| **GCM** | Galois/Counter Mode | 🟢 **Excellent** | ✅ **Yes** | ✅ Yes | **Default Choice.** Web (TLS), Files, General purpose. |
| **CTR** | Counter Mode | 🟡 Good | ❌ No | ✅ Yes | High-speed streaming, low latency requirements. |
| **CBC** | Cipher Block Chaining | 🟠 OK (Legacy) | ❌ No | ❌ Decrypt Only | Legacy systems, compatibility with old hardware. |
| **KW** | Key Wrap | 🔵 **Specialized** | ✅ **Yes** | ❌ No | **Encrypting other keys** (Key Management). |
| **ECB** | Electronic Codebook | 🔴 **Unsafe** | ❌ No | ✅ Yes | **NEVER** (unless encrypting < 16 bytes of random data). |

---

## 2. Detailed Breakdown & Python Snippets

**Prerequisite:** Install the library.

```bash
pip install pycryptodome

```

### 🏆 AES-GCM (The Gold Standard)

**Why use it:** It provides **Authenticated Encryption**. It ensures the data hasn't been tampered with (Integrity) while keeping it secret (Confidentiality). If a bit is flipped during transit, decryption will fail automatically.

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32) # AES-256
data = b'Sensitive data that needs integrity protection'

# --- Encrypt ---
cipher = AES.new(key, AES.MODE_GCM)
ciphertext, tag = cipher.encrypt_and_digest(data)
nonce = cipher.nonce

print(f"GCM Ciphertext: {ciphertext.hex()}")
print(f"Tag (Integrity): {tag.hex()}")

# --- Decrypt ---
cipher_dec = AES.new(key, AES.MODE_GCM, nonce=nonce)
try:
    decrypted_data = cipher_dec.decrypt_and_verify(ciphertext, tag)
    print("Decryption successful:", decrypted_data)
except ValueError:
    print("Tampering detected!")

```

---

### 🔑 AES-KW (Key Wrap)

**Why use it:** Designed specifically by NIST to **encrypt cryptographic keys**. It is robust and does not require a nonce or IV (it uses a fixed internal constant). It is perfect for Key Management Services (KMS) or storing a "Key Encryption Key" (KEK).

* **Note:** The data size must be a multiple of 8 bytes.

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# The "Master Key" (KEK) used to wrap other keys
kek = get_random_bytes(16)
# The "Target Key" to be wrapped (must be multiple of 8 bytes)
target_key = get_random_bytes(32)

# --- Wrap (Encrypt) ---
cipher = AES.new(kek, AES.MODE_KW)
wrapped_key = cipher.encrypt(target_key)

print(f"Wrapped Key: {wrapped_key.hex()}")

# --- Unwrap (Decrypt) ---
cipher_dec = AES.new(kek, AES.MODE_KW)
unwrapped_key = cipher_dec.decrypt(wrapped_key)

assert target_key == unwrapped_key
print("Key unwrapped successfully.")

```

---

### ⚡ AES-CTR (High Speed)

**Why use it:** It turns AES into a stream cipher. It generates a "keystream" and XORs it with your data. It is incredibly fast and parallelizable.
**Warning:** You must **never** reuse a Nonce/IV with the same key.

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
data = b'Stream this video data fast...'

# --- Encrypt ---
cipher = AES.new(key, AES.MODE_CTR)
ciphertext = cipher.encrypt(data)
nonce = cipher.nonce

# --- Decrypt ---
cipher_dec = AES.new(key, AES.MODE_CTR, nonce=nonce)
decrypted_data = cipher_dec.decrypt(ciphertext)

```

---

### 🐢 AES-CBC (The Legacy Standard)

**Why use it:** Compatibility. If you are talking to an old bank mainframe or an older hardware security module (HSM), they likely use CBC. It requires "padding" because data must fit perfectly into 16-byte blocks.

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)
data = b'Block data requires padding'

# --- Encrypt ---
cipher = AES.new(key, AES.MODE_CBC)
# Pad data to be a multiple of 16 bytes
ciphertext = cipher.encrypt(pad(data, AES.block_size))
iv = cipher.iv

# --- Decrypt ---
cipher_dec = AES.new(key, AES.MODE_CBC, iv=iv)
decrypted_data = unpad(cipher_dec.decrypt(ciphertext), AES.block_size)

```

---

## 3. Specialized & "Good to Know" Modes

If you want to go deeper, here are the other prominent modes you might encounter in engineering:

### AES-XTS (Disk Encryption)

* **Use Case:** Full Disk Encryption (BitLocker, VeraCrypt, LUKS).
* **Why:** It is "tweakable." It encrypts data based on its physical sector address on the disk. This ensures that identical data written to two different sectors produces different ciphertexts, without expanding the data size (no extra storage overhead for tags/IVs).

### AES-CCM (Counter with CBC-MAC)

* **Use Case:** IoT, ZigBee, Bluetooth Low Energy (BLE), WPA2.
* **Why:** Like GCM, it provides Authenticated Encryption (Security + Integrity). However, it uses less silicon area on hardware chips than GCM, making it popular for low-power embedded devices.

### AES-SIV (Synthetic IV)

* **Use Case:** "Misuse-Resistant" Encryption.
* **Why:** In standard modes (GCM/CTR), if you accidentally reuse a specific number (Nonce), the security collapses. SIV is designed so that even if you mess up the implementation, the security degrades gracefully rather than failing catastrophically. It is also **Deterministic**: encrypting the same data with the same key always yields the same result (useful for searchable encryption).

---

## 4. Summary Recommendation

1. **General Encryption:** Use **AES-GCM**.
2. **Encrypting Keys:** Use **AES-KW**.
3. **Encrypted Hard Drives:** Use **AES-XTS**.
4. **Low-Power IoT:** Use **AES-CCM**.
5. **Streaming Video:** Use **AES-CTR**.
