import time
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction


class YouTubeGesturesTest(unittest.TestCase):
    def setUp(self):
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '11',
            'deviceName': 'Pixel_4_API_30',
            'app': '/Users/tester/Downloads/YouTube_v17.10.35.apk',
            'automationName': 'UiAutomator2'
        }
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.action = TouchAction(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_scroll(self):
        self.driver.find_element_by_android_uiautomator('new UiScrollable(new UiSelector().scrollable(true)).scrollTextIntoView("Trending")')
        time.sleep(2)

    def test_long_press(self):
        video_item = self.driver.find_element_by_xpath('(//android.view.ViewGroup[@content-desc="Video item"])[1]')
        self.action.long_press(video_item, duration=3000).release().perform()
        time.sleep(2)

    def test_swipe(self):
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2
        start_y = window_size['height'] * 0.8
        end_y = window_size['height'] * 0.2
        self.action.press(x=start_x, y=start_y).wait(1000).move_to(x=start_x, y=end_y).release().perform()
        time.sleep(2)

    def test_tap(self):
        search_button = self.driver.find_element_by_id('com.google.android.youtube:id/menu_item_1')
        self.action.tap(search_button).perform()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_id('com.google.android.youtube:id/search_edit_text'))


    def test_pinch_zoom(self):
        el = self.driver.find_element_by_id('com.google.android.youtube:id/player_view')
        multi_action = MultiAction(self.driver)
        action1 = TouchAction(self.driver)
        action2 = TouchAction(self.driver)
        loc = el.location
        size = el.size

        center_x = loc['x'] + size['width'] / 2
        center_y = loc['y'] + size['height'] / 2

        action1.press(x=center_x, y=center_y - 100).move_to(x=center_x, y=center_y - 200).release()
        action2.press(x=center_x, y=center_y + 100).move_to(x=center_x, y=center_y + 200).release()

        multi_action.add(action1, action2)
        multi_action.perform()
        time.sleep(2)

if __name__ == '__main__':
    unittest.main()
