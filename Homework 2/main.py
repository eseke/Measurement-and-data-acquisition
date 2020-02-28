import serial as ser
import sys
import numpy as np
import threading
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QWidget, QLineEdit,QTextEdit

try:
    ser = ser.Serial("COM4", 9600)  #otvaranje serijskog porta
except:
    print('Fatalna greska!!')
    sys.exit(0)


global pobedaB;
pobedaB = 0;
global pobedaA;
pobedaA = 0;
global fajl

class App(QWidget):           #klasa za gui u kojoj definisemo potrebne elemente gui-ja i funkcije dugmadi
    def __init__(self):
        super().__init__()
        self.left = 200
        self.top = 400
        self.width = 400
        self.heigh = 155
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Igra Iks-oks')
        self.setGeometry(self.left, self.top, self.width, self.heigh)
        self.setFixedSize(self.width, self.heigh)

        self.button1=QPushButton('Pokreni igru',self);
        self.button1.resize(100,50);
        self.button1.move(10,10);
        self.button1.clicked.connect(self.pokretanje_fcn);

        self.button2=QPushButton('Pokreni partiju',self);
        self.button2.resize(100,50);
        self.button2.move(150,10);
        self.button2.clicked.connect(self.partija_fcn);

        self.button3=QPushButton('Zaustavi',self);
        self.button3.resize(100,50);
        self.button3.move(290,10);
        self.button3.clicked.connect(self.zaustavi_fcn);

        self.text_output1 =QLabel('Igrac 1',self);
        self.text_output1.resize(100,20);
        self.text_output1.move(10,75);

        self.text_output2 =QLabel('Igrac 2',self);
        self.text_output2.resize(100,20);
        self.text_output2.move(10,100);

        self.text_output3 =QLabel('Ime fajla',self);
        self.text_output3.resize(100,20);
        self.text_output3.move(10,125);

       

        self.text_input1 =QLineEdit('fvef',self);
        self.text_input1.resize(100,20);
        self.text_input1.move(80,75);

        self.text_input2 =QLineEdit('vv',self);
        self.text_input2.resize(100,20);
        self.text_input2.move(80,100);

        self.text_input3 =QLineEdit('vwsdv',self);
        self.text_input3.resize(100,20);
        self.text_input3.move(80,125);

       
        self.show()
    
    def closeEvent(self, event):
         if ser.is_open:
            ser.close();
         if 'fajl' in globals():
            fajl.close();

    def pokretanje_fcn(self):             #klik na dugme pokreni igru
        if not((self.text_input1.text()=='') | (self.text_input2.text()=='') | (self.text_input3.text()=='')):
            
            self.button1.setDisabled(1);
            self.button2.setDisabled(0);
            app.processEvents();
            
            global fajl
            fajl = open(self.text_input3.text()+'.txt','a')
            fajl.writelines(self.text_input1.text()+' '+self.text_input2.text()+'\n');
            self.text_input1.setDisabled(1);
            self.text_input2.setDisabled(1);
            self.text_input3.setDisabled(1);
            br='3'
            ser.write(br.encode());
            br = '0'
            ser.write(br.encode());
            br = '0'
            ser.write(br.encode());

    def partija_fcn(self):              #pokretanje nove partije
        self.button2.setDisabled(1);
        self.button3.setDisabled(1);
        t1=threading.Thread(target=igra,args = (self,));
        t1.start();

    def zaustavi_fcn(self):            #zaustavljanje programa
        if ser.is_open:
            ser.close();   
        self.close();
        if 'fajl' in globals():
            fajl.close();
try:           
    def comm(a):              #funkcija koja komunicira sa arduinom
        global data;
        try:
            ser.write(a.encode());
            data=ser.readline();
            ser.flush();
        except:
            print('Fatalna greska! Iskljuci program!')
            if ser.is_open:
                ser.close();
            if 'fajl' in globals():
                fajl.close();
            sys.exit(0)
   

    def parsiraj(temp):     #parsiranje podataka sa seriala
        try:
            i=1;
            while(temp[i]!='\\'):
                i=i+1;
            return int(temp[2:i]);
        except:
            print('')

    def pob(mat):        #ispitivanje da li postoji pobednik
        mat1=np.sum(mat,0);
        mat2=np.sum(mat,1);
        zb1=0;
        zb2=0;
        global pobedaA
        global pobedaB
        for i in range(0,3):
            if((mat1[i]==3)|(mat2[i]==3)):
                pobedaA=pobedaA+1;
                return 1;
            elif((mat1[i]==0)|(mat2[i]==0)):
                    pobedaB=pobedaB+1;
                    return 1;
            zb1=zb1+mat[i,i];
            zb2=zb2+mat[i,2-i];
        if((zb1==3)|(zb2==3)):
            pobedaA=pobedaA+1;
            return 1;
        elif((zb1==0)|(zb2==0)):
            pobedaB=pobedaB+1;
            return 1;
        return 0;

    def ispis(mat):      #ispisivanje tabele igre
        for i in range(0,3):
            for j in range(0,3):
                if(j==2):
                    if(mat[i,j]<10):
                        print(str(mat[i,j])+' ');
                    else:
                        print(str(mat[i,j]));
                else:
                    if(mat[i,j]<10):
                        print(str(mat[i,j])+' ',end=' ');
                    else:
                        print(str(mat[i,j]),end=' ');
            if(i==2):
                print('-----------')

    def ner(mat):     #proverava neresen rezultat
        for i in range(0,3):
            for j in range(0,3):
                if(mat[i][j]==10):
                    return 0
        return 1

    def igra(self):        #glavna funkcija koja upravlja igrom
        try:
            mat=np.full((3,3),10);
            pobeda=0;
            neres=0;
            valid=0;
            ispis(mat);
            a='1';   
            while((pobeda==0)&(neres==0)):
                while(valid==0):
           
                    comm(a);
                    temp1=data;
                    temp1=parsiraj(str(temp1));
                    if(temp1<30):
                        valid=1;
           
       
                temp1=temp1//10;
                valid=0;
                while(valid==0):
            
                    comm(a);
                    temp2=data;
                    temp2=parsiraj(str(temp2));
                    if(temp2<30):
                        valid=1;
            
        
                temp2=temp2//10;
                if(a=='1'):
                    upis=1;
                else:
                    upis=0;
                global pobedaA,pobedaB
                if(mat[temp1,temp2]==10):
                    mat[temp1,temp2]=upis;
                    pobeda=pob(mat);
                    if(pobeda==0):
                        neres=ner(mat);
                    ispis(mat); 
                    if(a=='1'):
                        a='2';
                    else:
                        a='1';
                valid = 0;
            print('kraj partije');
            ex.button2.setEnabled(1);
            ex.button3.setEnabled(1);
            print('\n');
            print('\n');
    
            br='3'
            try:
                ser.write(br.encode());
                br = str(pobedaA)
                ser.write(br.encode());
                br = str(pobedaB)
                ser.write(br.encode());
    
                global fajl
                fajl.write(str(pobedaA)+' '+str(pobedaB)+'\n');
            except:
                print('Fatalna greska! Iskljuci program!')
                if ser.is_open:
                    ser.close();
                if 'fajl' in globals():
                    fajl.close();
                sys.exit(0)
        except:
            print('')
except:
    print('')
app=QApplication(sys.argv)     #instanciranje glavnog prozora
global ex
ex=App()
ex.button2.setDisabled(1)
app.exec_()
   

  