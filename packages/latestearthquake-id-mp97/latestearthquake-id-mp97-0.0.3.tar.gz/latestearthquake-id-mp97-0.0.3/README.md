# Latest Indonesia Earthquake
This package will get the latest earthquake from BMKG | Meteorological, Climatological, and Geophysical Agency

## HOW IT WORK?
This package will scrape from [BMKG](https://bmkg.go.id) to get latest earthquake happened in Indonesia

This package will use Beautfulsoup4 and Request to produce output in the form JSON that is ready to be used in web or mobile application

## HOW TO USE
```
import gempaterkini

if __name__== '__main__':
    print('Aplikasi Utama')
    result = gempaterkini.ekstrasi_data()
    gempaterkini.tampilkan_data(result)
```

# AUTHOR
Eko Wijaya