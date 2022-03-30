from pygame.locals import *
import pygame #pygame(pyhton ile oyun yapma motoru) kütüphanesi çağırıldı
import sqlite3
from random import sample
import os

pygame.init() #pygame başlatıldı
pygame.display.set_caption("Justhink") # pencere (oyunun) adı


##############      GÖRSELLER KISMI     ###############
#	ekran arkaplanları
ozelT_image = pygame.image.load("SpecialThanks-1.png.png")
ayarlar_image = pygame.image.load("Settings-1.png.png")
referanslar_image = pygame.image.load("References-1.png.png")
menuEkrani_image = pygame.image.load("Menuekranı.png")
dialogkutusu_image = pygame.image.load("DialogBox.png")
kullanici_image = pygame.image.load("UnknownPerson-1.png.png")
laptop_image = pygame.image.load("Laptop-1.png.png")
laptop_image = pygame.transform.scale(laptop_image,(800,600))
masaustu_image = pygame.image.load("ekran+MasaUstu.jpeg")
masaustu_image = pygame.transform.scale(masaustu_image,(800,600))

oyuncu_surf = pygame.image.load("Labirent(sen)-1.png.png")
block_surf = pygame.image.load("Labirent(bitis)-3.png.png")
bitis_surf = pygame.image.load("Labirent(bitis)-2.png.png")

yuz1_image = pygame.image.load('Face-1.png.png')
yuz2_image = pygame.image.load('Face-2.png.png')
yuz3_image = pygame.image.load('Face-3.png.png')
yuz4_image = pygame.image.load('Face-4.png.png')

#	Butonların görselleri
geri_butonu_yuzey = pygame.image.load("back_button.png")
geri_butonu_basilmis_yuzey = pygame.image.load("back_button_green.png")

oyna_butonu_yuzey = pygame.image.load("Oyna_ikonu.png")
oyna_butonu_basilmis_yuzey = pygame.image.load("Oyna_ikonu_basılı.png")

ozelt_butonu_yuzey = pygame.image.load("Ozelt_ikonu.png")
ozelt_butonu_basilmis_yuzey = pygame.image.load("Ozelt_ikonu_basılı-1.png.png")

ayarlar_butonu_yuzey = pygame.image.load("Ayarlar_ikonu.png")
ayarlar_butonu_basilmis_yuzey = pygame.image.load("Ayarlar_ikonu_basılı.png")

referanslar_butonu_yuzey = pygame.image.load("Referanslar_ikonu.png")
referanslar_butonu_basilmis_yuzey = pygame.image.load("Referanslar_ikonu_basılı.png")

dialog_butonu_yuzey = pygame.image.load("Dialogbutton.png")
dialog_butonu_basilmis_yuzey = pygame.image.load("Dialogbutton_basılı.png")

masaustu_butonu_yuzey = pygame.image.load("masaustu_butonu.png")
masaustu_butonu_basilmis_yuzey = pygame.image.load("masaustu_butonu_basili.png")

sesacik_butonu_yuzey = pygame.image.load("sound_on.png")
sesacik_butonu_basilmis_yuzey = pygame.image.load("sound_on_basilmis.png")

seskapali_butonu_yuzey = pygame.image.load("sound_off.png")
seskapali_butonu_basilmis_yuzey = pygame.image.load("sound_off_basilmis.png")

sifirla_butonu_yuzey = pygame.image.load("sifirla_butonu.png")
sifirla_butonu_basilmis_yuzey = pygame.image.load("sifirla_butonu_basilmis.png")


class DataBase():
	def __init__(self):
		#kullanıcı adı = (ka)
		self.eski_ka = ''
		#tamamlanan level = (tl)
		self.eski_tl = 0
		#muzik = (mz)
		self.eski_mz = 1

		self.dongu_sayi = 0

	def downdate(self):
		print("c")
		with sqlite3.connect("justhink.db") as con :
			cursor = con.cursor()
			try :
				print("b")
				con.execute("CREATE TABLE justhink_data(kullanici_adi TEXT,tamamlanan INT,muzik BOOL)")
				con.execute("INSERT INTO justhink_data(kullanici_adi,tamamlanan,muzik) VALUES(:b1,:b2,:b3)",{'b1':'','b2':0,'b3':1})
			except sqlite3.OperationalError:
				print("c")
				cursor.execute("SELECT * from justhink_data")
				for i in cursor.fetchall() :
					self.eski_ka = i[0]
					self.eski_tl = i[1]
					self.eski_mz = i[2]
				if self.eski_ka != '' :
					if self.eski_ka != g.kullanici_adi :
						g.kullanici_adi = self.eski_ka
				if self.eski_tl != 0 :
					if self.eski_tl != l.tamamlanan :
						l.tamamlanan = self.eski_tl
						l.mevcut_level = l.tamamlanan +1
				if self.eski_mz!= 1 :
					g.muzik = self.eski_mz
			con.commit()

	def update(self,kontrol):
		with sqlite3.connect("justhink.db") as con :
			cursor = con.cursor()
			if kontrol == 'ka'and g.kullanici_adi != self.eski_ka :
				cursor.execute("UPDATE justhink_data SET kullanici_adi=:b1",{'b1':g.kullanici_adi})
				self.eski_ka = g.kullanici_adi
			elif kontrol == 'tl'and l.tamamlanan != self.eski_tl :
				cursor.execute("UPDATE justhink_data SET tamamlanan=:b1",{'b1':l.tamamlanan})
				self.eski_tl = l.tamamlanan
			elif kontrol == 'mz'and g.muzik != self.eski_mz :
				cursor.execute("UPDATE justhink_data SET muzik=:b1",{'b1':g.muzik})
				self.eski_mz = g.muzik
			con.commit()

	def resetle(self):
		g.SCREEN = None
		g.pencere.fill(g.siyah)
		text_blit("İLERLEME SIFIRLANDI","ortala",285,30,"beyaz")
		if self.dongu_sayi <= 250 :
			self.dongu_sayi += 1
		else :
			ekran_gecisi_1.yap("beyaz")
			if ekran_gecisi_1.dongu == False :
				self.dongu_sayi = 0
				self.bolumekrani_dongu = 0
				sifirla_butonu.dongu = False
				self.dialog = True
				ekran_gecisi_1.__init__()
				ekran_gecisi_2.__init__()
				geciken_blit_1.__init__()
				geciken_blit_2.__init__()
				player.__init__()
				g.SCREEN = 'menu'
				g.kullanici_adi = ''
				l.__init__()
				soru_1.rastgele_soru()
				soru_1.soru_cek()
				soru_2.soru_cek()
				soru_3.soru_cek()
				if g.muzik == 0:
					seskapali_butonu.dongu = True
					g.muzik = 1
				self.update('ka')
				self.update('tl')
				self.update('mz')

#database'i kullanmak için bir nesne
db=DataBase()


####     EKRANA YAZI YAZDIRMA
def text_blit(text,yazikonumu_x,yazikonumu_y,yaziY=14,renk="siyah"):
	font=pygame.font.SysFont("Helvetica",yaziY)
	if renk == "siyah":
		yazi = font.render(text,1,(0,0,0))
	elif renk == "beyaz":
		yazi = font.render(text,1,(255,255,255))
	elif renk == 'kirmizi':
		yazi = font.render(text,1,(204,0,0))
	elif renk == 'yesil':
		yazi = font.render(text,1,(0,204,0))
	yaziX = yazi.get_size()[0]
	if yazikonumu_x == "ortala":
		yazikonumu_x = (800-yaziX) // 2
	g.pencere.blit(yazi,(yazikonumu_x,yazikonumu_y))
class Geciken_yazi() :
	def __init__(self):
		self.dongu = True
		self.i = 0
		self.gecik = 0
		self.max_ = 0
		self.cumle = ""
		self.font=pygame.font.SysFont("Helvetica",18)
	def ciz(self,text,yazikonumu_x,yazikonumu_y) :
		if not (self.cumle in text):
			self.i = 0
			self.gecik = 0
			self.max_ = 0
			self.cumle = ""
		if self.gecik == self.max_ and self.dongu == True:
			self.cumle += text[self.i]
			if len(self.cumle) < len(text) :
				self.i += 1
			if self.cumle != text :
				self.max_+=4
		if self.cumle != text and self.i < len(text) and self.dongu == True:
			self.gecik+=1
			yazi = self.font.render(self.cumle,1,(255,255,255))
		else :
			self.dongu = False
			self.i = 0
			self.gecik = 0
			self.max_ = 0
			self.cumle = ""
			yazi = self.font.render(text,1,(255,255,255))
		g.pencere.blit(yazi,(yazikonumu_x,yazikonumu_y))
def tablo1():
			text_blit('Cevabınızı girip ENTER\'a basınız','ortala',292,)
			text_blit('Operatör:',200,20,24)
			text_blit('+',200,48,24)
			text_blit('-',200,76,24)
			text_blit('*',200,104,24)
			text_blit('/',200,132,24)
			text_blit('%',200,160,24)
			text_blit('**',200,188,24)
			text_blit('//',200,216,24)

			text_blit('Adı:',350,20,24)
			text_blit('Toplama',350,48,24)
			text_blit('Çıkarma',350,76,24)
			text_blit('Çarpma',350,104,24)
			text_blit('Bölme',350,132,24)
			text_blit('Mod Alma',350,160,24)
			text_blit('Üs Alma',350,188,24)
			text_blit('Tam Bölme',350,216,24)

			text_blit('Örnek:',500,20,24)
			text_blit('2 + 3 = 5',500,48,24)
			text_blit('3 - 2 = 1',500,76,24)
			text_blit('3 * 2 = 6',500,104,24)
			text_blit('3 / 2 = 1.5',500,132,24)
			text_blit('5 % 2 = 1',500,160,24)
			text_blit('2 ** 3 = 8',500,188,24)
			text_blit('3 // 2 = 1',500,216,24)

# geciken yazı komutunu vermek için bir nesne olusturdum
geciken_blit_1 = Geciken_yazi()
geciken_blit_2 = Geciken_yazi()



##############      LABİRENT SINIFLARI #############
class Maze() :
	def __init__(self):
		self.cikis = None
		self.duvarlar = []
		self.M = 40
		self.N = 30
		self.maze = [
		0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
		0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,
		0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
		0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,
		0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,
		0,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,
		0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,
		0,1,0,1,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,
		0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,
		0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,
		0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,
		0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,
		0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,
		0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,
		0,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,
		0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
		0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,
		0,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,0,1,
		0,1,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,
		0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,
		0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,
		0,1,1,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,
		0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,
		0,1,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,
		0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,2,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,
		0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
			]

	def draw(self):
		bx = 0
		by = 0
		for i in range(0,self.M*self.N):
			if self.maze[ bx + (by*self.M) ] == 1:
				duvar_konumu = (bx * 20 , by * 20)
				g.pencere.blit(block_surf,duvar_konumu)
				self.duvarlar.append(duvar_konumu)
			elif self.maze[ bx + (by*self.M) ] == 2:
				self.cikis_konumu = bx * 20 , by * 20
				g.pencere.blit(bitis_surf,self.cikis_konumu)
			bx = bx + 1
			if bx > self.M-1:
				bx = 0 
				by = by + 1
maze = Maze()

class Player() :
	def __init__(self) :
		self.x = 360
		self.y = 560
		self.hiz = 20
		self.duvarlar = maze.duvarlar
		self.ilerle = 1
		self.dongu = True

	def kontrol(self,event):
		if (event.key == K_RIGHT):
			if (self.x + self.hiz,self.y) in self.duvarlar:
				self.ilerle = 0
			self.x = self.x + self.hiz*self.ilerle
		elif (event.key == K_LEFT):
			if (self.x - self.hiz,self.y) in self.duvarlar:
				self.ilerle = 0
			self.x = self.x - self.hiz*self.ilerle
		elif (event.key == K_UP):
			if (self.x,self.y - self.hiz) in self.duvarlar:
				self.ilerle = 0
			self.y = self.y - self.hiz*self.ilerle
		elif (event.key == K_DOWN):
			if (self.x,self.y + self.hiz) in self.duvarlar:
				self.ilerle = 0
			self.y = self.y + self.hiz*self.ilerle
		self.ilerle = 1
		if maze.cikis_konumu == (self.x,self.y) :
			self.dongu = False

player = Player()


##############      BUTON SINIFI     ###############
class Button():
	def __init__(self, image, basilmis_image, x_konum, y_konum,kontrol = False):
		self.dongu = False

		self.kontrol = kontrol
		self.deger = False
		self.image = image
		self.basilmis_image = basilmis_image
		self.x_konum = x_konum
		self.y_konum = y_konum
		self.rect = self.image.get_rect(center=(self.x_konum, self.y_konum))

	def checkForInput(self, position):
		if self.kontrol == False :
			if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
				self.dongu = True
		elif self.kontrol == True :
			if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
				if self.deger == True :
					self.dongu = True
					self.deger = False
				else :
					self.deger = True
			else :
				self.deger = False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			g.pencere.blit(self.basilmis_image, self.rect)
		else:
			g.pencere.blit(self.image, self.rect)
###  BUTONLARI OLUŞTURMA ###
oyna_butonu = Button(oyna_butonu_yuzey,oyna_butonu_basilmis_yuzey,399,300)
ozelt_butonu = Button(ozelt_butonu_yuzey,ozelt_butonu_basilmis_yuzey,149,535)
ayarlar_butonu = Button(ayarlar_butonu_yuzey,ayarlar_butonu_basilmis_yuzey,399,520)
referanslar_butonu = Button(referanslar_butonu_yuzey,referanslar_butonu_basilmis_yuzey,649,535)
geri_butonu = Button(geri_butonu_yuzey,geri_butonu_basilmis_yuzey,35,35)
dialog_butonu = Button(dialog_butonu_yuzey,dialog_butonu_basilmis_yuzey,455,578)
masaustu_butonu = Button(masaustu_butonu_yuzey,masaustu_butonu_basilmis_yuzey,386,305)
muzikacik_butonu = Button(masaustu_butonu_yuzey,masaustu_butonu_basilmis_yuzey,386,305)
sesacik_butonu = Button(sesacik_butonu_yuzey,sesacik_butonu_basilmis_yuzey,400,325)
seskapali_butonu = Button(seskapali_butonu_yuzey,seskapali_butonu_basilmis_yuzey,400,325)
sifirla_butonu = Button(sifirla_butonu_yuzey,sifirla_butonu_basilmis_yuzey,400,200,True)


class soru_butonu() :
	def __init__(self,box_y,level,soru_sayisi):
		self.liste = []
		self.sayi = None
		self.soru = None
		self.cevap = None
		self.soru_sayisi = soru_sayisi

		self.girdi = ""
		self.sonuc = None
 
		self.box_y = box_y
		self.font = pygame.font.SysFont("helvetica",24)
		self.color_acik = pygame.Color('lightskyblue3')
		self.color_koyu = pygame.Color('gray30')
		self.color_yesil = pygame.Color('green3')
		self.color = self.color_koyu
		self.text_butonu_aktif = False
		self.box_x = 350
		self.box_w = 0
		if self.soru_sayisi == 1 :
			for i in range(1,10):
				self.liste.append(((level-1)*10)+i)
		self.rastgele_soru()
		self.soru_cek()

	def rastgele_soru(self):
		if self.soru_sayisi == 1 :
			self.sorular = sample(self.liste,k=3)
			self.sayi = self.sorular[0]
	def soru_cek(self):
		if self.soru_sayisi != 1 :
			self.sayi = soru_1.sorular[self.soru_sayisi-1]
		with sqlite3.connect("justhink.db") as con :
			cursor = con.cursor()
			try :
				con.execute("CREATE TABLE justhink_soru(soru TEXT,cevap TEXT,_id INT)")
				for i in range(1,10):
					if i == 1 :
						bilgi_1,bilgi_2,bilgi_3='Mario ((7-3) kere (5//2) adım ilerleyip) ,3 adım geri gelirse kaç adım ilerlemiş olur ?', '5', 1
					elif i == 2 :
						bilgi_1,bilgi_2,bilgi_3='Mario ((70//7,6) kere 3 adım geri 6 adım ileri) giderse kaç adım ilerlemiş olur ?', '27', 2
					elif i == 3 :
						bilgi_1,bilgi_2,bilgi_3='Mario 3 adım ileri gidip (216-230) geri gelirse kaç adım ilerlemiş olur ?', '17', 3
					elif i == 4 :
						bilgi_1,bilgi_2,bilgi_3='Mario ((3**2)*2 adım) geri gelip (8-33 kere) geri giderse kaç adım ilerlemiş olur ?', '7', 4
					elif i == 5 :
						bilgi_1,bilgi_2,bilgi_3='Mario (2-5*2 adım) ilerleyip ((-3)*6/2 adım) geri gelirse kaç adım ilerlemiş olur ?', '1', 5
					elif i == 6 :
						bilgi_1,bilgi_2,bilgi_3='Mario (5 adım) ileri (1*3-2/2) geri gelirse kaç adım gerilemiş olur ?', '-3', 6
					elif i == 7 :
						bilgi_1,bilgi_2,bilgi_3='Mario (20*36)/(2*18) adım ileri ve (20 adım) geri gelirse kaç adım atmış olur ?', '40', 7
					elif i == 8 :
						bilgi_1,bilgi_2,bilgi_3='Mario (2/3 kere 27 adım) ileri (10 adım) geri gelirse kaç adım atmış olur ?', '28', 8
					elif i == 9 :
						bilgi_1,bilgi_2,bilgi_3='Mario 2(123%29 adım) ilerlerse kaç adım ilerlemiş olur ?', '14', 9

					con.execute("INSERT INTO justhink_soru(soru,cevap,_id) VALUES(:b1,:b2,:b3)",{'b1':bilgi_1,'b2':bilgi_2,'b3':bilgi_3})
					print("a")
			except :
				pass
			cursor.execute("SELECT * from justhink_soru WHERE _id =:sayi",{'sayi':self.sayi})
			for i in cursor.fetchall() :
				self.soru = i[0]
				self.cevap = i[1]

	def mousedown_kontrol(self,event,position):
		if not self.sonuc :
			if self.input_rect.collidepoint(position) :
				self.text_butonu_aktif = True
			elif not self.input_rect.collidepoint(position) :
				self.text_butonu_aktif = False
	def key_kontrol(self,event):
		if not self.sonuc :
			if self.text_butonu_aktif == True :
				if event.key == pygame.K_BACKSPACE:
					self.girdi = self.girdi[:-1]
				elif event.key == pygame.K_RETURN :
					if self.girdi == self.cevap :
						self.sonuc = True
					else :
						self.sonuc = False
				elif len(self.girdi)<=5:
					self.girdi += event.unicode
	def ciz(self):
		text_blit(self.soru,'ortala',self.box_y - 40,18)
		if self.sonuc == True:
			self.color = self.color_yesil
			text_blit('Cevabınız Doğru !','ortala',self.box_y + 24,18,'yesil')
		else :
			if self.text_butonu_aktif :
				self.color = self.color_acik
			else :
				self.color = self.color_koyu
			if self.sonuc == False :
				text_blit('Cevabınız Yanlış !','ortala',self.box_y + 24,18,'kirmizi')
		if self.sonuc == True:
			g.pencere.blit(self.text_surface,(self.input_rect.x + 5,self.input_rect.y + 5))
			pygame.draw.rect(g.pencere,self.color,self.input_rect,2)
		else : 
			self.input_rect = pygame.Rect(self.box_x,self.box_y-16,self.box_w,32)
			self.text_surface = self.font.render(self.girdi,True,(0,0,0))
			pygame.draw.rect(g.pencere,self.color,self.input_rect,2)
			g.pencere.blit(self.text_surface,(self.input_rect.x + 5,self.input_rect.y + 5))
			self.box_x = 400 - max(50,self.text_surface.get_width() // 2)
			self.box_w = max(100,self.text_surface.get_width() + 10)

#	soru-cevap butonları :
soru_1 = soru_butonu(350,1,1)
soru_2 = soru_butonu(450,1,2)
soru_3 = soru_butonu(550,1,3)

class ad_alma_butonu() :
	def __init__(self,box_y):
		self.dongu = True 
		self.box_y = box_y
		self.font = pygame.font.SysFont("helvetica",24)
		self.color_acik = pygame.Color('lightskyblue3')
		self.color_koyu = pygame.Color('gray30')
		self.color = self.color_koyu
		self.text_butonu_aktif = False
		self.box_x = 350
		self.box_w = 0
	
	def mousedown_kontrol(self,event,position):
		if self.input_rect.collidepoint(position) :
			self.text_butonu_aktif = True
		elif not self.input_rect.collidepoint(position) :
			self.text_butonu_aktif = False
	def key_kontrol(self,event):
		if self.text_butonu_aktif == True :
			if event.key == pygame.K_BACKSPACE:
				g.kullanici_adi= g.kullanici_adi[:-1]
			elif event.key == pygame.K_RETURN :
				self.dongu=False
			elif len(g.kullanici_adi)<=20:
				g.kullanici_adi += event.unicode
	def ciz(self):
		if self.text_butonu_aktif :
			self.color = self.color_acik
		else :
			self.color = self.color_koyu
		self.input_rect = pygame.Rect(self.box_x,self.box_y-16,self.box_w,32)
		self.text_surface = self.font.render(g.kullanici_adi,True,(255,255,255))
		pygame.draw.rect(g.pencere,self.color,self.input_rect,2)
		g.pencere.blit(self.text_surface,(self.input_rect.x+5,self.input_rect.y+5))
		self.box_x = 400 - max(50,self.text_surface.get_width()//2)
		self.box_w = max(100,self.text_surface.get_width() + 10)
		db.update('ka')
		
### Text inputu alan butonları oluşturma
ad_al_butonu = ad_alma_butonu(300)
ad_degis_butonu = ad_alma_butonu(500)

########## Daha iyi görüntü için geçiş animasyon sınıfları
class ekran() :
	def __init__(self):
		self.gecis = 0
		self.dongu = True
		self.renk_6 = 0,0,0
		self.renk_5 = 55,55,55
		self.renk_4 = 105,105,105
		self.renk_3 = 155,155,155
		self.renk_2 = 205,205,205
		self.renk_1 = 230,230,230
	def yap(self,yon):
		if yon == "beyaz" :
			self.renk_1 = 25,25,25
			self.renk_2 = 50,50,50
			self.renk_3 = 100,100,100
			self.renk_4 = 150,150,150
			self.renk_5 = 200,200,200
			self.renk_6 = 255,255,255
		elif yon == "siyah" :
			self.renk_6 = 0,0,0
			self.renk_5 = 55,55,55
			self.renk_4 = 105,105,105
			self.renk_3 = 155,155,155
			self.renk_2 = 205,205,205
			self.renk_1 = 230,230,230
		if self.gecis <=210 :
			if self.gecis<=35:
				g.pencere.fill((self.renk_1))
			elif self.gecis<=70:
				g.pencere.fill((self.renk_2))
			elif self.gecis<=105:
				g.pencere.fill((self.renk_3))
			elif self.gecis<=140:
				g.pencere.fill((self.renk_4))
			elif self.gecis<=175:
				g.pencere.fill((self.renk_5))
			else:
				g.pencere.fill((self.renk_6))
			self.gecis += 1
		else :
			self.dongu = False
			self.gecis = 0
### ekran geçisi nesnesi
ekran_gecisi_1 = ekran()
ekran_gecisi_2 = ekran()


class Dialog_kutusu() :
	def __init__(self):
		self.dialogdongunun_sayisi = 0
		self.dialog_yapildi = False
		self.sayi = 21
	def ciz(self,konusan) :
		if dialog_butonu.dongu == True :
			if self.dialogdongunun_sayisi <= 7:
				g.pencere.blit(dialogkutusu_image,(0,429 + int(self.sayi)))
				self.dialogdongunun_sayisi += 0.2
				self.sayi += 5
			else :
				l.dialog = False
				self.dialogdongunun_sayisi = 0
				dialog_butonu.dongu = False
				self.sayi = 0
		else:
			l.dialog = True
			g.pencere.blit(dialogkutusu_image,(0,429))
			dialog_butonu.changeColor((g.x,g.y))
			if konusan == "kullanici" :
				g.pencere.blit(kullanici_image,(22,460))
			elif konusan == 'yuz_1' :
				g.pencere.blit(yuz1_image,(29,480))
			elif konusan == 'yuz_2' :
				g.pencere.blit(yuz2_image,(29,480))
			elif konusan == 'yuz_3' :
				g.pencere.blit(yuz3_image,(29,480))
			elif konusan == 'yuz_4' :
				g.pencere.blit(yuz4_image,(29,480))
	
#
dialog_kutusu = Dialog_kutusu()
dialog_kutusu_2 = Dialog_kutusu()

class Gunluk_gif(pygame.sprite.Sprite) :
	def __init__ (self) :
		super().__init__()
		self.sayi=1
# 	gif için görselleri indirme ve liste oluşturma
		self.sprites = []
		self.mevcut_sprite = 0

	def guncelle(self) :
		if self.sayi <= 18 :
			self.sprites.append(pygame.image.load(f'Diary-{self.sayi}.png.png'))
			self.sayi += 1
		self.image = self.sprites[int(self.mevcut_sprite)]
		self.mevcut_sprite += 0.3
		if self.mevcut_sprite >= len(self.sprites) :
			self.mevcut_sprite = 0
		self.image = self.sprites[int(self.mevcut_sprite)]
		g.pencere.blit(self.image,(0,-50))

# gunluk gifini kullanmak için nesne
gunluk = Gunluk_gif()






##############      OYUNU YÜRÜTME  SINIFI     ###############
class Game():
	def __init__(self):
		self.running ,self.playing ,self.oyunda = True,True,False
		self.SCREEN = "menu"
		self.kullanici_adi = ''
		self.muzik = 1
		self.clock = pygame.time.Clock()
		self.pencere = pygame.display.set_mode((800,600) , pygame.HWSURFACE) # 800 ,600 boyutunda video penceresi aç
		self.siyah,self.beyaz = (0,0,0),(255,255,255) # rgb renklerine değişken atandı
		self.mouseX,self.mouseY = None,None

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running, self.playing = False,False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if self.SCREEN == "menu":
					oyna_butonu.checkForInput((self.x,self.y))
					ozelt_butonu.checkForInput((self.x,self.y))
					ayarlar_butonu.checkForInput((self.x,self.y))
					referanslar_butonu.checkForInput((self.x,self.y))
				else:
					if self.SCREEN != None :
						geri_butonu.checkForInput((self.x,self.y))
					if l.mevcut_level == "kullanici_adi_al" and self.oyunda == True:
						ad_al_butonu.mousedown_kontrol(event,(self.x,self.y))
					if self.SCREEN == "ayarlar" :
						ad_degis_butonu.mousedown_kontrol(event,(self.x,self.y))
						if self.muzik == 1 :
							sesacik_butonu.checkForInput((self.x,self.y))
						elif self.muzik == 0 :
							seskapali_butonu.checkForInput((self.x,self.y))
						sifirla_butonu.checkForInput((self.x,self.y))
					if l.dialog == True :
						dialog_butonu.checkForInput((self.x,self.y))
					if l.mevcut_level == 1 and self.oyunda == True and l.kisim == 4:
						masaustu_butonu.checkForInput((self.x,self.y))
					if l.mevcut_level == 2 and l.kisim == 2 :
						soru_1.mousedown_kontrol(event,(self.x,self.y))
						soru_2.mousedown_kontrol(event,(self.x,self.y))
						soru_3.mousedown_kontrol(event,(self.x,self.y))
			if event.type == pygame.KEYDOWN :
				if l.mevcut_level == "kullanici_adi_al" and self.oyunda == True:
					ad_al_butonu.key_kontrol(event)
				if self.SCREEN == "ayarlar" :
					ad_degis_butonu.key_kontrol(event)
				if l.mevcut_level == 2 and l.kisim == 2 :
					soru_1.key_kontrol(event)
					soru_2.key_kontrol(event)
					soru_3.key_kontrol(event)
				if l.mevcut_level == 2 and l.kisim == 'hack_1' :
					player.kontrol(event)

	def oyun_dongusu(self):
		while self.playing :
			db.downdate
			self.x,self.y=pygame.mouse.get_pos()
			self.check_events()
			if self.oyunda == False :
				if self.SCREEN == 'ayarlar' or self.SCREEN == None :
					if sifirla_butonu.dongu == True :
						db.resetle()
					if self.SCREEN == 'ayarlar' :
						if self.muzik == 1 and sesacik_butonu.dongu == True:
							self.muzik = 0
							sesacik_butonu.dongu = False
							db.update('mz')
						elif self.muzik == 0 and seskapali_butonu.dongu == True:
							self.muzik = 1
							seskapali_butonu.dongu = False
							db.update('mz')
				if oyna_butonu.dongu == True:
					self.SCREEN = "mevcut_level"
					oyna_butonu.dongu=False
				if ozelt_butonu.dongu == True:
					self.SCREEN = "ozelt"
					ozelt_butonu.dongu=False
				if ayarlar_butonu.dongu == True:
					self.SCREEN = "ayarlar"
					ayarlar_butonu.dongu=False
				if referanslar_butonu.dongu == True:
					self.SCREEN = "referanslar"
					referanslar_butonu.dongu=False
				if geri_butonu.dongu == True:
					self.SCREEN = "menu"
					geri_butonu.dongu=False
			elif self.SCREEN == "mevcut_level":
				l.play_mevcut_level()
				if geri_butonu.dongu == True:
					self.SCREEN = "menu"
					geri_butonu.dongu=False


			self.ekrani_boya()
			pygame.display.update()

	def ekrani_boya(self):
		self.oyunda_mi()
		if self.SCREEN == "menu" :
			self.pencere.blit(menuEkrani_image,(0,0))
			text_blit("Oynadığınız için teşekkürler !","ortala",115,12)
			text_blit("Bu oyundaki yazılım bilgisi","ortala",216,12)
			text_blit("Python dili esaslıdır","ortala",230,12)
			text_blit("Justhink","ortala",400,30)
			oyna_butonu.changeColor((self.x,self.y))
			ozelt_butonu.changeColor((self.x,self.y))
			ayarlar_butonu.changeColor((self.x,self.y))
			referanslar_butonu.changeColor((self.x,self.y))
		else:
			if self.oyunda == False:
				if self.SCREEN == "ozelt":
					self.pencere.blit(ozelT_image,(0,0))
				elif self.SCREEN == "ayarlar":
					self.pencere.blit(ayarlar_image,(0,0))
					text_blit("Adınızda değişiklik yapabilirsiniz","ortala",450,24,"beyaz")
					text_blit("Müzik Açma/Kapama","ortala",257,24,"beyaz")
					text_blit("İlerleme SIFIRLAMA (çift basın)","ortala",132,24,"beyaz")
					ad_degis_butonu.ciz()
					sifirla_butonu.changeColor((self.x,self.y))
					if self.muzik == 1 :
						sesacik_butonu.changeColor((self.x,self.y))
					elif self.muzik == 0 :
						seskapali_butonu.changeColor((self.x,self.y))
				elif self.SCREEN == "referanslar":
					self.pencere.blit(referanslar_image,(0,0))
			else:
				if l.mevcut_level == "kullanici_adi_al"and self.SCREEN == "mevcut_level":
					self.pencere.fill(self.siyah)
					ad_al_butonu.ciz()
					text_blit("GİRİŞ BÖLÜMÜ","ortala",168,24,"beyaz")
					text_blit("Adınızı giriniz (en fazla 20 karakter olarak)","ortala",202,24,"beyaz")
					text_blit("Her zaman ayarlardan değiştirilebilir","ortala",236,24,"beyaz")
					text_blit("Devam etmek için Enter'a basın","ortala",340,18,"beyaz")

				elif l.mevcut_level == 2 and l.kisim == 2 :
					soru_1.ciz()
					soru_2.ciz()
					soru_3.ciz()
			if self.SCREEN != None :
				geri_butonu.changeColor((self.x,self.y))

	def oyunda_mi(self):
		if self.SCREEN == "menu" or self.SCREEN == "ozelt" or self.SCREEN == "ayarlar" or self.SCREEN == "referanslar" or self.SCREEN == None :
			self.oyunda=False
		else :
			self.oyunda=True
class Game_level():
	def __init__(self):
		self.mevcut_level = "kullanici_adi_al"
		self.level_gecildi = False
		self.tamamlanan = 0
		self.dialog = True
		self.kisim = 1
		self.bolumekrani_dongu = 0
	def play_mevcut_level(self):
		if type(self.mevcut_level) == int:
			if self.mevcut_level == 1:
				self.intro()
			elif self.mevcut_level == 2:
				self.level_2()
			elif self.mevcut_level == 3:
				self.level_3()
			elif self.mevcut_level == 4:
				self.level_4()
			elif self.mevcut_level == 5:
				self.level_5()
			elif self.mevcut_level == 6:
				self.level_6()
			elif self.mevcut_level == 7:
				self.level_7()
			elif self.mevcut_level == 8:
				self.level_8()
			elif self.mevcut_level == 9:
				self.level_9()
			elif self.mevcut_level == 10:
				self.final()
			if self.level_gecildi == True:
				self.mevcut_level+=1
				self.tamamlanan+=1
				self.kisim = 1
				self.level_gecildi = False
				db.update('tl')
		elif self.mevcut_level == "kullanici_adi_al":
			if self.tamamlanan == 0 :
				self.kullanici_adi_al()
			else :
				self.mevcut_level = self.tamamlanan
	def kullanici_adi_al(self):
		self.mevcut_level = "kullanici_adi_al"
		if ad_al_butonu.dongu == False :
			ad_al_butonu.dongu = True
			self.mevcut_level = self.tamamlanan + 1

	def intro(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("beyaz")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.beyaz)
				gunluk.guncelle()
				if self.dialog == True :
					dialog_kutusu.ciz("kullanici")
				if dialog_butonu.dongu == False and self.dialog == True :
					text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
					geciken_blit_1.ciz("Günlüğüme bakıyordum ,her günümün aynı geçtiğini fark ettim. Büyü-",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("müştüm ,ama hiç üretken değildim. Bir amaç edinmek istiyordum.",200,509)
				elif self.dialog == False:
					self.kisim += 1
					self.dialog = True
					geciken_blit_1.dongu = True
					geciken_blit_2.dongu = True
					ekran_gecisi_1.dongu = True

		elif self.kisim == 2 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					g.pencere.blit(laptop_image,(0,0))
					text_blit("Justhink","ortala",176,30,"siyah")
					text_blit("asistan ile oyun yapımı !","ortala",210,24,"siyah")
					if self.dialog == True :
						dialog_kutusu.ciz("kullanici")
					if dialog_butonu.dongu == False and self.dialog == True :
						text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
						geciken_blit_1.ciz("kod yazmak bana mantıklı geldi. Ücretsiz kaynakları araştırdım ",200,487)
						if geciken_blit_1.dongu == False : 
							geciken_blit_2.ciz("ve kodlama temelleri ile oyun yapmak için JUSTHINK'i buldum",200,509)
					elif self.dialog == False:
						self.kisim += 1
						self.dialog = True
						geciken_blit_1.dongu = True
						geciken_blit_2.dongu = True
						ekran_gecisi_1.dongu = True
						ekran_gecisi_2.dongu = True
		elif self.kisim == 3 :
			g.pencere.fill(g.beyaz)
			g.pencere.blit(laptop_image,(0,0))
			text_blit("Justhink","ortala",176,30,"siyah")
			text_blit("asistan ile oyun yapımı !","ortala",210,24,"siyah")
			if self.dialog == True :
				dialog_kutusu.ciz("kullanici")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
				text_blit("Justhink","ortala",176,30,"siyah")
				text_blit("asistan ile oyun yapımı !","ortala",210,24,"siyah")
				geciken_blit_1.ciz("Uygulamayı denesem ne kaybedebilirdim ,indirdim",200,487)
			elif self.dialog == False:
				self.kisim += 1
				self.dialog = True
				geciken_blit_1.dongu = True

		elif self.kisim == 4 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					g.pencere.blit(masaustu_image,(0,0))
					masaustu_butonu.changeColor((g.x,g.y))
					if self.dialog == True :
						dialog_kutusu.ciz("kullanici")
					if dialog_butonu.dongu == False and self.dialog == True :
						text_blit(g.kullanici_adi + " :",180,465,18,"beyaz")
						geciken_blit_1.ciz("Uygluma indi ve masaustume ekledim (dialog kutusunu kapatıp uygula-",200,487)
						if geciken_blit_1.dongu == False : 
							geciken_blit_2.ciz("maya basın ve Bölüm 2 başlasın)",200,509)
					elif self.dialog == False:
						if masaustu_butonu.dongu == True :
							masaustu_butonu.dongu = False
							self.dialog = True
							self.level_gecildi = True
							geciken_blit_1.dongu = True
							geciken_blit_2.dongu = True
							ekran_gecisi_1.dongu = True
							ekran_gecisi_2.dongu = True
	def level_2(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("2. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 'ara1'
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True
		elif self.kisim == 'ara1' :
			g.pencere.fill(g.beyaz)
			tablo1()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("Justhink'e Hoşgeldin !",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("Oyun yapma eğitimi 6 kursdan oluşmakta.",200,509)
			elif self.dialog == False:
				self.kisim = 'ara2'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'ara2' :
			g.pencere.fill(g.beyaz)
			tablo1()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_1")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("Şuan 1. kurstasın .Bu Dialoğu kapattığında çıkacak soruların ,yukarıdaki",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("tabloya göre , doğru cevaplarını bul !",200,509)
			elif self.dialog == False:
				self.kisim = 2
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 2 :
			g.pencere.fill(g.beyaz)
			tablo1()
			if soru_1.sonuc and soru_2.sonuc and soru_3.sonuc :
				self.kisim = 'ara3'
				
		elif self.kisim == 'ara3' :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				maze.draw()
				if self.dialog == True :
					dialog_kutusu.ciz("yuz_2")
				if dialog_butonu.dongu == False and self.dialog == True :
					text_blit("asistan :",180,465,18,"beyaz")
					geciken_blit_1.ciz("BİR ŞEYLER TERS GİDİYOR !!",200,487)
					if geciken_blit_1.dongu == False : 
						geciken_blit_2.ciz("SALDIRI ALTINDAYIZ ZAMAN AZ.",200,509)
				elif self.dialog == False:
					self.kisim = 'ara4'
					self.dialog = True
					geciken_blit_1.dongu = True
					geciken_blit_2.dongu = True
					ekran_gecisi_1.dongu = True
		elif self.kisim == 'ara4' :
			g.pencere.fill(g.siyah)
			maze.draw()
			if self.dialog == True :
				dialog_kutusu.ciz("yuz_2")
			if dialog_butonu.dongu == False and self.dialog == True :
				text_blit("asistan :",180,465,18,"beyaz")
				geciken_blit_1.ciz("Dialoğu kapattığında bir an önce yön tuşlarıyla BİTİŞ'e ulaş",200,487)
				if geciken_blit_1.dongu == False : 
					geciken_blit_2.ciz("ve saldırıdan kurtul !!!",200,509)
			elif self.dialog == False:
				self.kisim = 'hack_1'
				self.dialog = True
				geciken_blit_1.dongu = True
				geciken_blit_2.dongu = True
		elif self.kisim == 'hack_1' :
			g.pencere.fill(g.siyah)
			maze.draw()
			g.pencere.blit(oyuncu_surf ,(player.x,player.y))
			if player.dongu == False :
				ekran_gecisi_1.dongu = True
				self.level_gecildi = True



	def level_3(self):
		if self.kisim == 1 :
			ekran_gecisi_1.yap("siyah")
			if ekran_gecisi_1.dongu == False :
				g.pencere.fill(g.siyah)
				text_blit("3. BÖLÜM","ortala",285,30,"beyaz")
				if self.bolumekrani_dongu <=250 :
					self.bolumekrani_dongu+=1
				else :
					ekran_gecisi_2.yap("beyaz")
				if ekran_gecisi_2.dongu == False :
					g.pencere.fill(g.beyaz)
					self.bolumekrani_dongu = 0
					self.kisim = 2
					ekran_gecisi_1.dongu = True
					ekran_gecisi_2.dongu = True

		if self.kisim == 2 :
			g.pencere.fill(g.beyaz)




"""
	def level_4(self):
	def hack_2(self):
	def level_5(self):
	def level_6(self):
	def level_7(self):
	def level_8(self):
	def level_9(self):
	def final(self):
"""



g=Game() #oyun döngüsünde kullanmak için Game sınıfından nesne oluşturuldu
l=Game_level()
db.downdate()
while g.running :
	g.oyun_dongusu()
pygame.quit()
