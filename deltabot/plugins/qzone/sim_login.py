#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

QQ 空间模拟登录
Modified from https://github.com/luolongfei/qzone-spider/blob/master/qzone_spider.py

"""

import os
import pickle
import random
import time
import traceback
from threading import Lock
from urllib.request import urlretrieve

import cv2
import numpy as np
from PIL import Image
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ... import config

get_relative_path = lambda p: os.path.join(os.path.dirname(__file__), p)

class QzoneSimLogin(object):

    timeout = config.QZONE_SIM_LOGIN_TIMEOUT
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'

    # 空间留言板地址
    qzone_message_board_url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb'

    def __init__(self):
        self.options = webdriver.ChromeOptions()

        self.options.add_argument(f'user-agent={QzoneSimLogin.user_agent}')
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument('--disable-extensions')  # 禁用扩展
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument('--incognito')  # 隐身模式
        self.options.add_argument('--disable-plugins-discovery')
        self.options.add_argument('--start-maximized')
        # self.options.add_argument('--window-size=1366,768')

        self.options.add_argument('--headless')  # 启用无头模式
        self.options.add_argument('--disable-gpu')  # 谷歌官方文档说加上此参数可减少 bug，仅适用于 Windows 系统

        # 解决 unknown error: DevToolsActivePort file doesn't exist
        self.options.add_argument('--no-sandbox')  # 绕过操作系统沙箱环境
        self.options.add_argument('--disable-dev-shm-usage')  # 解决资源限制，仅适用于 Linux 系统

        self.driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_PATH, options=self.options)
        self.driver.implicitly_wait(QzoneSimLogin.timeout)

        # 防止通过 window.navigator.webdriver === true 检测模拟浏览器
        # 参考：
        # https://www.selenium.dev/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.webdriver.html#selenium.webdriver.chrome.webdriver.WebDriver.execute_cdp_cmd
        # https://chromedevtools.github.io/devtools-protocol/tot/Page/#method-addScriptToEvaluateOnNewDocument
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

        # 隐藏无头浏览器特征，增加检测难度
        with open(get_relative_path('resources/stealth.min.js')) as f:
            stealth_js = f.read()

            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_js
            })

        # 统配显式等待
        self.wait = WebDriverWait(self.driver, timeout=QzoneSimLogin.timeout, poll_frequency=0.5)

        self.uin = str(config.UIN)
        self.password = config.PASSWORD

    def login(self) -> (str, str):
        """登录 QQ 空间
        获取的 cookies 及令牌
        Returns:
            cookies & g_tk
        """

        logger.info("开始模拟登录")

        self.driver.get('https://qzone.qq.com/')

        login_frame = self.driver.find_element_by_id('login_frame')
        self.driver.switch_to.frame(login_frame)
        self.driver.find_element_by_id('switcher_plogin').click()

        logger.info("正在模拟输入账号...")
        u = self.driver.find_element_by_id('u')
        u.clear()
        self.send_keys_delay_random(u, self.uin)

        time.sleep(2)

        logger.info("正在模拟输入密码...")
        p = self.driver.find_element_by_id('p')
        p.clear()
        self.send_keys_delay_random(p, self.password)

        self.driver.find_element_by_id('login_button').click()

        self.__fuck_captcha()

        cookies = {cookie['name']: cookie['value'] for cookie in self.driver.get_cookies()}
        g_tk = self.calculate_g_tk(cookies)

        self.driver.quit()
        logger.info("模拟登录成功，已关闭浏览器")

        return self.get_str_cookies(cookies), g_tk

    @staticmethod
    def __get_track(distance):
        """
        获取移动轨迹
        先加速再减速，滑过一点再反方向滑到正确位置，模拟真人
        :param distance:
        :return:
        """
        # 初速度
        v = 0

        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.2

        # 位移 / 轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []

        # 当前的位移
        curr_position = 0

        # 到达mid值开始减速
        mid = distance * 7 / 8

        # 先滑过一点，最后再反着滑动回来
        distance += 10

        while curr_position < distance:
            if curr_position < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = random.randint(2, 4)  # 加速运动
            else:
                a = -random.randint(3, 5)  # 减速运动

            # 初速度
            v0 = v

            # 0.2秒时间内的位移
            s = v0 * t + 0.5 * a * (t ** 2)

            # 当前的位置
            curr_position += s

            # 添加到轨迹列表
            tracks.append(round(s))

            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t

        # 反着滑动到大概准确位置
        for i in range(4):
            tracks.append(-random.randint(2, 3))
        for i in range(4):
            tracks.append(-random.randint(1, 3))

        return tracks

    @staticmethod
    def __get_distance_x(bg_block, slide_block):
        """
        获取滑块与缺口图块的水平距离
        :param bg_block:
        :param slide_block:
        :return:
        """
        image = cv2.imread(bg_block, 0)  # 带缺口的背景图
        template = cv2.imread(slide_block, 0)  # 缺口图块

        # 图片置灰
        tmp_dir = get_relative_path('./images/tmp/')
        os.makedirs(tmp_dir, exist_ok=True)
        image_gray = os.path.join(tmp_dir, 'bg_block_gray.jpg')
        template_gray = os.path.join(tmp_dir, 'slide_block_gray.jpg')
        cv2.imwrite(image_gray, template)
        cv2.imwrite(template_gray, image)
        image = cv2.imread(template_gray)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = abs(255 - image)
        cv2.imwrite(template_gray, image)

        # 对比两图重叠区域
        image = cv2.imread(template_gray)
        template = cv2.imread(image_gray)
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        y, x = np.unravel_index(result.argmax(), result.shape)

        return x

    def __is_visibility(self, locator: tuple) -> bool:
        """
        判断元素是否存在且可见
        :param locator: 定位器
        :return:
        """
        try:
            return bool(self.wait.until(EC.visibility_of_element_located(locator)))
        except Exception as e:
            return False

    def __fuck_captcha(self, max_retry_num=6):
        """
        模拟真人滑动验证
        :param max_retry_num: 最多尝试 max_retry_num 次
        :return:
        """
        # 判断是否出现滑动验证码
        logger.info('正在检查是否存在滑动验证码...')
        if not (self.__is_visibility((By.ID, 'newVcodeArea'))):
            logger.info('无滑动验证码，直接登录')
            return

        logger.info('发现滑动验证码，正在验证...')

        # 切换到验证码 iframe
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'tcaptcha_iframe')))
        time.sleep(0.2)  # 切换 iframe 会有少许延迟，稍作休眠

        for i in range(1, max_retry_num + 1):
            # 背景图
            bg_block = self.wait.until(EC.visibility_of_element_located((By.ID, 'slideBg')))
            bg_img_width = bg_block.size['width']
            bg_img_x = bg_block.location['x']
            bg_img_url = bg_block.get_attribute('src')
            print(bg_img_url)

            # 滑块图
            slide_block = self.wait.until(EC.visibility_of_element_located((By.ID, 'slideBlock')))
            slide_block_x = slide_block.location['x']
            slide_img_url = slide_block.get_attribute('src')
            print(slide_img_url)

            # 小滑块
            drag_thumb = self.wait.until(EC.visibility_of_element_located((By.ID, 'tcaptcha_drag_thumb')))

            # 下载背景图和滑块图
            os.makedirs(get_relative_path('./images/'), exist_ok=True)
            # logger.warning(bg_img_url, slide_img_url)
            urlretrieve(bg_img_url, get_relative_path('./images/bg_block.jpg'))
            urlretrieve(slide_img_url, get_relative_path('./images/slide_block.jpg'))

            # 获取图片实际宽度的缩放比例
            bg_real_width = Image.open(get_relative_path('./images/bg_block.jpg')).width
            width_scale = bg_real_width / bg_img_width

            # 获取滑块与缺口的水平方向距离
            distance_x = self.__get_distance_x(get_relative_path('./images/bg_block.jpg'), get_relative_path('./images/slide_block.jpg'))
            real_distance_x = distance_x / width_scale - (slide_block_x - bg_img_x) + 4

            # 获取移动轨迹
            track_list = self.__get_track(real_distance_x)

            # 按住小滑块不放
            ActionChains(self.driver).click_and_hold(on_element=drag_thumb).perform()
            time.sleep(0.2)

            # 分段拖动小滑块
            for track in track_list:
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 将鼠标移动到当前位置 (x, y)
                time.sleep(0.002)
            time.sleep(1)

            # 放开小滑块
            ActionChains(self.driver).release(on_element=drag_thumb).perform()
            time.sleep(5)  # 跳转需要时间

            # 判断是否通过验证
            if 'user' in self.driver.current_url:
                logger.info('已通过滑动验证', 1)
                self.driver.switch_to.default_content()

                return True
            else:
                logger.warning(f'滑块验证不通过，正在进行第 {i} 次重试...')
                self.wait.until(EC.element_to_be_clickable((By.ID, 'e_reload'))).click()
                time.sleep(0.2)

        raise UserWarning(f'滑块验证不通过，共尝试{max_retry_num}次')

    @staticmethod
    def calculate_g_tk(cookies: dict) -> int:
        """
        生成 QQ 空间令牌
        :param cookies:
        :return:
        """
        h = 5381
        s = cookies.get('p_skey', None) or cookies.get('skey', None) or ''
        for c in s:
            h += (h << 5) + ord(c)

        return h & 0x7fffffff


    @staticmethod
    def get_str_cookies(cookies: dict) -> str:
        return ";".join([str(arg) + "=" + str(key) for arg, key in cookies.items()])

    def send_keys_delay_random(self, element, keys, min_delay=0.13, max_delay=0.52):
        """
        随机延迟输入
        :param element:
        :param keys:
        :param min_delay:
        :param max_delay:
        :return:
        """
        for key in keys:
            element.send_keys(key)
            time.sleep(random.uniform(min_delay, max_delay))


def run(thread_lock: Lock) -> None:
    """
    Simulate login Qzone and save cookies & g_tk
    Args:
        thread_lock (Lock): thread lock

    Returns:
        None
    """
    logger.warning("Simulate Qzone login thread started!")
    with thread_lock:
        s = QzoneSimLogin()
        try:
            cookies, g_tk =  s.login()
        except AssertionError as ae:
            logger.error('参数错误：{}'.format(str(ae)))
        except NoSuchElementException as nse:
            logger.error('匹配元素超时，超过{}秒依然没有发现元素：{}'.format(s.timeout, str(nse)))
        except TimeoutException:
            logger.error(f'请求超时：{s.driver.current_url}')
        except UserWarning as uw:
            logger.error('警告：{}'.format(str(uw)))
        except WebDriverException as wde:
            logger.error(f'未知错误：{str(wde)}')
        except Exception as e:
            logger.error('出错：{} 位置：{}'.format(str(e), traceback.format_exc()))
        else:
            with open(get_relative_path('./data/cookies.pkl'), 'wb') as f:
                pickle.dump([cookies, g_tk], f)
            logger.info("Succeeded in getting Qzone login token.")
    logger.warning("Simulate Qzone login thread finished.")