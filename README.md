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

## Analiza oraz wizualizacja zbioru danych 

### Zaczytanie finalnej wersji pliku oraz usunięcie kolumny "Unnamed"

Usuwamy kolumne "Unnamed" powstałą przy czytaniu data frame z pliku .csv przy użyciu biblioteki pandas.
```
df= pd.read_csv('wersja_finalowa.csv', low_memory = False)
df.drop('Unnamed: 0',axis=1,inplace=True)
```
Import odpowiednich bibliotek do wizualizacji danych oraz dostosowanie wyglądu.
```
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly.express as px
%matplotlib inline

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (9, 5)
matplotlib.rcParams['figure.facecolor'] = '#00000000'
```

Wygląd oczyszcznego data frame.

![image](https://user-images.githubusercontent.com/108089259/175571387-664f0932-fb2f-4196-88fe-5c59eb575fd4.png)

Opis danych staystycznych utworzonego zbioru danych.

```
oczyszczony_data_frame.describe().round(3)
```


Analiza kolumn liczbowych i ich statystyk w naszym zbiorze danych.


![image](https://user-images.githubusercontent.com/108089259/177625556-03b8fd61-0014-412c-a49e-922e2befa60c.png)


## Wizualizacja danych 

### Ilość dni które samochody spędzają na sprzedaży 

```
fig = px.histogram(oczyszczony_data_frame, x="Dni na rynku", marginal="box", title='Ilość dni na rynku samochodów używanych')
fig.update_layout(yaxis_title = 'Liczba samochodów')
fig.show()
```

Wizualizacja kolumny `daysonmarket`, która podaje nam liczbę dni, przez które używany samochód pozostaje na rynku

![image](https://user-images.githubusercontent.com/108089259/177626325-2c6ddabc-1f9f-4b65-b36d-52ed8ed08300.png)


Dni na rynku: Tutaj widzimy, że samochód pozostaje na rynku średnio przez około 1-2 miesiące przed sprzedażą. Niektóre samochody sprzedają się w ciągu jednego dnia, ale niektóre mogą również sprzedawać się dużo dłużej.
Widać wyraźnie, że jest to wartość odstająca, a 75% samochodów jest sprzedawanych w ciągu 80 dni od wejścia na rynek, przy medianie 35 dni.

### Maksymalna liczby siedzeń, którą mają samochody używane

Tutaj tworzymy wykres słupkowy za pomocą matplotlib.


```
maksymalna_liczba_miejsc_w_samochodzie = oczyszczony_data_frame['maximum_seating'].value_counts()
maksymalna_liczba_miejsc_w_samochodzie.plot.bar()
plt.title("Maksymalna liczba zarejestrowanych miejsc siedzących w samochodach używanych");
plt.xlabel("Maksymalna liczba zarejestrowanych miejsc siedzących");
plt.ylabel("Liczba samochodów");
```

![image](https://user-images.githubusercontent.com/108089259/177652528-2e9b99a1-f03f-4a11-a8f3-6442966b3d6c.png)

Wyraźnie widać, że większość samochodów to samochody 5-osobowe, następnie 7, a następnie 6-osobowe.

### Systemy napędowe samochodów używanych

```
system_napedowy = oczyszczony_data_frame['wheel_system'].value_counts()
system_napedowy.plot.pie(autopct='%1.2f%%',radius=1.8,figsize=(5,5),startangle=180);
plt.title('SYSTEM NAPĘDOWY W SAMOCHODACH UŻYWANYCH', y= 1.3);
```

![image](https://user-images.githubusercontent.com/108089259/177652697-5b70710b-7eab-4f83-a425-fb02f3941415.png)


Mamy 5 rodzajów napędów na koła, z których większość samochodów to napęd na przednie koła, następnie automatyczny, a następnie 4WD.

### Rozkład cen używanych samochodów w USA

```
fig = px.histogram(oczyszczony_data_frame, x="price", marginal="box", title='Cena sprzedaży samochodów używanych')
fig.update_layout(yaxis_title = 'Liczba samochodów')
```

![image](https://user-images.githubusercontent.com/108089259/177653046-6945ca29-a36f-4edf-8d20-84ffa77bf485.png)

Jak widać, większość samochodów jest wyceniana na mniej niż 75 tys. USD, więc przyjrzyjmy się teraz uważnie rozkładowi cen w tym przedziale z wyłączeniem wartości odstających.

```
oczyszczony_data_frame['price'].sort_values(ascending = True).iloc[1300000]
a = oczyszczony_data_frame['price'].sort_values(ascending = True).iloc[:1300000]
df = pd.DataFrame(a)
fig = px.histogram(df, x="price", marginal="box", title='Cena sprzedaży większości sprzedanych aut używanych')
fig.update_layout(yaxis_title = 'Liczba samochodów')
```

![image](https://user-images.githubusercontent.com/108089259/177653229-996cade6-599c-445e-9f24-c6956ba7866d.png)

Jak widać o wiele lepiej teraz, że większość samochodów jest wyceniana w granicach 18-25 tys. USD, gdzie średnia cena nowego samochodu zawsze wynosi około 38 tys. USD za lekki pojazd silnikowy według danych „Statista 2021”.

Tak więc kupno używanego samochodu może być bardzo korzystną i mądrą decyzją!

### Ocena sprzedawców samochodów 

```
sns.set_theme(style="ticks");
fig = sns.boxplot(x=oczyszczony_data_frame['seller_rating']);
fig.set(xlabel='Seller Ratings')
plt.title("Ocena sprzedawców samochodów używanych");
plt.show();
```



![image](https://user-images.githubusercontent.com/108089259/177653485-01b47aa3-d216-43df-9a21-ace89022f576.png)

Jak widać, mediana ocen sprzedawców w USA wynosi około 4,4, a 75% sprzedawców ma ocenę powyżej 4,6.

To pokazuje nam, że sprzedawcy wykonują całkiem dobrą robotę, jeśli chodzi o zadowolenie klienta, czy to sprzedawca samochodu, czy kupujący. Obie strony ogólnie oceniają sprzedawców dość wysoko, co jest niezwykłe dla tych sprzedawców, biorąc pod uwagę, jak konkurencyjna i techniczna jest domena.

## Analiza pytań o rynku samochodów używanych w USA 

### Zależność ceny samochodu w zależności od jego mocy

```
px.scatter(oczyszczony_data_frame,x='horsepower',y='price',title='Cena względem mocy samochodu')
```


![image](https://user-images.githubusercontent.com/108089259/177655173-b88e9afe-c7f7-4def-ba38-cefe01210bba.png)

Jak widać, nie ma bezpośredniej ani proporcjonalnej relacji między ceną a mocą samochodu, co oznacza, że muszą istnieć inne czynniki, które odgrywają kluczową rolę w decydowaniu o cenie samochodu używanego, a nie jego moc.

### Które marki są najczęściej sprzedawane na rynku wtórnym?

```
df = oczyszczony_data_frame[['make_name']]
df = df.make_name.value_counts().head(30).sort_values(ascending = True)
df = pd.DataFrame(df)
df.plot(kind='barh',figsize=(15,10),title='Liczba samochodów względem marki na rynku samochodów używanych ',xlabel='Nazwa marki',ylabel='Liczba samochodów');
```

![image](https://user-images.githubusercontent.com/108089259/177655502-73d0349f-90ec-473d-9a45-3bdb8314b8cc.png)

Jak widzimy, niektóre marki, takie jak Ford, Chevrolet, Toyota, zdecydowanie mają dużą liczbę sprzedawanych samochodów na rynku, a marki luksusowe, takie jak Janguar, Mini, Porsche itp., mają bardzo ograniczoną liczbę samochodów na rynku wtórnym. Może to wynikać z różnych powodów, takich jak:

1. Liczba samochodów luksusowych jest bardzo ograniczona w porównaniu z innymi samochodami na drogach, dlatego też liczba samochodów na rynku wtórnym jest ograniczona.
2. Osoby kupujące luksusowe samochody nie sprzedają ich tak dużo, jak zwykli nabywcy samochodów. W przeciwieństwie do zwykłych nabywców z klasy średniej mogą mieć przy sobie więcej niż jeden samochód, a tym samym nie wprowadzać swoich samochodów na rynek wtórny.
3. Jakość samochodów luksusowych jest taka, że użytkownicy mają tendencję do używania ich przez dłuższy czas w porównaniu ze zwykłym samochodem.

### Które miasta są najbardziej aktywne na rynku samochodów używanych?


```
df = oczyszczony_data_frame[['city','price']]
df1 = df.groupby('city')[['price']].count().sort_values('price',ascending= False) 
df2 = df1.head(30).sort_values('price',ascending=True);
df2.plot(kind='barh',legend=False,xlabel='City',ylabel='Liczba samochodów na sprzedarz', title='Top 30 miast z największą ilością samochodów używanych na sprzedaż',figsize=(13,8));
``` 

![image](https://user-images.githubusercontent.com/108089259/177656040-a44f9648-ac8b-4826-bbd0-b2a1933a0452.png)

Jak widać, rozkład liczby samochodów pomiędzy miastami jest dobry.

Tutaj właśnie zwizualizowaliśmy 30 najlepszych miast, ale podążając za trendem, możemy być pewni, że na rynku samochodów używanych jest wiele miast z pokaźną liczbą samochodów.

### Czy sezonowość ma wpływ na ceny samochodów? W jakich miesiącach widzimy najwyższe i najniższe ceny auta używanego?

```
oczyszczony_data_frame['year']=oczyszczony_data_frame['listed_date'].dt.year
oczyszczony_data_frame['month']=oczyszczony_data_frame['listed_date'].dt.month
df1 = oczyszczony_data_frame.sort_values(by='price', ascending= True)
df1 = df1.iloc[:1300000]
df2 = df1.groupby(['year','month'])['price'].median()
df3 = df2.reset_index()
df4 = df3.pivot('year','month','price')
plt.figure(figsize = (16,8))
sns.heatmap(df4,fmt="d",cmap='Greens');
``` 

![image](https://user-images.githubusercontent.com/108089259/177656187-c6d3894c-3558-4fd4-8742-c57ca3bca825.png)

Tutaj widzimy, że ceny rosły na przestrzeni lat ze względu na inflację lub z innych powodów, podobnie jak ceny nowych samochodów rosną z biegiem lat. Nie ma dużej różnicy między cenami samochodów sprzedawanych w różnych miesiącach, a cena rozkłada się niemal równomiernie. Można więc śmiało powiedzieć, że sezonowość nie odgrywa kluczowej roli w sprzedaży lub kupnie używanego samochodu.

### Ile osób kupuje lub sprzedaje samochód powypadkowy?

![image](https://user-images.githubusercontent.com/108089259/177656381-0d33bf76-5bbd-4bf8-9812-65d005c90dcd.png)

![image](https://user-images.githubusercontent.com/108089259/177656464-f28ff325-e43a-48b2-bd89-cbafdfd4efee.png)

To dość zaskakujące, ponieważ codziennie widzimy na ulicy liczne samochody z wgnieceniami i rysami. Jednak to, co widzimy tutaj, jest zupełnie inne, ponieważ 99% samochodów na rynku używanych nie podaje informacji o uszkodzeniach.

Powodem tego może być to, że gdy ktoś idzie sprzedać lub kupić używany samochód, obie strony zapewniają, że nie ma fizycznych uszkodzeń pojazdu, ponieważ nie jest to pożądane dla żadnej z zaangażowanych stron, a zatem 99% sprzedawane samochody nie są fizycznie uszkodzone!

### tóre marki są najbardziej poszukiwane na rynku samochodów używanych?

```
df = oczyszczony_data_frame.groupby('make_name')['daysonmarket'].median().sort_values(ascending=True)
df.plot(kind='bar',figsize=(22,10),title='Czas sprzedaży samochodu danej marki',xlabel='Brands',ylabel='Number of Days');
```

![image](https://user-images.githubusercontent.com/108089259/177656679-7d273298-dc3f-4889-9a10-0c8450d0ef36.png)


Możemy to przeanalizować, przyglądając się, ile dni potrzeba, aby używany samochód danej marki został sprzedany lub kupiony ogólnie na rynku.

Jak widać, większość marek jest na rynku sprzedawana przez podobny czas. Jednak niektóre marki, takie jak Daewood, Karma, Maybach, Aston Martin, utrzymują się na rynku dość długo.

Może to wynikać z wielu czynników:
a. Samochody w próbie nie były w najlepszym stanie, aby były pożądane przez innego użytkownika.

b. Samochody takie jak Rolls Royce są jedyne w swoim rodzaju i dlatego osoby zainteresowane kupnem takiego auta wolałyby nowy zamiast używanego, ponieważ jest to bardziej symbol statusu dla ludzi niż tylko samochód.

Jednocześnie mamy takie marki jak Subaru, Toyota, Mazda, Chevrolet, Lexus, GMC, Toyota, które dość szybko poruszają się na rynku.
Przyczyny mogą być następujące:

a. Większość ludzi kupuje i sprzedaje te samochody, stąd liczba samochodów dostępnych na rynku jest ogromna i szybko się poruszają.

b. Marki te oferują ekonomiczne samochody dla ludzi, dzięki czemu wartość odsprzedaży staje się znacznie tańsza dla użytkownika. Powoduje to, że wiele osób kupuje te samochody w porównaniu do drogich.

