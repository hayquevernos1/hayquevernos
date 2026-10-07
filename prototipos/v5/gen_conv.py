"""Genera conversiones.js: el motor único de conversión (proveedor y cotizador usan lo mismo que la hoja
«Conversiones de unidades HQV» validada por Diego) + precios de referencia y sugerencias por tipo de evento."""
import json, re, runpy, sys
SP = '/tmp/claude-0/-home-claude-hayquevernos/51f3e6ce-695f-5356-ac4c-dcebed5d12b3/scratchpad/conv_xlsx.py'
g = runpy.run_path(SP)
rows, ADJ = g['rows'], g['ADJ']
d = json.loads(re.search(r'window\.HQV_SVC=(.*);\s*$', open('/home/claude/hqv/v5/catalogo_servicios.js').read(), re.S).group(1))
allowed = {(c['n'], s): us for c in d['cats'] for s, t, us in c['s']}
catof = {s: c for (c, s) in allowed}

units = {r['u']: [r['comp'], r['t'], r['R'], r['Q']] for r in rows}
adj = {}
for s, u, R, why in ADJ:
    adj[s + '|' + u] = 'fijo' if R == 'fijo' else R
adj['Pistas de baile|Por m²'] = 2
adj['Pistas de baile|Por m² por día'] = 2
# Piezas que NO son una por invitado (equipo, mobiliario, decoración)
for s, u, R in [('Mesas en renta', 'Por pieza', 10), ('Mesas en renta', 'Por pieza por día', 10), ('Piñatas', 'Por pieza', 'fijo'),
                ('Arreglos florales', 'Por pieza', 10), ('Baños portátiles', 'Por pieza por día', 50), ('Calefactores', 'Por equipo', 25),
                ('Letras y números gigantes', 'Por pieza', 'fijo'), ('Backdrops y fondos decorativos', 'Por pieza', 'fijo')]:
    if (catof.get(s), s) in allowed and u in allowed[(catof[s], s)]:
        adj[s + '|' + u] = R

# Personal: «por persona» = por cada persona del staff, no por invitado. Invitados que atiende cada uno.
STAFF = {'Meseros': 15, 'Bartenders': 40, 'Baristas': 60, 'Capitanes de meseros': 100, 'Personal de limpieza': 50, 'Lavalozas': 60,
         'Ayudantes de cocina': 40, 'Chefs y cocineros': 80, 'Anfitriones y edecanes': 100, 'Recepcionistas y personal de registro': 150,
         'Guardarropa y atención de paquetería': 150, 'Coordinadores de piso': 150, 'Niñeras y cuidadores infantiles': 8,
         'Personal de montaje y desmontaje': 50, 'Promotores y demostradores de marca': 100}

# Precios de referencia (CDMX, MXN, supuesto HQV hasta tener datos de proveedores): sub -> [unidad, precio, personas del paquete]
REF = {
 'Taquizas': ['Por persona', 210], 'Buffet': ['Por persona', 330], 'Banquete emplatado': ['Por persona', 520],
 'Catering de cóctel y canapés': ['Por persona', 220], 'Comida tradicional y antojitos': ['Por persona', 180],
 'Parrilladas y asados': ['Por persona', 380], 'Desayunos y brunch': ['Por persona', 240], 'Box lunch y alimentos empacados': ['Por persona', 180],
 'Food trucks': ['Por persona', 200], 'Estaciones de comida en vivo': ['Por persona', 190], 'Carritos de alimentos': ['Por hora', 1200],
 'Menús infantiles': ['Por niño', 150], 'Mesas de dulces': ['Por paquete', 3500, 50], 'Mesas de postres': ['Por persona', 75],
 'Mesas de botanas': ['Por persona', 90], 'Pasteles de celebración': ['Por porción', 45], 'Cupcakes y repostería individual': ['Por pieza', 35],
 'Galletas decoradas': ['Por pieza', 30], 'Helados y paletas': ['Por persona', 60], 'Fuentes de chocolate': ['Por paquete', 3200, 80],
 'Tablas de quesos y charcutería': ['Por persona', 140], 'Paellas y arroces': ['Por persona', 260], 'Recena y alimentos de madrugada': ['Por persona', 90],
 'Catering para reuniones corporativas': ['Por persona', 350], 'Coffee break': ['Por persona', 120], 'Cenas privadas con chef': ['Por persona', 900],
 'Barra libre': ['Por persona', 320], 'Barra de coctelería': ['Por persona', 280], 'Coctelería sin alcohol': ['Por persona', 110],
 'Aguas frescas y bebidas preparadas': ['Por persona', 45], 'Refrescos y mezcladores': ['Por litro', 30], 'Agua embotellada': ['Por persona', 20],
 'Cerveza envasada': ['Por lata', 28], 'Cerveza de barril': ['Por barril', 2800], 'Vino': ['Por botella', 380], 'Vinos espumosos y brindis': ['Por persona', 90],
 'Destilados': ['Por botella', 650], 'Barra de café y baristas': ['Por persona', 70], 'Hielo de consumo': ['Por bolsa', 60],
 'DJ': ['Por hora', 1500], 'Grupos musicales y orquestas': ['Por hora', 4500], 'Bandas regionales': ['Por hora', 4500], 'Mariachi': ['Por hora', 4000],
 'Solistas y cantantes': ['Por hora', 2200], 'Tríos y serenatas': ['Por hora', 2500], 'Karaoke con operación': ['Por evento', 1800],
 'Hora loca y cotillón con animación': ['Por evento', 3500], 'Maestros de ceremonias': ['Por evento', 4000], 'Magos e ilusionistas': ['Por show', 3000],
 'Animadores de pista': ['Por evento', 3000], 'Batucadas': ['Por show', 4500], 'Conferencistas': ['Por evento', 15000], 'Cuartetos de cuerdas': ['Por evento', 7000],
 'Sistemas de sonido': ['Por equipo', 2500], 'Iluminación ambiental': ['Por evento', 2500], 'Iluminación escénica y robótica': ['Por evento', 5000],
 'Proyectores y pantallas de proyección': ['Por equipo', 3000], 'Pantallas LED': ['Por evento', 12000], 'Micrófonos y sistemas inalámbricos': ['Por juego', 900],
 'Sonorización de conferencias': ['Por evento', 6000], 'Guirnaldas de luces': ['Por evento', 2000],
 'Decoración con globos': ['Por evento', 2800], 'Centros de mesa florales': ['Por mesa', 650], 'Centros de mesa no florales': ['Por mesa', 350],
 'Backdrops y fondos decorativos': ['Por módulo', 2200], 'Escenografía temática': ['Por evento', 7000], 'Diseño y decoración integral': ['Por evento', 12000],
 'Decoración de ceremonias': ['Por evento', 4500], 'Globos con helio': ['Por docena (12 piezas)', 300], 'Piñatas': ['Por pieza', 600],
 'Letreros luminosos y neón': ['Por pieza por día', 900],
 'Sillas en renta': ['Por pieza', 25], 'Mesas en renta': ['Por pieza', 120], 'Manteles y cubremanteles': ['Por mesa', 90], 'Vajilla': ['Por persona', 35],
 'Cristalería': ['Por persona', 25], 'Salas lounge y sofás': ['Por juego', 1800], 'Periqueras y bancos altos': ['Por juego', 450],
 'Carpas y toldos': ['Por m²', 60], 'Pistas de baile': ['Por m²', 120], 'Baños portátiles': ['Por pieza por día', 1200], 'Calefactores': ['Por equipo', 600],
 'Animación infantil': ['Por evento', 2800], 'Inflables': ['Por equipo', 1800], 'Cabinas fotográficas': ['Por hora', 1500], 'Plataformas de video 360': ['Por hora', 1500],
 'Mesas de casino recreativo': ['Por evento', 3500], 'Pintacaritas': ['Por hora', 500], 'Talleres infantiles': ['Por sesión', 1800],
 'Actividades de integración de equipos': ['Por persona', 450], 'Glitter bar': ['Por evento', 2500], 'Juegos de feria y kermés': ['Por evento', 3500],
 'Fotografía de eventos': ['Por hora', 1200], 'Fotografía de bodas y celebraciones': ['Por evento', 12000], 'Video de eventos': ['Por hora', 1500],
 'Paquete integral de fotografía y video': ['Por evento', 18000], 'Fotografía instantánea para invitados': ['Por hora', 1400],
 'Fotografía aérea con dron': ['Por evento', 3500], 'Reels y videos cortos': ['Por video', 1500],
 'Maquillaje social y de novia': ['Por servicio', 1500], 'Peinado social y de novia': ['Por servicio', 1000],
 'Meseros': ['Por turno', 900], 'Bartenders': ['Por turno', 1100], 'Capitanes de meseros': ['Por turno', 1300], 'Personal de limpieza': ['Por turno', 800],
 'Chefs y cocineros': ['Por evento', 2500], 'Anfitriones y edecanes': ['Por turno', 900], 'Niñeras y cuidadores infantiles': ['Por hora', 150],
 'Coordinadores de piso': ['Por evento', 2500], 'Recepcionistas y personal de registro': ['Por turno', 900],
 'Valet parking': ['Por vehículo', 120], 'Autobuses y minibuses para invitados': ['Por vehículo por día', 6500],
 'Invitaciones impresas': ['Por pieza', 35], 'Recuerdos de celebración': ['Por pieza', 60], 'Invitaciones digitales': None,
 'Transmisión en vivo y streaming': ['Por evento', 8000], 'Plataformas de registro e inscripción': ['Por usuario', 25],
 'Cañones de confeti y serpentinas': None, 'Pirotecnia profesional': None, 'Máquinas de humo y niebla': None,
 'Limpieza previa y posterior': None, 'Vigilancia y seguridad privada': None, 'Brigadistas y primeros auxilios': None,
 'Lonas y banners': None, 'Kits de bienvenida y amenidades': None, 'Gafetes y acreditaciones impresas': None, 'Regalos corporativos y promocionales': None,
}
# completa los None con la primera unidad «fija» permitida y un precio genérico
FALLBACK = {'Invitaciones digitales': 1200, 'Cañones de confeti y serpentinas': 1500, 'Pirotecnia profesional': 8000, 'Máquinas de humo y niebla': 1200,
            'Limpieza previa y posterior': 3500, 'Vigilancia y seguridad privada': 1200, 'Brigadistas y primeros auxilios': 1500, 'Lonas y banners': 800,
            'Kits de bienvenida y amenidades': 250, 'Gafetes y acreditaciones impresas': 25, 'Regalos corporativos y promocionales': 300}
bad = []
ref = {}
for s, v in REF.items():
    c = catof.get(s)
    if not c: bad.append(('SUB?', s)); continue
    us = allowed[(c, s)]
    if v is None:
        pref = ['Por evento', 'Por servicio', 'Por persona', 'Por pieza', 'Por paquete', 'Por turno', 'Por hora']
        u = next((p for p in pref if p in us), us[0])
        v = [u, FALLBACK[s]] + ([50] if u == 'Por paquete' else [])
    if v[0] not in us: bad.append((s, v[0], us)); continue
    ref[c + '|' + s] = v
if bad:
    print('ERRORES', *bad, sep='\n'); sys.exit(1)

# Sugerencias por tipo de evento (lo que dejamos marcado de inicio)
B = ['Taquizas', 'Pasteles de celebración', 'Cerveza envasada', 'DJ', 'Decoración con globos', 'Sillas en renta']
SUG = {
 'Cumpleaños': B, '15 años': ['Banquete emplatado', 'Pasteles de celebración', 'Barra libre', 'DJ', 'Iluminación escénica y robótica', 'Centros de mesa florales', 'Fotografía de eventos', 'Hora loca y cotillón con animación'],
 'Boda': ['Banquete emplatado', 'Pasteles de celebración', 'Barra libre', 'Vinos espumosos y brindis', 'DJ', 'Centros de mesa florales', 'Fotografía de bodas y celebraciones', 'Meseros', 'Maquillaje social y de novia'],
 'Baby shower': ['Catering de cóctel y canapés', 'Mesas de postres', 'Coctelería sin alcohol', 'Decoración con globos', 'Backdrops y fondos decorativos'],
 'Revelación de género': ['Catering de cóctel y canapés', 'Mesas de postres', 'Decoración con globos', 'Cañones de confeti y serpentinas'],
 'Bautizo': ['Banquete emplatado', 'Pasteles de celebración', 'Aguas frescas y bebidas preparadas', 'Centros de mesa florales', 'Fotografía de eventos'],
 'Primera comunión': ['Banquete emplatado', 'Pasteles de celebración', 'Aguas frescas y bebidas preparadas', 'Centros de mesa florales', 'Animación infantil'],
 'Confirmación religiosa': ['Buffet', 'Pasteles de celebración', 'Aguas frescas y bebidas preparadas', 'Centros de mesa florales'],
 'Día del Niño': ['Menús infantiles', 'Pasteles de celebración', 'Animación infantil', 'Inflables', 'Decoración con globos', 'Piñatas'],
 'Posada / Navidad / fin de año': ['Buffet', 'Aguas frescas y bebidas preparadas', 'Barra libre', 'DJ', 'Piñatas', 'Escenografía temática'],
 'Graduación': ['Buffet', 'Cerveza envasada', 'DJ', 'Backdrops y fondos decorativos', 'Fotografía de eventos'],
 'Despedida de soltera o soltero': ['Catering de cóctel y canapés', 'Barra de coctelería', 'DJ', 'Decoración con globos'],
 'Aniversario': ['Banquete emplatado', 'Vino', 'Solistas y cantantes', 'Centros de mesa florales'],
 'Renovación de votos': ['Banquete emplatado', 'Vinos espumosos y brindis', 'Cuartetos de cuerdas', 'Decoración de ceremonias', 'Fotografía de eventos'],
 'Pedida de mano': ['Cenas privadas con chef', 'Vinos espumosos y brindis', 'Tríos y serenatas', 'Arreglos florales', 'Fotografía de eventos'],
 'Halloween': ['Comida tradicional y antojitos', 'Barra de coctelería', 'DJ', 'Escenografía temática'],
 'Fiesta temática': ['Comida tradicional y antojitos', 'Barra de coctelería', 'DJ', 'Escenografía temática'],
 '15 de septiembre': ['Comida tradicional y antojitos', 'Destilados', 'Mariachi', 'Escenografía temática'],
 'Año Nuevo': ['Banquete emplatado', 'Vinos espumosos y brindis', 'DJ', 'Cañones de confeti y serpentinas'],
 'Reunión': ['Parrilladas y asados', 'Cerveza envasada', 'Sistemas de sonido'],
 'Convivencia': ['Parrilladas y asados', 'Cerveza envasada', 'Sistemas de sonido'],
 'Picnic': ['Box lunch y alimentos empacados', 'Aguas frescas y bebidas preparadas'],
 'Reencuentro de generación': ['Buffet', 'Barra libre', 'DJ', 'Fotografía de eventos'],
 'Gala': ['Banquete emplatado', 'Barra libre', 'Grupos musicales y orquestas', 'Centros de mesa florales', 'Meseros'],
 # Empresariales
 'Conferencia': ['Coffee break', 'Sonorización de conferencias', 'Proyectores y pantallas de proyección', 'Recepcionistas y personal de registro'],
 'Congreso': ['Coffee break', 'Box lunch y alimentos empacados', 'Sonorización de conferencias', 'Pantallas LED', 'Gafetes y acreditaciones impresas', 'Plataformas de registro e inscripción'],
 'Convención': ['Buffet', 'Coffee break', 'Sonorización de conferencias', 'Pantallas LED', 'Gafetes y acreditaciones impresas'],
 'Seminario': ['Coffee break', 'Sonorización de conferencias', 'Proyectores y pantallas de proyección'],
 'Simposio': ['Coffee break', 'Sonorización de conferencias', 'Proyectores y pantallas de proyección'],
 'Foro': ['Coffee break', 'Sonorización de conferencias', 'Micrófonos y sistemas inalámbricos'],
 'Curso / bootcamp / taller / capacitación': ['Coffee break', 'Box lunch y alimentos empacados', 'Proyectores y pantallas de proyección'],
 'Asamblea': ['Coffee break', 'Sonorización de conferencias', 'Plataformas de registro e inscripción'],
 'Reunión': ['Coffee break', 'Proyectores y pantallas de proyección'],
 'Desayuno / comida / cena de negocios': ['Catering para reuniones corporativas', 'Vino', 'Meseros'],
 'Cóctel': ['Catering de cóctel y canapés', 'Barra de coctelería', 'DJ', 'Meseros'],
 'Lanzamiento': ['Catering de cóctel y canapés', 'Barra de coctelería', 'Pantallas LED', 'Fotografía de eventos', 'Video de eventos'],
 'Activación de marca': ['Escenografía temática', 'Promotores y demostradores de marca', 'Fotografía de eventos'],
 'Inauguración': ['Catering de cóctel y canapés', 'Vinos espumosos y brindis', 'Maestros de ceremonias', 'Fotografía de eventos'],
 'Posada / Navidad / fin de año': ['Buffet', 'Barra libre', 'DJ', 'Escenografía temática', 'Meseros'],
 'Integración': ['Parrilladas y asados', 'Aguas frescas y bebidas preparadas', 'Actividades de integración de equipos'],
 'Team building': ['Box lunch y alimentos empacados', 'Actividades de integración de equipos'],
 'Retiro': ['Buffet', 'Yoga y bienestar grupal', 'Actividades de integración de equipos'],
 'Aniversario': ['Banquete emplatado', 'Barra libre', 'DJ', 'Meseros'],
 'Entrega de premios': ['Banquete emplatado', 'Maestros de ceremonias', 'Iluminación escénica y robótica', 'Fotografía de eventos'],
 'Gala': ['Banquete emplatado', 'Barra libre', 'Grupos musicales y orquestas', 'Centros de mesa florales', 'Meseros'],
 'Rueda de prensa': ['Coffee break', 'Sonorización de conferencias', 'Transmisión en vivo y streaming'],
 'Webinar': ['Transmisión en vivo y streaming', 'Plataformas de registro e inscripción'],
 'Hackathon': ['Box lunch y alimentos empacados', 'Coffee break'],
 'Feria / expo / exhibición / showroom': ['Coffee break', 'Recepcionistas y personal de registro', 'Gafetes y acreditaciones impresas'],
 'Desfile de moda': ['Catering de cóctel y canapés', 'Iluminación escénica y robótica', 'DJ', 'Fotografía de eventos'],
 'Torneo': ['Box lunch y alimentos empacados', 'Aguas frescas y bebidas preparadas'],
 'Despedida de amigos / empleados': ['Catering de cóctel y canapés', 'Cerveza envasada', 'DJ'],
 'Encuentro': ['Coffee break', 'Catering de cóctel y canapés'],
 'Subasta': ['Catering de cóctel y canapés', 'Vino', 'Maestros de ceremonias'],
 'Evento de voluntariado': ['Box lunch y alimentos empacados', 'Aguas frescas y bebidas preparadas'],
}
# sugerencias por universo (la llave repetida «Reunión», «Aniversario», «Gala», «Posada» se separa por universo)
SOC = {k: v for k, v in SUG.items()}
SOC.update({'Reunión': ['Parrilladas y asados', 'Cerveza envasada', 'Sistemas de sonido'], 'Aniversario': ['Banquete emplatado', 'Vino', 'Solistas y cantantes', 'Centros de mesa florales'],
            'Posada / Navidad / fin de año': ['Buffet', 'Aguas frescas y bebidas preparadas', 'Barra libre', 'DJ', 'Piñatas', 'Escenografía temática']})
EMP = dict(SUG)
def keyed(dct, tipo):
    out = {}
    for ev, subs in dct.items():
        ks = [catof[s] + '|' + s for s in subs if s in catof]
        miss = [s for s in subs if s not in catof]
        if miss: print('SUG sin match', ev, miss)
        out[ev] = ks
    return out
sug = {'S': keyed(SOC, 'S'), 'E': keyed(EMP, 'E'), 'defS': keyed({'x': B}, 'S')['x'], 'defE': keyed({'x': ['Coffee break', 'Sonorización de conferencias', 'Meseros']}, 'E')['x']}

js = ('/* ¡Hay que vernos! · Motor de conversión (generado con gen_conv.py, no editar a mano).\n'
      '   Mismas reglas que la hoja «Conversiones de unidades HQV» (Drive de hayquevernos1).\n'
      '   units[u] = [comportamiento, tiempo, rinde para, cantidad típica] · adj["sub|unidad"] = rinde para o "fijo"\n'
      '   staff[sub] = invitados que atiende 1 persona del staff · ref["cat|sub"] = [unidad, precio, personas del paquete] (referencia HQV) */\n'
      'window.HQV_CONV=' + json.dumps({'units': units, 'adj': adj, 'staff': STAFF, 'ref': ref, 'sug': sug}, ensure_ascii=False, separators=(',', ':')) + ';\n' + r'''
/* Calcula cuánto le cuesta al anfitrión una línea de servicio.
   o = {cat, sub, u (unidad canónica o "__otra"), price, guests, hours, rinde (del proveedor), pkgP (personas del paquete), budget (para %)}
   Devuelve {total, qty, pend, note}. pend = true si no hay forma de estimarlo. */
window.hqvCost=function(o){const C=window.HQV_CONV,P=+o.price,g=Math.max(1,+o.guests||1),h=+o.hours||5;
 if(!(P>0))return{total:0,qty:0,pend:true,note:"Sin precio"};
 if(!o.u||o.u==="__otra"){const R=+o.rinde;return R>0?{total:Math.ceil(g/R)*P,qty:Math.ceil(g/R)}:{total:0,qty:0,pend:true,note:"Unidad nueva: el proveedor la cotiza"};}
 const U=C.units[o.u]||["Precio fijo","",null,null],comp=U[0],t=U[1],tm=t==="hora"?h:t==="minuto"?h*60:1;
 const staff=C.staff[o.sub]||(o.cat==="Personal"?null:0);
 if(o.cat==="Personal"&&(comp==="Por persona"||comp==="Por tiempo")){const n=staff?Math.max(1,Math.ceil(g/staff)):1;return{total:P*n*tm,qty:n,note:n>1?`${n} personas de staff (1 por cada ${staff} invitados)`:""};}
 if(comp==="Por persona")return{total:P*g*tm,qty:g};
 if(comp==="Precio fijo")return{total:P,qty:1};
 if(comp==="Por tiempo")return{total:P*tm,qty:1};
 if(comp==="Hora extra")return{total:0,qty:0,extra:P,note:"Solo si la fiesta se alarga"};
 if(comp==="Porcentaje")return{total:P/100*(+o.budget||0),qty:1,note:`${P}% del presupuesto`};
 if(comp==="Paquete"){const n=+o.pkgP||+U[2]||50;const k=Math.ceil(g/n);return{total:k*P,qty:k,note:k>1?`${k} paquetes de ${n} personas`:""};}
 const a=C.adj[o.sub+"|"+o.u],R=+o.rinde||(a==="fijo"?0:+a)||(comp==="Cantidad que define el proveedor"?0:+U[2]);
 if(a==="fijo")return{total:P*tm,qty:1};
 if(R>0){const k=Math.ceil(g/R);return{total:k*P*tm,qty:k};}
 if(comp==="Cantidad que define el proveedor"){const q=+U[3]||1;return{total:q*P*tm,qty:q};}
 return{total:0,qty:0,pend:true,note:"El proveedor te dice cuántas necesitas"};};
''')
open('/home/claude/hqv/v5/conversiones.js', 'w').write(js)
print('ok', len(js), 'ref', len(ref), 'adj', len(adj))
