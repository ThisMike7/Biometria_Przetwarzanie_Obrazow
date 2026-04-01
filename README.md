# Projekt Biometria - Przetwarzanie Obrazów

Aplikacja napisana w języku Python służąca do przetwarzania obrazów oraz podstawowej analizy biometrycznej. 

Wszystkie algorytmy zostały zaimplementowane od zera przy użyciu biblioteki NumPy.

## 🚀 Główne funkcjonalności

* **Operacje punktowe:** Konwersja do skali szarości, negatyw, korekta jasności, zmiana kontrastu, korekta gamma oraz progowanie (binaryzacja).
* **Filtry przestrzenne (Sploty):** * Wygładzające: Filtr uśredniający, Filtr Gaussa.
  * Krawędziowe: Filtr Laplace'a, Krzyż Robertsa (2x2), Operator Sobela (3x3).
* **Moduł analizy biometrycznej:** Generowanie w czasie rzeczywistym interaktywnych wykresów:
  * Projekcja pozioma i pionowa.
  * Histogram kanałów RGB.
 
## ⚙️ Jak uruchomić projekt

Projekt można uruchomić na dwa sposoby: bezpośrednio ze skryptu źródłowego (dla Windows/Linux) lub jako gotową aplikację (dla macOS)

### 💻 Opcja 1: Uruchomienie ze skryptu (Windows / Linux)

Do uruchomienia kodu źródłowego wymagany jest zainstalowany **Python w wersji 3.x**.

1. Otwórz terminal w głównym folderze projektu i zainstaluj wymagane pakiety wpisując komendę:
   ```bash
   pip install numpy pillow matplotlib
2. Uruchom skrypt:
   ```bash
   python main.py
### 🍏 Opcja 2: Gotowa aplikacja dla macOS

W repozytorium (lub w dołączonym archiwum) znajduje się gotowy, skompilowany plik aplikacji dla systemu macOS `main.app`). Nie wymaga on instalacji Pythona ani żadnych dodatkowych bibliotek.

