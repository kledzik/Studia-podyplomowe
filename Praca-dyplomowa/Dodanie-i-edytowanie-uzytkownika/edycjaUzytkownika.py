# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os, random

class EdycjaUzytkownika(unittest.TestCase):
    # Licznik plików ze zrzutami ekranu.
    licznik = 0
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://demo.testarena.pl/zaloguj"
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()
    
    def test_EdytujUzytkownika(self):
        """
            Edycja danych użytkownika.
        """
        print u"\n---EDYCJA DANYCH UŻYTKOWNIKA---"
        
        # Zalogowanie Admina
        self.login()
        
        # Edycja danych użytkownika
        self.edycja_danych_uzytkownika()
        
        # Dezaktywacja użytkownika
        self.dezaktywacja_uzytkownika()
        
        # Aktywacja użytkownika
        self.aktywacja_uzytkownika()
        
        # Zresetowanie hasła użytkownika
        self.resetowanie_hasla()
        
        # Brak Admina na liście użytkowników
        self.brak_admina_na_liscie()
        
        # Wylogowanie Admina
        self.logout()
    
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
    
    def edycja_danych_uzytkownika(self):
        """
            Edycja danych użytkownika. Wprowadzenie pustych danych, danych niepoprawnych oraz danych prawidłowych.
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Administracja").click()
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"UŻYTKOWNICY").click()
        self.assertEqual(u"Użytkownicy - TestArena Demo", driver.title)
        self.assertEqual(u"UŻYTKOWNICY", driver.find_element_by_css_selector("h1.content_title").text)
        self.zrzut_ekranu()
        print u"Edycja danych użytkownika, pierwszego na liście"
        driver.find_element_by_id("action_icon").click()
        driver.find_element_by_link_text("Edytuj").click()
        self.assertEqual(u"Edytuj użytkownika - TestArena Demo", driver.title)
        self.assertEqual(u"EDYTUJ UŻYTKOWNIKA", driver.find_element_by_css_selector("h1.content_title").text)
        self.zrzut_ekranu()
        print u"Próba zapisania pustych danych"
        driver.find_element_by_id("firstname").clear()
        driver.find_element_by_id("firstname").send_keys("")
        driver.find_element_by_id("lastname").clear()
        driver.find_element_by_id("lastname").send_keys("")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("")
        driver.find_element_by_name("save").click()
        try: self.assertEqual("Pole wymagane", driver.find_element_by_xpath("(//div[@id='text']/div)[1]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Pole wymagane", driver.find_element_by_xpath("(//div[@id='text']/div)[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Pole wymagane", driver.find_element_by_xpath("(//div[@id='text']/div)[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        print u"Próba zapisania nieprawidłowych danych"
        driver.find_element_by_id("firstname").clear()
        driver.find_element_by_id("firstname").send_keys("!")
        driver.find_element_by_id("lastname").clear()
        driver.find_element_by_id("lastname").send_keys("!")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("!")
        driver.find_element_by_name("save").click()
        try: self.assertEqual(u"Imię może zawierać wyłącznie litery, spacje oraz znaki '-", driver.find_element_by_xpath("(//div[@id='text']/div)[1]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Minimalna liczba znaków dla pola to 2.", driver.find_element_by_xpath("(//div[@id='text']/div)[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Nazwisko może zawierać wyłącznie litery, spacje oraz znaki '-", driver.find_element_by_xpath("(//div[@id='text']/div)[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Minimalna liczba znaków dla pola to 2.", driver.find_element_by_xpath("(//div[@id='text']/div[2])[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Nieprawidłowy format adresu e-mail. Wprowadź adres ponownie.", driver.find_element_by_xpath("(//div[@id='text']/div)[5]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Minimalna liczba znaków dla pola to 6.", driver.find_element_by_xpath("(//div[@id='text']/div[2])[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        print u"Zapisanie prawidłowych danych"
        driver.find_element_by_id("firstname").clear()
        driver.find_element_by_id("firstname").send_keys(u"UżytkownikTA")
        driver.find_element_by_id("lastname").clear()
        driver.find_element_by_id("lastname").send_keys(u"UżytkownikTA")
        driver.find_element_by_id("email").clear()
        self.edytowany_uzytkownik = "UzytkownikTA{0}@testarena{1}.pl".format(random.randint(1, 1000), random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        driver.find_element_by_id("email").send_keys(self.edytowany_uzytkownik)
        driver.find_element_by_id("organization").clear()
        driver.find_element_by_id("organization").send_keys("TestArena")
        driver.find_element_by_id("department").clear()
        driver.find_element_by_id("department").send_keys("QA")
        driver.find_element_by_id("phoneNumber").clear()
        driver.find_element_by_id("phoneNumber").send_keys("+48 12 34 56 789")
        #try: self.assertEqual("true", driver.find_element_by_id("activeUser").get_attribute("checked"))
        #except AssertionError as e: self.verificationErrors.append(str(e))
        #try: self.assertEqual(None, driver.find_element_by_name("administrator").get_attribute("checked"))
        #except AssertionError as e: self.verificationErrors.append(str(e))
        if not driver.find_element_by_id("activeUser").is_selected():
            driver.find_element_by_id("activeUser").click()
        try: self.assertTrue(driver.find_element_by_id("activeUser").is_selected())
        except AssertionError as e: self.verificationErrors.append(str(e))
        if driver.find_element_by_id("administrator").is_selected():
            driver.find_element_by_id("administrator").click()
        try: self.assertFalse(driver.find_element_by_id("administrator").is_selected())
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        driver.find_element_by_name("save").click()
        for i in range(60):
            try:
                if u"Użytkownik został zapisany." == driver.find_element_by_css_selector("p").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual(u"Użytkownik został zapisany.", driver.find_element_by_css_selector("p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        print u'Szukanie "wyedytowanego" użytkownika na liście'
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys(self.edytowany_uzytkownik)
        driver.find_element_by_id("j_filterButton").click()
        print u"Weryfikacja danych użytkownika"
        try: self.assertEqual(u"UżytkownikTA", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"UżytkownikTA", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertRegexpMatches(driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[4]").text, r"UzytkownikTA[0-9]+@testarena[A-Z]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Aktywny", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[5]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Nie", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[6]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TestArena", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[7]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("QA", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[8]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("+48 12 34 56 789", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[9]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertNotEqual("0000-00-00 00:00:00", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[10]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("0000-00-00 00:00:00", driver.find_element_by_xpath("//section[@id='content']/article/table/tbody/tr/td[11]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"Wyjdź z administracji").click()
        self.assertEqual("Kokpit - TestArena Demo", driver.title)
        try: self.assertEqual(u"KOKPIT", driver.find_element_by_css_selector("h1.content_title").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
    
    def dezaktywacja_uzytkownika(self):
        """
            Dezaktywacja użytkownika.
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Administracja").click()
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"UŻYTKOWNICY").click()
        self.assertEqual(u"Użytkownicy - TestArena Demo", driver.title)
        self.assertEqual(u"UŻYTKOWNICY", driver.find_element_by_css_selector("h1.content_title").text)
        print u'Szukanie "wyedytowanego" użytkownika na liście'
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys(self.edytowany_uzytkownik)
        driver.find_element_by_id("j_filterButton").click()
        print u'Weryfikacja że "wyedytowany" użytkownik jest aktywny'
        if driver.find_element_by_xpath("//*[@id='content']/article/table/tbody/tr[1]/td[5]").text == "Aktywny":
            try: self.assertEqual("Aktywny", driver.find_element_by_css_selector("td.t_status").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
            self.zrzut_ekranu()
            print u"Dezaktywacja użytkownika"
            driver.find_element_by_id("action_icon").click()
            driver.find_element_by_link_text("Dezaktywuj").click()
            for i in range(60):
                try:
                    if u"Użytkownik został dezaktywowany." == driver.find_element_by_css_selector("p").text: break
                except: pass
                time.sleep(1)
            else: self.fail("time out")
            try: self.assertEqual(u"Użytkownik został dezaktywowany.", driver.find_element_by_css_selector("p").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
            try: self.assertEqual("Nieaktywny", driver.find_element_by_css_selector("td.t_status").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
            self.zrzut_ekranu()
        else:
            print u"Użytkownik jest nieaktywny!"
            self.zrzut_ekranu()
        driver.find_element_by_link_text(u"Wyjdź z administracji").click()
        self.assertEqual("Kokpit - TestArena Demo", driver.title)
        try: self.assertEqual(u"KOKPIT", driver.find_element_by_css_selector("h1.content_title").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
    
    def aktywacja_uzytkownika(self):
        """
            Aktywacja użytkownika.
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Administracja").click()
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"UŻYTKOWNICY").click()
        self.assertEqual(u"Użytkownicy - TestArena Demo", driver.title)
        self.assertEqual(u"UŻYTKOWNICY", driver.find_element_by_css_selector("h1.content_title").text)
        print u'Szukanie "wyedytowanego" użytkownika na liście'
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys(self.edytowany_uzytkownik)
        driver.find_element_by_id("j_filterButton").click()
        print u'Weryfikacja że "wyedytowany" użytkownik jest nieaktywny'
        try: self.assertEqual("Nieaktywny", driver.find_element_by_css_selector("td.t_status").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        print u"Aktywacja użytkownika"
        driver.find_element_by_id("action_icon").click()
        driver.find_element_by_link_text("Aktywuj").click()
        for i in range(60):
            try:
                if u"Użytkownik został aktywowany." == driver.find_element_by_css_selector("p").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual(u"Użytkownik został aktywowany.", driver.find_element_by_css_selector("p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Aktywny", driver.find_element_by_css_selector("td.t_status").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"Wyjdź z administracji").click()
        self.assertEqual("Kokpit - TestArena Demo", driver.title)
        try: self.assertEqual(u"KOKPIT", driver.find_element_by_css_selector("h1.content_title").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
    
    def resetowanie_hasla(self):
        """
            Zresetowanie hasła użytkownika.
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Administracja").click()
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"UŻYTKOWNICY").click()
        self.assertEqual(u"Użytkownicy - TestArena Demo", driver.title)
        self.assertEqual(u"UŻYTKOWNICY", driver.find_element_by_css_selector("h1.content_title").text)
        self.zrzut_ekranu()
        print u'Szukanie "wyedytowanego" użytkownika na liście'
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys(self.edytowany_uzytkownik)
        driver.find_element_by_id("j_filterButton").click()
        print u"Zresetowanie hasła użytkownika"
        driver.find_element_by_id("action_icon").click()
        driver.implicitly_wait(1)
        if self.is_element_present(By.LINK_TEXT, u"Wymuś zmianę hasła"):
            driver.find_element_by_link_text(u"Wymuś zmianę hasła").click()
            for i in range(60):
                try:
                    if u"Użytkownikowi zostało zresetowane hasło." == driver.find_element_by_css_selector("p").text: break
                except: pass
                time.sleep(1)
            else: self.fail("time out")
            try: self.assertEqual(u"Użytkownikowi zostało zresetowane hasło.", driver.find_element_by_css_selector("p").text)
            except AssertionError as e: self.verificationErrors.append(str(e))
            self.zrzut_ekranu()
        else:
            print u"Brak możliwości zresetowania hasła"
            self.zrzut_ekranu()
        driver.find_element_by_link_text(u"Wyjdź z administracji").click()
        self.assertEqual("Kokpit - TestArena Demo", driver.title)
        try: self.assertEqual(u"KOKPIT", driver.find_element_by_css_selector("h1.content_title").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
    
    def brak_admina_na_liscie(self):
        """
            Zweryfikowanie, że pierwszy administrator stworzony w systemie nie jest widoczny na liście użytkowników.
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Administracja").click()
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"UŻYTKOWNICY").click()
        self.assertEqual(u"Użytkownicy - TestArena Demo", driver.title)
        self.assertEqual(u"UŻYTKOWNICY", driver.find_element_by_css_selector("h1.content_title").text)
        self.zrzut_ekranu()
        print u"Szukanie administratora na liście użytkowników"
        driver.find_element_by_id("search").clear()
        driver.find_element_by_id("search").send_keys("administrator@testarena.pl")
        driver.find_element_by_id("j_filterButton").click()
        try: self.assertEqual(u"Brak użytkowników.", driver.find_element_by_css_selector("article.article_in_content > div").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
        driver.find_element_by_link_text(u"Wyjdź z administracji").click()
        self.assertEqual("Kokpit - TestArena Demo", driver.title)
        try: self.assertEqual(u"KOKPIT", driver.find_element_by_css_selector("h1.content_title").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.zrzut_ekranu()
    
    def logout(self):
        """
            Wylogowanie Admina.
        """
        print "Wylogowanie z aplikacji TestArena Demo"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Wyloguj").click()
        self.assertEqual("TestArena Demo", driver.title)
        self.assertEqual("", driver.find_element_by_css_selector("a.login_tc_header").text)
        self.zrzut_ekranu()

    def zrzut_ekranu(self):
        """
            Wykonanie zrzutu ekranu i zapisanie go do pliku PNG w podkatalogu "\EdycjaUzytkownika".
        """
        print "Zapis zrzutu ekranu do pliku PNG"
        EdycjaUzytkownika.licznik += 1 # Kolejne pliki ze zrzutami ekranu mają numerację zwiększaną o "1".
        if not os.path.exists(os.getcwd() + "\\EdycjaUzytkownika"):
            os.mkdir(os.getcwd() + "\\EdycjaUzytkownika") # Utworzenie folderu "EdycjaUzytkownika".
        self.sciezka_pliku_zrzut = os.getcwd() + "\\EdycjaUzytkownika" + "\\EdycjaUzytkownika{0}.png".format(EdycjaUzytkownika.licznik)
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
