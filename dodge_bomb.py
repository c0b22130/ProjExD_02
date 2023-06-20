import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta={pg.K_UP:(0,-5),pg.K_DOWN:(0,+5),pg.K_LEFT:(-5,0),pg.K_RIGHT:(+5,0)} 

bb_imgs=[]  #拡大爆弾のリスト
accs=[a for a in range(1,11)]  #加速度のリスト


def offscreen_judge(rct: pg.Rect) -> tuple[bool,bool]:
    """
    こうかとんRect、爆弾Rectが画面外 or 画面内かを判定する関数
    引数:こうかとんRect or 爆弾Rect
    戻り値:横方向、縦方向の判定結果タプル（True:画面内/False:画面外）
    """
    yoko, tate = True, True
    if rct.left<0 or WIDTH<rct.right:  #yoko
       yoko=False
    if rct.top<0 or HEIGHT<rct.bottom:  #tate
        tate=False
    return yoko,tate                                                                                                               
                          

# def load_imgs():
#     kk_img = pg.image.load("ex02/fig/3.png")  #こうかとん
#     kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
#     kk_img_re = pg.transform.flip(kk_img,True,False)
#     kk_rct=kk_img.get_rect()
#     kk_rct.center=800,450
#     kk_imgs={
#     (-5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
#     (-5,-5):pg.transform.rotozoom(kk_img, 45, 1.0),
#     (0,-5):pg.transform.rotozoom(kk_img_re, 90, 1.0),
#     (+5,-5):pg.transform.rotozoom(kk_img_re, 135, 1.0),
#     (+5,0):pg.transform.rotozoom(kk_img_re, 180, 1.0),
#     (+5,+5):pg.transform.rotozoom(kk_img_re, 225, 1.0),
#     (0,+5):pg.transform.rotozoom(kk_img_re, 270, 1.0),
#     (-5,+5):pg.transform.rotozoom(kk_img, 315, 1.0)
#     }
#     return kk_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")  #BG
    go_img = pg.image.load("ex02/fig/4.png")
    go_rct=go_img.get_rect()
    kk_img = pg.image.load("ex02/fig/3.png")  #こうかとん
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_re = pg.transform.flip(kk_img,True,False)
    go_img = pg.transform.rotozoom(go_img, 0, 10.0)
    # こうかとんSurface（kk_img）からこうかとんRect（kk_rct）を抽出する
    kk_rct=kk_img.get_rect()
    kk_rct.center=800,450
    bomb=pg.Surface((20,20))
    pg.draw.circle(bomb,(255,0,0),(10,10),10)  #爆弾
    x=random.randint(0,WIDTH)
    y=random.randint(0,HEIGHT)
    bomb.set_colorkey((0,0,0))  # 黒い部分を透明にする
    # 爆弾Surface（bd_img）から爆弾Rect（bd_rct）を抽出する
    bomb_rct=bomb.get_rect()
    # 爆弾Rectの中心座標を乱数で指定する
    bomb_rct.center = x,y  #爆弾をランダムに配置

    #演習２用
    for r in range(1, 11): 
        bb_img= pg.Surface((20*r, 20*r)) 
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r) 
        bb_imgs.append(bb_img)


    vx,vy=+5,+5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bomb_rct):  #衝突したら
            screen.blit(go_img, [630,60])
            pg.display.update()
            clock.tick(0.4)
            return  #GameOver
        
        key_lst=pg.key.get_pressed()
        sum_mv=[0,0] # 合計移動量
        for k,mv in delta.items():  #移動
            if key_lst[k]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        kk_rct.move_ip(sum_mv)

        if offscreen_judge(kk_rct) != (True,True):  #こうかとんが画面の端に来たらそこから進まない
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)

        bomb_rct.move_ip(vx,vy)
        yoko,tate=offscreen_judge(bomb_rct)  #ボールが画面の端に来たら跳ね返る
        if not yoko:
            vx*=-1
        if not tate:
            vy*=-1

        screen.blit(bomb,bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()