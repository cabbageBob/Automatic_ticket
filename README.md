# Concert_Ticket
大麦网演唱会抢票程序
* Python3.7
* Selenium
## 准备工作
* 下载anaconda，对应python3.7
* 下载谷歌浏览器以及对应的chromedriver.exe，并且修改executable_path的chromedriver.exe路径
* 打开命令提示窗口，输入pip install selenium
* 如果提示其他包未安装，请用相同的方式下载，或自行谷歌
* 修改抢票目标页target_url
* choose_ticket(self,priceWanted)，priceWanted为价位的序号
* 修改user-data-dir，将user-data-dir修改为本机Chrome中User Data所在路径，dirverOptions.add_argument(argument=r'user-data-dir=C:\Users\10415\AppData\Local\Google\Chrome\User Data')
* 打开chrome,进入大麦网并登陆。
* 运行代码，在这个过程中注意观察串口输出
