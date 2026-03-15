
import os
import configparser

import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image

lista_possibili_cartelle_lavoro = [
    '/media/daniele/Daniele2TB/test/gif_radar',
    '/run/media/daniele.carnevale/Daniele2TB/test/gif_radar',
]

lista_possibili_ARC_STORICO = [
    '/media/daniele/Daniele2TB/test/piccolo_ARC_STORICO',
    '/mnt/ARC_STORICO',
]

cartella_lavoro = [
    x for x in lista_possibili_cartelle_lavoro if os.path.exists(x)][0]
os.chdir(cartella_lavoro)
del (lista_possibili_cartelle_lavoro)

cartella_ARC_STORICO = [
    x for x in lista_possibili_ARC_STORICO if os.path.exists(x)][0]
del (lista_possibili_ARC_STORICO)

'''
ssh cmi@omirl-gen1 (pass: pippo)
ssh omirl@omirl-ld (no pass)
cd /var/omirl/files/radarsat/radarRainInt5m/YYYY/MM/DD/images

Per copiare in locale:
vai cmi@omirl-gen1
rsync -rahzPuvv --info=progress2 --include="*/" --include="images/**" --exclude="*" omirl@omirl-ld:/var/omirl/files/radarsat/radarRainInt5m .

poi in locale:
rsync -rahzPuvv --info=progress2 cmi@omirl-gen1:/home/cmi/radarRainInt5m/ .

'''
cartella_ARC_STORICO = f'{cartella_lavoro}/a'

# %% Parametri dal file di configurazione
config = configparser.ConfigParser()
config.read('./config.ini')

##############

inizio_locale = pd.to_datetime(config.get('CONFIG', 'inizio_locale')).tz_localize('Europe/Rome')
fine_locale = pd.to_datetime(config.get('CONFIG', 'fine_locale')).tz_localize('Europe/Rome')

inizio_UTC = inizio_locale.tz_convert('UTC').tz_localize(None)
fine_UTC = fine_locale.tz_convert('UTC').tz_localize(None)

inizio_locale = inizio_locale.tz_localize(None)
fine_locale = fine_locale.tz_localize(None)

print(f"locale {str(inizio_locale):<19}   -   UTC {str(inizio_UTC)}")
print(f"locale {str(inizio_UTC):<19}   -   UTC {str(fine_UTC)}")

nome_gif = config.get('CONFIG', 'nome_gif')
if not nome_gif:
    nome_gif = f"radar_{inizio_locale.strftime('%Y%m%d-%H%M%S')}_{fine_locale.strftime('%Y%m%d-%H%M%S')}"

nome_gif = nome_gif.replace(' ', '_')
print(nome_gif)

##############

### Creo i path per i file .png
tempi_UTC = pd.date_range(inizio_UTC, fine_UTC, freq='5min') + pd.Timedelta(minutes=10)

lista_png = []
for t in tempi_UTC:
    # print(t)
    file_png = f'{cartella_ARC_STORICO}/FC/{t.year}/{t.month:02}/{t.day:02}/ralig{t.hour:02}{t.minute:02}.png'
    # file_png = f'{cartella_ARC_STORICO}/{t.year}/{t.month:02}/{t.day:02}/ralig{t.hour:02}{t.minute:02}.png'
    # file_png = f'{cartella_ARC_STORICO}/{t.year}/{t.month:02}/{t.day:02}/images/radarRainInt5m_std_{t.hour:02}{t.minute:02}.png'
    if '0000' not in file_png:
        if os.path.exists(file_png):
            lista_png.append(file_png)
        else:
            print(f'File {file_png} non trovato. Non lo aggiungo alla gif.')

### Carico le immagini
frames = [Image.open(x) for x in lista_png]

### Salva come GIF
frames[0].save(
    f"{cartella_lavoro}/{nome_gif}_{int(config.get('CONFIG', 'tempo_frame'))}.gif",
    format='GIF',
    append_images=frames[1:],
    save_all=True,
    duration=int(config.get('CONFIG', 'tempo_frame')),
    loop=0
)

print('\n\nDone')
