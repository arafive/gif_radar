
import os

cartella_out = '/run/media/daniele.carnevale/Daniele2TB/test/gif_radar/ordine'

for m in range(1, 13):
    mese = f'{m:02d}'
    print(f"{mese=}")

    cartella_out_2 = f"{cartella_out}/{mese}"
    os.makedirs(cartella_out_2, exist_ok=True)
    
    cartella_in = f'/run/media/daniele.carnevale/Daniele2TB/test/gif_radar/a/2025/{mese}'
    
    for giorno in sorted(os.listdir(cartella_in)):
        print(f"- {giorno=}")
        
        for j in sorted(os.listdir(f'{cartella_in}/{giorno}/images')):
            
            comando = f"cp {cartella_in}/{giorno}/images/{j} {cartella_out_2}/{mese}_{giorno}_{j}"
            if not os.path.exists("{cartella_out_2}/{mese}_{giorno}_{j}"):
                # print(comando)
                os.system(comando)
    
print('\n\nDone')
