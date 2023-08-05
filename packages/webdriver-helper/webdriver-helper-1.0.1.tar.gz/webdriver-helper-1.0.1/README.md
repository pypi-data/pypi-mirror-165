# WebDriver助手

并不是对selenium更高级的封装，而是通过增加以下的能力，让selenium用起来更方便：

- 😊 自动获取浏览器版本号、操作系统类型
- 😊 自动**下载**合适的浏览器驱动（国内镜像加速）
- 😊 自动**创建**和返回WebDriver对象
- 😊 可以**调试**Python和浏览器（Chromium内核）
- 😊 可以进行文件**拖拽上传**


## 环境要求：
Python >= 3.9


## 用法
### 启动浏览器

```python
from webdriver_helper import get_webdriver

chrome = get_webdriver()  # 默认启动chrome
chrome.get("https://baidu.com")
chrome.quit()

firefox = get_webdriver("fireFOX")  # 也可指定firefox，大小写不敏感
firefox.quit()
```

### 设置浏览器启动参数

```python
from selenium import webdriver
from webdriver_helper import get_webdriver

option = webdriver.ChromeOptions()  # 创建Option对象
option.add_argument("--headless")  # 无头模式

chrome = get_webdriver(options=webdriver.ChromeOptions())  # 传递Option参数
chrome.quit()

firefox = get_webdriver("firefox", options=webdriver.FirefoxOptions())
firefox.quit()

```

### 进入浏览器调试模式

```python
from webdriver_helper import debugger, get_webdriver

chrome = get_webdriver()  # 默认启动chrome
chrome.get("https://baidu.com")

debugger(chrome)  # 进入调试模式，浏览器和python将被挂起
# 在控制输入`c`并按下回车 ，退出调试模式

chrome.quit()
```

### 文件拖拽上传

```python
from webdriver_helper import debugger, get_webdriver
from selenium.webdriver.common.by import By

chrome = get_webdriver()  # 默认启动chrome

chrome.get("http://118.24.147.95:8086/upload.html")

ele = chrome.find_element(By.XPATH, "/html/body/div[2]/div")  # 定位文件要拖放的元素
ele.upload_by_drop('a.jpg')  # 将文件`a.jpg`上传

```
## 联系作者

如果在使用过程中遇到什么问题，欢迎通过以下方式联系：

-   email：**dongfangtianyu@gmail.com**

-   vx:  **python_sanmu** 
