# AES 256 CBC

AES in CBC mode by itself does not provide authenticity or integrity guarantees. It only provides confidentiality. If you rely solely on AES-CBC encryption, an attacker could potentially manipulate the ciphertext and cause predictable changes in the decrypted plaintext without detection. This is because CBC mode doesn’t include a built-in mechanism to verify that the ciphertext hasn’t been tampered with.

In practice, to achieve authenticity and integrity with CBC-mode encryption, you need to pair it with a separate Message Authentication Code (MAC), such as an HMAC. The resulting “Encrypt-then-MAC” scheme (first encrypt your plaintext, then compute a MAC over the resulting ciphertext) ensures that any unauthorized modification to the ciphertext is detected upon verification of the MAC. However, this is more cumbersome and error-prone than using an authenticated encryption mode like GCM, which inherently provides both confidentiality and authenticity.
