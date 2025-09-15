import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')



class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

    def test_choose_comfort_tariff(self):
        self.routes_page.click_request_taxi()
        self.routes_page.click_comfort_tariff()

    def test_add_telephone(self):
        self.routes_page.click_on_telephone_number()
        self.routes_page.wait_for_emergent_window_phone_number()
        self.routes_page.add_phone_number()
        self.routes_page.click_submit_phone_button()
        self.routes_page.get_sms_code()

    def test_add_payment_method(self):
        self.routes_page.click_payment_method()
        self.routes_page.click_add_card_button()
        self.routes_page.add_card_number()
        self.routes_page.add_card_code()
        self.routes_page.click_to_activate_button()
        self.routes_page.click_submit_card_button()
        self.routes_page.close_payment_window()

    def test_message_to_driver(self):
        self.routes_page.write_message()

    def test_ask_for_blanket_and_tissues(self):
        self.routes_page.click_blanket()

    def test_ask_for_ice_cream(self):
        self.routes_page.click_icecream()

    def test_final_cab_request_a_cab(self):
        self.routes_page.click_request_a_cab()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
