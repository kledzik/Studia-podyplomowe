# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os

class _1_Zablokowanie(unittest.TestCase):
    # Licznik plików ze zrzutami ekranu
    licznik = 0
    def setUp(self):
        fp = webdriver.FirefoxProfile()
        # Zablokowanie ciasteczek przez przeglądarkę Firefox
        fp.set_preference("network.cookie.cookieBehavior", 2)
        self.driver = webdriver.Firefox(firefox_profile = fp)
        self.driver.implicitly_wait(30)
        self.base_url = "http://demo.testarena.pl/zaloguj"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()
        self.driver.delete_all_cookies()
    
    def test_zablokowanie_ciasteczek(self):
        """
            Zablokowanie wszystkich ciasteczek przez przeglądarkę.
        """
        print u"\n---ZABLOKOWANIE WSZYSTKICH CIASTECZEK PRZEZ PRZEGLĄDARKĘ---"
        
        # Zalogowanie Admina
        self.login()
        
    def login(self):
        """
            Zalogowanie Admina z domyślnymi danymi.
        """
        driver = self.driver
        print "Otworzenie strony TestArena Demo"
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
        print u"Brak możliwości zalogowania użytkownika"
        time.sleep(2)
        self.assertEqual(u"WAŻNOŚĆ FORMULARZA WYGASŁA. SPRÓBUJ WYSŁAĆ O PONOWNIE.", driver.find_element_by_xpath("//div[@id='text-2']/div/form/div[4]/div[3]/div").text)
        self.zrzut_ekranu()
    
    def zrzut_ekranu(self):
        """
            Wykonanie zrzutu ekranu i zapisanie go do pliku PNG w podkatalogu "\Zablokowanie".
        """
        print "Zapis zrzutu ekranu do pliku PNG"
        _1_Zablokowanie.licznik += 1 # Kolejne pliki ze zrzutami ekranu mają numerację zwiększaną o "1".
        if not os.path.exists(os.getcwd() + "\\Zablokowanie"):
            os.mkdir(os.getcwd() + "\\Zablokowanie") # Utworzenie katalogu "\Zablokowanie".
        self.sciezka_pliku_zrzut = os.getcwd() + "\\Zablokowanie" + "\\Zablokowanie{0}.png".format(_1_Zablokowanie.licznik)
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
