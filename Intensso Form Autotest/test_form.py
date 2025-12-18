from faker import Faker
from formclasses import BrowserStarter, TestFunctions, RandomDataGenerator, RandomDataGeneratorWithErrors
import time
from loguru import logger

logger.add("test_form.log", format="{time} {level} {message}")

fake = Faker()
fake = Faker(["ru_RU"])

def positive_main():
    try:
        logger.info("""
                    =================================================
                    ======== Начало позитивного тестирования ========
                    =================================================
                    """)
        browser_manager = BrowserStarter()
        logger.info("Присаивание класса BrowserStarter переменной browser_manager")
        rdg = RandomDataGenerator()
        logger.info("Присаивание класса RandomDataGenerator переменной rdg")
        driver = browser_manager.setup_browser()
        logger.info("Инициализация Webdriver..")
        website = TestFunctions(driver)
        logger.info("Присваивание класса TestFunctions с аргументом driver переменной website")
        
        random_data = rdg.generate_random_data()
        logger.info("Формирование рандомных данных")
        
        website.open_website()
        logger.info("Выполнено открытие веб-сайта")
        website.go_to_booking()
        logger.info("Совершен переход на страницу броинрования")
        website.bring_the_form(random_data)
        logger.info("Произведено заполнение формы")
        website.select_dropdowns()
        logger.info("Выполнен выбор элементов выпадающих списков формы")
        website.click_checkbox()
        logger.info("Активирован чекбокс: соглашение на рассылку")
        website.get_booking()
        logger.info("Произведена отправка формы")
        booking_id = website.get_booking_id()
        logger.success(f"Тест завершен без ошибок, Booking ID: {booking_id}")
        driver.quit()  
    except:
        logger.exception("Произошла ошибка, тест провален!")
        driver.quit()  
def negative_main():
    """Запуск негативного тестирования 5 раз с разными паттернами данных"""
    
    # Определяем порядок тестирования вариаций
    test_variations = [1, 2, 3, 4, 5]  # 5 разных тестовых наборов
    
    for i, variation in enumerate(test_variations, 1):
        logger.info(f"""
                    ===========================================
                    НЕГАТИВНЫЙ ТЕСТ #{i} (Вариация {variation})
                    ===========================================
                    """)
        
        driver = None
        try:
            browser_manager = BrowserStarter()
            logger.info(f"Инициализация BrowserStarter для теста #{i}")
            rdg = RandomDataGeneratorWithErrors()
            logger.info(f"Инициализация RandomDataGeneratorWithErrors для теста #{i}")
            driver = browser_manager.setup_browser()
            logger.info(f"Запуск браузера для теста #{i}")
            website = TestFunctions(driver)
            logger.info(f"Инициализация TestFunctions для теста #{i}")
            
            random_data = rdg.generate_random_data(variation)
            logger.info(f"Сгенерированы данные вариации {variation}:")
            for key, value in random_data.items():
                logger.debug(f"  {key}: {value}")
            
            steps = [
                ("Открытие сайта", website.open_website),
                ("Переход к бронированию", website.go_to_booking),
                ("Заполнение формы", lambda: website.bring_the_form(random_data)),
                ("Выбор элементов выпадающих списков", website.select_dropdowns),
                ("Активация чекбокса", website.click_checkbox),
                ("Отправка формы", website.get_booking)
            ]
            
            for step_name, step_func in steps:
                logger.info(f"Тест #{i}: {step_name}")
                try:
                    step_func()
                except Exception as e:
                    logger.warning(f"Тест #{i}: Ошибка на шаге '{step_name}': {str(e)}")

            try:
                booking_id = website.get_booking_id()
                if booking_id:
                    logger.error(f"ТЕСТ #{i} ПРОВАЛЕН! Форма приняла некорректные данные.")
                    logger.error(f"Booking ID: {booking_id}")
                else:
                    logger.info(f"Тест #{i}: Booking ID не получен (ожидаемое поведение)")
            except Exception as e:
                logger.info(f"Тест #{i}: Ошибка при получении Booking ID: {e} (ожидаемое поведение)")
            
            logger.info(f"Тест #{i} завершен")
            
        except Exception as e:
            logger.error(f"КРИТИЧЕСКАЯ ОШИБКА в тесте #{i}: {str(e)}")
            logger.exception("Детали ошибки:")
            
        finally:

            try:
                if driver:
                    driver.quit()
                    logger.info(f"Браузер теста #{i} закрыт")
            except Exception as e:
                logger.error(f"Ошибка при закрытии браузера теста #{i}: {e}")
    
    logger.info(f"""
                {'='*60}
                НЕГАТИВНОЕ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО
                Всего выполнено тестов: {len(test_variations)}
                {'='*60}
                """)
positive_main()
negative_main()
    