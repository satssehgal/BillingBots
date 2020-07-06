from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from secrets import username, password, cc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

class Rogers:
	def __init__(self, username, password, cc):
		timeout=60
		self.username=username
		self.password=password
		self.cc=cc
		self.driver = webdriver.Firefox(executable_path='/Users/ss/Downloads/geckodriver')
		#self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.driver.get("http://www.rogers.com")
		time.sleep(3)
		self.driver.find_element_by_xpath('/html/body/browse-root/rci-main/rci-header/section/dsa-header/header[1]/div[1]/div[2]/div[2]/ul/li[4]/a/span[2]').click()
		WebDriverWait(self.driver, timeout).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/browse-root/rci-main/div/iframe")))
		WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="username"]'))).send_keys(username)
		WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]'))).send_keys(password)
		self.driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div[1]/form/div[5]/button').click()

	def getBalance(self):
		self.driver.switch_to.default_content()
		dollars=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/rci-main/main/rss-overview/div/section/rss-account-detail/div/section/rss-billing-widget/ds-tile/div/div/rss-account-balance/div/div/div/ds-price/div/div/div[2]')))
		cents=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/rci-main/main/rss-overview/div/section/rss-account-detail/div/section/rss-billing-widget/ds-tile/div/div/rss-account-balance/div/div/div/ds-price/div/div/div[3]/span')))
		print('Your Balance is: ${}{}'.format(dollars.text, cents.text))
		return str(dollars.text),str(cents.text)

	def checkPaymentRequired(self):
		dollars,cents=self.getBalance()
		time.sleep(1)
		balance=float(dollars+cents)
		if balance>0:
			self.makePayment()
		else:
			print('Balance is still 0')

	def makePayment(self):
		print('Begin payment flow')

def main():
	R=Rogers(username,password, cc)
	R.getBalance()
	#R.checkPaymentRequired()

if __name__ == "__main__":
	main()