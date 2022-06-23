# Projekt_inzynierski_P2
Analiza danych na rynku samochodów używanych w USA

## O projekcie 

W ramach projektu analizujemy zestaw danych o samochodach używanych w Stanach Zjednoczonych.
Link do źródła danych https://www.kaggle.com/datasets/ananaymital/us-used-cars-dataset.
Zestaw danych ma 3 miliony samochodów i 66 kolumn, chociaż do naszej analizy wykorzystamy 1,5 miliona samochodów i 15 kolumn.
W założeniu analizę przeprowadzamy dla połowy zestawu danych aby analiza była jak najbardziej wiarygodna.

Cel analizy:
 - Poznać lepiej rynek samochodów używanych w USA.
 - Pomoc w podejmowaniu najlepszych decyzji podczas sprzedaży i zakupu samochodu.
 - Pomoc w znalezieniu najbardziej optymalnej oferty dla swojego samochodu poprzez wizualizacje. 

## Technologie
- Python
- Jupyter Notebook
### Biblioteki
- jovian opendatasets
- pandas
- numpy
- seaborn
- matplotlib
- plotly.express

## Pobieranie zestawu danych 
Przy użyciu biblioteki opendatasets pobieramy dane żródłowe z platformy Kaggle
Podczas pobierania danych wymagane jest wprowadzenie nazwy użytkownika i klucza Kaggle
```
!pip install jovian opendatasets --upgrade --quiet
import opendatasets as od
dane_zrodlowe = 'https://www.kaggle.com/ananaymital/us-used-cars-dataset' 
od.download(dane_zrodlowe)
```

## Czyszczenie i przygotowywanie danych 

Czyszczenie danych to weryfikacja, dzięki której upewniamy się, że dane używane do analizy, są całkowicie przygotowane, to znaczy, nie mają duplikatów ani brakujących wartości, dane są w odpowiednim formacie, nie są uszkodzone, a tym samym gotowe do użycia do analizy.

### Załadowanie miliona wierszy z pliku żródłowego
```
import pandas as pd
import numpy as np
samochody_uzywane_csv = 'us-used-cars-dataset/used_cars_data.csv'
samochody_uzywane_df = pd.read_csv(usedcars_csv,  low_memory=False, nrows=1000000)
```

### Wybranie kolumn do analizy oraz załadowanie 1.5 miliona wierszy z wybranymi kolumnami 
```
wybrane_kolumny= ['city','daysonmarket','dealer_zip','engine_cylinders','frame_damaged','make_name','horsepower','listed_date','latitude','longitude','price','wheel_system','seller_rating','maximum_seating','sp_name']
uzywane_samochody_probka = pd.read_csv(samochody_uzywane_csv,  low_memory=False, nrows= 1500000, usecols=wybrane_kolumny)
uzywane_samochody_probka.head(2)
```


