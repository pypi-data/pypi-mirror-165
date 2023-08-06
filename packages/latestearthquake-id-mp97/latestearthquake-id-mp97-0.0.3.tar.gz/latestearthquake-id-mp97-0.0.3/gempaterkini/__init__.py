import requests
from bs4 import BeautifulSoup


def ekstrasi_data():
    """
        Tanggal: 12 Agustus 2022
        Wqktu: 12:25:02 WIB
        Magnitudo: 3.6
        Kedalaman: 4 km
        Lokasi: 3.74 LS - 119.54 BT
        Pusat gempa: Pusat Gempa berada di darat 10 km BaratDaya Pinrang
        Dirasakan: Dirasakan (Skala MMI): II-III Pinrang
        :return:
    """
    try:
        content = requests.get('https://bmkg.go.id')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        result = soup.find('span', {'class':'waktu'})
        result = result.text.split(', ')
        tanggal = result[0]
        waktu = result[1]

        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        for res in result:
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i+1




        hasil = dict()
        hasil ['tanggal'] = tanggal
        hasil ['waktu'] = waktu
        hasil ['magnitudo'] = magnitudo
        hasil ['kedalaman'] = kedalaman
        hasil ['lokasi'] ={'ls': ls, 'bt': bt}
        hasil ['pusat'] = lokasi
        hasil ['dirasakan'] = dirasakan
        return hasil
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print("tidak bisa tampilkan data gempa")
        return
    print('Gempa Terakhir berdasarkan BMKG')
    print (f"Tanggal      : {result['tanggal']}")
    print (f"Waktu        : {result['waktu']}")
    print (f"Magnitudo    : {result['magnitudo']}")
    print (f"Kedalaman    : {result['kedalaman']}")
    print (f"Lokasi       : LS={result['lokasi']['ls']}, BT={result['lokasi']['bt']}")
    print (f"Pusat Gempa  : {result['pusat']}")
    print (f"Dirasakan    : {result['dirasakan']}")

if __name__== '__main__':
    result = ekstrasi_data()
    tampilkan_data(result)
