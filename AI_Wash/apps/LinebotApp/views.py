from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, QuickReply, QuickReplyButton, MessageAction

import openai

Line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

def chatGPT(event):
    try:
        openai.api_key = settings.CHAT_GPT_TOKEN
        ans = openai.Completion.create(
            model="text-davinci-003",
            prompt= event.message.text,
            max_tokens=700,
            temperature=0.8
        )
        message = ans['choices'][0]['text']
        print(str(ans))
        # if str(message).startswith("\n",beg=1,end=10):
        # 需要刪除開頭空格
        Line_bot_api.reply_message(event.reply_token, TextSendMessage(text= message))
    except:
        Line_bot_api.reply_message(event.reply_token, TextSendMessage(text='chatGPT err'))

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
                    mtext = event.message.text

                    if mtext == '選擇離島地區':
                        pass

                    if mtext == '我的ID':
                        try:
                            Line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.source.user_id))
                        except:
                            Line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Get user_id err"))
                    
                    if mtext.startswith('我想問') == True:
                        chatGPT(event)
                    else:
                        chatGPT(event)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()