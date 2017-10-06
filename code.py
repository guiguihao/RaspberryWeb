#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("导入 RPi.GPIO 时出现错误！这可能由于没有超级用户权限造成的。您可以使用 'sudo' 来运行您的脚本。")
urls = (
    '/', 'index',
)
app = web.application(urls, globals())
render = web.template.render('templates/')
class index:
    def GET(self):
        name = '树莓派40pin引脚对照表'
        footnote = '欢迎收藏'
        wiringPi = 'wiringPi编码'
        BCM = 'BCM编码'
        fun = '功能名'
        pin = '物理引脚'
        web.header('Content-Type', 'text/html; charset=UTF-8')
        return (render.index(name,footnote,wiringPi,BCM,fun,pin))
    def POST(self):
        i = web.input()
        channel = i.channel
        mode = i.mode
        state = i.st
        print(i)
        stateStr = ''
        if state == '1':
            stateStr = '高电平'
        else:
            stateStr = '低电平'
        setGPIO(mode,int(channel),int(state))
        return ("SUCCEED:以BCM方式设置GPIO%s为%s" % (channel,stateStr))

def setGPIO(mode,channel,state):
    if mode == 'BOARD':
        GPIO.setmode(GPIO.BOARD)
    if mode == 'BCM':
        GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(channel, GPIO.OUT)
    GPIO.output(channel, state)


if __name__ == "__main__":
    # web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()