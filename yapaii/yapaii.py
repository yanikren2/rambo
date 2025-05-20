import random
import os
import json
import requests
from datetime import datetime, timedelta

API_KEY = "apı"

# Kullanıcı bilgilerini tutan sınıf
class Kullanici:
    def __init__(self, ad="", boy=0, kilo=0, cinsiyet="", hedef_su=0, sehir="", haftalik_hedef_yuruyus=150, uyku_verisi=None):
        self.ad = ad
        self.boy = boy
        self.kilo = kilo
        self.cinsiyet = cinsiyet
        self.hedef_su = hedef_su
        self.sehir = sehir
        self.haftalik_hedef_yuruyus = haftalik_hedef_yuruyus
        self.uyku_verisi = uyku_verisi if uyku_verisi else []


    def vki_hesapla(self):
        return self.kilo / (self.boy ** 2) if self.boy > 0 else 0

    def bilgileri_goster(self):
        print(f"\n--- {self.ad} Kullanıcı Bilgileri ---")
        print(f"Boy: {self.boy} m\nKilo: {self.kilo} kg\nCinsiyet: {self.cinsiyet.capitalize()}")
        print(f"Hedef Su: {self.hedef_su} litre\nŞehir: {self.sehir.capitalize()}")
        print(f"Vücut Kitle İndeksi (VKİ): {self.vki_hesapla():.2f}")
        print(f"Haftalık Hedef Yürüyüş: {self.haftalik_hedef_yuruyus} dakika")

    def gunluk_yuruyus_onerisi(self):
        vki = self.vki_hesapla()
        if vki < 18.5:
            sure = 20
        elif 18.5 <= vki <= 24.9:
            sure = 30
        elif 25 <= vki <= 29.9:
            sure = 45
        else:
            sure = 60

        hedef_gunluk = self.haftalik_hedef_yuruyus / 7
        print("\n--- Günlük Yürüyüş Önerisi ---")
        print(f"VKİ'nize göre önerilen süre: {sure} dakika.")
        print(f"Haftalık hedefinize göre günlük ortalama: {hedef_gunluk:.1f} dakika.")

    def spor_programi_onerisi(self):
        vki = self.vki_hesapla()

        if vki < 18.5:
            print("\nÖnerilen Spor Programları:")
            print(
                "1. Yavaş tempoda yürüyüş (30 dakika), yoga (20 dakika), hafif ağırlıklarla kuvvet çalışmaları (20 dakika).")
            print("2. Yürüyüş, yoga ve esneme hareketleri ile mobilite çalışmaları.")
            print("3. Hafif aerobik egzersizler, pilates ve core çalışmaları.")

        elif 18.5 <= vki <= 24.9:
            print("\nÖnerilen Spor Programları:")
            print("1. Orta tempo koşu (30 dakika), interval antrenmanlar (20 dakika), ağırlık çalışmaları (30 dakika).")
            print("2. Kardiyo (45 dakika), yoga (20 dakika), kuvvet çalışmaları (30 dakika).")
            print("3. HIIT (High-Intensity Interval Training) antrenmanı, ağırlık çalışmaları, esneme hareketleri.")

        elif 25 <= vki <= 29.9:
            print("\nÖnerilen Spor Programları:")
            print("1. Düşük tempolu yürüyüş (30 dakika), hafif koşu (20 dakika), kardiyo (20 dakika).")
            print("2. Düşük tempo koşu (25 dakika), yoga (15 dakika), bacak ve karın egzersizleri (20 dakika).")
            print("3. Düşük tempolu yürüyüş, interval kardiyo antrenmanları ve basit kuvvet egzersizleri.")

        else:
            print("\nÖnerilen Spor Programları:")
            print("1. Yavaş tempolu yürüyüş (20 dakika), yoga (20 dakika), düşük yoğunluklu ağırlık çalışmaları.")
            print("2. Yürüyüş, hafif kardiyo, ve kasları çalıştıran basit egzersizler.")
            print("3. Esneme çalışmaları, yavaş tempolu yürüyüş, meditasyon ve yoga.")

    def saglikli_yemek_onerisi(self):
                vki = self.vki_hesapla()
                print("\n--- Sağlıklı Yemek Önerisi ---")

                # VKİ'ye göre yemek önerileri
                if vki < 18.5:
                    print("Vücut kitle indeksiniz düşük. Beslenme için daha fazla kalori almanız gerekebilir.")
                    print("Önerilen yemekler: Yüksek kalorili, protein ve karbonhidrat içeren yemekler.")
                    print("Örnek yemekler: Izgara tavuk, avokado, fıstık ezmesi, mercimek çorbası.")
                elif 18.5 <= vki <= 24.9:
                    print("Vücut kitle indeksiniz normal aralıkta. Dengeli bir diyet önerilir.")
                    print("Önerilen yemekler: Dengeli miktarda protein, karbonhidrat ve yağ içeren yemekler.")
                    print("Örnek yemekler: Somonlu salata, sebzeli tavuk sote, quinoa, yoğurtlu meyve salatası.")
                elif 25 <= vki <= 29.9:
                    print(
                        "Vücut kitle indeksiniz biraz yüksek. Daha düşük kalorili, sağlıklı yemekler tercih edilmelidir.")
                    print("Önerilen yemekler: Az yağlı ve düşük kalorili yemekler.")
                    print(
                        "Örnek yemekler: Izgara sebzeler, haşlanmış tavuk, salatalar, avokado, düşük kalorili çorbalar.")
                else:
                    print(
                        "Vücut kitle indeksiniz yüksek. Daha fazla sebze, protein ve düşük kalorili yemekler önerilir.")
                    print("Önerilen yemekler: Yüksek lifli, düşük kalorili ve besleyici yemekler.")
                    print("Örnek yemekler: Haşlanmış sebzeler, baklagiller, kinoa, ton balıklı salata.")

    def hava_durumu_goster(self):
        if not self.sehir:
            print("Hata: Şehir bilgisi tanımlanmamış!")
            return

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={self.sehir}&appid={API_KEY}&units=metric&lang=tr"
            response = requests.get(url)
            data = response.json()

            if data.get("cod") != 200:
                print("Hata: Şehir bulunamadı. Lütfen şehir adını kontrol edin.")
                return

            # Hava durumu bilgilerini alma
            sicaklik = data['main']['temp']
            hissetilen_sicaklik = data['main']['feels_like']
            durum = data['weather'][0]['description']
            nem_orani = data['main']['humidity']
            ruzgar_hizi = data['wind']['speed']
            yagmur_var_mi = 'rain' in data

            print("\n--- Güncel Hava Durumu ---")
            print(f"Şehir: {self.sehir.capitalize()}")
            print(f"Sıcaklık: {sicaklik}°C")
            print(f"Hissedilen Sıcaklık: {hissetilen_sicaklik}°C")
            print(f"Durum: {durum.capitalize()}")
            print(f"Nem Oranı: {nem_orani}%")
            print(f"Rüzgar Hızı: {ruzgar_hizi} m/s")
            print(f"Yağmur Durumu: {'Var' if yagmur_var_mi else 'Yok'}")

            # Spor yapılabilirliği önerisi
            self.spor_yapabilir_miyim(sicaklik, ruzgar_hizi, yagmur_var_mi)

        except Exception as e:
            print(f"Hava durumu alınırken hata oluştu: {e}")

    def spor_yapabilir_miyim(self, sicaklik, ruzgar_hizi, yagmur_var_mi):
        # Spor yapmanın uygun olup olmadığını belirlemek için hava durumu verilerini analiz etme
        if yagmur_var_mi:
            print("Dışarıda yağmur var, dışarıda spor yapmanız önerilmez.")
        elif sicaklik > 35:
            print("Çok sıcak bir hava, dışarıda spor yapmanız sağlığınız açısından riskli olabilir.")
        elif sicaklik < 5:
            print("Hava çok soğuk, dışarıda spor yapmanız zor olabilir.")
        elif ruzgar_hizi > 15:
            print("Rüzgar hızı çok yüksek, dışarıda spor yaparken dikkatli olun.")
        else:
            print("Hava durumu uygun, dışarıda spor yapabilirsiniz!")

    def uyku_verisi_ekle(self, tarih, uyku_baslangic, uyku_bitis, hissetme_durumu):
        uyku_veri = {
            "tarih": tarih,
            "uyku_baslangic": uyku_baslangic,
            "uyku_bitis": uyku_bitis,
            "hissetme_durumu": hissetme_durumu
        }
        self.uyku_verisi.append(uyku_veri)

    def uyku_suresi_hesapla(self):
        toplam_sure = 0
        for veri in self.uyku_verisi:
            baslangic = datetime.strptime(veri["uyku_baslangic"], "%H:%M")
            bitis = datetime.strptime(veri["uyku_bitis"], "%H:%M")
            if bitis < baslangic:  # Gece yarısından sonra uyku
                bitis += timedelta(days=1)
            toplam_sure += (bitis - baslangic).seconds / 3600  # Saat cinsinden
        return toplam_sure

    def uyku_verilerini_goster(self):
        if not self.uyku_verisi:
            print("Hiç uyku verisi bulunmamaktadır.")
            return
        for veri in self.uyku_verisi:
            print(f"Tarih: {veri['tarih']} - Başlangıç: {veri['uyku_baslangic']} - Bitiş: {veri['uyku_bitis']} - Hissetme: {veri['hissetme_durumu']}")

    def yapay_zeka_saglik_analizi(self):
        print("\n--- Yapay Zeka Sağlık Analizi ---")

        # Kullanıcıdan günlük verileri alıyoruz
        uyku_suresi = input_float("Bugün kaç saat uyudunuz? ")
        su_miktari = input_float("Bugün içtiğiniz su miktarını girin (litre): ")
        egzersiz_yapildi = input("Bugün egzersiz yaptınız mı? (Evet/Hayır): ").strip().lower()

        hedefler_tamamlandi = True  # Başlangıçta hedeflerin tamamlandığını varsayıyoruz
        analiz = []  # Öneriler ve analizler bu listeye eklenecek

        # Uyku hedefi kontrolü
        if uyku_suresi < 7:
            analiz.append("Uyku düzeninize dikkat edin. Günde 7-8 saat uyumayı hedefleyin.")
            hedefler_tamamlandi = False
        else:
            analiz.append("Harika! Yeterli uyku aldınız, bu gününüzü daha verimli kılacak.")

        # Su içme hedefi kontrolü
        if su_miktari < 2:
            analiz.append("Yeterli su içmek sağlığınız için çok önemli. Bugün 2-3 litre arası su içmeyi unutmayın.")
            hedefler_tamamlandi = False
        else:
            analiz.append("Tebrikler! Yeterli su içtiniz, bu sağlığınız için harika bir adım.")

        # Egzersiz yapma hedefi kontrolü
        if egzersiz_yapildi == "hayır":
            analiz.append("Bugün egzersiz yapmadınız, yarın egzersiz yapmayı unutmayın!")
            hedefler_tamamlandi = False
        else:
            analiz.append("Harika! Bugün egzersiz yaptınız, bu fiziksel sağlığınız için çok faydalı.")

        # VKİ analizi
        vki = self.vki_hesapla()
        if vki < 18.5:
            analiz.append("VKİ'niz düşük. Dengeli bir diyetle kilo almayı hedefleyebilirsiniz.")
        elif 18.5 <= vki <= 24.9:
            analiz.append("VKİ'niz normal. Sağlıklı yaşam alışkanlıklarınıza devam edin!")
        elif 25 <= vki <= 29.9:
            analiz.append("VKİ'niz biraz yüksek. Daha fazla egzersiz ve düşük kalorili diyet önerilir.")
        else:
            analiz.append("VKİ'niz yüksek. Bir sağlık uzmanına danışarak beslenme ve egzersiz planı oluşturabilirsiniz.")

        # Sonuçları kullanıcıya göster
        print("\n--- Günlük Analiz ve Öneriler ---")
        for a in analiz:
            print(f"- {a}")

        # Tüm hedefler tamamlandığında olumlu bir mesaj
        if hedefler_tamamlandi:
            print("\nTebrikler! Bugün sağlığınız için harika bir gün geçirdiniz.")
        else:
            print("\nHedeflerinizi tamamlamak için biraz daha çaba gösterebilirsiniz.")



    def bilgileri_duzenle(self):
        print("\n--- Bilgileri Düzenle ---")
        print("1. Boy\n2. Kilo\n3. Cinsiyet\n4. Hedef Su Miktarı\n5. Şehir\n6. Haftalık Hedef Yürüyüş")

        secim = input("Düzenlemek istediğiniz bilgiyi seçin (1-10): ").strip()
        if secim == "1":
            self.boy = input_float("Yeni boyunuzu girin (metre cinsinden, örn: 1.75): ")
        elif secim == "2":
            self.kilo = input_float("Yeni kilonuzu girin (kg cinsinden): ")
        elif secim == "3":
            self.cinsiyet = input("Yeni cinsiyetinizi girin (Erkek/Kadın): ").strip().lower()
        elif secim == "4":
            self.hedef_su = input_float("Yeni hedef su tüketiminizi girin (litre cinsinden): ")
        elif secim == "5":
            self.sehir = input("Yeni şehri girin: ").strip()
        elif secim == "6":
            self.haftalik_hedef_yuruyus = input_float("Yeni haftalık yürüyüş hedefinizi girin (dakika): ")
        else:
            print("Geçersiz seçim!")
            return

        print("Bilgileriniz güncellendi!\n")
        self.bilgileri_goster()
        return True

# Kullanıcı kayıtlarını yükleme veya yeni kullanıcı oluşturma
def profil_yonet():
    dosya_adi = "kullanicilar.json"
    kullanicilar = {}

    if os.path.exists(dosya_adi):
        try:
            with open(dosya_adi, "r") as dosya:
                kullanicilar = json.load(dosya)
        except (json.JSONDecodeError, ValueError):
            print("Hata: Kullanıcı kayıt dosyası bozuk. Sıfırdan başlatılıyor.")

    kullanici_adi = input("Kullanıcı adınızı girin: ").strip()
    if kullanici_adi in kullanicilar:
        veri = kullanicilar[kullanici_adi]
        uyku_verisi = veri.get("uyku_verisi", [])
        return kullanicilar, kullanici_adi, Kullanici(
            kullanici_adi, veri.get("boy", 0), veri.get("kilo", 0),
            veri.get("cinsiyet", ""), veri.get("hedef_su", 0),
            veri.get("sehir", ""), veri.get("haftalik_hedef_yuruyus", 150), uyku_verisi
        )
    else:
        print("\nYeni kullanıcı oluşturuluyor...")
        boy = input_float("Boyunuzu giriniz (m): ")
        kilo = input_float("Kilonuzu giriniz (kg): ")
        cinsiyet = input("Cinsiyetinizi giriniz: ").strip().lower()
        hedef_su = input_float("Günlük hedef su (litre): ")
        sehir = input("Şehir: ").strip()
        haftalik_hedef = input_float("Haftalık yürüyüş hedefi (dakika): ")

        yeni_kullanici = Kullanici(kullanici_adi, boy, kilo, cinsiyet, hedef_su, sehir, haftalik_hedef)
        kullanicilar[kullanici_adi] = yeni_kullanici.__dict__
        with open(dosya_adi, "w") as dosya:
            json.dump(kullanicilar, dosya)
        return kullanicilar, kullanici_adi, yeni_kullanici

def input_float(mesaj):
    while True:
        try:
            deger = float(input(mesaj))
            if deger > 0:
                return deger
            else:
                print("Pozitif bir değer girin.")
        except ValueError:
            print("Geçersiz giriş!")

def main():
    kullanicilar, kullanici_adi, kullanici = profil_yonet()
    while True:
        print("\n--- Menü ---")
        print("1. Bilgileri Göster\n2. Bilgileri Düzenle\n3. Günlük Yürüyüş Önerisi")
        print("4. Hava Durumu\n5. Uyku Verilerini Göster\n6. Uyku Verisi Ekle")
        print("7. spor programı önerisi\n8. Sizin için yemek önerileri\n9. Sağlık hakkında konuşma")
        print("10 Çıkış")

        secim = input("Seçiminizi yapın (1-10): ").strip()
        if secim == "1":
            kullanici.bilgileri_goster()
        elif secim == "2":
            if kullanici.bilgileri_duzenle():
                kullanicilar[kullanici_adi] = kullanici.__dict__
                with open("kullanicilar.json", "w") as dosya:
                    json.dump(kullanicilar, dosya)
        elif secim == "3":
            kullanici.gunluk_yuruyus_onerisi()
        elif secim == "4":
            kullanici.hava_durumu_goster()
        elif secim == "5":
            kullanici.uyku_verilerini_goster()
        elif secim == "6":
            tarih = input("Uyku tarihi (gg/aa/yyyy): ")
            uyku_baslangic = input("Uyku başlangıç saati (HH:MM): ")
            uyku_bitis = input("Uyku bitiş saati (HH:MM): ")
            hissetme = input("Uyandıktan sonra nasıl hissediyorsunuz? (İyi/Kötü): ").strip()
            kullanici.uyku_verisi_ekle(tarih, uyku_baslangic, uyku_bitis, hissetme)
            kullanicilar[kullanici_adi] = kullanici.__dict__
            with open("kullanicilar.json", "w") as dosya:
                json.dump(kullanicilar, dosya)
        elif secim == "7":
            kullanici.spor_programi_onerisi()

        elif secim == "8":
            kullanici.saglikli_yemek_onerisi()

        elif secim =="9":
            kullanici.yapay_zeka_saglik_analizi()

        elif secim == "10":
            print("Çıkış yapılıyor. Sağlıklı günler!")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
