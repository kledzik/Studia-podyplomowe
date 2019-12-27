# -*- coding: utf-8 -*-

# https://docs.python.org/2/library/test.html

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os, io, sqlite3

class TestIcm(unittest.TestCase):
    def setUp(self):
        fp = webdriver.FirefoxProfile()
        # Skonfigurowanie profilu przeglądarki, aby po kliknięciu linka nie pojawiło się okno wyboru katalogu.
        # https://developer.mozilla.org/en-US/docs/Download_Manager_preferences
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        # Pliki mają zostać zapisane w katalogu w którym uruchamia się niniejszy skrypt.
        fp.set_preference("browser.download.dir", os.getcwd())
        # Pliki o podanym typie będą automatycznie zapisywane na dysk
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, text/csv, image/jpeg")
        
        self.driver = webdriver.Firefox(firefox_profile = fp)
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:9998/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    #______________________Pięć niezależnych suit testowych.______________________
    
    def test_icm_1_dodanie_incydentu(self):
        """
            Test 1. Dodanie incydentu do Admina.
        """
        print "---TEST 1. DODANIE INCYDENTU DO ADMINA---"
        
        # Poszukiwanie pliku "incydent.csv".
        self.plik_incydent()
        
        # Poszukiwanie pliku "incidents_JEDEN.csv".
        self.plik_incidents_JEDEN_usun()
        
        # Ustawienie dostępu do bazy danych.
        self.dostep_do_bazy_danych()
        
        # Zresetowanie bazy danych.
        self.zresetowanie_bazy_danych()
        
        # Otwarcie głównej strony aplikacji.
        self.strona_glowna()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Dodanie jednego incydentu do Admina.
        self.dodanie_incydentu()
        
        # Weryfikacja dodania incydentu do aplikacji.
        self.weryfikacja_incydentu_w_aplikacji()
        
        # Weryfikacja incydentu w bazie danych.
        self.weryfikacja_incydentu_w_bazie_danych()
        
        # Eksport pliku "incidents.csv".
        self.eksport_incydentow()
        
        # Weryfikacja zawartości pliku "incidents.csv".
        self.weryfikacja_zawartosci_incydentow()
        
        # Zmiana nazwy pliku z "incidents.csv" na "incidents_JEDEN.csv".
        self.zmiana_nazwy_pliku_incidents()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
    def test_icm_2_dodanie_audytu(self):
        """
            Test 2. Dodanie audytu do istniejącego incydentu.
        """
        print u"---TEST 2. DODANIE AUDYTU DO ISTNIEJĄCEGO INCYDENTU---"
        
        # Poszukiwanie pliku "audyt.csv".
        self.plik_audyt()
        
        # Ustawienie dostępu do bazy danych.
        self.dostep_do_bazy_danych()
        
        # Zresetowanie bazy danych.
        self.zresetowanie_bazy_danych()
        
        # Otwarcie głównej strony aplikacji.
        self.strona_glowna()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Dodanie audytu do istniejącego incydentu.
        self.dodanie_audytu()
        
        # Weryfikacja dodania audytu w aplikacji.
        self.weryfikacja_audytu_w_aplikacji()
        
        # Weryfikacja dodania audytu w bazie danych.
        self.weryfikacja_audytu_w_bazie_danych()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
    
    def test_icm_3_dodanie_i_download_pliku(self):
        """
            Test 3. Dodanie i download pliku do istniejącego audytu.
        """
        print u"---TEST 3. DODANIE I DOWNLOAD PLIKU DO ISTNIEJĄCEGO AUDYTU---"
        
        # Poszukiwanie pliku "rozszczelnione_okno.jpg".
        self.plik_rozszczelnione_okno()
        
        # Poszukiwanie pliku "rozszczelnione_okno_DOWNLOADED.jpg".
        self.plik_rozszczelnione_okno_DOWNLOADED_usun()
        
        # Zresetowanie bazy danych.
        self.zresetowanie_bazy_danych()
        
        # Otwarcie głównej strony aplikacji.
        self.strona_glowna()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Dodanie pliku "rozszczelnione_okno.jpg" do istniejącego audytu.
        self.dodanie_pliku_rozszczelnione_okno()
        
        # Download pliku "rozszczelnione_okno.jpg".
        self.download_pliku_rozszczelnione_okno()
        
        # Zmiana nazwy pliku na "rozszczelnione_okno_DOWNLOADED.jpg".
        self.zmiana_nazwy_pliku_rozszczelnione_okno()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
    
    def test_icm_4_dodanie_10_incydentow(self):
        """
            Test 4. Dodanie 10 incydentów do Admina.
        """
        print u"---TEST 4. DODANIE 10 INCYDENTÓW DO ADMINA---"
        
        # Poszukiwanie pliku "incydenty.csv".
        self.plik_incydenty()
        
        # Zresetowanie bazy danych.
        self.zresetowanie_bazy_danych()
        
        # Otwarcie głównej strony aplikacji.
        self.strona_glowna()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Dodanie 10 incydentów do Admina.
        self.dodanie_incydentow()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
    
    def test_icm_5_zmiana_statusu_incydentu(self):
        """
            Test 5. Zmiana stsusu istniejącego incydentu, od nowego do zamkniętego.
        """
        print u"---TEST 5. ZMIANA STATUSU INCYDENTU---"
        
        # Poszukiwanie pliku "incidents_ZAMKNIETY.csv".
        self.plik_incidents_ZAMKNIETY_usun()
        
        # Ustawienie dostępu do bazy danych.
        self.dostep_do_bazy_danych()
        
        # Zresetowanie bazy danych.
        self.zresetowanie_bazy_danych()
        
        # Otwarcie głównej strony aplikacji.
        self.strona_glowna()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Zmiana statusu istniejącego incydentu na "Zgłoszony".
        self.dodanie_statusu_zgloszony()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
        # Zalogowanie pracownika.
        self.logowanie_pracownika()
        
        # Zmiana statusu istniejącego incydentu na "Niepotwierdzony".
        self.dodanie_statusu_niepotwierdzony()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Zmiana statusu istniejącego incydentu na "Zamknięty".
        self.dodanie_statusu_niepotwierdzony_zamkniety()
        
        # Weryfikacja zamknięcia istniejącego incydentu w aplikacji.
        self.weryfikacja_statusu_zamkniety_w_aplikacji()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
        # Zresetowanie bazy danych.
        self.zresetowanie_bazy_danych()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Zmiana statusu istniejącego incydentu na "Zgłoszony".
        self.dodanie_statusu_zgloszony()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
        # Zalogowanie pracownika.
        self.logowanie_pracownika()
        
        # Zmiana statusu istniejącego incydentu na "Potwierdzony".
        self.dodanie_statusu_potwierdzony()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
        # Zalogowanie pracownika.
        self.logowanie_pracownika()
        
        # Zmiana statusu istniejącego incydentu na "Rozwiązany".
        self.dodanie_statusu_rozwiazany()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
        
        # Zalogowanie Admina.
        self.logowanie_admina()
        
        # Zmiana statusu istniejącego incydentu "Zamknięty".
        self.dodanie_statusu_zamkniety()
        
        # Weryfikacja zamknięcia istniejącego incydentu w aplikacji.
        self.weryfikacja_statusu_zamkniety_w_aplikacji()
        
        # Weryfikacja zamknięcia istniejącego incydentu w bazie danych.
        self.weryfikacja_statusu_zamkniety_w_bazie_danych()
        
        # Eksport pliku "incidents.csv".
        self.eksport_incydentow()
        
        # Weryfikacja zawartości pliku "incidents.csv".
        self.weryfikacja_zawartosci_incydentow()
        
        # Zmiana nazwy pliku z "incidents.csv" na "incidents_ZAMKNIETY.csv".
        self.zmiana_nazwy_pliku_incidents_ZAMKNIETY()
        
        # Wylogowanie z aplikacji.
        self.wylogowanie()
    
    #______________________Zestaw funkcji wykorzystywanych przez pięć suit testowych.______________________
    #______________________Funkcje są posortowane alfabetycznie w kolejności od A do Z_____________________
    
    def dodanie_audytu(self):
        """
            Dodanie audytu z pliku "audyt.csv" do istniejącego incydentu.
        """
        print u"Dodanie audytu do istniejącego incydentu"
        plik_odczyt = io.open(self.sciezka_pliku_audyt, "r", encoding = "utf-8")
        self.linia = plik_odczyt.readline()
        plik_odczyt.close()
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("assigneeId")).select_by_visible_text("icm-employee")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys(self.linia)
        driver.find_element_by_id("create").click()
        try: self.assertEqual(u"Nowy audyt o id 4 został pomyślnie utworzony!", driver.find_element_by_id("alert").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
    
    def dodanie_incydentow(self):
        """
            Dodanie 10 incydentów z pliku "incydenty.csv" do Admina.
        """
        print u"Dodanie 10 incydentów do Admina"
        driver = self.driver
        driver.get(self.base_url + "/")
        plik_odczyt = io.open(self.sciezka_pliku_incydenty, "r", encoding = "utf-8")
        for linia in plik_odczyt:
            self.linia_podzielona = linia.split(";")
            self.utworz_incydent()
        plik_odczyt.close()
    
    def dodanie_incydentu(self):
        """
            Dodanie jednego incydentu z pliku "incydent.csv" do Admina.
        """
        print "Dodanie jednego incydentu do Admina"
        plik_odczyt = io.open(self.sciezka_pliku_incydent, "r", encoding = "utf-8")
        linia = plik_odczyt.readline()
        self.linia_podzielona = linia.split(";")
        plik_odczyt.close()
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"Utwórz incydent").click()
        self.assertEqual(u"Utwórz incydent", driver.find_element_by_css_selector("legend").text)
        driver.find_element_by_id("type").clear()
        driver.find_element_by_id("type").send_keys(self.linia_podzielona[0])
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys(self.linia_podzielona[1])
        driver.find_element_by_id("addressLine").clear()
        driver.find_element_by_id("addressLine").send_keys(self.linia_podzielona[2])
        driver.find_element_by_id("cityLine").clear()
        driver.find_element_by_id("cityLine").send_keys(self.linia_podzielona[3])
        driver.find_element_by_id("create").click()
        # Weryfikacja utworzenia incydentu o ID 4, a nie ID dowolnym, ze względu na zresetowanie bazy do stanu początkowego.
        try: self.assertEqual(u"Nowy incydent o id 4 został pomyślnie utworzony!", driver.find_element_by_id("alert").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def dodanie_pliku_rozszczelnione_okno(self):
        """
            Dodanie pliku "rozszczelnione_okno.jpg" do istniejącego audytu.
        """
        print u"Dodanie pliku do istniejącego audytu"
        driver = self.driver
        driver.get(self.base_url + "/")
        # Dodanie pliku do incydentu o ID = 1.
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text(u"Szczegóły").click()
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//tr[3]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Nie znaleziono rekordów", driver.find_element_by_xpath("//div[2]/table/tbody/tr/td/p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        #driver.find_element_by_id("file").click() # Nie potrzeba otwierać tego okienka.
        driver.find_element_by_id("file").send_keys(self.sciezka_pliku_rozszczelnione_okno)
        driver.find_element_by_css_selector("td > form > button.btn.btn-default").click()
        # Zweryfikowanie że dodanie pliku było "niepuste".
        try: self.assertNotRegexpMatches(driver.find_element_by_xpath("//body/div/div").text, r"^exact:× [\s\S][\s\S]file\.empty_pl[\s\S][\s\S]$")
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("File rozszczelnione_okno.jpg uploaded successfully", driver.find_element_by_id("alert").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("image/jpeg", driver.find_element_by_xpath("//div[2]/table/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def dodanie_statusu_niepotwierdzony(self):
        """
            Zmiana statusu istniejącego incydentu ze "Zgłoszony" na "Niepotwierdzony".
        """
        print u'Zmiana statusu incydentu na "Niepotwierdzony"'
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Zmiana statusu incydentu "Zgłoszony" na "Niepotwierdzony".
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("newStatus")).select_by_visible_text("Niepotwierdzony")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("Zmiana statusu incydentu na \"Niepotwierdzony\".")
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy audyt o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual("Niepotwierdzony", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-employee", driver.find_element_by_xpath("//tr[8]/td/address/strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"\"Zgłoszony\" na \"Niepotwierdzony\"", driver.find_element_by_xpath("//tr[2]/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Opis')])[2]").click()
        for i in range(60):
            try:
                if "Zmiana statusu incydentu na \"Niepotwierdzony\"." == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Zmiana statusu incydentu na \"Niepotwierdzony\".", driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def dodanie_statusu_niepotwierdzony_zamkniety(self):
        """
            Zmiana statusu istniejącego incydentu z "Niepotwierdzony" na "Zamknięty".
        """
        print u'Zmiana statusu incydentu na "Zamknięty"'
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Zmiana statusu incydentu "Niepotwierdzony" na "Zamknięty".
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("newStatus")).select_by_visible_text(u"Zamknięty")
        Select(driver.find_element_by_id("assigneeId")).select_by_visible_text("icm-employee")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys(u"Zmiana statusu incydentu na \"Zamknięty\".")
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy audyt o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual(u"Zamknięty", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-employee", driver.find_element_by_xpath("//tr[8]/td/address/strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"\"Niepotwierdzony\" na \"Zamknięty\"", driver.find_element_by_xpath("//tr[3]/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Opis')])[3]").click()
        for i in range(60):
            try:
                if u"Zmiana statusu incydentu na \"Zamknięty\"." == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual(u"Zmiana statusu incydentu na \"Zamknięty\".", driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def dodanie_statusu_potwierdzony(self):
        """
            Zmiana statusu istniejącego incydentu ze "Zgłoszony" na "Potwierdzony".
        """
        print u'Zmiana statusu incydentu na "Potwierdzony"'
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Zmiana statusu incydentu "Zgłoszony" na "Potwierdzony".
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("newStatus")).select_by_visible_text("Potwierdzony")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("Zmiana statusu incydentu na \"Potwierdzony\".")
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy audyt o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual("Potwierdzony", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-employee", driver.find_element_by_xpath("//tr[8]/td/address/strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"\"Zgłoszony\" na \"Potwierdzony\"", driver.find_element_by_xpath("//tr[2]/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Opis')])[2]").click()
        for i in range(60):
            try:
                if "Zmiana statusu incydentu na \"Potwierdzony\"." == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Zmiana statusu incydentu na \"Potwierdzony\".", driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def dodanie_statusu_rozwiazany(self):
        """
            Zmiana statusu istniejącego incydentu z "Potwierdzony" na "Rozwiązany".
        """
        print u'Zmiana statusu incydentu na "Rozwiązany"'
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Zmiana statusu incydentu "Zgłoszony" na "Rozwiązany".
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("newStatus")).select_by_visible_text(u"Rozwiązany")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys(u"Zmiana statusu incydentu na \"Rozwiązany\".")
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy audyt o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual(u"Rozwiązany", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-employee", driver.find_element_by_xpath("//tr[8]/td/address/strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"\"Potwierdzony\" na \"Rozwiązany\"", driver.find_element_by_xpath("//tr[3]/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Opis')])[3]").click()
        for i in range(60):
            try:
                if u"Zmiana statusu incydentu na \"Rozwiązany\"." == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual(u"Zmiana statusu incydentu na \"Rozwiązany\".", driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def dodanie_statusu_zamkniety(self):
        """
            Zmiana statusu istniejącego incydentu z "Rozwiązany" na "Zamknięty".
        """
        print u'Zmiana statusu incydentu na "Zamknięty"'
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Zmiana statusu incydentu "Rozwiązany" na "Zamknięty".
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("newStatus")).select_by_visible_text(u"Zamknięty")
        Select(driver.find_element_by_id("assigneeId")).select_by_visible_text("icm-employee")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys(u"Zmiana statusu incydentu na \"Zamknięty\".")
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy audyt o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual(u"Zamknięty", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-employee", driver.find_element_by_xpath("//tr[8]/td/address/strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"\"Rozwiązany\" na \"Zamknięty\"", driver.find_element_by_xpath("//tr[4]/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//a[contains(text(),'Opis')])[4]").click()
        for i in range(60):
            try:
                if u"Zmiana statusu incydentu na \"Zamknięty\"." == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual(u"Zmiana statusu incydentu na \"Zamknięty\".", driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def dodanie_statusu_zgloszony(self):
        """
            Dodanie audytu do istniejącego incydentu, przypisanie do pracownika, i zmiana statusu na "Zgłoszony".
        """
        print u'Zmiana statusu incydentu na "Zgłoszony"'
        driver = self.driver
        driver.get(self.base_url + "/")
        # Incydent o ID = 1
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Zmiana statusu incydentu "Rozszczelnione okno" na "Zgłoszony".
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text("Dodaj audyt").click()
        self.assertEqual("Dodaj audyt", driver.find_element_by_css_selector("legend").text)
        Select(driver.find_element_by_id("assigneeId")).select_by_visible_text("icm-employee")
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys("Dodanie audytu i przypisanie incydentu do pracownika icm-employee.")
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy audyt o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual(u"Zgłoszony", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-employee", driver.find_element_by_xpath("//tr[8]/td/address/strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"\"Zgłoszony\" na \"Zgłoszony\"", driver.find_element_by_xpath("//td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Opis").click()
        for i in range(60):
            try:
                if "Dodanie audytu i przypisanie incydentu do pracownika icm-employee." == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Dodanie audytu i przypisanie incydentu do pracownika icm-employee.", driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def dostep_do_bazy_danych(self):
        """
            Ustawienie dostępu do bazy danych.
        """
        print u"Ustawienie dostępu do bazy danych"
        self.database_url = os.getcwd() + "\..\..\icm.db"
        self.conn = sqlite3.connect(self.database_url)
    
    def download_pliku_rozszczelnione_okno(self):
        """
            Download pliku "rozszczelnione_okno.jpg_" z istniejącego audytu.
        """
        print u"Download pliku z istniejącego audytu"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Incydenty").click()
        self.assertEqual("Incydenty", driver.find_element_by_css_selector("h2").text)
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text(u"Szczegóły").click()
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        # Weryfikacja czy ściągnięcie pliku dotyczy incydentu "Rozszczelnione okno".
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//tr[3]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("rozszczelnione_okno.jpg").click()
        # Odczekanie 2 sekundy na zakończenie ściągania pliku.
        time.sleep(2)
    
    def eksport_incydentow(self):
        """
            Eksport pliku "incidents.csv".
        """
        print "Eksport pliku z incydentami"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text("Dashboard").click()
        self.assertEqual("Dashboard", driver.find_element_by_css_selector("h2").text)
        driver.find_element_by_id("export-incidents-csv").click()
        # Odczekanie 2 sekundy na zakończenie ściągania pliku.
        time.sleep(2)
    
    def logowanie_admina(self):
        """
            Zalogowanie Admina.
        """
        print "Zalogowanie Admina"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"Zaloguj się").click()
        self.assertEqual(u"Zaloguj się", driver.find_element_by_css_selector("legend").text)
        driver.find_element_by_id("inputEmail").clear()
        driver.find_element_by_id("inputEmail").send_keys("icm-admin@icm.com")
        driver.find_element_by_id("inputPassword").clear()
        driver.find_element_by_id("inputPassword").send_keys("!1")
        driver.find_element_by_id("signin").click()
        self.assertEqual("Incydenty", driver.find_element_by_css_selector("h2").text)
    
    def logowanie_pracownika(self):
        """
            Zalogowanie pracownika.
        """
        print "Zalogowanie pracownika"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"Zaloguj się").click()
        self.assertEqual(u"Zaloguj się", driver.find_element_by_css_selector("legend").text)
        # Zalogowanie pracownika w celu obsłużenia incydentu.
        driver.find_element_by_id("inputEmail").clear()
        driver.find_element_by_id("inputEmail").send_keys("icm-employee@icm.com")
        driver.find_element_by_id("inputPassword").clear()
        driver.find_element_by_id("inputPassword").send_keys("!1")
        driver.find_element_by_id("signin").click()
        self.assertEqual("Incydenty", driver.find_element_by_css_selector("h2").text)
    
    def plik_audyt(self):
        """
            Poszukiwanie pliku "audyt.csv".
        """
        print 'Poszukiwanie pliku "audyt.csv"'
        self.sciezka_pliku_audyt = os.getcwd() + "\\audyt.csv"
        if not os.path.isfile(self.sciezka_pliku_audyt):
            print "Brak pliku {0} z opisem audytu. Przerwano wykonanie testu".format(self.sciezka_pliku_audyt)
            self.driver.quit()
            sys.exit()
    
    def plik_incidents_JEDEN_usun(self):
        """
            Poszukiwanie pliku "incidents_JEDEN.csv". Jeżeli plik istnieje - usunięcie go.
            Zabezpieczenie na wypadek testów regresji.
        """
        print 'Poszukiwanie pliku "incidents_JEDEN.csv"'
        self.sciezka_pliku_incidents_JEDEN = os.getcwd() + "\\incidents_JEDEN.csv"
        if os.path.isfile(self.sciezka_pliku_incidents_JEDEN):
            os.remove(self.sciezka_pliku_incidents_JEDEN)
    
    def plik_incidents_ZAMKNIETY_usun(self):
        """
            Poszukiwanie pliku "incidents_ZAMKNIETY.csv". Jeżeli plik istnieje - usunięcie go.
            Zabezpieczenie na wypadek testów regresji.
        """
        print 'Poszukiwanie pliku "incidents_ZAMKNIETY.csv"'
        self.sciezka_pliku_incidents_ZAMKNIETY = os.getcwd() + "\\incidents_ZAMKNIETY.csv"
        if os.path.isfile(self.sciezka_pliku_incidents_ZAMKNIETY):
            os.remove(self.sciezka_pliku_incidents_ZAMKNIETY)
    
    def plik_incydent(self):
        """
            Poszukiwanie pliku "incydent.csv".
        """
        print 'Poszukiwanie pliku "incydent.csv"'
        self.sciezka_pliku_incydent = os.getcwd() + "\\incydent.csv"
        if not os.path.isfile(self.sciezka_pliku_incydent):
            print "Brak pliku {0} z opisem incydentu. Przerwano wykonanie testu".format(self.sciezka_pliku_incydent)
            self.driver.quit()
            sys.exit()
    
    def plik_incydenty(self):
        """
            Poszukiwanie pliku "incydenty.csv".
        """
        print 'Poszukiwanie pliku "incydenty.csv"'
        self.sciezka_pliku_incydenty = os.getcwd() + "\\incydenty.csv"
        if not os.path.isfile(self.sciezka_pliku_incydenty):
            print u"Brak pliku {0} z opisem incydentów. Przerwano wykonanie testu".format(self.sciezka_pliku_incydenty)
            self.driver.quit()
            sys.exit()
    
    def plik_rozszczelnione_okno(self):
        """
            Poszukiwanie pliku "rozszczelnione_okno.jpg".
        """
        print 'Poszukiwanie pliku "rozszczelnione_okno.jpg"'
        self.sciezka_pliku_rozszczelnione_okno = os.getcwd() + "\\rozszczelnione_okno.jpg"
        if not os.path.isfile(self.sciezka_pliku_rozszczelnione_okno):
            print "Brak pliku {0} z opisem audytu. Przerwano wykonanie testu".format(self.sciezka_pliku_rozszczelnione_okno)
            self.driver.quit()
            sys.exit()
    
    def plik_rozszczelnione_okno_DOWNLOADED_usun(self):
        """
            Poszukiwanie pliku "rozszczelnione_okno_DOWNLOADED.jpg". Jeżeli plik istnieje - usunięcie go.
            Zabezpieczenie na wypadek testów regresji.
        """
        print 'Poszukiwanie pliku "rozszczelnione_okno_DOWNLOADED.jpg"'
        self.sciezka_pliku_okno_DOWNLOADED = os.getcwd() + "\\rozszczelnione_okno_DOWNLOADED.jpg"
        if os.path.isfile(self.sciezka_pliku_okno_DOWNLOADED):
            os.remove(self.sciezka_pliku_okno_DOWNLOADED)
    
    def strona_glowna(self):
        """
            Otwarcie głównej strony aplikacji.
        """
        print u"Otwarcie głównej strony aplikacji"
        driver = self.driver
        driver.get(self.base_url + "/")
        self.assertEqual(u"Zarządzanie incydentami", driver.find_element_by_css_selector("h1").text)
    
    def utworz_incydent(self):
        """
            Utworzenie kolejnego incydentu (n-tego z 10-ciu).
        """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_link_text(u"Utwórz incydent").click()
        self.assertEqual(u"Utwórz incydent", driver.find_element_by_css_selector("legend").text)
        driver.find_element_by_id("type").clear()
        driver.find_element_by_id("type").send_keys(self.linia_podzielona[1])
        driver.find_element_by_id("description").clear()
        driver.find_element_by_id("description").send_keys(self.linia_podzielona[2])
        driver.find_element_by_id("addressLine").clear()
        driver.find_element_by_id("addressLine").send_keys(self.linia_podzielona[3])
        driver.find_element_by_id("cityLine").clear()
        driver.find_element_by_id("cityLine").send_keys(self.linia_podzielona[4])
        driver.find_element_by_id("create").click()
        try: self.assertRegexpMatches(driver.find_element_by_id("alert").text, r"Nowy incydent o id [0-9]+")
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def weryfikacja_audytu_w_aplikacji(self):
        """
            Weryfikacja dodania audytu w aplikacji.
        """
        print u"Weryfikacja dodania audytu w aplikacji"
        driver = self.driver
        driver.get(self.base_url + "/")
        # Potwierdzenie dodania audytu
        driver.find_element_by_link_text("Incydenty").click()
        self.assertEqual("Incydenty", driver.find_element_by_css_selector("h2").text)
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[5]/div/button").click()
        driver.find_element_by_link_text(u"Szczegóły").click()
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        # Weryfikacja czy jest to incydent o ID = 1
        try: self.assertEqual("1", driver.find_element_by_css_selector("td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_link_text("Opis").click()
        for i in range(60):
            try:
                if self.linia == driver.find_element_by_css_selector("p.content").text: break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual(self.linia, driver.find_element_by_css_selector("p.content").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_css_selector("div.modal-footer > button.btn.btn-default").click()
    
    def weryfikacja_audytu_w_bazie_danych(self):
        """
            Weryfikacja dodania audytu w bazie danych.
        """
        print "Weryfikacja dodania audytu w bazie danych"
        conn = self.conn
        cursor = conn.cursor()
        # Zapytanie do bazy danych, o ID incydentu i opis dodanego audytu.
        result = cursor.execute("SELECT incident_id, description FROM audit WHERE incident_id = ? AND description = ?", (1, self.linia))
        # Pobranie i zweryfikowanie rezultatu.
        row = result.fetchone()
        self.assertEquals(1, row[0])
        self.assertEquals(self.linia, row[1])
    
    def weryfikacja_incydentu_w_aplikacji(self):
        """
            Weryfikacja dodania incydentu do aplikacji.
        """
        print "Weryfikacja dodania incydentu do aplikacji"
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr[4]/td[5]/div/button").click()
        driver.find_element_by_css_selector("div.btn-group.open > ul.dropdown-menu > li > a").click()
        self.assertEqual(u"Szczegóły", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual(self.linia_podzielona[0], driver.find_element_by_xpath("//tr[3]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        try: self.assertEqual(self.linia_podzielona[1], driver.find_element_by_xpath("//td/div").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(u"Zgłoszony", driver.find_element_by_xpath("//tr[5]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(self.linia_podzielona[2], driver.find_element_by_css_selector("address > span").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual(self.linia_podzielona[2], driver.find_element_by_xpath("//address/span[2]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.assertEqual("icm-admin", driver.find_element_by_css_selector("strong").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Weryfikacja braku przypisania incydentu.
        try: self.assertEqual("", driver.find_element_by_xpath("//tr[8]/td").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Weryfikacja braku audytu.
        try: self.assertEqual(u"Nie znaleziono rekordów", driver.find_element_by_css_selector("p.text-muted").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Weryfikacja braku dodanych plików.
        try: self.assertEqual(u"Nie znaleziono rekordów", driver.find_element_by_xpath("//div[2]/table/tbody/tr/td/p").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def weryfikacja_incydentu_w_bazie_danych(self):
        """
            Weryfikacja incydentu w bazie danych.
        """
        print "Weryfikacja incydentu w bazie danych"
        conn = self.conn
        cursor = conn.cursor()
        # Zapytanie do bazy danych, o typ i opis dodanego incydentu.
        result = cursor.execute("SELECT incident_type, description FROM incident WHERE incident_type = ? AND description = ?", (self.linia_podzielona[0], self.linia_podzielona[1]))
        # Pobranie i zweryfikowanie rezultatu.
        row = result.fetchone()
        self.assertEquals(self.linia_podzielona[0], row[0])
        self.assertEquals(self.linia_podzielona[1], row[1])
        # Zapytanie do bazy danych, o adres dodanego incydentu.
        # Tutaj trzeba sztucznie obejść błąd aplikacji ICM, polegający na niemożności dodania kodu pocztowego oraz nazwy miasta.
        result = cursor.execute("SELECT address_line, city_line FROM address WHERE address_line = ? AND city_line = ?", (self.linia_podzielona[2], self.linia_podzielona[2]))
        # Pobranie i zweryfikowanie rezultatu.
        row = result.fetchone()
        self.assertEquals(self.linia_podzielona[2], row[0])
        self.assertEquals(self.linia_podzielona[2], row[1])
    
    def weryfikacja_statusu_zamkniety_w_aplikacji(self):
        """
            Weryfikacja zamknięcia istniejącego incydentu w aplikacji.
        """
        print u"Weryfikacja zamknięcia istniejącego incydentu w aplikacji"
        driver = self.driver
        driver.get(self.base_url + "/")
        # Weryfikacja statusu incydentu "Rozszczelnione okno".
        driver.find_element_by_link_text("Incydenty").click()
        self.assertEqual("Incydenty", driver.find_element_by_css_selector("h2").text)
        try: self.assertEqual("Rozszczelnione okno", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[3]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        # Filtrowanie listy incydentów.
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
        driver.find_element_by_link_text(u"Zamknięty").click()
        # Na odfiltrowanej liście jest tylko jeden incydent o statusie "Zamknięty".
        self.assertEqual(1, len(driver.find_elements_by_xpath("//table/tbody/tr")))
        try: self.assertEqual(u"Zamknięty", driver.find_element_by_xpath("//table[@id='incidents']/tbody/tr/td[4]").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def weryfikacja_statusu_zamkniety_w_bazie_danych(self):
        """
            Weryfikacja zamknięcia istniejącego incydentu w bazie danych.
        """
        print u"Weryfikacja zamknięcia istniejącego incydentu w bazie danych"
        conn = self.conn
        cursor = conn.cursor()
        # Zapytanie do bazy danych, o typ i status istniejącego, zamkniętego incydentu.
        result = cursor.execute("SELECT incident_type, status FROM incident WHERE incident_type = ? AND status = ?", ("Rozszczelnione okno", "4"))
        # Pobranie i zweryfikowanie rezultatu.
        row = result.fetchone()
        self.assertEquals("Rozszczelnione okno", row[0])
        self.assertEquals(4, row[1])
    
    def weryfikacja_zawartosci_incydentow(self):
        """
            Weryfikacja zawartości pliku "incidents.csv".
        """
        print u"Weryfikacja zawartości pliku z incydentami"
        self.sciezka_pliku_incidents = os.getcwd() + "\\incidents.csv"
        if not os.path.isfile(self.sciezka_pliku_incidents):
            print u"Brak wyeksportowanego pliku z incydentami"
        else:
            plik_odczyt = io.open(self.sciezka_pliku_incidents, "r", encoding = "utf-8")
            linia = plik_odczyt.read()
            if len(linia) == 0:
                print "Plik z incydentami jest pusty"
            elif u"Mój incydent" or "CLOSED" in linia:
                pass # Na razie nie potrafię zrobić porządnego sprawdzenia zawartości pliku, jedynie na pojedyncze wyrazy.
            else:
                print u"Nieprawidłowe dane w wyeksportowanym pliku z incydentami"
            plik_odczyt.close()
    
    def wylogowanie(self):
        """
            Wylogowanie z aplikacji.
        """
        print "Wylogowanie z aplikacji"
        driver = self.driver
        driver.find_element_by_link_text("Logout").click()
        self.assertEqual(u"Zarządzanie incydentami", driver.find_element_by_css_selector("h1").text)
    
    def zmiana_nazwy_pliku_incidents(self):
        """
            Zmiana nazwy pliku z "incidents.csv" na "incidents_JEDEN.csv".
        """
        print "Zmiana nazwy pliku"
        self.sciezka_pliku_incidents = os.getcwd() + "\\incidents.csv"
        if not os.path.isfile(self.sciezka_pliku_incidents):
            print u"Brak ściągniętego pliku z incydentami. Nie jest możliwa zmiana nazwy pliku."
        else:
            os.rename(os.getcwd() + "\\incidents.csv", os.getcwd() + "\\incidents_JEDEN.csv")
    
    def zmiana_nazwy_pliku_incidents_ZAMKNIETY(self):
        """
            Zmiana nazwy pliku z "incidents.csv" na "incidents_ZAMKNIETY.csv".
        """
        print "Zmiana nazwy pliku"
        self.sciezka_pliku_incidents = os.getcwd() + "\\incidents.csv"
        if not os.path.isfile(self.sciezka_pliku_incidents):
            print u"Brak ściągniętego pliku z incydentami. Nie jest możliwa zmiana nazwy pliku."
        else:
            os.rename(os.getcwd() + "\\incidents.csv", os.getcwd() + "\\incidents_ZAMKNIETY.csv")
    
    def zmiana_nazwy_pliku_rozszczelnione_okno(self):
        """
            Zmiana nazwy pliku z "rozszczelnione_okno.jpg_" na "rozszczelnione_okno_DOWNLOADED.jpg".
        """
        print "Zmiana nazwy pliku"
        self.sciezka_pliku_okno = os.getcwd() + "\\rozszczelnione_okno.jpg_"
        if not os.path.isfile(self.sciezka_pliku_okno):
            print u"Brak ściągniętego pliku z audytu. Nie jest możliwa zmiana nazwy pliku."
        else:
            os.rename(os.getcwd() + "\\rozszczelnione_okno.jpg_", os.getcwd() + "\\rozszczelnione_okno_DOWNLOADED.jpg")
    
    def zresetowanie_bazy_danych(self):
        """
            Zresetowanie bazy danych.
        """
        print "Zresetowanie bazy danych"
        driver = self.driver
        driver.get(self.base_url + "/setup?action=do")
    
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
