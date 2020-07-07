from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from secrets import buser, bpw, cc, ccm, ccy, csc, fullname
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

class Bell:
    def __init__(self, username, password, cc):
        self.timeout=60
        self.username=username
        self.password=password
        self.cc=cc
        self.fullname=fullname
        self.driver = webdriver.Firefox(executable_path='/Users/ss/Downloads/geckodriver')
        self.driver.get("http://www.bell.ca")
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="rsx-login-register-button"]').click()
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="USER"]'))).send_keys(username)
        WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="PASSWORD"]'))).send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="labelLogin"]').click()
    
    def getBalance(self):
        timeout=self.timeout
        time.sleep(10)
        amt=WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located((By.XPATH,'/html/body/main/div[4]/div[1]/div/div/div[1]/div[2]/div[1]')))
        print('Your Balance is: {}'.format(amt.text))
        return float((amt.text).replace('$',''))
    
    def checkPaymentRequired(self):
        balance=self.getBalance()
        if (balance > 0 and balance <125):
            self.makePayment()
        else:
            print('No Payment Required')
            self.driver.find_element_by_xpath('//*[@id="mybell_gc_FIRST_BELL_LOGOUT"]').click()
            time.sleep(2)
            self.driver.close()
    
    def makePayment(self):
        timeout=self.timeout
        time.sleep(10)
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lnkMobileMakePayment"]'))).click()
        time.sleep(1)
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'/html/body/main/div/div[1]/form/div[2]/div[7]/div[4]/div[1]/div[5]/div/div/div/label/span'))).click()
        time.sleep(1)
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="SelectedCreditCard_CreditCardNumberMasked"]'))).send_keys(cc)
        time.sleep(1)
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="SelectedCreditCard_CardholderName"]'))).send_keys(fullname)
        time.sleep(1)
        mth=Select(WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="SelectedCreditCard_ExpireMonth"]')))).select_by_value(ccm)
        time.sleep(1)
        yr=Select(WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="SelectedCreditCard_ExpireYear"]')))).select_by_value(ccy)
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="SelectedCreditCard_SecurityCodeMasked"]'))).send_keys(csc)
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="btnContinuetoReview"]').click()
        time.sleep(5)
        self.driver.find_element_by_xpath('//*[@id="lnkContinue"]').click()
        print('Bill Paid')
        time.sleep(10)
        self.driver.find_element_by_xpath('//*[@id="logoutCTAHeaderconfirmation"]').click()
        self.driver.close()
        

def main():
    B=Bell(buser,bpw, cc)
    B.checkPaymentRequired()

if __name__ == "__main__":
	main()
