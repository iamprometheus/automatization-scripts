from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import sys
import os
import glob
import datetime
#print(sys.argv)

#os.chdir('CorteJun2022/dir/direcciones')
direcciones = glob.glob('CorteJun2022/dir/direcciones/*.csv')
print(direcciones)
# Utilidad: Barra de progreso + contador de tiempo
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

for file in direcciones:
    print(file)
    folder = file.split('.')[0]
    os.mkdir(folder) if not os.path.exists(folder) else 0
    df = pd.read_csv(file, sep = ',')
    print(df.shape)

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


    df_address['Url'] = ['https://www.google.com/maps/search/' + str(i) for i in df_address['Full_Address'] ]


    Url_With_Coordinates = []

    # Especificaciones del navegador 
    #
    options = Options()
    s = Service('./geckodriver.exe')
    options.headless = True
    options.add_argument("-disable-dev-shm-usage")
    options.add_argument("-no-sandbox")
    options.add_argument('-disable-gpu')
    options.set_preference("network.http.pipelining", True)
    options.set_preference("network.http.proxy.pipelining", True)
    options.set_preference("network.http.pipelining.maxrequests", 8)
    options.set_preference("content.notify.interval", 500000)
    options.set_preference("content.notify.ontimer", True)
    options.set_preference("content.switch.threshold", 250000)
    options.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
    options.set_preference("browser.startup.homepage", "about:blank")
    options.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
    options.set_preference("browser.pocket.enabled", False) # Duck pocket too!
    options.set_preference("loop.enabled", False)
    options.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
    options.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
    options.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
    options.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
    options.set_preference("browser.display.use_system_colors", True) # Use system colors.
    options.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
    options.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
    options.set_preference("browser.shell.checkDefaultBrowser", False)
    options.set_preference("browser.startup.homepage", "about:blank")
    options.set_preference("browser.startup.page", 0) # blank
    options.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
    options.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
    options.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
    options.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
    options.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
    options.set_preference("extensions.checkCompatibility", False) # Addon update disabled
    options.set_preference("extensions.checkUpdateSecurity", False)
    options.set_preference("extensions.update.autoUpdateEnabled", False)
    options.set_preference("extensions.update.enabled", False)
    options.set_preference("general.startup.browser", False)
    options.set_preference("plugin.default_plugin_disabled", False)
    options.set_preference("permissions.default.image", 2)
    driver = webdriver.Firefox(options=options,service = s)

    #Contador de tiempo inicial
    startTimeTemp = datetime.datetime.now()
    startTime = startTimeTemp - datetime.timedelta(microseconds=startTimeTemp.microsecond)
    runs = len(df_address.Url)
    i=1
    for url in df_address.Url: 
        driver.get(url)
        Url_With_Coordinates.append(driver.find_element(By.CSS_SELECTOR,'meta[itemprop=image]').get_attribute('content'))
        updt(runs, i,startTime)
        i+=1
    driver.close()
        
    #print(Url_With_Coordinates)
    import csv
    with open(folder + '/Url_With_Coordinates.csv', 'w') as file:
        wr = csv.writer(file)
        wr.writerow(Url_With_Coordinates)

    df_address['Url_With_Coordinates'] = Url_With_Coordinates

    col = ['idinscripcion', 'Full_Address', 'Url_With_Coordinates']
    df1 = df_address.loc[:, df_address.columns.isin(list(col))]

    df_address.to_csv(folder + '/address.csv', index = False)

    df2 = df1[~df1.Url_With_Coordinates.str.contains('&zoom=')]


    df2.to_csv(folder + '/add_errors.csv', index = False)

    #aqui hay que quitar los duplicados en lugar de hacer una copia
    df1 = df1[df1.Url_With_Coordinates.str.contains('&zoom=')].copy()

    df1['lat'] = [url.split('?center=')[1].split('&zoom=')[0].split('%2C')[0] for url in df1['Url_With_Coordinates'] ]
    df1['long'] = [url.split('?center=')[1].split('&zoom=')[0].split('%2C')[1] for url in df1['Url_With_Coordinates'] ]
    #print(df1)

    dfc = df1.drop(['Full_Address', 'Url_With_Coordinates'], axis = 1)

    #print(dfc)
    dfc = dfc.set_index('idinscripcion')
    df1.to_csv(folder + '/coordenadasdf1prueba.csv', index = False)
    dffin = pd.concat([df, dfc], axis = 1)
    dffin = dffin.reset_index()
    dffin.to_csv(folder + '/coordenadasprueba.csv', index = False)
    dffin.to_csv(folder + '/faltantesprueba.csv', index = False)
print('Obtuve las coordenadas lon,lat de las direcciones con exito')

