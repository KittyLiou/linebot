from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import urllib.parse
import urllib.request

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    if '天氣' in event.message.text:
						pos = event.message.text.find('天氣')
						location = event.message.text[pos-3:pos]
                        req = urllib.request.Request('http://opendata.cwb.gov.tw/opendataapi?dataid=F-C0032-001&authorizationkey=CWB-8C4DB566-AD62-4E69-91D8-6E7323B5F20A')
                        resp = urllib.request.urlopen(req)
                        content = resp.read()
                        content = content.decode().split(location)
                        content = content[1].split('<time>')
                        content = content[1].split('<parameterName>')
                        endpoint = content[1].find('</parameterName>')
                        result = content[1][:endpoint]
                        print(result)
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=location+result)
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=event.message.text)
                        )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()