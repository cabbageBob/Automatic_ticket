import os
import time
import pickle
from time import sleep
from selenium import webdriver

# 大麦网主页
damai_url = "https://www.damai.cn/"
# 登录页
login_url = "https://passport.damai.cn/login?ru=https%3A%2F%2Fwww.damai.cn%2F"
# 抢票目标页
target_url="https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.5fa628dfj4MGiZ&id=601280365318&clicktitle=WE%E2%80%A2%E7%BB%BD%E6%94%BE2019%E8%9A%8C%E5%9F%A0%E6%BC%94%E5%94%B1%E4%BC%9A"

name = "麦子14pOD"
phone = "18270913797"


class Concert(object):
    def __init__(self):

        self.status = 0  # 状态,表示如今进行到何种程度
        self.login_method = 1  # {0:模拟登录,1:Cookie登录}自行选择登录方式

    def set_cookie(self):
        self.driver.get(damai_url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            sleep(1)
        print("###请扫码登录###")
        while self.driver.title == '大麦登录':
            sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(target_url)

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value'),
                    "expires": "",
                    'path': '/',
                    'httpOnly': False,
                    'HostOnly': False,
                    'Secure': False}
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method == 0:
            self.driver.get(login_url)  # 载入登录界面
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):  # 如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(target_url)
                self.get_cookie()

    dirverOptions = webdriver.ChromeOptions()
    dirverOptions.add_argument(argument=r'user-data-dir=C:\Users\10415\AppData\Local\Google\Chrome\User Data')
    #禁止加载图片和css,1为显示，2为不显示
    # prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
    # dirverOptions.add_experimental_option("prefs",prefs)
    def enter_concert(self):
        print('###打开浏览器，进入大麦网###')
        self.driver = webdriver.Chrome(executable_path='G:\chromedriver.exe',chrome_options=self.dirverOptions)  # 默认Chrome浏览器
        self.driver.maximize_window()           #最大化窗口
        self.login()  # 先登录再说
        self.driver.refresh()  # 刷新页面
        self.status = 2  # 登录成功标识
        print("###登录成功###")

    def choose_ticket(self,priceWanted):
        if self.status == 2:  # 登录成功入口
            self.num = 1  # 第一次尝试

            print("=" * 30)
            print("###开始进行日期及票价选择###")
            while self.driver.title.find('支付宝 - 网上支付 安全快速！') == -1:  # 如果跳转到了付款界面就算这步成功了，否则继续执行此步
                # try:
                #     self.driver.find_elements_by_xpath(
                #         '//html//body//div[@class = "perform__order__price"]//div[2]//div//div//a[2]')[
                #         0].click()  # 购票数+1(若需要)
                # except:
                #     print("购票数添加失败")


                # try:
                # self.driver.find_elements_by_xpath('//div[@class = "perform__order__select perform__order__select__performs"]//div[2]//div//div[x]')[0].click()   #默认购票日期的选择,x为日期的选择，1，2，3....
                # except:
                # print("日期选择失败")

                # cart = self.driver.find_element_by_class_name('perform')  # 获得选票界面的表单值
                # cart = self.driver.find_element_by_class_name('perform__order__select')
                #选择价格
                try:
                    self.driver.find_elements_by_xpath(
                        '//div[@class="perform__order__select"]//div[@class="select_right"]//div[@class="select_right_list"]//div['+priceWanted+']'
                    )[0].click()
                except Exception as e:
                    print("###该价位的票已售完")
                    print(e)

                # try:各种按钮的点击,
                buybutton = self.driver.find_element_by_class_name('buybtn').text
                try:
                    # buybutton = self.driver.find_element_by_class_name('buybtn').text
                    if buybutton == "即将开售":
                        self.status = 2
                        self.driver.get(target_url)
                        print('###抢票未开始，刷新等待开始###')
                        continue

                    elif buybutton == "立即预订":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 3
                        self.num = 1
                    elif buybutton == "立即购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 4

                    # 选座购买暂时无法完成自动化
                    elif buybutton == "选座购买":
                        self.driver.find_element_by_class_name('buybtn').click()
                        self.status = 5

                    elif buybutton == "提交缺货登记":
                        print('###抢票失败，请手动提交缺货登记###')
                        break
                    else:
                        self.driver.get(target_url)

                except:
                    print('###未跳转到订单结算界面###')
                    self.driver.get(target_url)
                title = self.driver.title
                if title == "确认订单":
                    self.check_order()
                # 若是选座购买，自行选座
                elif self.status == 5:
                    print("###请自行选择位置和票价###")
                    break

                # if title !="支付宝 - 网上支付 安全快速！" :                                     #如果前一次失败了，那就刷新界面重新开始
                #     self.status=2
                #     self.driver.get(target_url)
                #     print('###抢票失败，从新开始抢票###')

    def check_order(self):
        if self.status in [3, 4]:
            print('###开始确认订单###')
            print('###默认购票人信息###')
            # try:
            #     # 姓名和电话的填写，这是绝对路径，由于大麦网目标页会更新，出现问题修改xpath即可
            #     time.sleep(0.5)
            #     self.driver.find_elements_by_xpath(
            #         '//div[@class = "w1200"]//div[@class = "delivery-form"]//div[1]//div[2]//span//input')[0].send_keys(
            #         name)
            #     time.sleep(0.5)
            #     self.driver.find_elements_by_xpath(
            #         '//div[@class = "w1200"]//div[@class = "delivery-form"]//div[2]//div[2]//span[2]//input')[
            #         0].send_keys(phone)
            #     time.sleep(0.5)
            # except Exception as e:
            #     print("###填写确认订单信息时，联系人手机号填写失败###")
            #     print(e)
            try:
                time.sleep(0.5)
                # 默认选第一个购票人信息
                self.driver.find_elements_by_xpath(
                    '//div[@class = "w1200"]//div[@class = "ticket-buyer-select"]//div//div[1]//span')[
                    0].click()  # 观影人1
                # 选第二个购票人信息(若购买多张票时需要开启此选项，增加购票人信息)
                time.sleep(0.5)
                self.driver.find_elements_by_xpath(
                    '//div[@class = "w1200"]//div[@class = "ticket-buyer-select"]//div//div[2]//span')[
                    0].click()  # 观影人2

            except Exception as e:
                print("###购票人信息选中失败，自行查看元素位置###")
                print(e)
            # try:
            #     self.driver.find_elements_by_xpath(
            #         '//div[@class = "confirmOrder_1"//div[@class = "submit-wrapper"]//button')[0].click()
            # except Exception as e:
            #     print("###提交订单失败，请自行提交###")
            #     print(e)

            print('###不选择订单优惠###')
            print('###请在付款完成后下载大麦APP进入订单详情页申请开具###')

            # 最后一步提交订单

            time.sleep(1)  # 太快会影响加载，导致按钮点击无效
            self.driver.find_elements_by_xpath('//div[@class = "w1200"]//div[2]//div//div[9]//button[1]')[0].click()

            # try:
            #     element = WebDriverWait(self.driver, 5).until(EC.title_contains('支付宝 - 网上支付 安全快速！'))
            #     self.status=6
            #     print('###成功提交订单,请手动支付###')
            # except:
            #     print('###提交订单失败,请查看问题###')

    # 若出现异常则关闭开启的浏览器及驱动，建议使用时注释掉，否则异常发生会关闭打开的浏览器
    def finish(self):
        self.driver.quit()


if __name__ == '__main__':
    try:
        con = Concert()  # 具体如果填写请查看类中的初始化函数
        con.enter_concert()
        con.choose_ticket("2")

    except Exception as e:
        print(e)
        # con.finish()