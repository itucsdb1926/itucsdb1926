CREATE TABLE ADRES (
	ID int NOT NULL PRIMARY KEY,
	IL varchar(15) NOT NULL,
	ILCE varchar(25) NOT NULL,
	SEMT varchar(25) NOT NULL,
	POSTA_KODU varchar(5) NOT NULL PRIMARY KEY,
	SOKAK varchar(20) 
)

CREATE TABLE ÇOCUK_ASI (
	NAME varchar(25),
	TARIH date,
	YONTEM varchar(15),
	DOZ varchar(15),
	YER varchar(25),
	ID int NOT NULL,
	FOREIGN KEY (ID) REFERENCES cocuk,
	PRIMARY KEY(ID),
	VELI int,
	FOREIGN KEY (VELI) REFERENCES kullanici(ID)
)

CREATE TABLE COCUK (
	ID int NOT NULL PRIMARY KEY,
	NAME varchar(30),
	YAS int,
	KILO varchar(5),
	BOY varchar(5),
	BMI varchar(5),
	KAN_GRUBU varchar(10),
	VELI int REFERENCES kullanici(ID)
)

CREATE TABLE kullanici (
	ID int NOT NULL PRIMARY KEY,
	NAME varchar(30),
	YAS int,
	KILO varchar(5),
	BOY varchar(5),
	BMI varchar(5),
	KAN_GRUBU varchar(10),
	AILE_HEKIMI varchar(30),
	AILE_PROFILI varchar(5)
)

CREATE TABLE ASI (
	NAME varchar(25),
	TARIH date,
	YONTEM varchar(15),
	DOZ varchar(15),
	YER varchar(25),
	ID int NOT NULL,
	FOREIGN KEY (ID) REFERENCES kullanici(ID),
	PRIMARY KEY(ID)
)

CREATE TABLE HASTANE (
	ID  int NOT NULL PRIMARY KEY,
	ADI  varchar(15) UNIQUE,
	SOKAK varchar(25) NOT NULL,
	TEL varchar(25) NOT NULL,
	TIP varchar(25) NOT NULL,
	KLINIK varchar(25) NOT NULL,
	POLIKLINIK varchar(25) NOT NULL,
	FOREIGN KEY (ID) REFERENCES adres
)

CREATE TABLE KLINIK (
	ID  int NOT NULL PRIMARY KEY,
	ADI  varchar(30) UNIQUE,
	KAT_NO varchar(25) NOT NULL,
	BINA_NO varchar(25) NOT NULL,
	DOKTOR_SAYISI  int NOT NULL,
	YAR_PER_SAYISI int  NOT NULL,
	HASTANE varchar(15),
	FOREIGN KEY(HASTANE) REFERENCES hastane(ADI)
)

CREATE TABLE DOKTOR (
	ID  int NOT NULL PRIMARY KEY,
	AD varchar(50) UNIQUE,
	TEL varchar(30) NOT NULL,
	BRANS varchar(55) NOT NULL,
	ODA_NO   varchar(25) NOT NULL,
	ASISTAN_ADI varchar(55) NOT NULL,
	HASTANE varchar(15),
	FOREIGN KEY(HASTANE) REFERENCES hastane(ADI),
	KLINIK varchar(15),
	FOREIGN KEY(KLINIK) REFERENCES klinik(ADI)
)

CREATE TABLE RANDEVU_BILGISI (
	 ID  int ,
	 HEKIM_ADI  varchar(30) NOT NULL, 
	 RANDEVU_TARIHI date,
	 HASTANE_ADI varchar(200) NOT NULL,  
	 KLINIK  varchar(200) NOT NULL,
	 MUAYENE_YERI   varchar(200) NOT NULL,
	 FOREIGN KEY (ID) REFERENCES kullanici(ID),
	 FOREIGN KEY (HASTANE_ADI) REFERENCES hastane(ADI ),
	 PRIMARY KEY(ID),
	 FOREIGN KEY (KLINIK) REFERENCES klinik (ADI),
	 FOREIGN KEY (HEKIM_ADI) REFERENCES doktor(AD)
)

CREATE TABLE RANDEVU_GECMISI (
 	ID  int,
 	HEKIM_ADI  varchar(30) NOT NULL, 
 	RANDEVU_TARIHI date,
 	HASTANE_ADI varchar(200) NOT NULL,
 	KLINIK  varchar(200) NOT NULL,
 	MUAYENE_YERI   varchar(200) NOT NULL,
 	DURUM varchar(200) NOT NULL,
 	FOREIGN KEY (ID) REFERENCES kullanici(ID),
 	PRIMARY KEY(ID),
	FOREIGN KEY (HASTANE_ADI) REFERENCES hastane(ADI ),
	FOREIGN KEY (KLINIK) REFERENCES klinik (ADI),
	FOREIGN KEY (HEKIM_ADI) REFERENCES doktor(AD)
)