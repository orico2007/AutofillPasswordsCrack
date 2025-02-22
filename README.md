# AutofillPasswordsChromeCrack

## Overview
This script extracts and decrypts saved passwords from Google Chrome and Microsoft Edge on a Windows machine and sends them via email. The passwords are encrypted using AES-GCM with a key that is uniquely tied to the Windows user account.
=======
# AutofillPasswordsChromeCrack

## Overview
This script extracts and decrypts saved passwords from Google Chrome on a Windows machine and sends them via email. The passwords are encrypted using AES-GCM with a key that is uniquely tied to the Windows user account.

## How It Works

### Extracting the Encryption Key
Chrome and Edge encrypt stored passwords using an AES key found in the `Local State` file located at:
```
C:\Users\<USERNAME>\AppData\Local\Google\Chrome\User Data\Local State
```
or
```
C:\Users\<USERNAME>\AppData\Local\Microsoft\Edge\User Data\Local State
```
=======
Chrome encrypts stored passwords using an AES key found in the `Local State` file located at:
```
C:\Users\<USERNAME>\AppData\Local\Google\Chrome\User Data\Local State
```
- The key is stored in Base64 format and must be decoded.
- The script extracts the `encrypted_key` field from this JSON file.
- The key is decrypted using Windows' `win32crypt.CryptUnprotectData`, which ensures the key is tied to the specific Windows user.

---

### Finding the Password Database

Chrome and Edge store saved login credentials in an SQLite database named `Login Data`.
=======
Chrome stores saved login credentials in an SQLite database named `Login Data`.
- The database is found in the profile directory:
```
C:\Users\<USERNAME>\AppData\Local\Google\Chrome\User Data\<Profile>\Login Data
```

or
```
C:\Users\<USERNAME>\AppData\Local\Microsoft\Edge\User Data\<Profile>\Login Data
```
- Both browsers can have multiple profiles (`Default`, `Profile 1`, `Profile 2`, etc.), so the script checks multiple profiles.
=======
- Chrome can have multiple profiles (`Default`, `Profile 1`, `Profile 2`, etc.), so the script checks multiple profiles.

---

### Decrypting Stored Passwords
- The script extracts `origin_url`, `username_value`, and `password_value` from the `logins` table in the SQLite database.

- The `password_value` is AES-encrypted and needs to be decrypted using the extracted browser key.
=======
- The `password_value` is AES-encrypted and needs to be decrypted using the extracted Chrome key.
- AES decryption is performed using `AES.MODE_GCM`.
- The decrypted passwords are stored in memory for later use.

---

### Sending Data via Email
- The collected data is formatted into a string.
- The script sends an email containing the extracted credentials using `smtplib` and `EmailMessage`.
- The sender must provide valid Gmail credentials (with app passwords or 2FA enabled for security reasons).

---


## Installation

### Prerequisites
- Python 3.x
- Windows OS (required for `win32crypt`)

### Required Python Packages
Install the required packages using `pip`:
```bash
pip install pycryptodome pypiwin32
```

---

## Usage
1. Clone the repository or download the script.
2. Install the required Python packages as shown above.
3. Update the `sender`, `password`, and `receiver` fields in the script with your Gmail credentials and recipient email address.
4. Run the script:
   ```bash
   python autofill_passwords_crack.py
   ```

---

=======
## Important Notes
- This script **only works on the local machine** where the passwords are stored due to Windows' `win32crypt.CryptUnprotectData`, which ensures that the encryption key cannot be used on a different system.
- This script is for **educational and research purposes only**. Unauthorized access to someone else's credentials is illegal and violates ethical hacking guidelines.
- Always obtain **explicit permission** before running this on any system that is not your own.


---

## Disclaimer
I do not take responsibility for any misuse of this script. It is meant for **educational and personal security research** purposes only. Unauthorized access to stored credentials may violate various laws and regulations depending on your location.

---

This updated `README.md` includes the necessary `pip install` instructions and clarifies the prerequisites and usage steps. It also maintains the ethical and legal disclaimers to ensure responsible use.
=======
## Disclaimer
I do not take responsibility for any misuse of this script. It is meant for **educational and personal security research** purposes only. Unauthorized access to stored credentials may violate various laws and regulations depending on your location.

