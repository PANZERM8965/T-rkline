import sys
import os
import json
import re
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QDialog, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox, QHBoxLayout, QVBoxLayout, QPushButton,
    QListWidget, QTextBrowser, QMainWindow, QInputDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QFont, QTextCursor


# --- Constants ---
DATA_FILE = "data/messages.json"
COUNTRY_CODES = [
    ("Türkiye", "+90"),
    ("ABD", "+1"),
    ("Almanya", "+49"),
    ("Fransa", "+33"),
    ("İngiltere", "+44"),
    ("Kanada", "+1"),
    ("Avustralya", "+61"),
    ("Hindistan", "+91"),
    ("Rusya", "+7"),
    ("Çin", "+86"),
    ("Japonya", "+81"),
    ("Meksika", "+52"),
]

# ========== Splash Screen ==========
class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#0B223F"))
        painter.setPen(Qt.white)
        font = QFont("Segoe UI", 64, QFont.Bold)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, "Türkline")

# ========== Dark ComboBox for Country Codes ==========
class DarkComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                background-color: #374151;
                color: #F9FAFB;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 15px;
                min-width: 110px;
            }
            QComboBox QAbstractItemView {
                background-color: #1F2937;
                color: #E5E7EB;
                selection-background-color: #2563EB;
                selection-color: white;
                border-radius: 8px;
                outline: none;
                font-size: 15px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left-width: 1px;
                border-left-color: #4B5563;
                border-left-style: solid;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                /* arrow icon için aşağıdaki satır eklenmeli, yoksa kendi Qt arrow çıkar */
                image: url(down_arrow.png); /* down_arrow.png varsa gösterir, yoksa sistem ok */
            }
        """)

# ========== Login Dialog ==========
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Türkline - Giriş")
        self.setFixedSize(440, 250)
        self.setStyleSheet("""
            QDialog {
                background-color: #1F2937;
                color: #E5E7EB;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #F3F4F6;
            }
            QLineEdit {
                background-color: #374151;
                border: 1.5px solid #4B5563;
                border-radius: 8px;
                padding: 10px 14px;
                color: #F9FAFB;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3B82F6;
                background-color: #2563EB;
                color: white;
            }
            QPushButton {
                background-color: #3B82F6;
                border-radius: 10px;
                padding: 10px 25px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)

        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.setFormAlignment(Qt.AlignCenter)
        layout.setVerticalSpacing(18)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Adınız")
        layout.addRow(QLabel("Adınız:"), self.name_input)

        hbox = QHBoxLayout()

        self.country_code_combo = DarkComboBox()
        for country, code in COUNTRY_CODES:
            self.country_code_combo.addItem(f"{country} ({code})", code)
        self.country_code_combo.setCurrentIndex(0)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Sadece sayılar, başta 0 olmadan")
        self.phone_input.setMaxLength(15)
        self.phone_input.setFixedHeight(36)
        self.phone_input.setMinimumWidth(280)
        self.phone_input.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        hbox.addWidget(self.country_code_combo)
        hbox.addSpacing(12)
        hbox.addWidget(self.phone_input)

        container = QWidget()
        container.setLayout(hbox)

        phone_label = QLabel("Telefon Numaranız:")
        phone_label.setFixedWidth(120)
        layout.addRow(phone_label, container)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept_dialog)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.user_name = None
        self.user_phone = None

        self.name_input.returnPressed.connect(self.accept_dialog)
        self.phone_input.returnPressed.connect(self.accept_dialog)

    def accept_dialog(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        country_code = self.country_code_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Uyarı", "Lütfen adınızı girin.")
            return

        if not phone:
            QMessageBox.warning(self, "Uyarı", "Lütfen telefon numaranızı girin.")
            return

        if not re.fullmatch(r"\d{7,15}", phone):
            QMessageBox.warning(self, "Uyarı", "Telefon numarası sadece rakamlardan oluşmalı ve en az 7 haneli olmalıdır.")
            return

        full_phone = country_code + phone
        self.user_name = name
        self.user_phone = full_phone
        self.accept()

# ========== Chat UI ==========
class ChatUI(QMainWindow):
    def __init__(self, user_name, user_phone):
        super().__init__()
        self.setWindowTitle(f"Türkline - {user_name} ({user_phone})")
        self.setGeometry(100, 100, 1000, 650)
        self.showMaximized()

        self.user_name = user_name
        self.user_phone = user_phone

        self.contacts = []  # [(name, phone), ...]
        self.messages = {}  # { phone: [ { sender, text }, ... ] }

        self.load_messages()

        # --- Left panel ---
        self.user_label = QLabel(f"Türkline\n{self.user_name} ({self.user_phone})")
        self.user_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.user_label.setStyleSheet("color: #F0F0F0; padding: 15px;")

        self.contact_list = QListWidget()
        self.contact_list.currentItemChanged.connect(self.change_contact)
        self.contact_list.setStyleSheet("""
            QListWidget {
                background-color: #34495E;
                border-radius: 15px;
                color: #ECF0F1;
                padding: 5px;
                font-size: 14px;
            }
            QListWidget::item:selected {
                background-color: #2980B9;
                border-radius: 10px;
                color: white;
            }
        """)

        self.add_contact_btn = QPushButton("Yeni Kişi Ekle")
        self.add_contact_btn.setCursor(Qt.PointingHandCursor)
        self.add_contact_btn.setStyleSheet(self.button_style())
        self.add_contact_btn.clicked.connect(self.add_contact)

        self.edit_contact_btn = QPushButton("Düzenle")
        self.edit_contact_btn.setCursor(Qt.PointingHandCursor)
        self.edit_contact_btn.setStyleSheet(self.button_style())
        self.edit_contact_btn.clicked.connect(self.edit_contact)

        self.delete_contact_btn = QPushButton("Sil")
        self.delete_contact_btn.setCursor(Qt.PointingHandCursor)
        self.delete_contact_btn.setStyleSheet(self.button_style())
        self.delete_contact_btn.clicked.connect(self.delete_contact)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_contact_btn)
        btn_layout.addWidget(self.edit_contact_btn)
        btn_layout.addWidget(self.delete_contact_btn)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.user_label)
        left_layout.addWidget(self.contact_list)
        left_layout.addLayout(btn_layout)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMinimumWidth(320)
        left_widget.setMaximumWidth(400)
        left_widget.setStyleSheet("background-color: #2C3E50; border-top-left-radius: 20px; border-bottom-left-radius: 20px;")

        # --- Right panel ---
        self.chat_label = QLabel("Sohbet")
        self.chat_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.chat_label.setStyleSheet("color: #F0F0F0; padding: 15px; border-bottom: 1px solid #34495E;")

        self.chat_area = QTextBrowser()
        self.chat_area.setStyleSheet("""
            QTextBrowser {
                background-color: #1E272E;
                color: #D0D7DE;
                border-radius: 15px;
                padding: 15px;
                font-size: 14px;
            }
        """)
        self.chat_area.setOpenLinks(False)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Mesaj yaz...")
        self.message_input.setStyleSheet("""
            QLineEdit {
                border-radius: 25px;
                padding: 15px 20px;
                background-color: #34495E;
                color: #ECF0F1;
                border: none;
                font-size: 15px;
            }
            QLineEdit:focus {
                background-color: #3F5873;
            }
        """)
        self.message_input.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Gönder")
        self.send_button.setCursor(Qt.PointingHandCursor)
        self.send_button.setStyleSheet(self.button_style())
        self.send_button.clicked.connect(self.send_message)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.message_input)
        bottom_layout.addWidget(self.send_button)
        bottom_layout.setContentsMargins(0, 10, 0, 10)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.chat_label)
        right_layout.addWidget(self.chat_area)
        right_layout.addLayout(bottom_layout)
        right_layout.setStretch(1, 1)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setStyleSheet("background-color: #1E272E; border-top-right-radius: 20px; border-bottom-right-radius: 20px;")

        # --- Main layout ---
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(right_widget)
        main_layout.setStretch(1, 3)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Load or initialize contacts and messages
        if not self.contacts:
            # Example users
            self.contacts = [("Kullanıcı 1", "+905551112233"), ("Kullanıcı 2", "+905559998877")]
            for name, phone in self.contacts:
                self.add_contact_list_item(name, phone)
                if phone not in self.messages:
                    self.messages[phone] = []
        else:
            for name, phone in self.contacts:
                self.add_contact_list_item(name, phone)

        self.current_contact_phone = None
        if self.contact_list.count() > 0:
            self.contact_list.setCurrentRow(0)

    def button_style(self):
        return """
            QPushButton {
                border-radius: 18px;
                background-color: #2980B9;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3498DB;
            }
            QPushButton:pressed {
                background-color: #1B6CA8;
            }
        """

    def add_contact_list_item(self, name, phone):
        display_text = f"{name} ({phone})"
        self.contact_list.addItem(display_text)

    def parse_contact_list_item(self, text):
        if "(" in text and text.endswith(")"):
            name = text[: text.rfind("(")].strip()
            phone = text[text.rfind("(") + 1 : -1].strip()
            return name, phone
        return text, ""

    def add_contact(self):
        dialog = AddContactDialog()
        if dialog.exec() == QDialog.Accepted:
            name = dialog.contact_name
            phone = dialog.contact_phone

            # kontrol: telefon numarası zaten var mı
            for n, p in self.contacts:
                if p == phone:
                    QMessageBox.warning(self, "Uyarı", "Bu telefon numarası zaten kayıtlı.")
                    return

            self.contacts.append((name, phone))
            self.messages[phone] = []
            self.add_contact_list_item(name, phone)
            self.save_messages()

    def edit_contact(self):
        current = self.contact_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir kişi seçin.")
            return

        old_name, old_phone = self.parse_contact_list_item(current.text())

        text, ok = QInputDialog.getText(self, "Kişi Düzenle", "Yeni isim:", text=old_name)
        if ok and text.strip():
            new_name = text.strip()
            if new_name != old_name:
                idx = -1
                for i, (n, p) in enumerate(self.contacts):
                    if p == old_phone:
                        idx = i
                        break
                if idx != -1:
                    self.contacts[idx] = (new_name, old_phone)
                    current.setText(f"{new_name} ({old_phone})")
                    if self.chat_label.text() == f"{old_name} ({old_phone})":
                        self.chat_label.setText(f"{new_name} ({old_phone})")
                    self.save_messages()

    def delete_contact(self):
        current = self.contact_list.currentItem()
        if not current:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için bir kişi seçin.")
            return

        name, phone = self.parse_contact_list_item(current.text())

        confirm = QMessageBox.question(
            self,
            "Kişi Sil",
            f"'{name} ({phone})' kişisini silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            idx = self.contact_list.row(current)
            self.contact_list.takeItem(idx)
            self.contacts = [(n, p) for n, p in self.contacts if p != phone]
            if phone in self.messages:
                del self.messages[phone]
            self.chat_area.clear()
            self.chat_label.setText("Sohbet")
            self.save_messages()

    def change_contact(self, current, previous):
        if current:
            name, phone = self.parse_contact_list_item(current.text())
            self.current_contact_phone = phone
            self.chat_label.setText(f"{name} ({phone})")
            self.load_chat_messages(phone)
        else:
            self.current_contact_phone = None
            self.chat_area.clear()
            self.chat_label.setText("Sohbet")

    def load_chat_messages(self, phone):
        self.chat_area.clear()
        if phone in self.messages:
            for msg in self.messages[phone]:
                sender = msg.get("sender", "")
                text = msg.get("text", "")
                if sender == self.user_phone:
                    # Gönderen kendimizse sağda göster
                    self.chat_area.append(f'<div style="text-align:right; color:#58D68D;">{text}</div>')
                else:
                    # Diğer kullanıcıdan mesaj solda
                    self.chat_area.append(f'<div style="text-align:left; color:#F0F0F0;">{sender}: {text}</div>')
            self.chat_area.moveCursor(QTextCursor.End)

    def send_message(self):
        if not self.current_contact_phone:
            QMessageBox.warning(self, "Uyarı", "Lütfen mesaj göndermek için bir kişi seçin.")
            return
        text = self.message_input.text().strip()
        if not text:
            return
        # Mesajı ekle
        msg = {"sender": self.user_phone, "text": text}
        self.messages.setdefault(self.current_contact_phone, []).append(msg)
        self.load_chat_messages(self.current_contact_phone)
        self.message_input.clear()
        self.save_messages()

    def load_messages(self):
        if not os.path.exists(DATA_FILE):
            # data klasörünü oluştur
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump({"contacts": [], "messages": {}}, f, indent=4)

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.contacts = data.get("contacts", [])
                self.messages = data.get("messages", {})
        except Exception:
            self.contacts = []
            self.messages = {}

    def save_messages(self):
        data = {
            "contacts": self.contacts,
            "messages": self.messages
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

# ========== Add Contact Dialog ==========
class AddContactDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Kişi Ekle")
        self.setFixedSize(400, 180)
        self.setStyleSheet("""
            QDialog {
                background-color: #1F2937;
                color: #E5E7EB;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #374151;
                border: 1.5px solid #4B5563;
                border-radius: 8px;
                padding: 10px 14px;
                color: #F9FAFB;
                font-size: 15px;
            }
            QLineEdit:focus {
                border: 1.5px solid #3B82F6;
                background-color: #2563EB;
                color: white;
            }
            QPushButton {
                background-color: #3B82F6;
                border-radius: 10px;
                padding: 10px 25px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)

        layout = QFormLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Adı girin")
        layout.addRow(QLabel("Ad:"), self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon numarası (başında 0 olmadan)")
        self.phone_input.setMaxLength(15)
        layout.addRow(QLabel("Telefon:"), self.phone_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept_dialog)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.contact_name = None
        self.contact_phone = None

        self.name_input.returnPressed.connect(self.accept_dialog)
        self.phone_input.returnPressed.connect(self.accept_dialog)

    def accept_dialog(self):
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Uyarı", "Lütfen isim girin.")
            return

        if not phone:
            QMessageBox.warning(self, "Uyarı", "Lütfen telefon numarası girin.")
            return

        if not re.fullmatch(r"\d{7,15}", phone):
            QMessageBox.warning(self, "Uyarı", "Telefon numarası sadece rakamlardan oluşmalı ve 7 ile 15 hane arasında olmalıdır.")
            return

        self.contact_name = name
        self.contact_phone = phone
        self.accept()

# ========== Main ==========
def main():
    app = QApplication(sys.argv)

    splash = SplashScreen()
    splash.show()

    def start_app():
        splash.close()
        login = LoginDialog()
        if login.exec() == QDialog.Accepted:
            try:
                window = ChatUI(login.user_name, login.user_phone)
                window.show()
                app.window = window  # Önemli: pencerenin çöp toplamasını önler
            except Exception as e:
                QMessageBox.critical(None, "Hata", f"Uygulama başlatılırken hata oluştu:\n{e}")
                app.quit()
        else:
            app.quit()

    QTimer.singleShot(2000, start_app)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
