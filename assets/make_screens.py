# -*- coding: utf-8 -*-
"""Десктопные скриншоты 1280x720 для Яндекс.Игр — воссоздают интерфейс игры."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT   = os.path.dirname(os.path.abspath(__file__))
EMOJI = "C:/Windows/Fonts/seguiemj.ttf"
BLACK = "C:/Windows/Fonts/ariblk.ttf"
BOLD  = "C:/Windows/Fonts/arialbd.ttf"
REG   = "C:/Windows/Fonts/arial.ttf"

GOLD=(255,180,60); GOLD2=(255,217,138); CREAM=(244,230,212)
LINE=(90,60,34); DIM=(169,138,107); GREEN=(110,227,110); RED=(255,77,77)
PANEL=(59,39,24); PANEL2=(41,26,16); DARKP=(28,18,11)
W,H=1280,720

def font(p,s): return ImageFont.truetype(p,s)
def emoji(ch,px):
    st=109; f=font(EMOJI,st)
    t=Image.new("RGBA",(st*2,st*2),(0,0,0,0))
    ImageDraw.Draw(t).text((st*0.5,st*0.4),ch,font=f,embedded_color=True,anchor="mm")
    t=t.crop(t.getbbox()); sc=px/max(t.size)
    return t.resize((int(t.width*sc),int(t.height*sc)),Image.LANCZOS)
def pc(base,l,cx,cy): base.alpha_composite(l,(int(cx-l.width/2),int(cy-l.height/2)))

import re
_EMO=re.compile(r'[\U0001F000-\U0001FAFF←-⇿⌀-➿⬀-⯿️⃣❤]+')
def rich_width(d,parts,f,epx):
    w=0
    for kind,val in parts:
        w+= (epx+3) if kind=="e" else d.textlength(val,font=f)
    return w
def split_rich(s):
    """Разбивает строку на текст и эмодзи-руны."""
    parts=[]; i=0
    for m in _EMO.finditer(s):
        if m.start()>i: parts.append(("t",s[i:m.start()]))
        for ch in _cluster(m.group()): parts.append(("e",ch))
        i=m.end()
    if i<len(s): parts.append(("t",s[i:]))
    return parts
def _cluster(s):
    out=[]; i=0
    while i<len(s):
        ch=s[i]; j=i+1
        while j<len(s) and s[j]=='️': j+=1
        out.append(s[i:j]); i=j
    return out
def rich(img,d,x,y,s,f,fill,epx,anchor="lm"):
    parts=split_rich(s)
    total=rich_width(d,parts,f,epx)
    cx = x-total/2 if anchor=="mm" else x
    for kind,val in parts:
        if kind=="e":
            im=emoji(val,epx); img.alpha_composite(im,(int(cx),int(y-im.height/2))); cx+=epx+3
        else:
            d.text((cx,y),val,font=f,fill=fill,anchor="lm"); cx+=d.textlength(val,font=f)
    return cx

def bg():
    img=Image.new("RGB",(W,H),(21,15,10))
    px=img.load()
    for y in range(H):
        t=y/(H-1); r=int(74-53*t); g=int(47-32*t); b=int(28-18*t)
        for x in range(W): px[x,y]=(r,g,b)
    img=img.convert("RGBA")
    st=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(st)
    for x in range(0,W,76): sd.rectangle((x,0,x+38,H),fill=(0,0,0,26))
    img.alpha_composite(st)
    gl=Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(gl).ellipse((-200,-360,W+200,180),fill=(255,180,60,40))
    img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(80)))
    return img

def rr(d,box,rad,fill=None,outline=None,width=1):
    d.rounded_rectangle(box,radius=rad,fill=fill,outline=outline,width=width)

def stat(img,d,x,y,txt,val,bad=False):
    f=font(BOLD,20); fv=font(BLACK,20)
    tw=rich_width(d,split_rich(txt+" "),f,20); vw=rich_width(d,split_rich(val),fv,20)
    box=(x,y,x+tw+vw+28,y+42)
    rr(d,box,10,fill=PANEL,outline=LINE,width=2)
    rich(img,d,x+14,y+21,txt,f,CREAM,20)
    rich(img,d,x+14+tw,y+21,val,fv,(RED if bad else GOLD),20)
    return box[2]

def hud(img,d,money,day,rent,hearts,tsec):
    rr(d,(0,0,W,58),0,fill=(26,17,9))
    d.line((0,58,W,58),fill=LINE,width=3)
    x=24
    x=stat(img,d,x,8,"💰",f"{money}")+10
    x=stat(img,d,x,8,"📅 Смена",f"{day}")+10
    x=stat(img,d,x,8,"🏦 Аренда",f"{rent}")+10
    x=stat(img,d,x,8,"🧠",hearts)+10
    x=stat(img,d,x,8,"⏱",f"{tsec}")+10
    # timer bar
    rr(d,(0,58,W,66),0,fill=(26,17,9))
    frac=tsec/60
    for i in range(int(W*frac)):
        t=i/W; col=(int(110+145*t),int(227-47*t),int(110-50*t))
        d.line((i,58,i,65),fill=col)

def cust_card(img,d,x,y,face,order_items,say,pat,sel=False,pay=None,hint=""):
    w,hh=210,220
    fill=PANEL2 if not pay else (61,52,24)
    oc=GOLD if sel else (201,160,44) if pay else LINE
    rr(d,(x,y,x+w,y+hh),16,fill=fill,outline=oc,width=3 if sel else 3)
    # hint
    rr(d,(x-8,y-10,x+22,y+12),7,fill=GOLD)
    d.text((x+7,y+1),hint,font=font(BLACK,14),fill=(42,22,6),anchor="mm")
    if pay: pc(img,emoji("💰",26),x+w-6,y-2)
    pc(img,emoji(face,54),x+w/2,y+38)
    if pay:
        d.text((x+w/2,y+80),"Товар отдан. Дал",font=font(REG,13),fill=CREAM,anchor="mm")
        d.text((x+w/2,y+100),f"{pay[0]} ₽",font=font(BLACK,20),fill=GOLD,anchor="mm")
        d.text((x+w/2,y+124),f"Ценник: {pay[1]} ₽",font=font(REG,13),fill=CREAM,anchor="mm")
    else:
        ox=x+w/2-(len(order_items)*46)/2+23
        for em,q,done in order_items:
            bw=42
            bx=ox-bw/2
            rr(d,(bx,y+72,bx+bw,y+100),8,fill=DARKP,outline=(GREEN if done else (107,71,38)),width=2)
            pc(img,emoji(em,20),ox-8,y+86)
            d.text((ox+12,y+86),f"×{q}",font=font(BLACK,15),fill=(GREEN if done else CREAM),anchor="mm")
            ox+=bw+4
    # say
    d.text((x+w/2,y+hh-42),f"«{say}»",font=font(REG,12),fill=DIM,anchor="mm")
    # patience
    rr(d,(x+10,y+hh-20,x+w-10,y+hh-13),4,fill=(26,17,9))
    pw=(w-20)*pat
    pcol=GREEN if pat>0.5 else GOLD if pat>0.25 else RED
    rr(d,(x+10,y+hh-20,x+10+pw,y+hh-13),4,fill=pcol)

def tray(img,d,y,label,chips,cash=False,total=None):
    rr(d,(30,y,W-30,y+70),14,fill=(255,180,60,18) if cash else (0,0,0,90),
       outline=(201,160,44) if cash else LINE,width=3)
    d.text((48,y+35),label,font=font(BLACK,15),fill=DIM,anchor="lm")
    cx=48+d.textlength(label,font=font(BLACK,15))+24
    for c in chips:
        if cash:
            tw=d.textlength(c,font=font(BLACK,15))
            rr(d,(cx,y+18,cx+tw+18,y+52),9,fill=(74,47,22),outline=GOLD,width=2)
            d.text((cx+9,y+35),c,font=font(BLACK,15),fill=GOLD2,anchor="lm")
            cx+=tw+28
        else:
            rr(d,(cx,y+18,cx+40,y+52),9,fill=(74,47,22),outline=GOLD,width=2)
            pc(img,emoji(c,22),cx+20,y+35); cx+=50
    if total is not None:
        d.text((W-48,y+35),f"= {total} ₽",font=font(BLACK,20),fill=GOLD,anchor="rm")

def shelf(img,d,y,items,cash=False):
    cols=len(items); gap=8; mx=30
    cw=(W-2*mx-gap*(cols-1))/cols
    for i,(em,nm,key,kind) in enumerate(items):
        x=mx+i*(cw+gap)
        if kind=="bill": fill=(47,74,42); oc=(79,122,69)
        elif kind=="coin": fill=(74,65,22); oc=(122,108,38)
        else: fill=(74,47,22); oc=LINE
        rr(d,(x,y,x+cw,y+92),14,fill=fill,outline=oc,width=3)
        d.text((x+cw-8,y+8),key,font=font(REG,12),fill=DIM,anchor="rm")
        pc(img,emoji(em,34 if not cash else 26),x+cw/2,y+34)
        d.text((x+cw/2,y+74),nm,font=font(BOLD,14),fill=(198,240,189) if kind=="bill" else CREAM,anchor="mm")

def buttons(img,d,y,left,right,left_red=True,right_green=False):
    mx=30; gap=10; bw=(W-2*mx-gap)/2
    def btn(x,txt,c1,c2,shadow,txtcol):
        rr(d,(x,y,x+bw,y+56),12,fill=c1,outline=None)
        rich(img,d,x+bw/2,y+28,txt,font(BLACK,22),txtcol,24,anchor="mm")
    btn(mx,left,(192,58,34) if left_red else (74,47,22),None,None,(42,13,6) if left_red else GOLD)
    btn(mx+bw+gap,right,(63,155,44) if right_green else (255,180,60),None,None,(13,42,6) if right_green else (42,22,0))

def banner(img,d,txt):
    f=font(BLACK,28); tw=rich_width(d,split_rich(txt),f,28)
    x0=(W-tw)/2-24
    rr(d,(x0,70,W-x0,124),14,fill=(184,31,0),outline=(255,208,160),width=3)
    rich(img,d,W/2,98,txt,f,(255,255,255),28,anchor="mm")

FLAV=[("🦀","Крабовые","1","x"),("🥓","Бекон","2","x"),("🧅","Лук-сметана","3","x"),
      ("🌶️","Паприка","4","x"),("🧀","Сыр","5","x"),("🐟","Вобла","6","x")]
CASH=[("🪙","10 ₽","1","coin"),("🪙","50 ₽","2","coin"),("💵","100 ₽","3","bill"),
      ("💵","500 ₽","4","bill"),("💶","1000 ₽","5","bill")]

# ---------- 1: ПРИЁМ ЗАКАЗА ----------
def screen_order():
    img=bg(); d=ImageDraw.Draw(img)
    hud(img,d,340,1,395,"❤❤❤❤❤",47)
    cy=96
    cust_card(img,d,340,cy,"🧔",[("🦀",1,True),("🧀",1,False)],"Мамка сказала эти брать.",0.72,sel=True,hint="Q")
    cust_card(img,d,560,cy,"👵",[("🌶️",2,False)],"Я тут с 8 утра стою.",0.5,hint="W")
    cust_card(img,d,780,cy,"👮",[("🐟",1,False)],"Быстрее, у меня матч.",0.85,hint="E")
    tray(img,d,332,"ПРИЛАВОК:",["🦀","🧀"])
    shelf(img,d,418,FLAV)
    buttons(img,d,524,"СМЕСТИ ВСЁ 🧹","ВЫДАТЬ 🤝")
    # подпись
    d.text((W/2,650),"Собери ровно заказ и жми ВЫДАТЬ",font=font(BOLD,20),fill=DIM,anchor="mm")
    img.convert("RGB").save(os.path.join(OUT,"screen-1-order.png"))

# ---------- 2: ОТСЧЁТ СДАЧИ ----------
def screen_change():
    img=bg(); d=ImageDraw.Draw(img)
    hud(img,d,712,2,776,"❤❤❤❤🖤",38)
    cy=96
    cust_card(img,d,430,cy,"🐻",None,"Сдачу до рубля, я считаю.",0.6,sel=True,pay=(500,270),hint="Q")
    cust_card(img,d,650,cy,"🦊",[("🥓",1,False)],"Дай пакетик, дай пакетик.",0.9,hint="W")
    tray(img,d,332,"СДАЧА:",["100 ₽","100 ₽","10 ₽","10 ₽","10 ₽"],cash=True,total=230)
    shelf(img,d,418,CASH,cash=True)
    buttons(img,d,524,"ЗАБРАТЬ ОБРАТНО","ОТДАТЬ СДАЧУ 💸",left_red=False,right_green=True)
    d.text((W/2,650),"Отсчитай сдачу купюрами — точно до рубля дают чаевые",font=font(BOLD,20),fill=DIM,anchor="mm")
    img.convert("RGB").save(os.path.join(OUT,"screen-2-change.png"))

# ---------- 3: НАПЛЫВ ----------
def screen_rush():
    img=bg(); d=ImageDraw.Draw(img)
    # красноватый оттенок
    ov=Image.new("RGBA",(W,H),(120,20,0,50)); img.alpha_composite(ov)
    hud(img,d,1980,4,1240,"❤❤❤🖤🖤",22)
    banner(img,d,"🔥 НАПЛЫВ! ЦЕНЫ ×2 — 6")
    cy=140
    cust_card(img,d,120,cy,"🤡",[("🦀",2,False)],"Живее, кабан!",0.35,hint="Q")
    cust_card(img,d,350,cy,"👽",[("🧅",1,True),("🌶️",1,False)],"Мне для собаки. Себе тоже.",0.55,sel=True,hint="W")
    cust_card(img,d,580,cy,"🤠",[("🧀",1,False)],"На день рождения.",0.7,hint="E")
    cust_card(img,d,810,cy,"🧟",[("🐟",2,False)],"Час стою! Час!",0.2,hint="R")
    tray(img,d,376,"ПРИЛАВОК:",["🧅"])
    shelf(img,d,462,FLAV)
    d.text((W/2,650),"Раз за смену — 10 секунд толпы и двойной ценник",font=font(BOLD,20),fill=GOLD2,anchor="mm")
    img.convert("RGB").save(os.path.join(OUT,"screen-3-rush.png"))

# ---------- 4: МОДЕРНИЗАЦИЯ ----------
def screen_upgrades():
    img=bg(); d=ImageDraw.Draw(img)
    cw,ch=760,600; x0=(W-cw)/2; y0=(H-ch)/2
    rr(d,(x0,y0,x0+cw,y0+ch),18,fill=(35,23,14),outline=LINE,width=4)
    d.text((W/2,y0+40),"СМЕНА 2 ЗАКРЫТА",font=font(BLACK,34),fill=GOLD,anchor="mm")
    d.text((W/2,y0+72),"Ни один клиент не ушёл. Кабан доволен, аж хрюкает.",font=font(REG,15),fill=DIM,anchor="mm")
    rows=[("Обслужено рыл","16"),("Выручка с чипсов","2340 ₽"),("Чаевые","927 ₽"),
          ("Аренда ларька","−395 ₽"),("В кассе осталось","2872 ₽")]
    yy=y0+110
    d.line((x0+30,yy,x0+cw-30,yy),fill=LINE,width=2)
    for i,(a,b) in enumerate(rows):
        yy+=38
        big=(i==len(rows)-1)
        d.text((x0+34,yy),a,font=font(BOLD,17 if not big else 19),fill=CREAM,anchor="lm")
        col=RED if b.startswith("−") else GOLD
        d.text((x0+cw-34,yy),b,font=font(BLACK,17 if not big else 20),fill=col,anchor="rm")
    d.line((x0+30,yy+22,x0+cw-30,yy+22),fill=LINE,width=2)
    ups=[("💸 Жирный ценник","Каждая пачка дороже на 20%","420 ₽"),
         ("📺 Телик в очереди","Клиенты терпят на 20% дольше","380 ₽"),
         ("🥫 Банка для чаевых","Чаевые +50%","340 ₽"),
         ("📢 Баннер у трассы","Больше клиентов — больше бабок","500 ₽")]
    ux=x0+30; uy=yy+38; uw=(cw-60-9)/2; uh=78
    for i,(t,dd,p) in enumerate(ups):
        gx=ux+(i%2)*(uw+9); gy=uy+(i//2)*(uh+9)
        rr(d,(gx,gy,gx+uw,gy+uh),13,fill=PANEL,outline=LINE,width=3)
        rich(img,d,gx+14,gy+19,t,font(BLACK,16),CREAM,18)
        d.text((gx+14,gy+42),dd,font=font(REG,12),fill=DIM,anchor="lm")
        d.text((gx+14,gy+62),p,font=font(BLACK,15),fill=GOLD,anchor="lm")
    # кнопка
    by=y0+ch-56
    rr(d,(W/2-160,by,W/2+160,by+44),12,fill=GOLD)
    d.text((W/2,by+22),"СЛЕДУЮЩАЯ СМЕНА",font=font(BLACK,20),fill=(42,22,0),anchor="mm")
    img.convert("RGB").save(os.path.join(OUT,"screen-4-upgrades.png"))

screen_order(); screen_change(); screen_rush(); screen_upgrades()
print("screens saved")
