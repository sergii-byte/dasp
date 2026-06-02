# -*- coding: utf-8 -*-
"""Рендер схем меморандума в отдельные PNG (для вставки в DOCX)."""
from fpdf import FPDF
import pypdfium2 as pdfium
from PIL import Image

FD = "/usr/share/fonts/truetype/dejavu"
NAVY=(20,38,71); STEEL=(70,90,120); GREY=(95,95,95); LIGHT=(243,245,249)
LINE=(205,210,220); ACC=(140,25,25); INK=(28,28,28); CONN=(95,115,145); BOXF=(236,240,247)

class A(FPDF):
    def __init__(self):
        super().__init__("P","mm","A4")
        self.set_auto_page_break(False)
        self.add_font("D","",f"{FD}/DejaVuSans.ttf")
        self.add_font("D","B",f"{FD}/DejaVuSans-Bold.ttf")
        self.set_margins(18,12,18)
        self.cw=174

    def structure(self, stage, compact=False, show_plant=True):
        cx=105; sub_size=7.0
        def box(x,y,w,h,title,sub,dashed=False):
            self.set_fill_color(*((255,255,255) if dashed else BOXF)); self.set_draw_color(*NAVY); self.set_line_width(0.5)
            if dashed: self.set_dash_pattern(dash=1.3,gap=1.3)
            self.rect(x,y,w,h,"DF")
            if dashed: self.set_dash_pattern()
            self.set_line_width(0.2); self.set_font("D","B",8.2); self.set_text_color(*NAVY)
            self.set_xy(x,y+1.8); self.cell(w,3.8,title,align="C")
            if sub:
                self.set_font("D","",sub_size); self.set_text_color(75,75,75)
                self.set_xy(x+1.5,y+5.7); self.multi_cell(w-3,3.3,sub,align="C",new_x="LMARGIN",new_y="NEXT")
        def vconn(x,y1,y2,tip=False):
            self.set_draw_color(*CONN); self.set_line_width(0.4); self.line(x,y1,x,y2)
            if tip: self.line(x-1.2,y2-1.8,x,y2); self.line(x+1.2,y2-1.8,x,y2)
            self.set_line_width(0.2)
        def hconn(x1,x2,y):
            self.set_draw_color(*CONN); self.set_line_width(0.4); self.line(x1,y,x2,y); self.set_line_width(0.2)
        def label(x,y,txt):
            self.set_font("D","",6.7); self.set_text_color(*GREY); self.set_xy(x,y); self.cell(34,3,txt)
        y=self.get_y()+1
        box(72,y,66,8,"ИНВЕСТОРЫ","")
        vconn(cx,y+8,y+12,tip=True)
        hh=11 if compact else 12
        box(33,y+12,144,hh,"ХОЛДИНГ — Великобритания (рекомендуется)","владеет проектом и правами на разработку; распределяет прибыль инвесторам")
        busy=y+12+hh
        vconn(cx,busy,busy+3); hconn(63,147,busy+3); vconn(63,busy+3,busy+7,tip=True); vconn(147,busy+3,busy+7,tip=True)
        label(cx-16,busy+0.2,"владеет 100% обеих компаний")
        oy=busy+7; oh=13 if compact else 15
        if stage==1:
            box(24,oy,78,oh,"PrincipalCo — Болгария","производство и закупки; владеет проектом и правами на разработку")
            box(108,oy,78,oh,"SalesCo — Болгария","военно-экспортная лицензия; продажа готовых самолётов")
            if show_plant:
                ay=oy+oh; vconn(63,ay,ay+5,tip=True); label(66,ay+0.5,"сборка по заказу")
                box(33,ay+5,144,11,"Aero Vodochody — Чехия  (вне группы)","независимый завод: собирает самолёт по заказу за плату",dashed=True)
        else:
            box(24,oy,78,oh,"Производственная компания — Польша или Болгария","собственный завод: сборка самолёта внутри группы")
            box(108,oy,78,oh,"SalesCo — Болгария","военно-экспортная лицензия; продажа готовых самолётов")

    def flow_diagram(self, steps):
        y=self.get_y()+2; n=len(steps); gap=18; bw=(self.cw-gap*(n-1))/n; h=21; x=18
        for i,(amount,labl,arrow) in enumerate(steps):
            self.set_fill_color(*((214,228,214) if i==n-1 else BOXF)); self.set_draw_color(*NAVY); self.set_line_width(0.4)
            self.rect(x,y,bw,h,"DF"); self.set_line_width(0.2)
            self.set_font("D","B",9), self.set_text_color(*NAVY); self.set_xy(x,y+2.8); self.cell(bw,5,amount,align="C")
            self.set_font("D","",6.8); self.set_text_color(75,75,75); self.set_xy(x+1.5,y+8.6); self.multi_cell(bw-3,3.1,labl,align="C",new_x="LMARGIN",new_y="NEXT")
            if i>0:
                ax=x; ay=y+h/2; self.set_draw_color(*CONN); self.set_line_width(0.5)
                self.line(ax-gap,ay,ax-1.2,ay); self.line(ax-3,ay-1.4,ax,ay); self.line(ax-3,ay+1.4,ax,ay); self.set_line_width(0.2)
                if arrow:
                    red=arrow.startswith("−"); self.set_font("D","B",6.3); self.set_text_color(*(ACC if red else (90,110,90)))
                    self.set_xy(ax-gap,ay-4.3); self.cell(gap,3,arrow,align="C")
            x+=bw+gap

    def control_split(self):
        y=self.get_y()+2; NV=NAVY; th=13
        self.set_draw_color(*NV); self.set_line_width(0.45)
        self.set_fill_color(255,255,255); self.set_dash_pattern(dash=1.3,gap=1.3); self.rect(20,y,74,th,"DF"); self.set_dash_pattern()
        self.set_fill_color(*BOXF); self.rect(100,y,74,th,"DF"); self.set_line_width(0.2)
        self.set_font("D","B",8.2); self.set_text_color(*NV)
        self.set_xy(20,y+1.8); self.cell(74,4,"Экономическое участие",align="C")
        self.set_xy(100,y+1.8); self.cell(74,4,"Право голоса и контроль",align="C")
        self.set_font("D","",7.0); self.set_text_color(75,75,75)
        self.set_xy(21.5,y+5.8); self.multi_cell(71,3.2,"все инвесторы, включая инвесторов вне НАТО — получают прибыль",align="C",new_x="LMARGIN",new_y="NEXT")
        self.set_xy(101.5,y+5.8); self.multi_cell(71,3.2,"только лица НАТО и ЕС: директора с допуском, «золотая акция»",align="C",new_x="LMARGIN",new_y="NEXT")
        by=y+th+12; self.set_fill_color(*BOXF); self.set_draw_color(*NV); self.set_line_width(0.5); self.rect(52,by,90,13,"DF"); self.set_line_width(0.2)
        self.set_font("D","B",8.3); self.set_text_color(*NV); self.set_xy(52,by+2); self.cell(90,4,"SalesCo — держатель экспортной лицензии",align="C")
        self.set_font("D","",7.0); self.set_text_color(75,75,75); self.set_xy(53.5,by+6.2); self.multi_cell(87,3.2,"Болгария · член НАТО и ЕС",align="C",new_x="LMARGIN",new_y="NEXT")
        self.set_draw_color(*CONN); self.set_line_width(0.5)
        self.set_dash_pattern(dash=1.3,gap=1.3); self.line(57,y+th,75,by); self.set_dash_pattern()
        self.line(75,by,73.5,by-1.8); self.line(75,by,76.4,by-1.6)
        self.line(137,y+th,119,by); self.line(119,by,120.5,by-1.8); self.line(119,by,117.6,by-1.6); self.set_line_width(0.2)
        self.set_font("D","",6.6); self.set_text_color(*GREY)
        self.set_xy(40,y+th+4); self.cell(40,3,"прибыль"); self.set_xy(135,y+th+4); self.cell(40,3,"решения и управление")

    def jurisdiction_map(self):
        y=self.get_y()+2
        cards=[("Великобритания","Холдинг","0%","на дивиденды","НАТО"),("Болгария","Операции и продажи","10%","на прибыль","НАТО и ЕС")]
        n=len(cards); gap=8; cw=min((self.cw-gap*(n-1))/n, 80); ch=32
        total=cw*n+gap*(n-1); x=18+(self.cw-total)/2
        for name,role,rate,rlab,tag in cards:
            self.set_fill_color(*BOXF); self.set_draw_color(*NAVY); self.set_line_width(0.4); self.rect(x,y,cw,ch,"DF")
            self.set_fill_color(*NAVY); self.rect(x,y,cw,1.8,"F"); self.set_line_width(0.2)
            self.set_font("D","B",8.6); self.set_text_color(*NAVY); self.set_xy(x,y+3.4); self.cell(cw,4,name,align="C")
            self.set_font("D","",6.8); self.set_text_color(75,75,75); self.set_xy(x,y+8); self.cell(cw,3.5,role,align="C")
            self.set_font("D","B",15); self.set_text_color(*NAVY); self.set_xy(x,y+12.5); self.cell(cw,7,rate,align="C")
            self.set_font("D","",6.6); self.set_text_color(95,95,95); self.set_xy(x,y+20.3); self.cell(cw,3,rlab,align="C")
            self.set_font("D","",6.4); self.set_text_color(*STEEL); self.set_xy(x,y+24.5); self.cell(cw,3,tag,align="C")
            x+=cw+gap

    def bar_chart(self, items):
        y0=self.get_y()+6; maxh=38; base=y0+maxh; maxv=max(v for v,_,_,_ in items); n=len(items); gap=12; bw=(self.cw-gap*(n-1))/n; x=18
        self.set_draw_color(*LINE); self.line(18,base,18+self.cw,base)
        for v,labl,load,hl in items:
            h=maxh*v/maxv
            self.set_fill_color(*((210,226,210) if hl else BOXF)); self.set_draw_color(*((40,110,60) if hl else NAVY)); self.set_line_width(0.4)
            self.rect(x,base-h,bw,h,"DF"); self.set_line_width(0.2)
            self.set_font("D","B",9); self.set_text_color(*NAVY); self.set_xy(x,base-h-5.2); self.cell(bw,4,f"{v:,}".replace(',',' ')+" €",align="C")
            self.set_font("D","",7.4); self.set_text_color(90,90,90); self.set_xy(x,base-6.5); self.cell(bw,4,"нагрузка "+load,align="C")
            self.set_font("D","",6.9); self.set_text_color(75,75,75); self.set_xy(x,base+1.5); self.multi_cell(bw,3.2,labl,align="C",new_x="LMARGIN",new_y="NEXT")
            x+=bw+gap

    def cashflow_chart(self, data, breakeven_idx):
        y0=self.get_y()+4; above,below=22.0,22.0; zero_y=y0+above
        rng=max(max(v for _,v in data), -min(v for _,v in data)); scale=min(above/rng,below/rng)*0.92
        n=len(data); gap=2.5; bw=(self.cw-gap*(n-1))/n; x=18
        self.set_draw_color(120,130,150); self.set_line_width(0.4); self.line(18,zero_y,18+self.cw,zero_y); self.set_line_width(0.2)
        for i,(lbl,v) in enumerate(data):
            h=abs(v)*scale
            if v>=0:
                self.set_fill_color(40,120,70); self.set_draw_color(30,100,55); self.rect(x,zero_y-h,bw,h,"DF")
                self.set_font("D","B",6.2); self.set_text_color(30,100,55); self.set_xy(x-1,zero_y-h-3.4); self.cell(bw+2,3,("+%d"%v),align="C")
            else:
                self.set_fill_color(*BOXF); self.set_draw_color(*NAVY); self.rect(x,zero_y,bw,h,"DF")
                self.set_font("D","",6.0); self.set_text_color(110,110,110); self.set_xy(x-1,zero_y+h+0.5); self.cell(bw+2,3,str(v),align="C")
            if i==breakeven_idx:
                lx=x-gap/2
                self.set_draw_color(*ACC); self.set_line_width(0.6); self.set_dash_pattern(dash=1.5,gap=1.2)
                self.line(lx,y0-3,lx,zero_y+below+1); self.set_dash_pattern(); self.set_line_width(0.2)
                self.set_font("D","B",6.4); self.set_text_color(*ACC); self.set_xy(lx-14,y0-5.5); self.cell(28,3,"окупаемость",align="C")
            x+=bw+gap
        x=18; self.set_font("D","",6.4); self.set_text_color(90,90,90)
        for lbl,v in data:
            self.set_xy(x,y0+above+below+0.5); self.cell(bw,3,lbl,align="C"); x+=bw+gap

    def gantt(self, tasks, total=38):
        y0=self.get_y()+5; label_w=70; tx=18+label_w; tw=self.cw-label_w; row_h=7.5
        self.set_font("D","",6.4); self.set_text_color(120,120,120)
        for m in (0,12,24,36):
            gx=tx+tw*m/total; self.set_draw_color(*LINE); self.set_line_width(0.2); self.line(gx,y0-3,gx,y0+row_h*len(tasks))
            self.set_xy(gx-6,y0-6); self.cell(12,3,("%d мес."%m) if m else "старт",align="C")
        for i,(label,s,e) in enumerate(tasks):
            ry=y0+i*row_h
            self.set_font("D","",7.4); self.set_text_color(*INK); self.set_xy(18,ry+1.4); self.multi_cell(label_w-2,3.2,label,new_x="LMARGIN",new_y="TOP")
            bx=tx+tw*s/total; bw2=max(tw*(e-s)/total,1.5); bh=row_h-3.2; cy=ry+1+bh/2
            self.set_fill_color(*NAVY); self.set_draw_color(*NAVY); self.rect(bx,ry+1,bw2,bh,"DF")
            if e>=total:  # ongoing — стрелка вправо
                tip=bx+bw2+3
                self.set_fill_color(*NAVY)
                try:
                    self.polygon([(bx+bw2,cy-2.2),(bx+bw2,cy+2.2),(tip,cy)],style="F")
                except Exception:
                    self.set_line_width(0.6); self.line(bx+bw2,cy-2.2,tip,cy); self.line(bx+bw2,cy+2.2,tip,cy); self.set_line_width(0.2)

def render(name, fn):
    a=A(); a.add_page(); a.set_y(14); fn(a); a.output(f"/tmp/{name}.pdf")
    page=pdfium.PdfDocument(f"/tmp/{name}.pdf")[0].render(scale=6.0).to_pil().convert("RGB")
    # autocrop white
    from PIL import ImageChops
    bg=Image.new("RGB",page.size,(255,255,255))
    diff=ImageChops.difference(page,bg); bbox=diff.getbbox()
    if bbox:
        l,t,r,b=bbox; pad=18
        page=page.crop((max(0,l-pad),max(0,t-pad),min(page.size[0],r+pad),min(page.size[1],b+pad)))
    page.save(f"/home/user/dasp/assets_{name}.png")
    print("wrote assets_"+name+".png", page.size)

render("summary", lambda a: a.structure(1,compact=True,show_plant=False))
render("jurmap", lambda a: a.jurisdiction_map())
render("stage1", lambda a: a.structure(1,compact=False,show_plant=True))
render("stage2", lambda a: a.structure(2,compact=False))
render("flow", lambda a: a.flow_diagram([("1 000 000 €","операционная прибыль · Болгария",None),("900 000 €","после налога на прибыль","−10% налог"),("900 000 €","в холдинге · Великобритания","0%"),("900 000 €","выплата инвестору","0%")]))
render("bars", lambda a: a.bar_chart([(900000,"Болгария\n10%","10%",True),(840000,"Румыния\n16%","16%",False),(810000,"Польша\n19%","19%",False),(790000,"Чехия\n21%","21%",False)]))
render("control", lambda a: a.control_split())
render("cashflow", lambda a: a.cashflow_chart([("1",-150),("2",-320),("3",-420),("4",-348),("5",-276),("6",-180),("7",-84),("8",60),("9",204),("10",348),("11",492)], 7))
render("gantt", lambda a: a.gantt([("Двигатель, крыло, КД, макет, 1-й опытный",0,14),("2-й опытный (испытания на прочность)",0,18),("3-й и 4-й опытные (крыло, вооружение)",0,22),("Все виды испытаний",14,36),("Предсерийный самолёт заказчику",30,36),("Серийное производство (с 37-го мес.)",36,40)],total=40))
print("done")
