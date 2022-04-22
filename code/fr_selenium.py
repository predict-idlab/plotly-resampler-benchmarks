import time
from typing import Union

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class FigureResamplerGUITests:
    """Wrapper for performing figure-resampler GUI. """

    def __init__(self, driver: webdriver, port: int):
        """Construct an instance of A firefox selenium driver to fetch wearable data.

        Parameters
        ----------
        driver: webdriver
            The webdriver which will be used
        port: int
            The port on which the web-application will be tests

        """
        self.port = port
        self.driver: Union[webdriver.Firefox, webdriver.Chrome] = driver
        self.on_page = False

    def go_to_page(self, page: str = None):
        """Navigate to FigureResampler page."""
        time.sleep(1)
        if page is None:
            self.driver.get("http://localhost:{}".format(self.port))
        else:
            self.driver.get(page)
        self.on_page = True

    def wait_element(self, class_name, wait_time_s = 3):
        WebDriverWait(self.driver, wait_time_s).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )

    def clear_requests(self, sleep_time_s=1):
        time.sleep(1)
        del self.driver.requests

    def get_requests(self, delete: bool = True):
        requests = self.driver.requests
        if delete:
            self.clear_requests()

        return requests

    def drag_and_zoom(self, div_classname, x0=0.25, x1=0.5, y0=0.25, y1=0.5):
        """
        Drags and zooms the div with the given classname.

        Parameters
        ----------
        div_classname : str
            The classname of the div to be dragged and zoomed.
        x0 : float, default: 0.5
            The relative x-coordinate of the upper left corner of the div.
        x1 : float, default: 0.5
            The relative x-coordinate of the lower right corner of the div.
        y0 : float, default: 0.5
            The relative y-coordinate of the upper left corner of the div.
        y1 : float, default: 0.5
            The relative y-coordinate of the lower right corner of the div.

        """
        if not self.on_page:
            self.go_to_page()

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, div_classname))
        )

        subplot = self.driver.find_element(By.CLASS_NAME, div_classname)
        size = subplot.size
        w, h = size["width"], size["height"]

        actions = ActionChains(self.driver)
        actions.move_to_element_with_offset(subplot, xoffset=w * x0, yoffset=h * y0)
        actions.click_and_hold()
        actions.pause(0.2)
        actions.move_by_offset(xoffset=w * (x1 - x0), yoffset=h * (y1 - y0))
        actions.pause(0.2)
        actions.release()
        actions.pause(0.2)
        actions.perform()

    def _get_modebar_btns(self):
        if not self.on_page:
            self.go_to_page()

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modebar-group"))
        )
        return self.driver.find_elements(By.CLASS_NAME, "modebar-btn")

    def autoscale(self):
        for btn in self._get_modebar_btns():
            data_title = btn.get_attribute("data-title")
            if data_title == "Autoscale":
                ActionChains(self.driver).move_to_element(btn).click().perform()
                return

    def reset_axes(self):
        for btn in self._get_modebar_btns():
            data_title = btn.get_attribute("data-title")
            if data_title == "Reset axes":
                ActionChains(self.driver).move_to_element(btn).click().perform()
                return

    def click_legend_item(self, legend_name):
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modebar-group"))
        )
        for legend_item in self.driver.find_elements(By.CLASS_NAME, "legendtext"):
            if legend_name in legend_item.get_attribute("data-unformatted"):
                # move to the center of the item and click it
                (
                    ActionChains(self.driver)
                    .move_to_element(legend_item)
                    .pause(0.1)
                    .click()
                    .perform()
                )
                return

    # ------------------------------ DATA MODEL METHODS  ------------------------------
    def __del__(self):
        self.driver.close()
