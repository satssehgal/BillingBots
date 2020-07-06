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
		self.username=username
		self.password=password
		self.cc=cc
		self.driver = webdriver.Firefox(executable_path='/Users/ss/Downloads/geckodriver')
		#self.driver = webdriver.Chrome(ChromeDriverManager().install())
	def login(self):
		self.driver.get("http://www.rogers.com")
		time.sleep(5)
		self.driver.find_element_by_xpath('/html/body/browse-root/rci-main/rci-header/section/dsa-header/header[1]/div[1]/div[2]/div[2]/ul/li[4]/a/span[2]').click()
		WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/browse-root/rci-main/div/iframe")))
		user=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="username"]'))).send_keys(username)
		pw=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="password"]'))).send_keys(password)
		self.driver.find_element_by_xpath('/html/body/app-root/div/div/app-login/div[1]/form/div[5]/button').click()
		time.sleep(5)
		self.driver.switch_to.default_content()
		dollars=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/rci-main/main/rss-overview/div/section/rss-account-detail/div/section/rss-billing-widget/ds-tile/div/div/rss-account-balance/div/div/div/ds-price/div/div/div[2]')))
		cents=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/rci-main/main/rss-overview/div/section/rss-account-detail/div/section/rss-billing-widget/ds-tile/div/div/rss-account-balance/div/div/div/ds-price/div/div/div[3]/span')))
		#print('Your Balance is: ${}{}'.format(dollars.text, cents.text))
		return str(dollars.text),str(cents.text)

	def makePayment(self):
		dollars,cents=self.login()
		time.sleep(1)
		balance=float(dollars+cents)
		if (balance ==0 or balance<0):
			WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mainContent"]/rss-overview/div/section/rss-account-detail/div/section/rss-billing-widget/ds-tile/div/div/rss-billing-payment-button/div/button/span'))).click()
			WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[6]/div[1]/section/div[1]/myr-account-balance/div/div[3]/div/button/span'))).click()
			time.sleep(5)
			amount=WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="paymentAmount"]')))
			amount.click()
			amount.send_keys(Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE,Keys.BACK_SPACE)
			time.sleep(1)
			amount.send_keys('33.89')
			time.sleep(5)
			WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[11]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/label'))).click()
			try:
				WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[11]/div[2]/div/div/div[1]/div[3]/div/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/label'))).click()
			except Exception as e:
				print(e)
				pass
			WebDriverWait(self.driver, 30).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="sema"]')))
			cc=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="pan"]')))
			cc.click()
			cc.send_keys(self.cc)
			self.driver.switch_to.default_content()
			mth = Select(WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[11]/div[2]/div/div/div[1]/div[3]/div/div[2]/div/div/div[3]/form/div/ute-credit-card/div/div/div/div[2]/div[4]/div[1]/div[2]/select'))))
			mth.select_by_value('6')
			# yr=WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[11]/div[2]/div/div/div[1]/div[3]/div/div[2]/div/div/div[3]/form/div/ute-credit-card/div/div/div/div[2]/div[4]/div[1]/div[3]/select')))
			# yr.select_by_visible_text('2020')
			# sec=WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="securityCode"]')))
			# sec.click()
			# sec.send_keys('123')
			# time.sleep(5)
			# self.driver.close()
		else:
			print('Balance is $0.00')
			time.sleep(2)
			self.drive.close()
def main():
	R=Rogers(username,password, cc)
	R.makePayment()

if __name__ == "__main__":
	main()