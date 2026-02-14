# KML/GPS Processor

Nowoczesny system do przetwarzania i analizy danych GPS w formatach GPX i KML z zaawansowanymi możliwościami wizualizacji.

## 🏗️ Struktura Projektu

```
kml_processor/
├── data/
│   ├── input/                  # GPX + KML (17 plików MIX)
│   │   ├── *.gpx              # Trasy GPS  
│   │   └── *.kml              # Trasy KML (konwertuj ↓)
│   └── output/
│       ├── *.kml              # Wynik konwersji GPX→KML ✓
│       ├── *.gpx              # Wynik konwersji KML→GPX ✓
│       ├── gps_master.csv     # NOWE: wszystkie trasy ✓
│       └── *.png              # profile wysokości ✓
├── src/
│   ├── core/
│   │   ├── converter.py       # DWUKIERUNKOWY GPX↔KML ✓
│   │   └── analyzer.py        # Analiza statystyczna
│   ├── scripts/
│   │   ├── 01_gpx_to_master_csv.py  # NOWE (GPX+KML→CSV)
│   │   ├── batch_convert.py   # Wsadowa konwersja ✓
│   │   └── visualize.py       # Wizualizacje
│   └── main.py                # Główne CLI ✓
├── analysis/                  # NOWE dla Razaq
│   └── gps_viz_razaq.Rmd      # 18 wykresów ggplot2 ✓
├── route_analysis.ipynb       # Jupyter notebook
├── requirements.txt            # Zależności
└── README.md                  # Dokumentacja
```

## 🚀 Nowe Funkcjonalności

### ✅ Konwersja Dwukierunkowa GPX↔KML
- Pełne wsparcie dla obu formatów
- Zachowanie metadanych (czas, wysokość, nazwy tras)
- Konwersja pojedyncza i wsadowa

### ✅ Master CSV Database
- Agregacja wszystkich plików GPX+KML do jednego CSV
- Ustandaryzowane kolumny: `placemark`, `latitude`, `longitude`, `altitude`, `time`, `source_file`
- Metadane przetwarzania i typy plików

### ✅ Zaawansowana Wizualizacja (18 wykresów)
- **Rozkłady statystyczne:** wysokości, współrzędne, typy plików
- **Wykresy czasowe:** rozkład punktów według godzin
- **Mapy i rozrzut:** punkty GPS, gęstość 2D
- **Analiza tras:** statystyki per trasa, zasięg geograficzny
- **Korelacje:** zależności między współrzędnymi i wysokością
- **Tabele podsumowujące:** interaktywne statystyki tras

## 📦 Instalacja

```bash
# Klonowanie repozytorium
git clone https://github.com/tomekbiel/kml-processor.git
cd kml-processor

# Instalacja zależności
pip install -r requirements.txt

# Dla wizualizacji R (opcjonalnie)
# R packages: tidyverse, readr, lubridate, ggplot2, plotly, DT, knitr, kableExtra
```

## 🛠️ Użycie

### CLI Interface

```bash
# Konwersja pojedynczego pliku
python src/main.py --action convert --file "trasa.gpx" --from-format gpx --to-format kml

# Konwersja wsadowa
python src/main.py --action batch --from-format gpx --to-format kml

# Tworzenie master CSV
python src/main.py --action master-csv

# Analiza statystyczna
python src/main.py --action analyze
```

### Skrypty

```bash
# Master CSV z wszystkich plików
python src/scripts/01_gpx_to_master_csv.py

# Wsadowa konwersja
python src/scripts/batch_convert.py

# Wizualizacje Python
python src/scripts/visualize.py
```

### Wizualizacja R (Razaq)

```r
# W folderze analysis/
library(rmarkdown)
render("gps_viz_razaq.Rmd")
# Otwórz gps_viz_razaq.html w przeglądarce
```

## 📊 Przykładowe Wyniki

### Master CSV Structure
```
placemark,latitude,longitude,altitude,time,source_file,file_type,processed_date
from Glendalough to Valleymount,53.054276,-6.382625,800.11,2025-05-03T21:59:53Z,trasa.gpx,gpx,2026-02-13T12:00:00
...
```

### 18 Wykresów R Markdown
1. Rozkład punktów według typów plików
2. Histogram wysokości
3. Wykres pudełkowy wysokości według tras
4. Rozkład szerokości geograficznej
5. Rozkład długości geograficznej
6. Wysokość vs Szerokość geograficzna
7. Wysokość vs Długość geograficzna
8. Rozkład punktów w czasie (godziny)
9. Liczba punktów na trasę
10. Średnia wysokość na trasę
11. Mapa punktów GPS (rozrzut)
12. Wysokość vs Czas
13. Statystyki wysokości według typów plików
14. Gęstość punktów 2D (kontur)
15. Zasięg geograficzny każdej trasy
16. Korelacja między współrzędnymi
17. Rozkład wysokości z podziałem na kwartyle
18. Tabela podsumowujące statystyki tras

## 🔧 Technologie

- **Python:** gpxpy, simplekml, pykml, pandas, matplotlib
- **R:** tidyverse, ggplot2, plotly, DT, knitr
- **Formaty:** GPX 1.1, KML 2.2, CSV
- **Wizualizacja:** HTML interaktywne wykresy

## 📈 Statystyki Projektu

- **17 plików wejściowych:** GPX + KML mix
- **18 wykresów wizualizacyjnych**
- **Dwukierunkowa konwersja formatów**
- **Master CSV z metadanymi**
- **Modułowa architektura**

## 🤝 Współpraca

Projekt przygotowany dla analizy danych GPS z możliwościami:
- Przetwarzania wsadowego
- Zaawansowanej wizualizacji
- Analizy statystycznej
- Konwersji między formatami

---

*Generated with ❤️ for GPS data analysis*
