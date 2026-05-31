# Cryptography
My playground on cryptography — practical examples for automotive cybersecurity engineers.

## Structure

```
cryptography/
├── symmetric/
│   └── aes/
│       ├── aes-256-cbc/    — AES-CBC with HMAC (encrypt-then-MAC)
│       └── aes-256-gcm/    — AES-GCM authenticated encryption
├── asymmetric/
│   ├── rsa/               — RSA-2048 OAEP encryption & PSS signatures
│   ├── ecdsa/             — ECDSA P-256 (V2X, ISO 15118)
│   ├── ecdh/              — ECDH key exchange + HKDF derivation
│   └── ed25519-x25519/    — Modern curves (WireGuard, Signal)
└── pqc/
    ├── ml-kem/            — ML-KEM (Kyber) key encapsulation [FIPS 203]
    ├── ml-dsa/            — ML-DSA (Dilithium) digital signatures [FIPS 204]
    ├── slh-dsa/           — SLH-DSA (SPHINCS+) hash-based sigs [FIPS 205]
    └── hybrid/            — X25519 + ML-KEM hybrid key exchange
```

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
# WIN (git bash): source venv/Scripts/Activate
pip install -r requirements.txt
```

## Quick Reference

| Category | Algorithm | Automotive Use |
|----------|-----------|---------------|
| Symmetric | AES-128-CMAC | SecOC message authentication |
| Symmetric | AES-256-GCM | OTA firmware encryption |
| Asymmetric | ECDSA P-256 | V2X BSM signing, secure boot |
| Asymmetric | ECDH P-256 | TLS key exchange, key provisioning |
| Asymmetric | Ed25519 | Backend/internal protocols |
| PQC | ML-KEM-768 | Future quantum-safe key exchange |
| PQC | ML-DSA-65 | Future quantum-safe firmware signing |
| Hash | SHA-256 | Integrity verification |
| KDF | HKDF-SHA256 | Deriving keys from shared secrets |
