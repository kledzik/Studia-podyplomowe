# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os

class _2_Usuniecie(unittest.TestCase):
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
    
    def test_usuniecie_ciasteczek(self):
        """
            Usunięcie wszystkich ciasteczek i "wyrzucenie" użytkownika z aplikacji.
        """
        print u'\n---USUNIĘCIE CIASTECZEK I "WYRZUCENIE" UŻYTKOWNIKA Z APLIKACJI---'
        
        # Zalogowanie Admina
        self.login()
        
        # Usunięcie wszystkich ciasteczek.
        self.usun_ciasteczka()
    
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
    
    def usun_ciasteczka(self):
        """
            Usunięcie wszystkich ciasteczek.
        """
        print u"Usunięcie wszystkich ciasteczek"
        driver = self.driver
        driver.get(self.base_url + "/")
        self.driver.delete_all_cookies()
        print u'Próbne otwarcie zakładki "Administracja"'
        driver.find_element_by_link_text("Administracja").click()
        print u'"Wyrzucenie" użytkownika z aplikacji'
        self.assertEqual("TestArena Demo", driver.title)
        self.assertEqual("", driver.find_element_by_css_selector("a.login_tc_header").text)
        self.zrzut_ekranu()
    
    def zrzut_ekranu(self):
        """
            Wykonanie zrzutu ekranu i zapisanie go do pliku PNG w podkatalogu "\Usuniecie".
        """
        print "Zapis zrzutu ekranu do pliku PNG"
        _2_Usuniecie.licznik += 1 # Kolejne pliki ze zrzutami ekranu mają numerację zwiększaną o "1".
        if not os.path.exists(os.getcwd() + "\\Usuniecie"):
            os.mkdir(os.getcwd() + "\\Usuniecie") # Utworzenie katalogu "\Usunieci".
        self.sciezka_pliku_zrzut = os.getcwd() + "\\Usuniecie" + "\\Usuniecie{0}.png".format(_2_Usuniecie.licznik)
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
