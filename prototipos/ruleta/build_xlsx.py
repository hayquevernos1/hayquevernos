import json,collections,unicodedata,re,openpyxl
from openpyxl.styles import Font,PatternFill,Alignment,Border,Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table,TableStyleInfo
nrm=lambda s:unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
st=json.load(open('/home/claude/hqv/ruleta/stage1.json'));rows=st['rows']
s=open('/home/claude/hqv/v5/catalogo_v2.js').read();CAT=json.loads(s[s.index('{'):s.rindex('}')+1])['cats']
OURS=[c['n'] for c in CAT]
A='Agregado: catálogo actual HQV'
ADD=[('Catering','Renta de equipo de cocina','Chafers y calentadores',d) for d in ['Chafer rectangular','Chafer redondo','Calentador','Otro']]+\
 [('Catering','Renta de equipo de cocina','Barras móviles',d) for d in ['Sencilla','Iluminada','Otro']]+\
 [('Catering','Renta de equipo de cocina','Dispensadores y vitroleros',d) for d in ['Vitrolero','Dispensador de bebidas','Otro']]+\
 [('Audio, iluminación, foto y video','Cabinas fotográficas','Cabina 360',d) for d in ['Con video en cámara lenta','Otro']]+\
 [('Decoración y ambientación','Elementos decorativos',f,'Otro') for f in ['Backdrop o muro','Arco']]+\
 [('Registro y protocolo','Ceremonias','Oficiante',d) for d in ['Civil simbólica','Religiosa','Otro']]+\
 [('Permisos y trámites','Licencias','Derechos musicales',d) for d in ['Gestión','Otro']]+\
 [('Sustentabilidad y limpieza','Residuos','Evento cero residuos',d) for d in ['Plan integral','Otro']]
seen={(r[0],nrm(r[1]),nrm(r[2]),nrm(r[3])) for r in rows}
for c,sv,f,d in ADD:
    if (c,nrm(sv),nrm(f),nrm(d)) not in seen: rows.append([c,sv,f,d,A])
# ---------- unidades ----------
DEF={'Catering':('Por persona','Por evento · Por pieza'),'Música':('Por hora','Por evento'),'Entretenimiento y shows':('Por evento','Por hora'),
 'Infraestructura':('Por evento','Por día · Por m²'),'Mobiliario y montaje':('Por pieza','Por juego · Por evento'),'Cristalería y cubertería':('Por pieza','Por juego · Por docena'),
 'Audio, iluminación, foto y video':('Por evento','Por hora · Por día'),'Tecnología':('Por evento','Por día'),'Decoración y ambientación':('Por evento','Por pieza'),
 'Marketing y comunicación':('Por proyecto','Por mes · Por evento'),'Transporte':('Por viaje','Por hora · Por día'),'Hospedaje':('Por noche','Por persona'),
 'Maquillaje y estilismo':('Por persona','Por evento'),'Registro y protocolo':('Por evento','Por hora · Por persona'),'Exposición y negocios':('Por stand','Por m² · Por evento'),
 'Souvenirs y regalos':('Por pieza','Por paquete · Por ciento'),'Seguridad, salud y protección civil':('Por hora','Por evento'),'Actividades y experiencias':('Por persona','Por evento'),
 'Impresión y producción gráfica':('Por pieza','Por millar · Por m²'),'Vestuario y accesorios':('Por pieza','Por persona · Por evento'),'Permisos y trámites':('Por trámite','Por proyecto'),
 'Sustentabilidad y limpieza':('Por evento','Por kilo · Por hora')}
OV=[ # (categoría o *, regex sobre «servicio | formato | detalle», unidad, otras)
 ('*',r'^personal independiente','Por hora','Por turno (5 h) · Por evento'),
 ('*',r'^renta de','Por día','Por pieza · Por evento'),
 ('Catering',r'\| box lunch','Por caja','Por persona'),
 ('Catering',r'\| productos individuales','Por pieza','Por docena · Por ciento'),
 ('Catering',r'^pasteles','Por pieza','Por porción'),
 ('Catering',r'^reposteria','Por pieza','Por docena · Por ciento'),
 ('Catering',r'^botanas \| a granel','Por kilo','Por persona'),
 ('Catering',r'^postres y dulces \| (mesa|fuente)','Por evento','Por persona'),
 ('Catering',r'servicio embotellado','Por pieza','Por caja'),
 ('Catering',r'\| barril','Por pieza','Por litro'),
 ('Catering',r'food truck|carrito','Por evento','Por persona · Por hora'),
 ('Catering',r'^degustacion','Por sesión','Por persona'),
 ('Música',r'composicion|produccion musical','Por proyecto','Por pieza'),
 ('Entretenimiento y shows',r'juegos y atracciones','Por día','Por evento · Por hora'),
 ('Entretenimiento y shows',r'^animacion|personajes','Por hora','Por evento'),
 ('Infraestructura',r'carpas|pisos|pistas de baile|escenarios|gradas','Por m²','Por evento · Por día'),
 ('Infraestructura',r'sanitarios','Por pieza','Por día'),
 ('Infraestructura',r'energia','Por día','Por evento'),
 ('Mobiliario y montaje',r'^montaje','Por evento','Por pieza'),
 ('Cristalería y cubertería',r'^lavado','Por pieza','Por evento'),
 ('Cristalería y cubertería',r'consumibles','Por paquete','Por pieza'),
 ('Audio, iluminación, foto y video',r'cabinas|streaming|sonorizacion','Por hora','Por evento'),
 ('Audio, iluminación, foto y video',r'postproduccion','Por proyecto','Por pieza'),
 ('Decoración y ambientación',r'^flores|^globos|elementos decorativos','Por pieza','Por evento'),
 ('Transporte',r'valet|movilidad interna','Por hora','Por evento'),
 ('Transporte',r'mensajeria','Por envío','Por viaje'),
 ('Hospedaje',r'hospitalidad|reservas','Por evento','Por persona'),
 ('Registro y protocolo',r'idiomas|conduccion|hospitalidad|recepcion|accesos','Por hora','Por evento'),
 ('Registro y protocolo',r'registro|acreditacion|rsvp|invitados','Por persona','Por evento'),
 ('Exposición y negocios',r'leads|matchmaking|networking|ventas|expositores','Por evento','Por persona'),
 ('Souvenirs y regalos',r'entrega','Por envío','Por evento'),
 ('Souvenirs y regalos',r'kits|canastas','Por pieza','Por paquete'),
 ('Seguridad, salud y protección civil',r'ambulancias|proteccion civil|prevencion|vigilancia','Por evento','Por hora'),
 ('Actividades y experiencias',r'integracion|juegos|deporte','Por evento','Por persona'),
 ('Impresión y producción gráfica',r'diseno grafico','Por proyecto','Por pieza'),
 ('Impresión y producción gráfica',r'gran formato|rotulacion|senaletica|instalacion grafica','Por m²','Por pieza'),
 ('Vestuario y accesorios',r'renta','Por pieza','Por día'),
 ('Vestuario y accesorios',r'^vestuario \|','Por evento','Por hora'),
 ('Sustentabilidad y limpieza',r'^limpieza','Por hora','Por evento'),
 ('Sustentabilidad y limpieza',r'consultoria|huella','Por proyecto','Por evento'),
]
def unit(r):
    t=nrm(' | '.join(r[1:3]))
    for c,rx,u,o in OV:
        if (c=='*' or c==r[0]) and re.search(rx,t): return u,o
    return DEF[r[0]]
# ---------- orden ----------
FOOD=['Banquete','Buffet','Cóctel','Estación de especialidad','Box lunch','Productos individuales'];DRINK=['Barra','Estación','Mesa','Carrito','Dispensador','Barril']
SVO={'Catering':['Alimentos','Bebidas','Postres y dulces','Pasteles','Repostería','Botanas','Degustación de menú','Renta de equipo de cocina']}
def ksv(c,sv):
    L=SVO.get(c,[]);
    if sv=='Otro':return(9,'')
    if sv=='Personal independiente':return(8,'')
    if sv.startswith('Renta de') and sv not in L:return(7,nrm(sv))
    return (0,L.index(sv)) if sv in L else (1,nrm(sv))
def kf(sv,f):
    if f=='Otro':return(9,'')
    L=FOOD if sv=='Alimentos' else DRINK if sv=='Bebidas' else []
    return (0,L.index(f)) if f in L else (1,nrm(f))
kd=lambda d:(9,'') if d=='Otro' else (1,nrm(d))
rows.sort(key=lambda r:(OURS.index(r[0]),ksv(r[0],r[1]),kf(r[1],r[2]),kd(r[3])))
for r in rows: u,o=unit(r);r+= [u,o]
# ---------- staff ----------
mm=openpyxl.load_workbook('/root/.claude/uploads/51f3e6ce-695f-5356-ac4c-dcebed5d12b3/6442ac23-Base_ruleta_servicios_HQV_1.xlsx',data_only=True)['Matriz maestra']
REN={'Audio, fotografía y video':'Audio, iluminación, foto y video','Imagen y decoración':'Decoración y ambientación','Servicios legales, administrativos y permisos':'Permisos y trámites','Sustentabilidad y gestión ambiental':'Sustentabilidad y limpieza'}
staff={}
for r in mm.iter_rows(min_row=2,values_only=True):
    if not r[1] or r[1]=='Equipamiento':continue
    c=REN.get(r[1],r[1]);txt=re.sub(r',? cuando .*$','',r[3] or '').rstrip('.')
    staff[c]=[x.strip()[0].upper()+x.strip()[1:] for x in txt.split(',') if x.strip()]
PRE={'Catering':['Mesero','Cocinero','Capitán de meseros'],'Música':['DJ'],'Mobiliario y montaje':['Montador de mobiliario'],'Audio, iluminación, foto y video':['Técnico de sonido','Fotógrafo'],'Registro y protocolo':['Hostess'],'Seguridad, salud y protección civil':['Guardia de seguridad'],'Transporte':['Chofer'],'Maquillaje y estilismo':['Maquillista'],'Decoración y ambientación':['Decorador']}
json.dump({'cats':OURS,'emo':{c['n']:c['e'] for c in CAT},'rows':[r[:4]+r[5:7] for r in rows],'staff':staff,'pre':PRE},open('/home/claude/hqv/ruleta/ruleta_data.json','w'),ensure_ascii=False)
# ---------- Excel ----------
F='Arial';H=Font(name=F,bold=True,color='FFFFFF');B=Font(name=F);BB=Font(name=F,bold=True)
fill=lambda c:PatternFill('solid',start_color=c);PUR=fill('7B2FF7');LIL=fill('EFE6FF');YEL=fill('FFF7C2');GRN=fill('E6FFF4')
wb=openpyxl.Workbook()
# Léeme
ws=wb.active;ws.title='Léeme'
txt=[('Base de la ruleta de servicios · ¡Hay que vernos!',Font(name=F,bold=True,size=16,color='7B2FF7')),
 ('Versión vigente · 15 oct 2026 · hecha a partir de «Base_ruleta_servicios_HQV_1» de Diego',Font(name=F,italic=True,color='6B6280')),('',B),
 ('¿Qué es?',BB),('Las 4 dimensiones con las que el proveedor alinea los rodillos: Categoría → Servicio/producto → Formato → Detalle.',B),
 ('Cada rodillo depende del anterior: si eliges Catering, el segundo rodillo solo muestra lo de Catering.',B),('',B),
 ('Pestañas',BB),('Ruleta: la base completa, una fila por combinación, con la unidad sugerida.',B),
 ('Unidades: el criterio con el que propongo la unidad de cada combinación (el proveedor siempre la puede cambiar).',B),
 ('Staff por categoría: los perfiles que se sugieren en «¿Qué staff incluye?».',B),
 ('Cambios: qué moví o renombré respecto a tu Excel para usar nuestras 22 categorías.',B),
 ('Resumen: cuántas opciones tiene cada rodillo por categoría (se calcula solo).',B),('',B),
 ('Colores en la pestaña Ruleta',BB),('Blanco: viene tal cual de tu Excel.',B),('Lila: categoría o formato renombrado.',B),
 ('Amarillo: reubicado desde «Equipamiento» (esa categoría ya no existe; su equipo se repartió).',B),('Verde: agregado para cubrir algo del catálogo actual del prototipo.',B),('',B),
 ('Siempre, sin importar la unidad',BB),('Al final de cada producto o paquete preguntamos: «¿Para cuántas personas alcanza?». Así lo llevamos al cotizador del anfitrión.',B),
 ('Los insumos se escriben libres (con texto predictivo), sin cantidad ni unidad: se entiende que alcanzan para esas personas.',B)]
for i,(t,f) in enumerate(txt,1): c=ws.cell(i,1,t);c.font=f
ws.column_dimensions['A'].width=120
# Ruleta
ws=wb.create_sheet('Ruleta');hd=['Categoría','Servicio/producto','Formato','Detalle','Unidad sugerida','Otras unidades comunes','Origen']
ws.append(hd)
for r in rows: ws.append([r[0],r[1],r[2],r[3],r[5],r[6],r[4]])
COL={'Excel de Diego':None,'Excel de Diego (categoría renombrada)':LIL,'Excel de Diego (formato renombrado)':LIL,'Reubicado de «Equipamiento»':YEL,A:GRN}
for row in ws.iter_rows(min_row=2):
    f=COL.get(row[6].value)
    for c in row:
        c.font=B
        if f: c.fill=f
for c in ws[1]: c.font=H;c.fill=PUR;c.alignment=Alignment(vertical='center')
for i,w in enumerate([30,30,30,30,16,28,36],1): ws.column_dimensions[get_column_letter(i)].width=w
ws.freeze_panes='A2';ws.auto_filter.ref=f'A1:G{ws.max_row}'
NR=ws.max_row
# Unidades
ws=wb.create_sheet('Unidades');ws.append(['Categoría','Unidad sugerida (general)','Otras unidades comunes','Excepciones dentro de la categoría','¿Por qué?'])
WHY={'Catering':'Comida y bebida se comparan por persona; lo que se vende por pieza o caja tiene su excepción.','Música':'Los músicos y DJ suelen cobrar por hora o por evento con mínimo de horas.',
 'Mobiliario y montaje':'Se renta por pieza (sillas, mesas); el montaje se cobra por evento.','Cristalería y cubertería':'Se renta por pieza o por juego.','Hospedaje':'El estándar del mercado es por noche.',
 'Transporte':'Se cotiza por viaje (redondo o sencillo).','Exposición y negocios':'Los stands se cobran por pieza o por m².','Permisos y trámites':'Cada trámite tiene su costo.',
 'Marketing y comunicación':'Se cotiza por proyecto o por mes.','Impresión y producción gráfica':'Por pieza; el gran formato por m².'}
for c in OURS:
    lab=lambda rx:rx.replace('\\|','›').replace('^','').replace('|',' o ').replace('(','').replace(')','').strip(' ›').capitalize()
    ACC={'reposteria':'repostería','composicion':'composición','produccion':'producción','degustacion':'degustación','animacion':'animación','diseno':'diseño','grafico':'gráfico','grafica':'gráfica','senaletica':'señalética','rotulacion':'rotulación','instalacion':'instalación','proteccion':'protección','prevencion':'prevención','consultoria':'consultoría','mensajeria':'mensajería','integracion':'integración','conduccion':'conducción','recepcion':'recepción','acreditacion':'acreditación','sonorizacion':'sonorización','postproduccion':'postproducción','musical':'musical','energia':'energía','huella':'huella','renta':'renta'}
    fx=lambda t:' '.join(ACC.get(w.lower(),w) if w.lower() in ACC else w for w in t.split(' ')).replace(t.split(' ')[0],t.split(' ')[0]) 
    ex=[f'«{(lambda z:z[0].upper()+z[1:])(fx(lab(rx)))}» → {u}' for cc,rx,u,o in OV if cc==c]
    ws.append([c,DEF[c][0],DEF[c][1],'\n'.join(ex) or '—',WHY.get(c,'Es como se cotiza normalmente en esta categoría.')])
ws.append(['Todas','—','—','«Personal independiente» → Por hora\n«Renta de …» → Por día','El staff se cobra por hora; el equipo sin operación, por día.'])
ws.append([]);ws.append(['Regla para todos','Siempre se pregunta «¿Para cuántas personas alcanza?», aunque la unidad sea por pieza, hora o evento.'])
for row in ws.iter_rows(min_row=2):
    for c in row: c.font=B;c.alignment=Alignment(wrap_text=True,vertical='top')
for c in ws[1]: c.font=H;c.fill=PUR
ws.cell(ws.max_row,1).font=BB;ws.cell(ws.max_row,2).fill=YEL
for i,w in enumerate([32,22,30,52,60],1): ws.column_dimensions[get_column_letter(i)].width=w
ws.freeze_panes='A2'
# Staff
ws=wb.create_sheet('Staff por categoría');ws.append(['Categoría','Perfiles de staff (predictivo)','Ya marcados por defecto'])
for c in OURS: ws.append([c,', '.join(staff.get(c,[])),', '.join(PRE.get(c,[])) or '—'])
for row in ws.iter_rows(min_row=2):
    for c in row: c.font=B;c.alignment=Alignment(wrap_text=True,vertical='top')
for c in ws[1]: c.font=H;c.fill=PUR
for i,w in enumerate([32,90,34],1): ws.column_dimensions[get_column_letter(i)].width=w
# Cambios
ws=wb.create_sheet('Cambios');ws.append(['En tu Excel','En la base vigente','Tipo de cambio'])
for a,b in REN.items(): ws.append([a,b,'Categoría renombrada a la del prototipo'])
EQ=[('Accesibilidad','Infraestructura · Accesibilidad'),('Audio','Audio, iluminación, foto y video · Renta de equipo de audio'),('Climatización','Infraestructura · Climatización'),('Cocina','Catering · Renta de equipo de cocina'),('Comunicación','Tecnología · Renta de radios e intercom'),('Conectividad','Tecnología · Conectividad'),('Energía','Infraestructura · Energía'),('Herramientas','Infraestructura · Renta de herramientas'),('Iluminación','Audio, iluminación, foto y video · Iluminación'),('Informática','Tecnología · Renta de equipo de cómputo'),('Instrumentos','Música · Renta de instrumentos'),('Video','Audio, iluminación, foto y video · Renta de equipo de video'),('Otro','Se quitó (cada categoría ya tiene su «Otro»)')]
for a,b in EQ: ws.append(['Equipamiento · '+a,b,'Reubicado: «Equipamiento» no es categoría del prototipo'])
ws.append(['Catering · Alimentos · Estación gastronómica','Catering · Alimentos · Estación de especialidad','Formato renombrado al nombre del prototipo'])
for c,sv,f,d in ADD: pass
for k,v in collections.OrderedDict(((c,sv,f),1) for c,sv,f,d in ADD).items(): ws.append(['—',' · '.join(k),'Agregado para cubrir el catálogo actual'])
ws.append(['Orden de los rodillos','Alimentos: Banquete, Buffet, Cóctel, Estación de especialidad, Box lunch, Productos individuales… · Bebidas: Barra, Estación, Mesa, Carrito, Dispensador, Barril…','Mismo orden que los botones del prototipo; «Otro» siempre al final'])
for row in ws.iter_rows(min_row=2):
    for c in row: c.font=B;c.alignment=Alignment(wrap_text=True,vertical='top')
for c in ws[1]: c.font=H;c.fill=PUR
for i,w in enumerate([46,62,46],1): ws.column_dimensions[get_column_letter(i)].width=w
# Resumen (fórmulas)
ws=wb.create_sheet('Resumen');ws.append(['Categoría','Combinaciones (filas)','Con detalle «Otro»','% «Otro»'])
for i,c in enumerate(OURS,2):
    ws.append([c,f'=COUNTIF(Ruleta!$A$2:$A${NR},A{i})',f'=COUNTIFS(Ruleta!$A$2:$A${NR},A{i},Ruleta!$D$2:$D${NR},"Otro")',f'=IF(B{i}=0,0,C{i}/B{i})'])
t=len(OURS)+2;ws.append(['Total',f'=SUM(B2:B{t-1})',f'=SUM(C2:C{t-1})',f'=IF(B{t}=0,0,C{t}/B{t})'])
for row in ws.iter_rows(min_row=2):
    for c in row: c.font=B
    row[3].number_format='0.0%'
for c in ws[t]: c.font=BB
for c in ws[1]: c.font=H;c.fill=PUR
for i,w in enumerate([36,22,20,12],1): ws.column_dimensions[get_column_letter(i)].width=w
wb.save('/home/claude/hqv/ruleta/Base_ruleta_servicios_HQV_v2.xlsx');print('rows',len(rows))

