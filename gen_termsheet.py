# -*- coding: utf-8 -*-
from fpdf import FPDF
FD="/usr/share/fonts/truetype/dejavu"
NAVY=(20,35,63); INK=(33,37,43); GREY=(95,102,112); SOFT=(238,241,247); LINE=(214,219,228); WHITE=(255,255,255); ACCENT=(176,141,87)

class TS(FPDF):
    def __init__(self):
        super().__init__("P","mm","A4")
        self.set_auto_page_break(True,16)
        self.add_font("S","",f"{FD}/DejaVuSans.ttf")
        self.add_font("S","B",f"{FD}/DejaVuSans-Bold.ttf")
        self.add_font("R","",f"{FD}/DejaVuSerif.ttf")
        self.add_font("R","B",f"{FD}/DejaVuSerif-Bold.ttf")
        self.set_margins(20,20,20); self.cw=170; self.first=True
    def header(self):
        if self.page_no()==1: return
        self.set_y(8); self.set_font("R","B",9); self.set_text_color(*NAVY)
        self.cell(0,5,"STRIKER",align="L")
        self.set_font("S","",7.5); self.set_text_color(*GREY)
        self.set_xy(20,8); self.cell(self.cw,5,"Indicative Term Sheet",align="R")
        self.set_draw_color(*LINE); self.set_line_width(0.2); self.line(20,15,190,15)
        self.set_y(20)
    def footer(self):
        self.set_y(-13); self.set_draw_color(*LINE); self.set_line_width(0.2); self.line(20,self.get_y(),190,self.get_y())
        self.set_y(-11); self.set_font("S","",7); self.set_text_color(*GREY)
        self.cell(self.cw-20,5,"Строго конфиденциально · STRIKER · подлежит оформлению договором",align="L")
        self.cell(20,5,f"{self.page_no()}",align="R")
    def hrule(self,col=NAVY,w=0.5,pad=2):
        self.ln(pad); self.set_draw_color(*col); self.set_line_width(w); self.line(20,self.get_y(),190,self.get_y()); self.ln(pad+1)
    def section(self,num,title):
        if self.get_y()>250: self.add_page()
        self.ln(3)
        y=self.get_y()
        self.set_fill_color(*NAVY); self.rect(20,y+0.4,6.4,6.4,"F")
        self.set_font("S","B",9); self.set_text_color(*WHITE); self.set_xy(20,y+1.4); self.cell(6.4,4.4,num,align="C")
        self.set_font("R","B",12); self.set_text_color(*NAVY); self.set_xy(28.5,y+0.6); self.cell(0,6,title)
        self.ln(9); self.set_draw_color(*LINE); self.set_line_width(0.2); self.line(20,self.get_y(),190,self.get_y()); self.ln(2)
    def body(self,txt,size=9.3,gap=1.6):
        self._fits(txt,self.cw)
        self.set_font("S","",size); self.set_text_color(*INK)
        self.multi_cell(self.cw,4.6,txt); self.ln(gap)
    def _fits(self,text,width,need_extra=2,lh=4.6,bottom=276):
        self.set_font("S","",9.3)
        lines=self.multi_cell(width,lh,text,dry_run=True,output="LINES")
        need=len(lines)*lh+need_extra
        if self.get_y()+need>bottom: self.add_page()
    def lead_para(self,lead,txt,size=9.3):
        self._fits(lead+txt,self.cw)
        self.set_x(20); self.set_font("S","B",size); self.set_text_color(*NAVY)
        self.write(4.6,lead)
        self.set_font("S","",size); self.set_text_color(*INK)
        self.write(4.6,txt); self.ln(5.4)
    def bullet(self,lead,txt,size=9.3):
        self._fits((lead or "")+txt,self.cw-5)
        x0=20; self.set_xy(x0,self.get_y())
        self.set_font("S","B",9); self.set_text_color(*ACCENT); self.cell(5,4.6,"—")
        self.set_xy(x0+5,self.get_y())
        if lead:
            self.set_font("S","B",size); self.set_text_color(*NAVY); self.write(4.6,lead)
        self.set_font("S","",size); self.set_text_color(*INK); self.write(4.6,txt); self.ln(5.2)

def kv_table(p,rows):
    p.set_draw_color(*LINE); lh=6.6; kw=46; vw=p.cw-kw
    for i,(k,v) in enumerate(rows):
        # measure value lines
        p.set_font("S","",8.6)
        lines=p.multi_cell(vw-4,4.2,v,dry_run=True,output="LINES")
        rowh=max(lh,4.2*len(lines)+3)
        if p.get_y()+rowh>270: p.add_page()
        y=p.get_y()
        p.set_fill_color(*SOFT); p.rect(20,y,kw,rowh,"F")
        p.set_draw_color(*LINE); p.set_line_width(0.2); p.rect(20,y,kw,rowh); p.rect(20+kw,y,vw,rowh)
        p.set_font("S","B",8.6); p.set_text_color(*NAVY); p.set_xy(22,y+1.6); p.multi_cell(kw-3,4.2,k)
        p.set_font("S","",8.6); p.set_text_color(*INK); p.set_xy(22+kw,y+1.6); p.multi_cell(vw-4,4.2,v)
        p.set_y(y+rowh)

def tranche_table(p,rows):
    p.ln(1); cols=[24,32,p.cw-56]; hh=7
    x=20; y=p.get_y(); p.set_fill_color(*NAVY)
    p.rect(20,y,p.cw,hh,"F"); p.set_font("S","B",8.4); p.set_text_color(*WHITE)
    heads=["Транш","Сумма","Условие разблокировки"]
    cx=20
    for w,htx in zip(cols,heads):
        p.set_xy(cx,y+1.6); p.cell(w,4,"  "+htx); cx+=w
    p.set_y(y+hh)
    for i,(a,b,c) in enumerate(rows):
        p.set_font("S","",8.4)
        lines=p.multi_cell(cols[2]-4,4.0,c,dry_run=True,output="LINES")
        rh=max(6.4,4.0*len(lines)+2.6); yy=p.get_y()
        if i%2==1:
            p.set_fill_color(248,249,252); p.rect(20,yy,p.cw,rh,"F")
        p.set_draw_color(*LINE); p.set_line_width(0.2); p.rect(20,yy,p.cw,rh)
        cx=20
        p.set_font("S","B",8.4); p.set_text_color(*NAVY); p.set_xy(cx+2,yy+1.4); p.cell(cols[0]-2,4,a); cx+=cols[0]
        p.set_font("S","",8.4); p.set_text_color(*INK); p.set_xy(cx+2,yy+1.4); p.cell(cols[1]-2,4,b); cx+=cols[1]
        p.set_xy(cx+2,yy+1.4); p.multi_cell(cols[2]-4,4.0,c)
        p.set_y(yy+rh)

p=TS(); p.add_page()
# ---------- COVER ----------
p.set_fill_color(*NAVY); p.rect(0,0,210,52,"F")
p.set_y(14); p.set_font("R","B",30); p.set_text_color(*WHITE); p.cell(0,12,"STRIKER",align="C")
p.set_font("S","",10); p.set_text_color(214,221,233); p.set_y(28); p.cell(0,5,"Проект F/A-259U · лёгкий многоцелевой боевой самолёт",align="C")
p.set_draw_color(*ACCENT); p.set_line_width(0.6); p.line(86,37,124,37)
p.set_font("S","B",10.5); p.set_text_color(*WHITE); p.set_y(40); p.cell(0,5,"ОСНОВНЫЕ УСЛОВИЯ ИНВЕСТИЦИОННОЙ СДЕЛКИ · INDICATIVE TERM SHEET",align="C")
p.set_y(58)
p.set_font("S","",8.2); p.set_text_color(*GREY)
p.cell(0,4,"STRICTLY PRIVATE & CONFIDENTIAL   ·   SUBJECT TO CONTRACT   ·   2026",align="C")
p.ln(8)
p.set_font("S","",8.6); p.set_text_color(*GREY)
p.multi_cell(p.cw,4.3,"Настоящий документ носит индикативный и предварительный характер, отражает структуру обсуждаемой сделки и не является офертой или обязательством. Связывающими являются только разделы 15 и 16. Окончательные условия фиксируются в обязывающих договорах (подписное и акционерное соглашения, устав холдинга).")
p.ln(3)
# summary heading
p.set_font("R","B",12); p.set_text_color(*NAVY); p.cell(0,6,"Краткая сводка ключевых условий"); p.ln(8)
kv_table(p,[
 ("Эмитент (Холдинг)","[•] Limited — Англия и Уэльс; владеет болгарскими PrincipalCo (производство) и SalesCo (продажи)."),
 ("Инвестор(ы)","[•]"),
 ("Инициаторы проекта","[•]"),
 ("Инструмент","[привилегированные / обыкновенные] акции холдинга"),
 ("Объём раунда","[•]  (ориентир — полное финансирование трёх лет, ≈ 420 млн USD)"),
 ("Оценка pre / post-money","[•] / [•]  (ориентир post-money 0,7–1,1 млрд USD)"),
 ("Доля инвестора(ов)","[•]%  (ориентир 40–60%)"),
 ("Транширование","3 транша по достижении вех (раздел 3)"),
 ("Ликвидационная преференция","[1,0× non-participating]"),
 ("Совет директоров","[•] инвесторы / [•] инициаторы / 1 независимый; контрольное большинство — лица НАТО и ЕС"),
 ("Применимое право","английское; арбитраж [LCIA, Лондон]"),
 ("Юридический статус","необязывающий, кроме разделов 15–16"),
])

# ---------- SECTIONS ----------
p.section("1","Стороны")
p.bullet("Инвестор(ы): ","[•].")
p.bullet("Инициаторы (организаторы) проекта: ","[•].")
p.bullet("Компания (Эмитент): ","холдинговая компания в Великобритании ([•] Limited), которой принадлежат болгарские операционная (PrincipalCo) и продающая (SalesCo) компании.")

p.section("2","Предмет сделки и инструмент")
p.body("Инвестор подписывается на вновь выпускаемые акции холдинга. Класс и права акций определяются разделами 5 и 7 (разделение экономического участия и контроля).")

p.section("3","Объём инвестиций, оценка и транширование")
p.bullet("Объём раунда: ","[•] — полное финансирование трёх лет разработки, испытаний и запуска серийного производства.")
p.bullet("Оценка: ","pre-money [•] / post-money [•].")
p.bullet("Доля инвестора(ов): ","[•]% на полностью разводнённой основе.")
tranche_table(p,[
 ("Транш 1","[•]","подписание обязывающих документов"),
 ("Транш 2","[•]","[веха: напр. первый опытный самолёт]"),
 ("Транш 3","[•]","[веха: начало сертификационных испытаний]"),
])
p.ln(2)
p.bullet("Последствия недовнесения транша: ","штрафное разводнение, приостановка прав вето и/или опцион выкупа доли неисполнившего инвестора [•].")

p.section("4","Использование средств")
p.body("Разработка, испытания и запуск серийного производства F/A-259U. Существенные отклонения от согласованного бюджета — вопрос вето (раздел 7).")

p.section("5","Структура капитала и классы акций")
p.body("Экономическое участие отделяется от контроля: инвесторы вне НАТО получают акции с экономическими правами, но без (или с ограниченным) правом голоса по оборонным вопросам; голосующий контроль и право вето — у инициаторов и инвесторов из стран НАТО и ЕС (раздел 7.5 меморандума). Опционный пул для ключевых сотрудников (ESOP): [•]% на полностью разводнённой основе.")

p.section("6","Ликвидационная преференция и распределение")
p.body("[1,0× non-participating] для инвестора при продаже или ликвидации; далее распределение пропорционально долям.")

p.section("7","Корпоративное управление — два контура")
p.lead_para("А. Коммерческое управление. ","Совет директоров — [•] от инвесторов, [•] от инициаторов, 1 независимый; контрольное большинство — за директорами от лиц из стран НАТО и ЕС.")
p.body("Вопросы вето инвесторов (квалифицированное большинство): бюджет и крупные вложения; займы и гарантии; эмиссия и изменение прав акций; сделки со связанными сторонами; передача прав на разработку; смена контроля; M&A; дивидендная политика; смена аудитора; изменение устава и акционерного соглашения; ликвидация и банкротство.")
p.lead_para("Б. Оборонный контур (security). ","Доступ к секретной информации, выбор экспортных рынков и конечных пользователей, экспортное лицензирование и исполнение соглашения о безопасности решает комитет по безопасности из директоров с допуском к гостайне (граждане НАТО/ЕС) — единолично, без права вето внеблоковых акционеров. Кворум по таким вопросам требует участия директоров с допуском.")

p.section("8","Менеджмент и основатели")
p.bullet("Управление: ","операционная реализация — за инициаторами; служебные договоры, KPI, ежемесячная/ежеквартальная отчётность, право инвестора на информацию.")
p.bullet("Vesting долей инициаторов: ","период удержания [•] + помесячно за [•] лет; разделение good leaver / bad leaver с обратным выкупом по [•].")
p.bullet("Обязательства: ","non-compete / non-solicit на срок [•]; передача созданной интеллектуальной собственности компании.")

p.section("9","Защита инвестора и анти-разводнение")
p.body("Право на информацию; защита от размывания (взвешенное среднее [•]); право следования при продаже (tag-along) на равных условиях; преимущественное право на новые эмиссии (пропорционально доле).")

p.section("10","Ограничения на передачу долей")
p.bullet("Передача: ","lock-up на срок [•]; право первого предложения / первого выкупа (ROFO/ROFR) с процедурой и сроками; разрешённые передачи аффилированным лицам.")
p.bullet("Оборонное условие: ","любая передача доли и любая смена контроля над акционером — только после проверки иностранных инвестиций (FDI) и при сохранении допуска к лицензии.")
p.bullet("Аварийный механизм: ","принудительный выкуп при попадании акционера под санкции, потере допуска или враждебной смене контроля над ним — по [•].")

p.section("11","Принудительная продажа и выход")
p.bullet("Drag-along: ","при [квалифицированном большинстве] — только покупателю, прошедшему FDI-скрининг; drag не передаёт контроль непроверенному или внеблоковому лицу.")
p.bullet("Выход: ","IPO или продажа стратегу; ориентировочный горизонт ликвидности — [•]; registration rights при IPO.")
p.bullet("Тупиковые ситуации: ","эскалация, посредничество, опционы выкупа — в тех же FDI-ограничениях.")

p.section("12","Условия закрытия (Conditions Precedent)")
p.body("Разрешение болгарского регулятора по проверке иностранных инвестиций; подписанное соглашение о безопасности; согласованный порядок экспортного лицензирования (Чехия и Болгария); договоры с Aero Vodochody, IAI и поставщиком двигателя; подтверждённая финансовая модель и завершённая проверка (due diligence); отсутствие существенного неблагоприятного изменения (MAC); корпоративные одобрения; подписанные служебные договоры ключевых лиц.")

p.section("13","Заверения и гарантии")
p.body("Инициаторы предоставляют деловые заверения и гарантии с раскрытием (disclosure) и индемнити в объёме, согласуемом в обязывающих документах.")

p.section("14","Расходы")
p.body("Каждая сторона несёт собственные расходы [или: разумные расходы инвестора на проверку компенсируются при закрытии — [•]].")

p.section("15","Эксклюзивность и конфиденциальность  (связывающие положения)")
p.bullet("Эксклюзивность (no-shop): ","на срок [•] стороны не ведут переговоров с третьими лицами по аналогичной сделке.")
p.bullet("Конфиденциальность: ","содержание документа и переговоров конфиденциально; публичные анонсы — только по взаимному письменному согласию.")

p.section("16","Применимое право, споры и статус  (связывающие положения)")
p.bullet("Применимое право: ","английское; споры — международный арбитраж [LCIA, место — Лондон].")
p.body("Настоящий term sheet носит предварительный и НЕ обязывающий характер и сам по себе не создаёт обязанности заключить сделку. Связывающими являются только разделы 15 и 16; прочие условия становятся обязательными после подписания долгосрочных документов.")

# signatures
p.hrule(col=NAVY,w=0.4,pad=4)
p.set_font("S","",8.6); p.set_text_color(*GREY)
p.multi_cell(p.cw,4.3,"Принято к сведению и согласовано в качестве основы для дальнейших переговоров:"); p.ln(8)
y=p.get_y()
for i,lab in enumerate(["От имени Эмитента / Инициаторов","От имени Инвестора"]):
    x=20+i*88
    p.set_draw_color(*INK); p.set_line_width(0.3); p.line(x,y,x+78,y)
    p.set_font("S","B",8.6); p.set_text_color(*NAVY); p.set_xy(x,y+1.5); p.cell(78,4,lab)
    p.set_font("S","",8.4); p.set_text_color(*GREY)
    p.set_xy(x,y+7); p.cell(78,4,"Имя:")
    p.set_xy(x,y+12); p.cell(78,4,"Должность:")
    p.set_xy(x,y+17); p.cell(78,4,"Дата:")

p.output("STRIKER_Term_Sheet.pdf")
print("pages",p.page_no())
