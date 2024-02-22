import pandas as pd
import sys
import os
import glob
import datetime
import googlemaps

def updt(total, progress,startTime):
    previousTime = startTime
    barLength= 20
    item = progress
    progress = float(progress) / float(total)

    if progress % 10 == 0:
        previousTime = nowTime - previousTime

    if progress >= 1:
        progress, "\r\n"
    block = int(round(barLength * progress))
    nowTimeTemp = datetime.datetime.now()
    nowTime = nowTimeTemp - datetime.timedelta(microseconds=nowTimeTemp.microsecond)
    text = "\r[{}] {}/{} | {:.0f}% | {} ".format(
        "#" * block + "-" * (barLength - block), item,total,round(progress * 100, 0), ( total * (nowTime - startTime) ) / item - (nowTime - startTime))
    sys.stdout.write(text)
    sys.stdout.flush()

gmaps = googlemaps.Client(key='Your Key')

direcciones = glob.glob('CorteJun2022/dir/direcciones/*.csv')

comps = {
  'country': 'MX'
}

for file in direcciones:
    print(file)
    folder = file.split('.')[0]
    os.mkdir(folder) if not os.path.exists(folder) else 0
    df = pd.read_csv(file, sep = ',')

    col = ['idinscripcion', "Full_Address"]
    df_address = df.loc[:, df.columns.isin(list(col))]
    df = df.set_index('idinscripcion')

    df_address.Full_Address = df_address.Full_Address.replace('S/N', '')
    df_address.Full_Address = df_address.Full_Address.replace('SN', '')
    df_address.Full_Address = df_address.Full_Address.replace('S/N.', '')
    df_address.Full_Address = df_address.Full_Address.replace('SIN NUMERO', '')
    df_address.Full_Address = df_address.Full_Address.replace('ENTRE', '')
    df_address.Full_Address = df_address.Full_Address.replace('DESC.', '')
    df_address.Full_Address = df_address.Full_Address.replace('#', '')
    df_address.Full_Address = df_address.Full_Address.replace('CONOCIDO', '')
    df_address.Full_Address = df_address.Full_Address.replace('DESCONOCIDO', '')
    df_address.Full_Address = df_address.Full_Address.replace('SE IGNORA', '')
    df_address.Full_Address = df_address.Full_Address.replace('SIN DATOS', '')
    df_address.Full_Address = df_address.Full_Address.replace('DESC', '')
    df_address.Full_Address = df_address.Full_Address.replace('XXX', '')
    df_address.Full_Address = df_address.Full_Address.replace('SE DESCONOCE', '')
    df_address.Full_Address = df_address.Full_Address.replace('DESCONOCE', '')
    df_address.Full_Address = df_address.Full_Address.replace('SE IGNORA', '')
    df_address.Full_Address = df_address.Full_Address.replace('LOCALIDAD DESCONOCIDA', '')
    df_address.Full_Address = df_address.Full_Address.replace('NO APLICA', '')
    df_address.Full_Address = df_address.Full_Address.replace('/', '')

    #Contador de tiempo inicial
    startTimeTemp = datetime.datetime.now()
    startTime = startTimeTemp - datetime.timedelta(microseconds=startTimeTemp.microsecond)
    runs = len(df_address.Full_Address)
    i=1

    coords = []
    for address in df_address.Full_Address: 
        updt(runs, i,startTime)

        search_location = gmaps.geocode(address, components=comps)
        try:  
            coords.append(str(search_location[0]["geometry"]["location"]["lat"]) + ',' + str(search_location[0]["geometry"]["location"]["lng"]) )
        except:
            coords.append('0,0')
        i+=1

    df_address['Coordinates'] = coords

    col = ['idinscripcion', 'Full_Address', 'Coordinates']
    df1 = df_address.loc[:, df_address.columns.isin(list(col))]

    df2 = df1[~df1.Coordinates.str.contains('0,0')]
    
    df2.to_csv(folder + '/add_errors.csv', index = False)

    #aqui hay que quitar los duplicados en lugar de hacer una copia
    #df1 = df1[df1.Url_With_Coordinates.str.contains('&zoom=')].copy()

    df1['lat'] = [coords.split(',')[0] for coords in df1['Coordinates'] ]
    df1['long'] = [coords.split(',')[1] for coords in df1['Coordinates'] ]

    df1.to_csv(folder + '/Id_Coords.csv', index = False)
print('Obtuve las coordenadas lon,lat de las direcciones con exito')
