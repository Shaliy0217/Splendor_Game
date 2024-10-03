def main():
    # 璀璨寶石
    import pygame
    import os
    import json
    import random
    
    #設定遊戲介面
    FPS = 60 
    WIDTH = 600#介面寬度
    HEIGHT = 700#介面高度
    
    #設定顏色(RGB)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0,0,255)
    
    #設定各寶石數量 and 變數
    green_number = 6
    white_number = 6
    blue_number = 6
    black_number = 6
    red_number = 6
    gold_number = 6
    catch = 0
    Round = 1
    flag = 1
    catch_green = 0
    catch_white = 0
    catch_blue = 0
    catch_red = 0
    catch_black = 0
    level1 = 0
    flag_mousedown = 0
    volume = 0.3
    
    # 遊戲初始化 and 創建視窗
    pygame.init()#初始化所有變數
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#畫面大小
    pygame.display.set_caption("璀璨寶石")#設定遊戲標題
    clock = pygame.time.Clock()#設定一個時鐘變數
    
    #載入卡牌資料
    with open("card.json") as f:
        data = json.load(f)
    # 載入圖片
    card_imgs = []
    for i in range(90):
        card_imgs.append(pygame.image.load(os.path.join("img", f"{i + 1}.png")).convert_alpha())
    start_img = pygame.image.load(os.path.join("img", "start_img.png")).convert()
    start_img = pygame.transform.scale(start_img, (WIDTH + 50, HEIGHT + 50))
    background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
    player_img = pygame.image.load(os.path.join("img", "test2.png")).convert_alpha()
    green_img = pygame.image.load(os.path.join("img", "green2.png")).convert_alpha()
    white_img = pygame.image.load(os.path.join("img", "white.png")).convert_alpha()
    blue_img = pygame.image.load(os.path.join("img", "blue.png")).convert_alpha()
    black_img = pygame.image.load(os.path.join("img", "black.png")).convert_alpha()
    red_img = pygame.image.load(os.path.join("img", "red.png")).convert_alpha()
    card1_img = pygame.image.load(os.path.join("img", "39.png")).convert_alpha()
    font_name = os.path.join("font.ttf")#字體
    
    # 載入音樂
    item_sound = pygame.mixer.Sound(os.path.join("sound", "item.mp3"))
    card_sound = pygame.mixer.Sound(os.path.join("sound", "card.mp3"))
    pygame.mixer.music.set_volume(volume)
    
    def draw_text(surf, text, size, x, y,color = WHITE):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.centerx = x
        text_rect.top = y
        surf.blit(text_surface, text_rect)
        
    def draw_init():
        screen.blit(start_img, (-25,-25))
        draw_text(screen, '按滑鼠左鍵進入遊戲', 28, WIDTH/2, HEIGHT/2)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif pygame.mouse.get_pressed()[0]:
                    waiting = False
                    return False
                
    def rule_init():
        screen.blit(background_img, (0,0))
        draw_text(screen, '規則', 20, WIDTH/2, HEIGHT/9)
        draw_text(screen, '一回合可以拿取三個不同顏色的寶石', 20, WIDTH/2, HEIGHT*2/9)
        draw_text(screen, '或是當該顏色寶石總數大於等於四時可以拿取兩個相同顏色的寶石', 20, WIDTH/2, HEIGHT*3/9)
        draw_text(screen, '當寶石數達到卡牌要求的數量時可以購買卡牌', 20, WIDTH/2, HEIGHT*4/9)
        draw_text(screen, '卡牌上的寶石為永久資源', 20, WIDTH/2, HEIGHT*5/9)
        draw_text(screen, '可以當作購買下一張卡牌的資源並且不會消失', 20, WIDTH/2, HEIGHT*6/9)
        draw_text(screen, '當分數達到15分時即結束遊戲', 20, WIDTH/2, HEIGHT*7/9)
        draw_text(screen, '你可以隨時按下滑鼠右鍵來返回規則', 28, WIDTH/2, HEIGHT*8/9,color = RED)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif pygame.mouse.get_pressed()[0]:
                    waiting = False
                    return False
                
    def end_init():
        cards = 0
        for i in player.cards.values():
            cards += i
        screen.blit(background_img, (0,0))
        draw_text(screen, '結束', 20, WIDTH/2, HEIGHT/9)
        draw_text(screen, '本次成績', 20, WIDTH/2, HEIGHT*2/9)
        draw_text(screen, f'分數:{player.point}分', 20, WIDTH/2, HEIGHT*3/9)
        draw_text(screen, f'花費回合數:{Round}回合', 20, WIDTH/2, HEIGHT*4/9)
        draw_text(screen, f'手上擁有的卡牌數:{cards}', 20, WIDTH/2, HEIGHT*5/9)
        draw_text(screen, '按空格鍵來重新開始遊戲!', 20, WIDTH/2, HEIGHT*6/9)
        pygame.display.update()
        waiting = True
        while waiting:
            clock.tick(FPS)
            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        return False
    
    def new_card(w = 0,u = 0,g = 0,r = 0,k = 0,level = 1,color = "w",point = 0,x = 0,number = 1):
        c = card(w,u,g,r,k,level,color,point,x,number)
        all_sprites.add(c)
        cards.add(c)
        
    def Random(level):
        if level == 1:
            return random.randint(0, 39)
        if level == 2:
            return random.randint(40, 69)
        if level == 3:
            return random.randint(70, 89)
    
    def new_green(number = green_number):
        g = green(number)
        all_sprites.add(g)
        greens.add(g)
        
    def new_white(number = white_number):
        w = white(number)
        all_sprites.add(w)
        whites.add(w)
    
    def new_blue(number = blue_number):
        b = blue(number)
        all_sprites.add(b)
        blues.add(b)
        
    def new_black(number = black_number):
        b = black(number)
        all_sprites.add(b)
        blacks.add(b)
    
    def new_red(number = red_number):
        r = red(number)
        all_sprites.add(r)
        reds.add(r)
    
    def new_green_player():
        g = green_player(green_number)
        all_sprites.add(g)
        greens_player.add(g)
        
    def new_white_player():
        w = white_player(white_number)
        all_sprites.add(w)
        whites_player.add(w)
    
    def new_blue_player():
        b = blue_player(blue_number)
        all_sprites.add(b)
        blues_player.add(b)
        
    def new_black_player():
        b = black_player(black_number)
        all_sprites.add(b)
        blacks_player.add(b)
    
    def new_red_player():
        r = red_player(red_number)
        all_sprites.add(r)
        reds_player.add(r)
    
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(player_img, (125, 100))#物件圖片和調整大小
            self.image.set_colorkey(WHITE)
            self.rect = self.image.get_rect()#物件位置變數
            self.rect.x = 10#物件x座標位置
            self.rect.bottom = HEIGHT-10#物件y座標位置
            self.green_number = 0
            self.white_number = 0
            self.blue_number = 0
            self.black_number = 0
            self.red_number = 0
            self.cards = {"w":0,"u":0,"g":0,"r":0,"k":0}
            self.all_number = 0
            self.point = 0
        def update(self):
            self.all_number = self.green_number + self.white_number + self.blue_number + self.black_number + self.red_number
        def click(self,x = 0,y = 0):
            c = Click(x , y)
            all_sprites.add(c)
            clicks.add(c)
    
    class Click(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.Surface((1,1))#物件大小
            self.image.fill(GREEN)#物件圖片
            self.rect = self.image.get_rect()#物件位置變數
            self.rect.center = event.pos#物件座標位置
            if x != 0:
                self.rect.x = x#物件x座標位置
                self.rect.y = y#物件y座標位置
            self.Existence_time = 2
        def update(self):
            self.Existence_time -= 1
            if self.Existence_time <= 0:
                self.kill()
                
    class card(pygame.sprite.Sprite):
        def __init__(self,w,u,g,r,k,level,color,point,x,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.smoothscale(card_imgs[number], (90.4, 124.6))#物件大小
            self.rect = self.image.get_rect()#物件位置變數
            self.rect.x = 50 + x * 100
            self.rect.y = 100 + ((3 - level) * 150)
            self.x = x
            self.w = w#需要花費的白色寶石數
            self.u = u#需要花費的藍色寶石數
            self.g = g#需要花費的綠色寶石數
            self.r = r#需要花費的紅色寶石數
            self.k = k#需要花費的黑色寶石數
            self.color = color#卡牌本身的顏色
            self.point = point#卡牌的分數
            self.level = level#卡牌的階級
            
        def update(self):
            pass
    
        
    class green(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(green_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.center = (WIDTH - (self.number*5)-50,100)#物件x座標位置
        
        def update(self):
            pass
    
    class white(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(white_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.center = (WIDTH - (self.number*5) - 50,200)#物件座標位置
        def update(self):
            pass
    
    class blue(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(blue_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.center = (WIDTH-(self.number*5)-50,300)#物件座標位置
        def update(self):
            pass
        
    class black(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(black_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.center = (WIDTH-(self.number*5)-50,400)#物件座標位置
        def update(self):
            pass
    
    class red(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(red_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.center = (WIDTH-(self.number*5)-50,500)#物件座標位置
        def update(self):
            pass
        
    class green_player(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(green_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.x = 100 + (self.number * 5)#物件x座標位置
            self.rect.bottom = HEIGHT-10#物件y座標位置
        
        def update(self):
           pass
    
    class white_player(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(white_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.x = 200 + (self.number * 5)#物件x座標位置
            self.rect.bottom = HEIGHT-10#物件y座標位置
        def update(self):
            pass
    
    class blue_player(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(blue_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.x = 300 + (self.number * 5)#物件x座標位置
            self.rect.bottom = HEIGHT-10#物件y座標位置
            
        def update(self):
            pass
        
    class black_player(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(black_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.x = 400 + (self.number * 5)#物件x座標位置
            self.rect.bottom = HEIGHT-10#物件y座標位置
        def update(self):
            pass
    
    class red_player(pygame.sprite.Sprite):
        def __init__(self,number):
            pygame.sprite.Sprite.__init__(self)#初始化
            self.image = pygame.transform.scale(red_img, (75, 75))#物件圖片和調整大小
            self.rect = self.image.get_rect()#物件位置變數
            self.number = number
            self.rect.x = 500 + (self.number * 5)#物件x座標位置
            self.rect.bottom = HEIGHT-10#物件y座標位置
        def update(self):
            pass
           
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    cards = pygame.sprite.Group()
    clicks = pygame.sprite.Group()
    greens = pygame.sprite.Group()
    whites = pygame.sprite.Group()
    blues = pygame.sprite.Group()
    blacks = pygame.sprite.Group()
    reds = pygame.sprite.Group()
    greens_player = pygame.sprite.Group()
    whites_player = pygame.sprite.Group()
    blues_player = pygame.sprite.Group()
    blacks_player = pygame.sprite.Group()
    reds_player = pygame.sprite.Group()
    player = Player()
    players.add(player)
    all_sprites.add(player)
    
    drawn_cards = []#被抽出的卡片
    for i in range(green_number):
        new_green(i)
    for i in range(white_number):
        new_white(i)
    for i in range(blue_number):
        new_blue(i)
    for i in range(black_number):
        new_black(i)
    for i in range(red_number):
        new_red(i)
    for i in range(3):
        for j in range(4):
            r = Random(i+1)
            while r in drawn_cards:
                r = Random(i+1)
            card_info = data[f"level{i+1}"][f"{r+1}"]
            new_card(w = card_info["wprice"],u = card_info["uprice"],g = card_info["gprice"]\
                    ,r = card_info["rprice"],k = card_info["kprice"],level = i+1,color = card_info["Gem_color"]\
                    ,point = card_info["point"],x = j,number = r)
            drawn_cards.append(r)
            
    
    # 遊戲迴圈True
    show_init = True
    Rule_init = True
    End_init = False
    running = True
    while running:
        if show_init:
            close = draw_init()
            if close:
                break
            show_init = False
        if Rule_init:
            close = rule_init()
            if close:
                break
            Rule_init = False
        if End_init:
            close = end_init()
            if close:
                break
            End_init = False
            main()
        clock.tick(FPS)#遊戲迴圈執行速度
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #離開遊戲
                running = False
            elif pygame.mouse.get_pressed()[0] and flag_mousedown == 0: #按滑鼠左鍵
                flag_mousedown = 1
                player.click()
            elif pygame.mouse.get_pressed()[0] == False:
                flag_mousedown = 0
            if player.point >= 15: #結束遊戲
                End_init = True
            elif pygame.mouse.get_pressed()[2]: # 按滑鼠右鍵看規則
                Rule_init = True
    
        # 更新遊戲
        all_sprites.update()
        
        #主程式
        if catch == 3:
            Round += 1
            #變數初始化
            catch = 0
            flag = 1
            catch_green = 0
            catch_white = 0
            catch_blue = 0
            catch_red = 0
            catch_black = 0
        catch_all = catch_green + catch_white + catch_blue + catch_red + catch_black
        
        #拿取寶石
        if player.all_number <= 8 or catch_all > 0:
            if (catch_green == 0 and player.all_number <= 7) or (catch_all > 0 and player.all_number <= 8 \
                and catch_green == 0 and catch == 1) or (catch_all > 0 and player.all_number <= 9 \
                and catch_green == 0 and catch == 2) or (green_number >= 4 and catch_all == 0 \
                or (catch_green == 1 and green_number >= 3 and catch_all == 1)):

                hits = pygame.sprite.groupcollide(greens, clicks, True, True)
                for hit in hits:
                    green_number -= 1
                    new_green_player()
                    if catch_green == 1:
                        catch += 1
                    player.green_number += 1
                    catch_green += 1
                    catch += 1
                    flag = 0
                    item_sound.play()
            if (catch_white == 0 and player.all_number <= 7) or (catch_all > 0 and player.all_number <= 8 and catch_white == 0 and catch == 1) or (catch_all > 0 and player.all_number <= 9 and catch_white == 0 and catch == 2) or (white_number >= 4 and catch_all == 0 or (catch_white == 1 and white_number >= 3 and catch_all == 1)):
                hits = pygame.sprite.groupcollide(whites, clicks, True, True)
                for hit in hits:
                    white_number -= 1
                    new_white_player()
                    if catch_white == 1:
                        catch += 1
                    player.white_number += 1
                    catch_white += 1
                    catch += 1
                    flag = 0
                    item_sound.play()
            if (catch_blue == 0 and player.all_number <= 7) or (catch_all > 0 and player.all_number <= 8 and catch_blue == 0 and catch == 1) or (catch_all > 0 and player.all_number <= 9 and catch_blue == 0 and catch == 2) or (blue_number >= 4 and catch_all == 0 or (catch_blue == 1 and blue_number >= 3 and catch_all == 1)):
                hits = pygame.sprite.groupcollide(blues, clicks, True, True)
                for hit in hits:
                    blue_number -= 1
                    new_blue_player()
                    if catch_blue == 1:
                        catch += 1
                    player.blue_number += 1
                    catch_blue += 1
                    catch += 1
                    flag = 0
                    item_sound.play()
            if (catch_black == 0 and player.all_number <= 7) or (catch_all > 0 and player.all_number <= 8 and catch_black == 0 and catch == 1) or (catch_all > 0 and player.all_number <= 9 and catch_black == 0 and catch == 2) or (black_number >= 4 and catch_all == 0 or (catch_black == 1 and black_number >= 3 and catch_all == 1)):
                hits = pygame.sprite.groupcollide(blacks, clicks, True, True)
                for hit in hits:
                    black_number -= 1
                    new_black_player()
                    if catch_black == 1:
                        catch += 1
                    player.black_number += 1
                    catch_black += 1
                    catch += 1
                    flag = 0
                    item_sound.play()
            if (catch_red == 0 and player.all_number <= 7) or (catch_all > 0 and player.all_number <= 8 and catch_red == 0 and catch == 1) or (catch_all > 0 and player.all_number <= 9 and catch_red == 0 and catch == 2) or (red_number >= 4 and catch_all == 0 or (catch_red == 1 and red_number >= 3 and catch_all == 1)):
                hits = pygame.sprite.groupcollide(reds, clicks, True, True)
                for hit in hits:
                    red_number -= 1
                    new_red_player()
                    if catch_red == 1:
                        catch += 1
                    player.red_number += 1
                    catch_red += 1
                    catch += 1
                    flag = 0
                    item_sound.play()
        #拿取卡牌
        hits = pygame.sprite.groupcollide(cards, clicks, False, False)
        for hit in hits:
            if flag == 1 and player.cards["g"] + player.green_number >= hit.g and player.cards["w"] + player.white_number >= hit.w and player.cards["u"] + player.blue_number >= hit.u and player.cards["k"] + player.black_number >= hit.k and player.cards["r"] + player.red_number >= hit.r:
                Round += 1
                card_sound.play()
                hits = pygame.sprite.groupcollide(cards, clicks, True, True)
                for hit in hits:
                    r = Random(hit.level)
                    while r in drawn_cards:
                        r = Random(hit.level)
                        drawn_cards.sort()
                        try:
                            if drawn_cards[39] == 39:
                                del drawn_cards[0 : 39]
                        except:
                            pass
                    card_info = data[f"level{hit.level}"][f"{r+1}"]
                    new_card(w = card_info["wprice"],u = card_info["uprice"],g = card_info["gprice"],r = card_info["rprice"],k = card_info["kprice"],level = hit.level,color = card_info["Gem_color"],point = card_info["point"],x = hit.x,number = r)
                    drawn_cards.append(r)
                    player.cards[hit.color] += 1
                    player.point += hit.point
                    
                    if player.cards["g"]  < hit.g:
                        for i in range(hit.g - player.cards["g"]):
                            player.click(x = 126,y = HEIGHT-15)
                            green_hits = pygame.sprite.groupcollide(greens_player, clicks, True, True)
                            new_green(green_number)
                            green_number += 1
                            player.green_number -= 1
                    if player.cards["w"]  < hit.w:
                        for i in range(hit.w - player.cards["w"]):
                            player.click(x = 226,y = HEIGHT-15)
                            white_hits = pygame.sprite.groupcollide(whites_player, clicks, True, True)
                            
                            new_white(white_number)
                            white_number += 1
                            player.white_number -= 1
                    if player.cards["u"]  < hit.u:
                        for i in range(hit.u - player.cards["u"]):
                            player.click(x = 326,y = HEIGHT-15)
                            blue_hits = pygame.sprite.groupcollide(blues_player, clicks, True, True)
                            
                            new_blue(blue_number)
                            blue_number += 1
                            player.blue_number -= 1
                    if player.cards["k"]  < hit.k:
                        for i in range(hit.k - player.cards["k"]):
                            player.click(x = 426,y = HEIGHT-15)
                            black_hits = pygame.sprite.groupcollide(blacks_player, clicks, True, True)
                            
                            new_black(black_number)
                            black_number += 1
                            player.black_number -= 1
                    if player.cards["r"]  < hit.r:
                        for i in range(hit.r - player.cards["r"]):
                            player.click(x = 526,y = HEIGHT-15)
                            red_hits = pygame.sprite.groupcollide(reds_player, clicks, True, True)
                            
                            new_red(red_number)
                            red_number += 1
                            player.red_number -= 1
                                
            
    
        
        
    
        # 畫面顯示
        screen.blit(background_img, (0,0))#畫面圖片
        all_sprites.draw(screen)#畫出所有物件
        draw_text(screen, "回合:" + str(Round), 18, WIDTH/2, 50)
        draw_text(screen, str(green_number), 18, WIDTH - 125,100)
        draw_text(screen, str(white_number), 18, WIDTH - 125,200)
        draw_text(screen, str(blue_number), 18, WIDTH - 125,300)
        draw_text(screen, str(black_number), 18, WIDTH - 125,400)
        draw_text(screen, str(red_number), 18, WIDTH - 125,500)
        draw_text(screen, str(player.green_number) + "+" + str(player.cards["g"]), 18, 150,HEIGHT-125,GREEN)
        draw_text(screen, str(player.white_number) + "+" + str(player.cards["w"]), 18, 250,HEIGHT-125)
        draw_text(screen, str(player.blue_number) + "+" + str(player.cards["u"]), 18, 350,HEIGHT-125,(100,149,237))
        draw_text(screen, str(player.black_number) + "+" + str(player.cards["k"]), 18, 450,HEIGHT-125,BLACK)
        draw_text(screen, str(player.red_number) + "+" + str(player.cards["r"]), 18, 550,HEIGHT-125,RED)
        draw_text(screen, "分數:" + str(player.point), 18, 65,HEIGHT-155)
        draw_text(screen,str(f"持有寶石數:{player.all_number}"), 18, 65,HEIGHT-135)
        pygame.display.update()#畫面更新
    pygame.quit()
main()