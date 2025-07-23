from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()
driver.get("https://demoqa.com/webtables")
add_btn = driver.find_element(By.XPATH, "//button[@id='addNewRecordButton']")
add_btn.click()
first_name = driver.find_element(By.XPATH, "//input[@id='firstName']")
last_name = driver.find_element(By.XPATH, "//input[@id='lastName']")
email = driver.find_element(By.XPATH, "//input[@id='userEmail']")
age = driver.find_element(By.XPATH, "//input[@id='age']")
salary = driver.find_element(By.XPATH, "//input[@id='salary']")
dept = driver.find_element(By.XPATH, "//input[@id='department']")
submit_btn = driver.find_element(By.XPATH, "//button[@id='submit']")
first_name.send_keys("Sanjuta")
last_name.send_keys("Tidke")
email.send_keys("abc@xyz.com")
age.send_keys("12")
salary.send_keys("12345")
dept.send_keys("IT")
submit_btn.click()
time.sleep(3)
table = driver.find_element(By.CLASS_NAME, "rt-td")
print(table.text)
assert "Sanjuta" in table.text

delete_btn = driver.find_element(By.CSS_SELECTOR, "span['Delete']")
delete_btn[-1].click()
time.sleep(3)
driver.quit()

