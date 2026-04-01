# Projekt Biometria - Przetwarzanie Obrazów

Aplikacja desktopowa napisana w języku Python służąca do przetwarzania obrazów oraz podstawowej analizy biometrycznej. 

Wszystkie algorytmy zostały zaimplementowane od zera przy użyciu biblioteki NumPy.

## 🚀 Główne funkcjonalności

Projekt realizuje operacje na obrazach z wykorzystaniem zdefiniowanego pipeline'u.

* **Operacje punktowe:** Konwersja do skali szarości, negatyw, korekta jasności, zmiana kontrastu, korekta gamma oraz progowanie (binaryzacja).
* **Filtry przestrzenne (Sploty):** * Wygładzające: Filtr uśredniający, Filtr Gaussa.
  * Krawędziowe: Filtr Laplace'a, Krzyż Robertsa (2x2), Operator Sobela (3x3).
* **Moduł analizy biometrycznej:** Generowanie w czasie rzeczywistym interaktywnych wykresów:
  * Projekcja pozioma i pionowa.
  * Histogram kanałów RGB.
