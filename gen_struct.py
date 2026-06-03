# -*- coding: utf-8 -*-
from fpdf import FPDF
import pypdfium2 as pdfium
from PIL import Image, ImageChops
FD="/usr/share/fonts/truetype/dejavu"
GREENF=(216,231,205); GREENB=(120,150,100)
BLUEF=(206,224,242); BLUEB=(90,120,170)
GREYF=(236,237,239); GREYB=(120,125,135)
ORANGEF=(250,228,198); ORANGEB=(190,150,90)
INK=(25,25,25); ARROW=(80,80,85)

class S(FPDF):
    def __init__(self):
        super().__init__("P","mm","A4"); self.set_auto_page_break(False)
        self.add_font("D","",f"{FD}/DejaVuSans.ttf"); self.add_font("D","B",f"{FD}/DejaVuSans-Bold.ttf")
        self.set_margins(10,10,10)
    def box(self,x,y,w,h,fill,border,title,sub,body,dashed=False,tsize=11):
        self.set_fill_color(*fill); self.set_draw_color(*border); self.set_line_width(0.5)
        if dashed: self.set_dash_pattern(dash=1.6,gap=1.4)
        self.rect(x,y,w,h,"DF")
        if dashed: self.set_dash_pattern()
        self.set_line_width(0.2)
        self.set_font("D","B",tsize); self.set_text_color(*INK); self.set_xy(x,y+2.4); self.cell(w,5,title,align="C")
        cy=y+8.2
        if sub:
            self.set_font("D","I",8.2) if False else self.set_font("D","",8.2)
            self.set_text_color(60,60,60); self.set_xy(x,cy); self.cell(w,4,sub,align="C"); cy+=5.5
        if body:
            self.set_font("D","",7.6); self.set_text_color(40,40,40)
            self.set_xy(x+3,cy+1.5); self.multi_cell(w-6,3.7,body,align="L")
    def arrow(self,x,y1,y2,label=None):
        self.set_draw_color(*ARROW); self.set_line_width(0.5); self.line(x,y1,x,y2)
        self.line(x,y2,x-1.4,y2-2.2); self.line(x,y2,x+1.4,y2-2.2); self.set_line_width(0.2)
        if label:
            self.set_font("D","",8.4); self.set_text_color(40,40,40); self.set_xy(x+1.5,(y1+y2)/2-2.4); self.cell(20,4,label)
    def elbow(self,x0,y0,x1,y2):
        self.set_draw_color(*ARROW); self.set_line_width(0.5)
        ym=y0+5; self.line(x0,y0,x0,ym); self.line(x0,ym,x1,ym); self.line(x1,ym,x1,y2)
        self.line(x1,y2,x1-1.4,y2-2.2); self.line(x1,y2,x1+1.4,y2-2.2); self.set_line_width(0.2)

def render(stage):
    p=S(); p.add_page()
    cx=105
    # Investors (green)
    p.box(63,12,84,15,GREENF,GREENB,"Инвесторы и Участники Проекта","","",tsize=11.5)
    p.arrow(cx,27,33,"100%")
    # Holding (blue)
    p.box(35,33,140,30,BLUEF,BLUEB,"Holding Co","(рекомендуется Великобритания)",
          "Владеет проектом через 100% собственности в PrincipalCo и SalesCo; финансирует проект; распределяет прибыль инвесторам.",tsize=12)
    # split to two
    p.set_draw_color(*ARROW); p.set_line_width(0.5)
    p.line(cx,63,cx,69); p.line(57,69,153,69); p.line(57,69,57,73.5); p.line(153,69,153,73.5)
    for xx in (57,153):
        p.line(xx,73.5,xx-1.4,71.3); p.line(xx,73.5,xx+1.4,71.3)
    p.set_line_width(0.2); p.set_font("D","",8.4); p.set_text_color(40,40,40); p.set_xy(cx+1.5,64.5); p.cell(14,4,"100%")
    # Principal Co (grey)
    if stage==1:
        pbody="IP права на документацию; держатель DOA и Сертификата Типа; общее управление проектом, организация производства и послепродажного обслуживания."
    else:
        pbody="IP права на документацию; держатель DOA и Сертификата Типа; общее управление проектом, сборка самолётов и послепродажное обслуживание на собственных мощностях."
    SUBH=38
    p.box(14,73.5,86,SUBH,GREYF,GREYB,"Principal Co — OEM","(рекомендуется Болгария)",pbody,tsize=11)
    p.box(110,73.5,86,SUBH,GREYF,GREYB,"Sales Co","(рекомендуется Болгария)",
          "Военно-экспортная лицензия; контракты с покупателями; продажа готовых самолётов.",tsize=11)
    if stage==1:
        ay=73.5+SUBH
        p.arrow(57,ay,ay+7,"заказ производства")
        p.box(14,ay+7,182,24,ORANGEF,ORANGEB,"Aero Vodochody — toll / contract manufacturing","(Чехия, независимый завод)",
              "Производит сборку самолётов на основании документации Principal Co, по её заказу и за плату.",dashed=True,tsize=11.5)
    p.output(f"/tmp/struct{stage}.pdf")
    pg=pdfium.PdfDocument(f"/tmp/struct{stage}.pdf")[0].render(scale=6.0).to_pil().convert("RGB")
    bg=Image.new("RGB",pg.size,(255,255,255)); bb=ImageChops.difference(pg,bg).getbbox()
    if bb:
        l,t,r,b=bb; pad=24; pg=pg.crop((max(0,l-pad),max(0,t-pad),min(pg.size[0],r+pad),min(pg.size[1],b+pad)))
    pg.save(f"/home/user/dasp/struct_stage{stage}.png"); print("struct_stage%d.png"%stage, pg.size)

render(1); render(2)
