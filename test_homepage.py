import os
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Fixture to set up and tear down the WebDriver for each test
@pytest.fixture
def setup():
    """
    Pytest fixture that handles WebDriver setup and cleanup.
    - Initializes Chrome WebDriver with specific configurations
    - Maximizes window and sets up error handling
    - Automatically closes browser after each test
    """
    # Get the absolute path to the chromedriver executable
    chrome_driver_path = os.path.abspath(r'F:\STUDY\projects\selenium-entrata-tests\chromedriver-win64\chromedriver.exe')
    
    # Verify ChromeDriver existence before proceeding
    if not os.path.isfile(chrome_driver_path):
        raise FileNotFoundError(f"ChromeDriver not found at {chrome_driver_path}")
    
    # Configure Chrome options for optimal testing environment
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')        # Start with maximized window
    options.add_argument('--ignore-certificate-errors')  # Ignore SSL errors
    options.add_argument('--disable-popup-blocking')    # Prevent popups from interfering
    driver = webdriver.Chrome(service=service, options=options)
    
    # Set implicit wait for better element detection
    driver.implicitly_wait(10)
    
    # Yield the driver for test use
    yield driver
    # Cleanup after test completion
    driver.quit()

def wait_for_element(driver, by, value, timeout=10):
    """
    Helper function to wait for and find elements with error handling.
    Args:
        driver: WebDriver instance
        by: Selenium By class locator strategy
        value: Locator value
        timeout: Maximum wait time in seconds
    Returns:
        WebElement if found
    Raises:
        pytest.fail if element not found, includes screenshot
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        # Capture failure state with screenshot
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = f'error_screenshot_{timestamp}.png'
        driver.save_screenshot(screenshot_path)
        pytest.fail(f"Element not found: {value}. Screenshot saved as {screenshot_path}")

def test_homepage_title(setup):
    """
    Verify that the homepage loads successfully and has the correct title.
    Tests basic site accessibility and correct page loading.
    """
    driver = setup
    driver.get("https://www.entrata.com")
    assert "Entrata" in driver.title

def test_navigation_menu(setup):
    """
    Verify that main navigation menu items are present and visible.
    Includes cookie consent handling and checks for key navigation elements.
    """
    driver = setup
    driver.get("https://www.entrata.com")
    
    # Handle cookie consent popup if present
    try:
        cookie_accept = driver.find_element(By.ID, "rcc-confirm-button")
        if cookie_accept.is_displayed():
            cookie_accept.click()
    except:
        pass  # Cookie banner might not appear
    
    # Verify presence of main menu items
    menu_items = {
        "Solutions": "//a[contains(text(), 'Solutions')]",
        "Resources": "//a[contains(text(), 'Resources')]"
    }
    
    for item_name, xpath in menu_items.items():
        try:
            element = wait_for_element(driver, By.XPATH, xpath)
            assert element.is_displayed(), f"{item_name} menu item is not displayed"
        except Exception as e:
            pytest.fail(f"Failed to find {item_name} menu item: {str(e)}")

def test_watch_demo_button(setup):
    """
    Verify that the Watch Demo button is present and properly displayed.
    Tests critical conversion element accessibility.
    """
    driver = setup
    driver.get("https://www.entrata.com")
    
    try:
        demo_button = wait_for_element(
            driver, 
            By.CLASS_NAME, 
            "button-text"
        )
        assert demo_button.is_displayed()
        assert "Watch Demo" in demo_button.text
        
    except Exception as e:
        # Capture failure state
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        driver.save_screenshot(f"error_screenshot_{timestamp}.png")
        pytest.fail(f"Watch Demo button test failed: {str(e)}")

def test_sign_in_functionality(setup):
    """
    Verify that the Sign In link is present and accessible.
    Tests user authentication entry point.
    """
    driver = setup
    driver.get("https://www.entrata.com")
    
    try:
        sign_in_button = wait_for_element(
            driver,
            By.XPATH,
            "//a[contains(text(), 'Sign In')]"
        )
        assert sign_in_button.is_displayed()
    except Exception as e:
        pytest.fail(f"Sign In functionality test failed: {str(e)}")

def test_basecamp_button(setup):
    """
    Verify that the Basecamp button is present and clickable.
    Tests access to the Basecamp feature.
    """
    driver = setup
    driver.get("https://www.entrata.com")
    
    try:
        basecamp_button = wait_for_element(
            driver,
            By.XPATH,
            "//a[text()='Basecamp']"
        )
        assert basecamp_button.is_displayed()
        assert basecamp_button.is_enabled()
    except Exception as e:
        pytest.fail(f"Basecamp button test failed: {str(e)}")

def test_responsive_layout(setup):
    """
    Verify that the website is responsive across different screen sizes.
    Tests viewport adaptability for:
    - Desktop (1920x1080)
    - Laptop (1366x768)
    - Tablet (768x1024)
    - Mobile (375x812)
    """
    driver = setup
    driver.get("https://www.entrata.com")
    
    # Test various device viewport sizes
    viewports = [
        (1920, 1080),  # Desktop
        (1366, 768),   # Laptop
        (768, 1024),   # Tablet
        (375, 812)     # Mobile
    ]
    
    for width, height in viewports:
        try:
            driver.set_window_size(width, height)
            # Ensure page has finished adjusting
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            # Verify page accessibility by checking logo presence
            logo = wait_for_element(driver, By.XPATH, "//a[contains(@class, 'logo') or contains(@class, 'brand')]")
            assert logo.is_displayed()
        except Exception as e:
            pytest.fail(f"Responsive layout test failed for viewport {width}x{height}: {str(e)}")

# Execute tests when run as main script
if __name__ == "__main__":
    pytest.main(["-v"])