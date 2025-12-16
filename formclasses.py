import datetime
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from loguru import logger

fake = Faker()
fake = Faker(["ru_RU"])

class BrowserStarter:
    def setup_browser(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        return driver

class RandomDataGenerator:
    def __init__(self):
        self.fake = fake
    
    def generate_random_data(self):   
        return {
            "first_name": self.fake.first_name(),
            "phone": self.fake.numerify(text='+79#########'),
            "email": self.fake.email(),
            "date": "31122025",
            "time": "14:00",
            "special-requests": self.fake.text()
        }
        
class RandomDataGeneratorWithErrors:
    def __init__(self):
        self.fake = fake
    
    def generate_random_data(self, variation):   
        match variation:
            case 1:
                return {
                    #пустые поля
                    "first_name": "",
                    "phone": "",
                    "email": "",
                    "date": "",
                    "time": "",
                    "special-requests": ""
                }
            case 2:
                return {
                    #некорректные символы в полях + sql инъекция
                    "first_name": "1&@&#9",
                    "phone": "abca^^#*&vv",
                    "email": "&(*^%EDJS@)",
                    "date": "01010001",
                    "time": "25:60",
                    "special-requests": "SELECT 'Приветствие' AS Hi"
                }
            case 3:
                return {
                    #относительно некорректные символы в полях
                    "first_name": "?Андрей?",
                    "phone": self.fake.numerify(text='+7##########'),
                    "email": "1@1.ком",
                    "date": "08.02.2026",
                    "time": "14:11",
                    "special-requests": ""
                }
            case 4:
                return {
                    #граничные значения
                    "first_name": "Поле не ограниченооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооооо",
                    "phone": self.fake.numerify(text='+79999999999'),
                    "email": "u@u.com",
                    "date": "16.03.2026",
                    "time": "22:59",
                    "special-requests": ""
                }
            case 5:
                return {
                    #граничные значения 2
                    "first_name": "j",
                    "phone": self.fake.numerify(text='+79999999999'),
                    "email": "uwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww@wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwu.com",
                    "date": "16.06.2025",
                    "time": "12:01",
                    "special-requests": ""
                }
  
class TestFunctions:
    def __init__(self, driver):
        self.driver = driver

    def open_website(self):
        self.driver.get("https://intensso.vercel.app/")
        self.driver.maximize_window()
    
    def go_to_booking(self):
        self.driver.find_element(By.XPATH, "//div/a[2]").click()
        
        
    def bring_the_form(self, random_data):
        fields = [
            ("name", random_data["first_name"]),
            ("phone", random_data["phone"]),
            ("email", random_data["email"]),
            ("date", random_data["date"]),
            ("time", random_data["time"]),
            ("special-requests", random_data["special-requests"])
        ]
        
        for field_name, value in fields:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, field_name))
            )
            element.clear()
            element.send_keys(value)
                
    def select_dropdowns(self):
        self.driver.find_element(By.ID, "guests").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#guests"))
        )

        # Выбираем нужную опцию
        options = self.driver.find_elements(By.CSS_SELECTOR, "#guests > option:nth-child(4)")
        for option in options:
            if option.text == "3 гостя":
                option.click()
                
        self.driver.find_element(By.ID, "table-type").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#table-type"))
        )

        # Выбираем нужную опцию
        options = self.driver.find_elements(By.CSS_SELECTOR, "#guests > option:nth-child(4)")
        for option in options:
            if option.text == "VIP зона":
                option.click()
                
    def click_checkbox(self):
        self.driver.find_element(By.ID, "newsletter").click()
    
    def get_booking(self):
        self.driver.find_element(By.CSS_SELECTOR, "#booking-form > button").click()
    
    def get_booking_id(self):
         b_id = WebDriverWait(self.driver, 10).until(
             EC.presence_of_element_located((By.XPATH, '//*[@id="confirmation-content"]//span[2]'))
        )
         return b_id.text
            