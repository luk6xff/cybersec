AES-256-GCM combines AES encryption (in Counter mode) with an integrated authentication mechanism based on the Galois Message Authentication Code (GMAC). Here’s how it works in more detail:

1. **Encryption Using AES in Counter Mode:**
   GCM uses AES in CTR (Counter) mode for the encryption portion. CTR mode turns the AES block cipher into a stream cipher by encrypting successive values of a counter and XORing them with the plaintext to produce ciphertext.

2. **Associated Data and Ciphertext Input to GMAC:**
   Along with producing ciphertext, GCM can also handle Associated Authenticated Data (AAD)—such as headers or metadata—that should be authenticated but not encrypted. Both the ciphertext and the AAD are passed into the GMAC function.

3. **Polynomial MAC Calculation (GMAC):**
   GMAC computes a polynomial-based authentication tag using a finite field (Galois field). It treats the ciphertext blocks and AAD as elements in a polynomial evaluated over GF(2¹²⁸). Through Galois field multiplication and XOR operations, it produces a unique authentication tag (also called an authentication field).

4. **Authentication Tag (Integrity Check):**
   At the end of the encryption process, GCM outputs not only the ciphertext but also a short authentication tag (often 128 bits). This tag provides integrity protection—if any bit in the ciphertext or the associated data is changed, the tag verification will fail when the recipient tries to authenticate the message.

5. **Verification During Decryption:**
   When decrypting, the receiver uses the same GCM process on the ciphertext and associated data. If the computed tag matches the one sent with the ciphertext, it confirms that the message has not been altered. If there’s any mismatch, it indicates tampering or corruption.

In summary, the "Galois" part of AES-GCM is what provides the built-in authentication. By combining AES encryption in CTR mode with a polynomial-based MAC, AES-GCM ensures both confidentiality (via encryption) and integrity/authenticity (via GMAC).
