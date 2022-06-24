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
Podczas pobierania danych wymagane jest wprowadzenie nazwy użytkownika i wygenerowanego klucza Kaggle
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
Pogląd załadowanych danych
![image](https://user-images.githubusercontent.com/108089259/175470420-5804b9b6-8f21-47ad-8a04-e45a5a48ba4a.png)

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

Dzięki sprawdzeniu możemy zauważyć że w 6 kolumnach brakuje nam danych. 
Aby rozwiązać ten problem musimy zastosować którąś z odpowiednich technik dla każdej z kolumn.

Sposoby procesowania niekompletnych danych.
- Zostawienie brakujących danych bez zmian, jeśli nie wpłyną na naszą analizę
- Zastąpienie brakujących danych średnią
- Zastąpienie brakujących danych inną stałą wartością
- Usunięcie wierszy niezawierających kompletu danych
- Użycie wartości z innych wierszy i kolumn, aby oszacować brakujące wartości

#### Czyszczenie kolumny "engine_cylinders"

Zaczynamy od pierwszej kolumny "engine_cylinders"
![image](https://user-images.githubusercontent.com/108089259/175472710-eeefdc46-a90b-4c71-8402-2707e0be0268.png)

W tej sytuacji najlepszy podejściem będzie zamiana wartości None na stały tekst "Nieznany".
Jako że chcemy zamienić wszystkie puste wartości i wartości None na stały tekst transformujemy puste stringi na wartości none po czym zamieniamy wszystkie wartości none na stały tekst 
```
probka_danych_finalowa = probka_danych_finalowa.replace(r'^\s+$', np.nan, regex=True)
probka_danych_finalowa['engine_cylinders'] = probka_danych_finalowa['engine_cylinders'].fillna(value = 'Nieznany')
```
Po wykonaniu tych transformacji możemy sprawdzić że wartości None już nie występują.
![image](https://user-images.githubusercontent.com/108089259/175473548-c49a5fd8-86f7-44ad-8f04-759ba53b195e.png)


#### Czyszczenie kolumny "frame_damaged"

Kolumna "frame_damaged" zwraca wartości true lub false w zależności od tego czy samochód jest uszkodzony.
Ponawiamy kroki jak dla kolumny "engine_cylinders" wyszukujemy wartości None i zastępujemy je stałym stringiem "Nieznany".

![image](https://user-images.githubusercontent.com/108089259/175486485-cea0fef5-1d09-4bb6-91f4-e5060de627e1.png)

### Czyszczenie kolumny "horsepower" 

Czyszczenie kolumny "horsepower" zaczynamy od wyszukania wartości None oraz sprawdzenia wartości dla tej kolumny przy użyciu funkcji describe()

![image](https://user-images.githubusercontent.com/108089259/175487398-a1336d42-a3e1-4b10-ae7b-02606fad2fb4.png)

Odchylenie standardowe nie jest bardzo duże wynosi ~88 co oznacza że możemy te dane zastąpić.
W tej sytuacji najlepszym podejściem będzie zastąpienie brakujących danych średnimi wartościami między 200 a 300 

```
import random
probka_danych_finalowa['horsepower'].fillna(random.uniform(200,300),inplace=True)
```

### Czyszczenie kolumny "maximum_seating"

Wykazanie ilości brakujących danych, unikalnych wartości dla tej kolumny oraz sumy wystąpień zarejestrowanych miejsc w samochodzie.

![image](https://user-images.githubusercontent.com/108089259/175500701-ab21d46a-3827-4675-80b0-64703661ebd6.png)

Aby oczyścić te dane wykonujemy dwa kroki.
1. Zamiana wartości None na "5 seats" jako że większość samochów prawie 70% ma 5 miejsc możemy zamienić wartości None na "5 seats" nie powinno to wpłynąć negatywnie na naszą analize.

2. Kolejnym krokiem jest usunięcie wierszy zawierających wartość "--".

```
probka_danych_finalowa['maximum_seating'].fillna(value='5 seats', inplace=True)
probka_danych_finalowa['maximum_seating'].unique()
probka_danych_finalowa = probka_danych_finalowa[~probka_danych_finalowa['maximum_seating'].isin(['--'])]
```

![image](https://user-images.githubusercontent.com/108089259/175552632-79f74c3c-3e66-43cb-883d-9985d92a6028.png)


3. Usunięcie niepotrzebnego tekstu "seats" z kolumny oraz konwersja tej kolumny do typu numerycznego co pomoże nam pózniej podczas próby analizy i wizualizacji naszych danych.

```
def num(value):
  return value.split()[0]
  
probka_danych_finalowa['maximum_seating'].astype(str)
probka_danych_finalowa['maximum_seating'] = probka_danych_finalowa['maximum_seating'].apply(num)
probka_danych_finalowa['maximum_seating'] = probka_danych_finalowa['maximum_seating'].astype(np.int32)
```
Wynik po konwersji kolumny 

![image](https://user-images.githubusercontent.com/108089259/175553084-1366d9db-5048-4dba-8e68-5cf6a2f71270.png)


### Czyszczenie kolumny "seller_rating"

Usuwamy wszystkie wiersze zawierające wartość None

```
a = probka_danych_finalowa['seller_rating'].isnull()
probka_danych_finalowa = probka_danych_finalowa[~a]
```

### Czyszczenie kolumny "wheel_system"

Ponawiamy proces jak dla kolumny "seller_rating".

![image](https://user-images.githubusercontent.com/108089259/175566415-4a445031-8c4f-44f6-ab53-2509c35b2a60.png)


```
probka_danych_finalowa = probka_danych_finalowa[probka_danych_finalowa['wheel_system'].isin(['AWD', 'FWD', '4WD', 'RWD', '4X2'])]
```

## Efekt czyszczenia kolumn

![image](https://user-images.githubusercontent.com/108089259/175566986-af84e42b-f22a-4734-89cd-5fa20d5c184e.png)

![image](https://user-images.githubusercontent.com/108089259/175567035-1a875320-e5ab-4fbe-acc0-e0f776e51c98.png)

### Szlifowanie danych i zapis wersji finałowej

Proces resetu indeksu oraz wpisania finalnej wersji do pliku csv "wersja_finalowa.csv".

![image](https://user-images.githubusercontent.com/108089259/175567469-dc5baf51-c275-4644-99f1-6c19b932089d.png)









