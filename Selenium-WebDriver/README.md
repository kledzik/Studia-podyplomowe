# Automatyczne testy aplikacji ICM w Selenium WebDriver

Celem ćwiczenia było przetestowanie wybranych funkcjonalności aplikacji webowej ICM [1] przy użyciu automatycznego testu napisanego w języku skryptowym Python 2.x, z wykorzystaniem Selenium WebDriver.

## Uwzględniono następujące przypadki testowe:
1. Dodanie incydentu wraz z weryfikacją wszystkich istotnych pól w aplikacji, w bazie danych, oraz w pliku eksportu.
2. Dodawanie audytu do istniejącego incydentu, z wykorzystaniem incydentu już istniejącego w bazie danych. Zweryfikowanie audytu w aplikacji oraz bezpośrednio w bazie danych.
3. Dodanie pliku do istniejącego audytu oraz download tego pliku.
4. Dodanie dziesięciu incydentów z pliku CSV.
5. Zmiana statusu incydentu, od nowego do zamkniętego. Zweryfikowanie zmian w aplikacji (filtr na liście incydentów), w pliku CSV oraz w bazie danych.

## Linki
* [[1] Aplikacja ICM](https://github.com/kolorobot/spring-mvc-icm-demo)
