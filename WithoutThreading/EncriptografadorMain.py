# The code was written by Jose Guilherme de Castro Rodrigues
# Copyright 2016 José Guilherme de Castro Rodrigues
import sys
from PyQt4 import QtGui, QtCore

default_key = "WeQfHjkU31EdoIqf"

class Encriptografador(QtGui.QMainWindow):

    key = None
    width = None
    height = None
    mode = "e"

    def __init__(self, width, height, key):

        super(Encriptografador, self).__init__()

        self.key = key

        self.width = width
        self.height = height
        self.setGeometry(35, 35, self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)
        self.setWindowTitle("Encriptografador - Copyright 2016 José Guilherme de Castro Rodrigues")

        self.create_ui()

        self.show()

    def create_ui(self):

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))

        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu("&Arquivo")

        self.exit_action = QtGui.QAction("&Sair", self)
        self.exit_action.triggered.connect(self.close_app)
        self.exit_action.setShortcut("Ctrl+Q")

        self.change_key_action = QtGui.QAction("&Trocar Chave", self)
        self.change_key_action.triggered.connect(self.change_key)
        self.change_key_action.setShortcut("Ctrl+K")

        self.file_menu.addAction(self.change_key_action)
        self.file_menu.addAction(self.exit_action)

        self.about_action = QtGui.QAction("&Sobre", self)
        self.about_action.triggered.connect(self.show_about)
        self.about_action.setShortcut("Ctrl+H")

        self.main_menu.addAction(self.about_action)

        self.default_font = QtGui.QFont("Sans Serif", 14)

        self.decrypted_label = QtGui.QLabel("Texto", self)
        self.decrypted_label.move(425, 18)
        self.decrypted_label.setFont(self.default_font)

        self.decrypted_textbox = QtGui.QTextEdit(self)
        self.decrypted_textbox.move(175, 48)
        self.decrypted_textbox.resize(500, 200)

        self.encrypted_label = QtGui.QLabel("Texto encriptografado", self)
        self.encrypted_label.move(375, 248)
        self.encrypted_label.resize(200, 30)
        self.encrypted_label.setFont(self.default_font)

        self.encrypted_textbox = QtGui.QTextEdit(self)
        self.encrypted_textbox.move(175, 278)
        self.encrypted_textbox.resize(500, 200)

        self.crypt_btn = QtGui.QPushButton("Encriptografar", self)
        self.crypt_btn.move(25, 50)
        self.crypt_btn.clicked.connect(self.cryptbtn_click)

        self.save_btn = QtGui.QPushButton("Salvar arquivo .txt", self)
        self.save_btn.move(25, 90)
        self.save_btn.clicked.connect(self.save_in_txt)

        self.read_btn = QtGui.QPushButton("Ler arquivo .txt", self)
        self.read_btn.move(25, 130)
        self.read_btn.clicked.connect(self.read_from_txt)

        self.goto_encrypt_mode = QtGui.QRadioButton("Encriptografar", self)
        self.goto_encrypt_mode.move(25, 200)
        self.goto_encrypt_mode.setChecked(True)
        self.goto_encrypt_mode.clicked.connect(self.change_mode)

        self.goto_decrypt_mode = QtGui.QRadioButton("Desencriptografar", self)
        self.goto_decrypt_mode.resize(150, 50)
        self.goto_decrypt_mode.move(25, 225)
        self.goto_decrypt_mode.clicked.connect(self.change_mode)

        self.clear_decrypted_textbox_btn = QtGui.QPushButton("Limpar texto", self)
        self.clear_decrypted_textbox_btn.move(25, 300)
        self.clear_decrypted_textbox_btn.clicked.connect(lambda: self.clear_text(self.decrypted_textbox))
        
        self.clear_encrypted_textbox_btn = QtGui.QPushButton("Limpar T.E", self)
        self.clear_encrypted_textbox_btn.move(25, 330)
        self.clear_encrypted_textbox_btn.clicked.connect(lambda: self.clear_text(self.encrypted_textbox))

        self.progress_bar = QtGui.QProgressBar(self)
        self.progress_bar.move(25, 370)
 
    def cryptbtn_click(self):

        if self.mode == "e" and len(self.decrypted_textbox.toPlainText()) == 0:
            self.error_message("Erro!", "Você precisa digitar alguma coisa para poder encriptografar!")
            return
        elif self.mode == "d" and len(self.encrypted_textbox.toPlainText()) == 0:
            self.error_message("Erro!", "Você precisa digitar alguma coisa para poder desencriptografar!")
            return

        if self.mode == "e":            
            encrypted_message = self.encrypt_message(self.decrypted_textbox.toPlainText())
            self.encrypted_textbox.setText(encrypted_message)
        elif self.mode == "d":
            decrypted_message = self.decrypt_message(self.encrypted_textbox.toPlainText())
            self.decrypted_textbox.setText(decrypted_message)

    def encrypt_message(self, msg):

        self.progress_bar.setValue(0)

        counter = 0
        encrypted_msg = ""
        print("Starting encrypting")

        print(len(msg))
        pcount = 0

        for char in msg:
            encrypted_char = ord(char) * ord(self.key[counter])

            if encrypted_msg == "":
                encrypted_msg += str(encrypted_char)
            else:
                encrypted_msg += " " + str(encrypted_char)

            pcount += 1
            progress = pcount * 100 / len(msg)
            print(progress, "%")
            self.progress_bar.setValue(progress)

            counter += 1
            if counter >= len(self.key):
                counter = 0

        print("Finished encrypting")
        return encrypted_msg

    def decrypt_message(self, encrypted_msg):

        self.progress_bar.setValue(0)

        counter = 0
        decrypted_msg = ""

        encrypted_list = encrypted_msg.split(" ")

        print(len(encrypted_msg))
        pcount = 0

        for encrypted_element in encrypted_list:
            encrypted_char = int(encrypted_element)
            decryption_char = ord(self.key[counter])
            decrypted_int = int(encrypted_char / decryption_char)

            decrypted_char = chr(decrypted_int)

            decrypted_msg += decrypted_char

            pcount += 1
            progress = pcount * 100 / len(encrypted_list)
            print(progress, "%")
            self.progress_bar.setValue(progress)

            counter += 1
            if counter >= len(self.key):
                counter = 0
        
        return decrypted_msg 

    def change_key(self):

        new_key, ok = QtGui.QInputDialog.getText(self, "Trocar Chave", "Nova Chave (Máximo de 16 caracteres):",
                                                 QtGui.QLineEdit.Normal, self.key)

        if not ok:
            return

        if new_key is None or new_key is "":
            self.error_message("Erro!", "A nova chave não pode ser: '" + new_key + "'")
            return

        if len(new_key) > 16:
            self.error_message("Erro!", "A chave tem mais de 16 caracteres!")
            return

        fw = open("key.k", "w")
        fw.write(new_key)
        fw.close()

        self.key = new_key
    
    def clear_text(self, textbox):

        textbox.setText("")

    def save_in_txt(self):

        if self.mode == "e" and self.encrypted_textbox.toPlainText() == "":
            self.error_message("Erro!", "O campo de texto encriptografado não pode estar vazio!")
            return
        elif self.mode == "d" and self.decrypted_textbox.toPlainText() == "":
            self.error_message("Erro!", "O campo de texto desencriptografado não pode estar vazio!")
            return

        name = QtGui.QFileDialog.getSaveFileName(self, "Save File")

        if not name:
            return

        name += ".txt"

        fw = open(name, "w")
        if self.mode == "e":
            fw.write(self.encrypted_textbox.toPlainText())
        elif self.mode == "d":
            fw.write(self.decrypted_textbox.toPlainText())

        fw.close()

    def read_from_txt(self):

        name = QtGui.QFileDialog.getOpenFileName(self, "Open File")

        if not name:
            return

        fr = open(name, "r")
        text = fr.read()

        if self.mode == "e":
            self.decrypted_textbox.setText(text)
        elif self.mode == "d":
            self.encrypted_textbox.setText(text)

        fr.close()
    
    def change_mode(self):

        if self.goto_encrypt_mode.isChecked():
            self.goto_decrypt_mode.setChecked(False)
            self.mode = "e"
            self.crypt_btn.setText("Encriptografar")
        elif self.goto_decrypt_mode.isChecked():
            self.goto_encrypt_mode.setChecked(False)
            self.mode = "d"
            self.crypt_btn.setText("Desencriptografar")

        print("Mode is now: " + self.mode)

    def show_about(self):

        about = QtGui.QMainWindow(self)
        about.setWindowTitle("Encriptografador - Sobre")
        about.setGeometry(35, 35, 300, 175)
        about.setMinimumSize(300, 175)
        about.setMaximumSize(300, 175)

        author = QtGui.QLabel("Autor: José Guilherme de Castro \nRodrigues", about)
        author.move(0, 10)
        author.resize(300, 45)
        author.setFont(self.default_font)

        version = QtGui.QLabel("Versão: 1.0.0", about)
        version.move(0, 65)
        version.resize(300, 20)
        version.setFont(self.default_font)

        date = QtGui.QLabel("Data: 9/9/2016", about)
        date.move(0, 95)
        date.resize(300, 20)
        date.setFont(self.default_font)

        lic = QtGui.QLabel("Copyright 2016 José Guilherme de \nCastro Rodrigues", about)
        lic.move(0, 125)
        lic.resize(300, 45)
        lic.setFont(self.default_font)

        about.show()

    def error_message(self, title, message):

        QtGui.QMessageBox.critical(self, title, message, QtGui.QMessageBox.Ok)

    def close_app(self):

        sure = QtGui.QMessageBox.question(self, "?", "Tem certeza de que você quer sair?",
                                          QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                          QtGui.QMessageBox.No)

        if sure == QtGui.QMessageBox.Yes:
            sys.exit(0)

    def closeEvent(self, event):

        event.ignore()
        self.close_app()

def load_key():

    try:
        fr = open("key.k", "r")
        key = fr.read()
        print(key)
        fr.close()
        return key
    except FileNotFoundError:
        fr = open("key.k", "w")
        fr.write(default_key)
        fr.close()
        load_key()

def main():
    key = load_key()
    app = QtGui.QApplication(sys.argv)
    GUI = Encriptografador(720, 490, key)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# The code was written by Jose Guilherme de Castro Rodrigues
# Copyright 2016 José Guilherme de Castro Rodrigues
