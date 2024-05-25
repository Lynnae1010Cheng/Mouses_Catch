# -*- coding: utf-8 -*-
"""
Created on Wed May  1 01:27:39 2024

@author: YilinIling
"""

import pygame, random#加入pygame跟random
pygame.init() #啟動Pygame

#顯示素材
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #建立繪圖視窗
pygame.display.set_caption("出來抓老鼠，你當老鼠") #繪圖視窗標題
MM = pygame.image.load("mouse.png")#加入圖片ps:老鼠
bg = pygame.image.load("bg.png")#加入圖片ps:背景

def text_score(count,score,times):
    font = pygame.font.Font('Fonts/ttf/Cubic_11_1.100_R.ttf',30)#建立文字模組(讀取字體位置,字體大小)
    text_str="老鼠總數:  "+str(count)+"  你的得分:  "+str(score)+"  剩餘時間  "+str(int(times))#顯示文字
    text = font.render(text_str,True,(255,255,255))#文字導入模組
            #文字位置
    text_rect = text.get_rect()#取得文字位置
    text_rect.centerx = screen.get_rect().centerx#水平置中
    text_rect.y=10#垂直位置
    screen.blit(text,text_rect)#顯示文字於視窗
    
#匯入音效並重複撥放
pygame.mixer.music.load("d://bgm.mp3")#音樂
pygame.mixer.music.play()#播放
mouse_sound=pygame.mixer.Sound("006.wav")#音效

#計時器
clock = pygame.time.Clock()
#角色群組--列表
sprite_list = pygame.sprite.Group()
class MOUSE(pygame.sprite.Sprite):#建立角色
    def __init__(self):#創建
        pygame.sprite.Sprite.__init__(self)#加入角色self
        #導入老鼠隨機位置
        posx=random.randint(0,800)
        posy=random.randint(0,600)
        pos=(posx,posy)   
        self.pos= pos#角色的座標
        self.image = MM#角色的圖片
        #取得老鼠區域
        self.rect = self.image.get_rect()
        #老鼠出現座標(圖片中心)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        #導入老鼠的隨機速率 #每隻各以固定速率移動
        self.dx = random.randint(-10,10)
        self.dy = random.randint(-10,10)

    def update(self):#角色移動(更新座標)
        #計算老鼠新餘標
        self.rect.x += self.dx 
        self.rect.y += self.dy
        if self.rect.left <= 0: #角色左邊到達左邊界
           self.dx *= -1 #水平速度變號#反彈
           self.rect.left = 0#讓位置回到視窗內
        if self.rect.right >= screen.get_width(): #到達右邊界
           self.dx *= -1 #水平速度變號#反彈
           self.rect.right = screen.get_width()#讓位置回到視窗內
        if self.rect.top <= 0: #到達上邊界
           self.dy *= -1 #垂直速度變號#反彈
           self.rect.top = 0#讓位置回到視窗內
        if self.rect.bottom >= screen.get_height(): #到達下邊界
           self.dy *= -1 #垂直速度變號#反彈
           self.rect.bottom = screen.get_height()#讓位置回到視窗內


running = True#迴圈的變數
start = True
#初始值
FPS=60
count = 0
score = 0
time = FPS*20#FPS*秒數

while running: #無窮迴圈#True
    clock.tick(FPS) #每秒執行__次
    times = time/FPS#顯示秒數
    for event in pygame.event.get():#事件
        if event.type == pygame.QUIT: #使用者按關閉鈕
            running = False#檔案結束執行
        if event.type == pygame.MOUSEBUTTONDOWN:#按下滑鼠
            pos= pygame.mouse.get_pos() #抓取滑鼠的位置
            for s in sprite_list:#列表迴圈
                if s.rect.collidepoint(pos)==True:#如果老鼠跟點(滑鼠點擊的位置)碰撞
                    mouse_sound.play()#消除老鼠的聲音
                    score+=5#點擊一隻+五分
                    count-=1#點擊後數量-1
                    sprite_list.remove(s)#移除老鼠，限制老鼠數量
    if start:
        #增加老鼠
        if count < 3:#限制數量
            mouse=MOUSE()#在遊戲執行時不斷生成老鼠
            sprite_list.add(mouse)#加入老鼠進群組
            count += 1#增加老鼠
    
        time -= 1#一秒-FPS次
        if time%120 == 1:#兩秒增加一次老鼠
            mouse=MOUSE()#在遊戲執行時不斷生成老鼠
            sprite_list.add(mouse)#加入老鼠進群組
            count += 1#增加老鼠
    if time == 0:#當時間為0
        start = False#結束執行
        count = 0
        sprite_list.empty()

    #更新
    sprite_list.update()#上傳/更新群組
    #畫面顯示
    screen.blit(bg,(0,0))#加入背景圖片
    sprite_list.draw(screen)#把群組的老鼠畫出來
    text_score(count,score,times)
    pygame.display.update()#上傳/更新  


pygame.quit()#結束


