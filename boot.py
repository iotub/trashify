# refer to http://blog.sipeed.com/p/680.html
import sensor, image, lcd, time
import KPU as kpu
lcd.init()
lcd.clear()
try:
    img = image.Image("/sd/startup.jpg")
    lcd.display(img)
except:
    lcd.draw_string(lcd.width()//2-100,lcd.height()//2-4, "Error: Cannot find startup.jpg", lcd.WHITE, lcd.RED)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(1)
sensor.run(1)
f=open('/sd/labels.txt','r')
labels=f.readlines()
f.close()
task = kpu.load('/sd/b7e12bad85da152339158e734570a2a2_cd51f50726f11976c1aefe0403b6edd8.smodel') 
lcd.clear(0xFFFF)
clock = time.clock()
while(True):
    img = sensor.snapshot()
    clock.tick()
    fmap = kpu.forward(task, img)
    fps=clock.fps()
    plist=fmap[:]
    pmax=max(plist) 
    max_index=plist.index(pmax) 
    a = lcd.display(img, oft=(48,0))
    lcd.draw_string(48, 224, "%.2f:%s                            "%(pmax, labels[max_index].strip()))
    print(fps)
a = kpu.deinit(task)
