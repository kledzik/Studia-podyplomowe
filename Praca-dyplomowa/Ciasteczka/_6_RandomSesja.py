# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os, pickle, random

class _6_RandomSesja(unittest.TestCase):
    # Licznik plików ze zrzutami ekranu
    licznik = 0
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://demo.testarena.pl/zaloguj"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()
        self.driver.delete_all_cookies()
    
    def test_zapisanie_usuniecie_zmiana_sesji_zaladowanie_ciasteczek(self):
        """
            Zapisanie, usunięcie, zrandomizowana zmiana zaszyfrowanych danych sesji i załadowanie wyedytowanch ciasteczek do aplikacji.
        """
        print u"\n---ZAPISANIE, USUNIĘCIE, ZRANDOMIZOWANA ZMIANA ZASZYFROWANYCH DANYCH SESJI I ZAŁADOWANIE CIASTECZEK DO APLIKACJI---"
        
        # Zalogowanie Admina
        self.login()
        
        # Zapisanie, usunięcie, zrandomizowana zmiana zaszyfrowanych danych sesji i załadowanie wyedytowanch ciasteczek do aplikacji.
        self.zapisz_usun_zmien_szyfr_zaladuj_ciasteczka()
    
    def login(self):
        """
            Zalogowanie Admina z domyślnymi danymi.
        """
        print "Otworzenie strony TestArena Demo"
        driver = self.driver
        driver.get(self.base_url + "/")
        self.assertEqual("TestArena Demo", driver.title)
        self.zrzut_ekranu()
        self.assertEqual("", driver.find_element_by_css_selector("a.login_tc_header").text)
        print "Zalogowanie Admina"
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("administrator@testarena.pl")
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys("sumXQQ72$L")
        driver.find_element_by_id("login").click()
        self.assertEqual("Kokpit - TestArena Demo", driver.title)
        self.assertEqual("KOKPIT", driver.find_element_by_css_selector("h1.content_title").text)
        self.zrzut_ekranu()
    
    def plik_cookies(self):
        """
            Poszukiwanie pliku "cookies.pkl".
        """
        print 'Poszukiwanie pliku "cookies.pkl"'
        self.sciezka_pliku_cookies = os.getcwd() + "\\cookies.pkl"
        if not os.path.isfile(self.sciezka_pliku_cookies):
            print "Brak pliku {0} z ciasteczkami. Przerwano wykonanie testu".format(self.sciezka_pliku_cookies)
            self.driver.quit()
            os._exit(1)
    
    def zapisz_usun_zmien_szyfr_zaladuj_ciasteczka(self):
        """
            Zapisanie, usunięcie, zrandomizowana zmiana zaszyfrowanych danych sesji i załadowanie wyedytowanch ciasteczek do aplikacji.
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        print u"Zapisanie ciasteczek"
        self.sciezka_pliku_cookies = os.getcwd() + "\\cookies.pkl"
        # Pobranie ciasteczek i zapisanie pliku z nimi w trybie binarnym
        with open(self.sciezka_pliku_cookies, "wb") as plik:
            pickle.dump(driver.get_cookies(), plik)
        print u"Usunięcie wszystkich ciasteczek"
        self.driver.delete_all_cookies()
        self.plik_cookies()
        print "Utworzenie tymczasowego pliku z ciasteczkami"
        try:
            print "Edycja ciasteczek (zmiana zaszyfrowanych danych sesji) w pliku tymczasowym"
            # Otwarcie pliku z ciasteczkami w trybie binarnym
            plik_wejsciowy = open(self.sciezka_pliku_cookies, "rb")
            # Utworzenie tymczasowego pliku z ciasteczkami
            plik_tymczasowy = open(os.getcwd() + "\\cookies.pkl_temp", "wb")
            # Zamiana zaszyfrowanych danych sesji na niepoprawne, zrandomizowane
            # Do edycji wybrano ciasteczko o nazwie "SIDMRBUGGYFR" wrażliwe na zmiany
            # swojej zawartości. Cechę tą ustalono wcześniejszymi testami eksploracyjnymi
            linia = plik_wejsciowy.readlines()
            linia[12] = "V"
            for i in range(1, 16):
                linia[12] = linia[12] + str(random.randint(0, 9)) + random.choice("abcdefghijklmnopqrstuvwxyz")
            plik_tymczasowy.writelines(linia)
            plik_tymczasowy.close()
            plik_wejsciowy.close()
            # Usunięcie oryginalnego pliku z ciasteczkami
            os.remove(self.sciezka_pliku_cookies)
            # Zamiana tymczasowego pliku z ciasteczkami na właściwy do użycia w aplikacji
            os.rename(os.getcwd() + "\\cookies.pkl_temp", self.sciezka_pliku_cookies)
        except IOError:
            print u"Nie można otworzyć/zapisać pliku"
        # Otwarcie pliku z wyedytowanymi ciasteczkami w trybie binarnym
        with open(self.sciezka_pliku_cookies, "rb") as plik:
            self.ciasteczka = pickle.load(plik)
        print u"Załadowanie do aplikacji zestawu ciasteczek"
        for ciasteczko in self.ciasteczka:
            nowe_ciasteczko = {}
            nowe_ciasteczko['name'] = ciasteczko['name']
            nowe_ciasteczko['value'] = ciasteczko['value']
            driver.add_cookie(nowe_ciasteczko)
        print u'Próbne otwarcie zakładki "Administracja"'
        driver.find_element_by_link_text("Administracja").click()
        print u'"Wyrzucenie" użytkownika z aplikacji'
        self.assertEqual("TestArena Demo", driver.title)
        self.assertEqual("", driver.find_element_by_css_selector("a.login_tc_header").text)
        self.zrzut_ekranu()
    
    def zrzut_ekranu(self):
        """
            Wykonanie zrzutu ekranu i zapisanie go do pliku PNG w podkatalogu "\RandomSesja".
        """
        print "Zapis zrzutu ekranu do pliku PNG"
        _6_RandomSesja.licznik += 1 # Kolejne pliki ze zrzutami ekranu mają numerację zwiększaną o "1".
        if not os.path.exists(os.getcwd() + "\\RandomSesja"):
            os.mkdir(os.getcwd() + "\\RandomSesja") # Utworzenie katalogu "\RandomSesja".
        self.sciezka_pliku_zrzut = os.getcwd() + "\\RandomSesja" + "\\RandomSesja{0}.png".format(_6_RandomSesja.licznik)
        self.driver.get_screenshot_as_file(self.sciezka_pliku_zrzut)
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
