本專案主要是要建置一個天氣機器人，透過line使用者可以向機器人詢問某縣市的天氣。

#Setup
要製作line天氣機器人第一步就是要先擁有一個帳號，到 https://business.line.me/zh-hant/services/bot 註冊一個帳號<br>
接著為了要使用Line Messaging API，我們需要去下載line-bot-sdk<br>
`pip install line-bot-sdk`<br>
另外我們還需要下載django<br>
`pip install django`<br>
完成上述步驟後我們就可以開啟一個新的專案了，下列程式碼是產生一個新的專案line_bot<br>
`django-admin startproject line_bot`<br>
接著我們要再產生一個kittyweatherbot app<br>
`python manage.py startapp kittyweatherbot`<br>
上述的專案名稱及app名稱都可以自訂<br>
接著，為了不讓一些較為機密的值被記錄下來，我們將這些機密的值記錄在環境變數中而非寫死在程式碼裡
```
export SECRET_KEY='Django secret key'
export LINE_CHANNEL_ACCESS_TOKEN='Line channel access token'
export LINE_CHANNEL_SECRET='Line channel secret'
```
上述的Django secret key,Line channel access token,Line channel secret請自行替換成自己的secret key<br>
接著修改settings.py讓程式在執行時會自動去搜尋環境變數
```
SECRET_KEY = get_env_variable('SECRET_KEY')
LINE_CHANNEL_ACCESS_TOKEN = get_env_variable('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = get_env_variable('LINE_CHANNEL_SECRET')
```
另外在INSTALLED_APPS裡面要記得加入我們剛產生的app
```
INSTALLED_APPS = [
     ......,
    'kittyweatherbot'
]
```
接著要來設定URL，編輯專案中的urls.py，加入下列程式碼
```python
from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^kittyweatherbot/', include('kittyweatherbot.urls')),
]
```
接著在app的那個資料夾下新增一個檔案urls.py(以本例而言就是加在kittyweatherbot下)，urls.py裡面內容如下
```python
from django.conf.urls import url
from . import views
urlpatterns = [
    url('^callback/', views.callback),
]
```
至此設定大致上就完成了，接著就可以在views.py內實作想要的功能了<br>
以下列出需要先import的libraries
```python
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import urllib.parse
import urllib.request
```
詳細的實作流程請直接參考views.py內的程式碼<br>
最後一步就是要將我們所寫好的app deploy到Heroku上<br>
第一步驟也是去Heroku辦帳號<br>
Heroku: https://www.heroku.com/ <br>
接著安裝Heroku CLI<br>
在命令列中輸入`heroku login`，輸入信箱和密碼後即可登入heroku<br>
接著我們需要設定環境變數，設定方法如下(以LINE_CHANNEL_SECRET為例)<br>
`heroku config:set 'LINE_CHANNEL_SECRET='123445566777889990000'`<br>
用上述方法設定其他需要的環境變數<br>
最後在專案中加入Procfile和requirements.txt兩個檔案<br>
在命令列中輸入`git push heroku master`即可完成布署<br>
(push之前別忘了要先commit)<br>

以上就是整個weatherbot的建置流程
