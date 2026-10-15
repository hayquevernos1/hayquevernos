import openpyxl,collections,json,re,unicodedata
SRC='/root/.claude/uploads/51f3e6ce-695f-5356-ac4c-dcebed5d12b3/6442ac23-Base_ruleta_servicios_HQV_1.xlsx'
wb=openpyxl.load_workbook(SRC,data_only=True)
R=[tuple((x or '').strip() for x in r) for r in wb['Ruleta'].iter_rows(min_row=2,values_only=True) if r[0]]
nrm=lambda s:unicodedata.normalize('NFD',s.lower()).encode('ascii','ignore').decode()
s=open('/home/claude/hqv/v5/catalogo_v2.js').read();CAT=json.loads(s[s.index('{'):s.rindex('}')+1])['cats']
OURS=[c['n'] for c in CAT]
REN={'Audio, fotografía y video':'Audio, iluminación, foto y video','Imagen y decoración':'Decoración y ambientación',
 'Servicios legales, administrativos y permisos':'Permisos y trámites','Sustentabilidad y gestión ambiental':'Sustentabilidad y limpieza'}
EQ={'Accesibilidad':('Infraestructura','Accesibilidad'),'Audio':('Audio, iluminación, foto y video','Renta de equipo de audio'),
 'Climatización':('Infraestructura','Climatización'),'Cocina':('Catering','Renta de equipo de cocina'),'Comunicación':('Tecnología','Renta de radios e intercom'),
 'Conectividad':('Tecnología','Conectividad'),'Energía':('Infraestructura','Energía'),'Herramientas':('Infraestructura','Renta de herramientas'),
 'Iluminación':('Audio, iluminación, foto y video','Iluminación'),'Informática':('Tecnología','Renta de equipo de cómputo'),
 'Instrumentos':('Música','Renta de instrumentos'),'Video':('Audio, iluminación, foto y video','Renta de equipo de video')}
rows=[];seen=set()
def add(c,sv,f,d,orig):
    k=(c,nrm(sv),nrm(f),nrm(d))
    if k in seen: return
    seen.add(k);rows.append([c,sv,f,d,orig])
for c,sv,f,d in R:
    if c=='Equipamiento':
        if sv not in EQ: continue
        c2,sv2=EQ[sv];add(c2,sv2,f,d,'Reubicado de «Equipamiento»');continue
    o='Excel de Diego'
    if c in REN: c=REN[c];o='Excel de Diego (categoría renombrada)'
    if c=='Catering' and f=='Estación gastronómica': f='Estación de especialidad';o='Excel de Diego (formato renombrado)'
    add(c,sv,f,d,o)
# agregados del catálogo actual
for d in ['Bocadillos','Postres individuales','Pan dulce y salado','Otro']: add('Catering','Alimentos','Productos individuales',d,'Agregado: catálogo actual HQV')
assert set(r[0] for r in rows)==set(OURS),set(r[0] for r in rows)^set(OURS)
# cobertura del catálogo actual
miss=collections.defaultdict(list)
for C in CAT:
    blob=' | '.join(nrm(' '.join(r[1:4])) for r in rows if r[0]==C['n'])
    for it in C['full']+C['rent']:
        w=[x for x in re.split(r'[ ,()]+',nrm(it)) if len(x)>3]
        if w and not all(x[:-1] in blob for x in w): miss[C['n']].append(it)
json.dump({'rows':rows,'miss':miss},open('/home/claude/hqv/ruleta/stage1.json','w'),ensure_ascii=False)
print(len(rows));[print(k,v) for k,v in miss.items()]
