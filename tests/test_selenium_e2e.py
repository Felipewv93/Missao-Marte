import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    try:
        browser = webdriver.Chrome(options=options)
    except WebDriverException as error:
        pytest.fail(f"Chrome não disponível para o teste E2E: {error}")
    yield browser
    browser.quit()


def test_solicitacao_de_oxigenio_atualiza_painel(driver, painel_path):
    driver.get(painel_path.as_uri())
    try:
        antes = driver.find_element(By.ID, "nivel-oxigenio").text
        driver.find_element(By.ID, "quantidade").send_keys("125")
        driver.find_element(By.ID, "form-cota").submit()
        WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, "nivel-oxigenio"), "1125.00"))
        assert antes == "1000.00 kg"
        assert driver.find_element(By.ID, "mensagem").text.startswith("Cota")
    except (AssertionError, TimeoutException):
        driver.save_screenshot("evidencia-falha-painel.png")
        raise
