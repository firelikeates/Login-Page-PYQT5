import sys
from PyQt5 import QtWidgets
import sqlite3

class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui();
        self.tablo_oluştur();
        self.bilgileri_getir();
        self.count=0
    def ui(self):
        v_box=QtWidgets.QVBoxLayout()
        h_box = QtWidgets.QHBoxLayout()
        self.setGeometry(140,150,450,500)
        self.setWindowTitle("Login Page")
        self.kullanıc_adı_text = QtWidgets.QLabel("Username")
        self.kullanıc_adı_input = QtWidgets.QLineEdit()
        self.kullanıc_adı_input.setStyleSheet("margin-top:5px;")
        self.parola_text = QtWidgets.QLabel("Password")
        self.parola_input = QtWidgets.QLineEdit();
        self.parola_text.setStyleSheet("margin-top:15px")
        self.parola_input.setStyleSheet("margin-top:5px;")

        self.register_buton = QtWidgets.QPushButton("Register")
        self.register_buton.setStyleSheet("margin-top:10px;width:70px;height:20px")

        self.beni_hatırla_text = QtWidgets.QLabel("Remember Me")
        self.beni_hatırla_text.setStyleSheet("margin-top:10px")
        self.beni_hatırla_check_box = QtWidgets.QCheckBox()
        self.beni_hatırla_check_box.setStyleSheet("margin-left:15px;margin-top:10px")
        self.bilgilendirme_text = QtWidgets.QLabel("")
        self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:13px")


        v_box.addWidget(self.kullanıc_adı_text);
        v_box.addWidget(self.kullanıc_adı_input);
        v_box.addWidget(self.parola_text);
        v_box.addWidget(self.parola_input);

        h_box.addWidget(self.beni_hatırla_text)
        h_box.addWidget(self.beni_hatırla_check_box)
        h_box.addStretch()
        h_box.addWidget(self.register_buton)


        v_box.addLayout(h_box)
        v_box.addWidget(self.bilgilendirme_text)
        v_box.addStretch()

        self.register_buton.clicked.connect(self.bilgi_ekle)
        self.setLayout(v_box)
        self.show()


    def tablo_oluştur(self):
        sorgu = "Create Table If not exists patron(username TEXT,password TEXT,count INT)"
        self.connection = sqlite3.connect("kütüphane2.db")
        self.cursor=self.connection.cursor()
        self.cursor.execute(sorgu)
        self.connection.commit()
    def tablo_kapat(self):
        self.connection.close()
    def bilgileri_getir(self):
        sorgu = "Select * from patron";
        self.cursor.execute(sorgu)
        kitaplık = self.cursor.fetchall();
        if(len(kitaplık)==0):
            pass
        else:
            for i in kitaplık:
                if(i[2]%2!=0):
                    self.kullanıc_adı_input.setText(i[0])
                    self.parola_input.setText(i[1])
                    self.beni_hatırla_check_box.setChecked(True)
                else:
                    pass

    def bilgi_ekle(self):
        sorgu = "Select * from patron";
        self.cursor.execute(sorgu)
        kitaplık = self.cursor.fetchall();
        if(len(kitaplık)!=0):
            if (self.parola_input.text() != "" and self.kullanıc_adı_input.text() != ""):
                if (self.beni_hatırla_check_box.isChecked()):
                    for i in kitaplık:

                        if(self.kullanıc_adı_input.text()==i[0] and self.parola_input.text()==i[1]):
                            self.bilgilendirme_text.setText("Giriş Yapıldı!")
                            self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:15px;color:green")
                        else:
                            self.bilgilendirme_text.setText("Kullanıcı Adı veya Parola Hatalı!")
                            self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:15px;color:red")
                else:
                    sorgu3 = "Delete From patron where count = ?";
                    for i in kitaplık:

                        if(self.kullanıc_adı_input.text()==i[0] and self.parola_input.text()==i[1]):
                            self.bilgilendirme_text.setText("Giriş Yapıldı!")
                            self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:15px;color:green")
                        else:
                            self.bilgilendirme_text.setText("Kullanıcı Adı veya Parola Hatalı!")
                            self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:15px;color:red")
                    self.cursor.execute(sorgu3,(self.count+1,))
                    self.connection.commit()




        else:

            sorgu2 = "Insert into patron values(?,?,?)"
            if (self.parola_input.text() != "" and self.kullanıc_adı_input.text() != ""):
                if (self.beni_hatırla_check_box.isChecked()):
                    self.count += 1
                else:
                    self.count=0
                self.cursor.execute(sorgu2, (self.kullanıc_adı_input.text(), self.parola_input.text(), self.count))
                self.connection.commit()
                self.bilgilendirme_text.setText("Giriş Yapıldı")
                self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:15px;color:green")
            elif (self.parola_input.text() == ""):
                self.bilgilendirme_text.setText("Eksiksiz doldurun!")
                self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:13px;color:red")
            elif (self.kullanıc_adı_input.text() == ""):
                self.bilgilendirme_text.setText("Eksiksiz doldurun!")
                self.bilgilendirme_text.setStyleSheet("margin-top:20px;font-size:13px;color:red")







app = QtWidgets.QApplication(sys.argv)
pencere = LoginPage()
sys.exit(app.exec_())
