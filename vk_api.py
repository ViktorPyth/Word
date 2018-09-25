import vk_api
import datetime # работа с датой и временем
import time
import requests
from lxml import html


url = 'https://yandex.ru/pogoda/kazan'
while True:
    vk = vk_api.vk_api(token="7ee75e0161b92ed2dc121c1e6d1a9d39afaa9cbdf425a6eba952c86f0deb4e9112bdc72787b572431fe50")
    delta = datetime.timedelta(hours=3, minutes=0)
    t = (datetime.datetime.now(datetime.timezone.utc) + delta)
    nowtime = t.strftime("%H:%M")  # текущее время
    nowdate = t.strftime("%d.%m.%Y")  # текущая дата
    on = vk.method("friends.getOnline")  # получаем список id друзей онлайн
    counted = len(on)  # считаем кол-во элементов в списке
    endin = counted % 10
    if endin in range(2,5):
        endw = ' друга'
    elif endin == 1:
        endw = ' друг'
    else:
        endw = ' друзей'

    response = requests.get(url).content.decode()
    # print(response)
    stat = html.fromstring(response)
    temp = stat.xpath('//div[@class="fact"]/div/dl/dd/div/span/text()')[0]
    wanga = stat.xpath('//div[@class="fact"]/div/a/div/text()')[0]
    way = stat.xpath('//div[@class="fact"]/div/dl/dd/span/abbr/text()')[0]
    speed = stat.xpath('//div[@class="fact"]/div/dl/dd/span/text()')[0]
    if wanga == 'Открыть карту осадков':
        wanga = 'вчера в это время было ' + stat.xpath('//div[@class="fact"]/div/dl/dd/div/span/text()')[0]
    try:
        vk.method("status.set", {"text": "Дай угадаю, сейчас " + nowtime + '. '
                                                                       'За окном: ' + temp + ', Ветер ' + way + ', ' + speed + ' м/с' + ', и говорят, что ' + wanga.lower() + ". В сети: " + str(counted) + endw})
    except  vk_api.exceptions.Captcha:
        print( vk_api.exceptions.Captcha.sid)
        print( vk_api.exceptions.Captcha.key)
    time.sleep(30)  # погружаем скрипт в «сон» на 30 секунд
