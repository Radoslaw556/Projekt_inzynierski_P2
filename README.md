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
Ze względów na ograniczenia platformy nie jesteśmy w stanie załadować wszystkich danych.
```
import pandas as pd
import numpy as np
samochody_uzywane_csv = 'us-used-cars-dataset/used_cars_data.csv'
samochody_uzywane_df = pd.read_csv(usedcars_csv,  low_memory=False, nrows=1000000)
```

### Wybranie kolumn do analizy oraz załadowanie 1.5 miliona wierszy z wybranymi kolumnami 
Spośród 66 dostępnych kolumn wybieramy kolumny które zostaną wykorzystane podczas analizy danych, funkcja head() pozwala nam podglądnąć daną liczbę wierszy z zestawu danych co daje nam bezpośredni wgląd w strukturę danych.

```
wybrane_kolumny= ['city','daysonmarket','dealer_zip','engine_cylinders','frame_damaged','make_name','horsepower','listed_date','latitude','longitude','price','wheel_system','seller_rating','maximum_seating','sp_name']
uzywane_samochody_probka = pd.read_csv(samochody_uzywane_csv,  low_memory=False, nrows= 1500000, usecols=wybrane_kolumny)
uzywane_samochody_probka.head(2)
```

### Sprawdzenie typów danych oraz konwersja danych do odpowiednich formatów 

```
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
print(uzywane_samochody_probka.dtypes)
```
Wynik użycia funkcji

![image](https://user-images.githubusercontent.com/108089259/175406290-2eb71069-6e65-4503-86e2-0b84f58e9653.png)

Następnym krokiem jest przeczytanie 1.5 miliona wierszy z pliku żródłowego z poprzednio wyselekcjonowanymi kolumnami i typami danych oraz jednoczesna transformacja kolumny "listed_date" z typu Object(String) do typu DateTime.

```
 wybrane_typy_danych={
    'daysonmarket' : 'int32',
    'horsepower' :'float32',
    'latitude' : 'float32',
    'longitude' : 'float32',
    'price':'float32',
    'seller_rating': 'float32'
}
uzywane_samochody_probka = pd.read_csv(samochody_uzywane_csv,  low_memory=False, nrows= 1500000, usecols=wybrane_kolumny, dtype=wybrane_typy_danych, parse_dates=['listed_date'])
```

### Zamiana i zaczytanie pliku typu feather
Przeszktałcamy nasz zbiór danych typu .csv do typu .feather co znaczenie ułatwi oraz przyśpieszy proces ładowania i przetwarzania danych.

```
!pip install pyarrow
uzywane_samochody_probka.to_feather('samochody_uzywane.feather')
probka_danych_finalowa = pd.read_feather('samochody_uzywane.feather')
```
### Wyszukiwanie i usuwanie duplikatów 
Do wyszukania sumy duplikatów używamy funkcji duplicated()
```
probka_danych_finalowa.duplicated().sum()
```
Usuwanie duplikatów z pliku feather 
```
probka_danych_finalowa=probka_danych_finalowa.drop_duplicates()
```
### Wyszukiwanie i usuwanie niekompletnych danych

![image](https://user-images.githubusercontent.com/108089259/175408461-57753ea4-ec19-4b0a-b804-e4d359ada397.png)

Sposoby procesowania niekompletnych danych.
- Zostawienie brakujących danych bez zmian, jeśli nie wpłyną na naszą analizę
- Zastąpienie brakujących danych średnią
- Zastąpienie brakujących danych inną stałą wartością
- Usunięcie wierszy niezawierających kompletu danych
- Użycie wartości z innych wierszy i kolumn, aby oszacować brakujące wartości




