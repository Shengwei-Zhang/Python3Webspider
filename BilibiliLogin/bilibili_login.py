from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import base64
from PIL import Image
from selenium.webdriver import  ActionChains




#声明一些全局变量账户名，密码
USERNAME = 'enter your account_number'#输入自己的账户名
PASSWARD = 'enter your password'#输入自己的账号密码
#起始边界，
BORDER = 15




class Bilibililogin():
    def __init__(self):
        self.url = 'https://passport.bilibili.com/login'
        self.browser = webdriver.Chrome()
        self.username = USERNAME
        self.password = PASSWARD
        self.wait = WebDriverWait(self.browser,10)

    def get_image(self):
        '''
        image1:完整图片
        image2 带缺口图片
        :return: image1, image2
        '''
        #使用代码模拟，使验证码出现
        self.browser.get(self.url)
        account_number = self.wait.until(EC.element_to_be_clickable((By.ID,'login-username')))
        account_number.send_keys(self.username)
        pass_world = self.wait.until(EC.element_to_be_clickable((By.ID,'login-passwd')))
        pass_world.send_keys(self.password)
        button = self.browser.find_element_by_class_name('btn-login')
        button.click()
        #等待图片出现，并选择
        im = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slicebg')))
        # 调用JS获取图片，获取带缺口图片，保存到本地
        JS = 'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("iamge/png");'
        im_info = self.browser.execute_script(JS)
        im_base64 = im_info.split(',')[1]
        canvas_bg = base64.b64decode(im_base64)
        with open('canvas_bg.png', 'wb') as f:
            f.write(canvas_bg)
        # 获取完整图片保存到本地
        JS = 'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("iamge/png");'
        im_info = self.browser.execute_script(JS)
        im_base64 = im_info.split(',')[1]
        canvasfull_bg = base64.b64decode(im_base64)
        with open('canvasfull_bg.png', 'wb') as f:
            f.write(canvasfull_bg)
        image1 = Image.open('canvasfull_bg.png')
        image2 = Image.open('canvas_bg.png')
        return image1, image2


    def is_pixel_equal(self, image1, image2, x, y):
        '''
        判断像素是否相同
        image1:完整图片
        image2:带缺口图片
        :return:
        '''
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel2[0] - pixel1[0]) < threshold and abs(pixel2[1] - pixel1[1]) < threshold and     abs(
                pixel2[2] - pixel1[2]) < threshold:
            return True
        else:
            return False


    def get_position(self, image1, image2):
        '''
           image1:完整图片
           image2:带缺口完整图片
           遍历两张图片的像素，找出不同位置
           :return: 坐标
           '''
        left = 60
        # print(left)
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1,image2, i, j):
                    left = i
                    return left
        # print(left.bit_length())
        return left


    def get_track(self, distance):
        '''
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return:
        '''
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5  # 前4/5段加速 后1/5段减速
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                a = 3  # 加速度为+3
            else:
                a = -3  # 加速度为-3

            # 初速度v0
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track


    def get_slider(self):
        slider = self.browser.find_element_by_class_name('geetest_slider_button')
        return slider


    def slice_move(self, slider, tracks):
        '''
        :param slider: 滑块
        :param tracks: 轨迹
        :return:
        '''
        #按住鼠标
        ActionChains(self.browser).click_and_hold(slider).perform()
        #按照轨迹移动
        for x in tracks:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        #松开鼠标
        ActionChains(self.browser).release().perform()
        time.sleep(2)
    def get_judgment(self):
        '''
        成功登陆后，页面会跳转，通过判断跳转后的url，来判断是否登录成功
        :return:
        '''
        if self.browser.current_url != self.url:
            return True
        else:
            return False


    def login(self):
        print('......', '开始登陆')
        image1, image2 = self.get_image()
        distance = self.get_position(image1,image2) - BORDER
        tracks = self.get_track(distance)
        slider = self.get_slider()
        self.slice_move(slider=slider,tracks=tracks)
        time.sleep(2)
        judgment = self.get_judgment()
        # print(judgment)
        if judgment:
            print('登陆成功')
            self.close()
        else:
            self.login()


    def close(self):
        self.browser.quit()


if __name__ == '__main__':
    login = Bilibililogin()
    login.login()





