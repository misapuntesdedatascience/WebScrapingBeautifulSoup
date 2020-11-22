import requests
import unidecode
import pandas as pd
from bs4 import BeautifulSoup

req = requests.get('https://datosmacro.expansion.com/paises')
soup = BeautifulSoup(req.text, "lxml")

mydivs = soup.findAll("div", {"class": "flgB"})

listaDivs = str(mydivs).split(",")


listaPaises = []
for div in range(len(listaDivs)):
    
    listaTags = listaDivs[div].split(">")
    elementosDiv = listaTags[6].split('<')
    divPais = elementosDiv[0].split('<')
    listaPaises.append(divPais[0])
    

listaPaisesScrapingFormat = []

for scrapingDiv in range(len(listaDivs)):
    
    listaTags = listaDivs[scrapingDiv].split(">")
    elementosDiv = listaTags[1].split('"')
    paisUrl = elementosDiv[1]  
    
    listaPaisesScrapingFormat.append(paisUrl)
    

def obtenerDato(texto, fuente):        
       datoExtraido = None
       try:
           datoExtraido = fuente.find("td", text = texto).find_next_sibling("td").findNext('td').text
              
       except AttributeError:  
            datoExtraido = 'nan'  
            
       return datoExtraido
           
def extraerDato(texto, columna, fuente):    
       
    textoAbuscar = texto        
    dato = obtenerDato(textoAbuscar, fuente)
    columna.append(dato)
       
    
def obtenerTabla(listaPaisesScrapFormat, listaPaisesUTF8Format):

    paises = []
    poblacion = []
    
    densidad = []    
    riesgoPobreza = []
    esperanzaDeVida = []
    
    pibPerCapita = []
    deudaPerCapita = []
    gastoEduPerCapita = []
    gastoSaludPerCapita  = []
    indiceCorrup = []
    salarioMedio = []
    
    emisionesCO2perCapita = []
    
    muertosCovid = []
    casosConfirmados = []
    muertosXmillon = []   
    
    columnas = [pibPerCapita, densidad, riesgoPobreza, esperanzaDeVida, deudaPerCapita,
                gastoEduPerCapita, gastoSaludPerCapita, indiceCorrup, 
                salarioMedio, emisionesCO2perCapita, muertosCovid, casosConfirmados, muertosXmillon]
    
    textoPibPerCapita = "PIB Per Capita [+]"
    textoDensidad = "Densidad [+]"
    textoRiesgoPobreza = "% Riesgo Pobreza [+]"
    textoEsperanzaDeVida = "Esperanza de vida [+]"    
    
    textoDeudaPerCapita = "Deuda Per Cápita [+]"      
    textoGastoEduPerCapita = "Gasto Educación Per Capita [+]"
    textogastoSaludPerCapita = "G. Público Salud Per Capita [+]"
    textoIndiceCorrup = "Índice de Corrupción [+]"
    textoSalarioMedio = "Salario Medio [+]"
    
    textoEmisionesCO2perCapita = "CO2 t  per capita [+]"
    
    textoMuertosCovid = "COVID-19 - Muertos [+]"     
    textoCasosConfirmados = "COVID-19 - Confirmados [+]"
    textoMuertosXmillon = "COVID-19 - Muertos por millón habitantes [+]"
   
    
    
    
    textos = [textoPibPerCapita, textoDensidad, textoRiesgoPobreza,textoEsperanzaDeVida, textoDeudaPerCapita,
              textoGastoEduPerCapita, textogastoSaludPerCapita, textoIndiceCorrup, 
              textoSalarioMedio, textoEmisionesCO2perCapita, textoMuertosCovid, textoCasosConfirmados,
              textoMuertosXmillon]
    
    
    for elementoPais in range(10):#range(len(listaPaisesScrapFormat)):  
        paisUTF8format = listaPaisesUTF8Format[elementoPais]
        paises.append(paisUTF8format)
        print(paisUTF8format)        
         
        url = listaPaisesScrapFormat[elementoPais]
        req = requests.get(f'https://datosmacro.expansion.com/{url}')
        soup = BeautifulSoup(req.text, "lxml")
          
        cuadroPobl = str(soup.findAll("div", class_="cuadro"))
        liPobl = cuadroPobl.split('</li>')
        splitPobl = liPobl[1].split('>')
        elementoPobl = splitPobl[5].split(': ')
        datoPoblacion = elementoPobl[1]
        poblacion.append(datoPoblacion)
        
        for elementoTexto in range(len(textos)):
            extraerDato(textos[elementoTexto], columnas[elementoTexto], soup)
        
    data = {'País':paises,
            'Población':poblacion,
            'Densidad': densidad,
            '%Riesgo Pobreza': riesgoPobreza,
            'Esperanza de vida':esperanzaDeVida,            
            'PIB p.Cap': pibPerCapita,
            'Gasto Edu.p.Cap.': gastoEduPerCapita,
            'Gasto Salud p.Cap.': gastoSaludPerCapita,
            'Índice Corrup.': indiceCorrup,
            'Salario Medio': salarioMedio,
            'Emis.CO2 p.cap.': emisionesCO2perCapita,
            'Decesos':muertosCovid,
            'Casos confirmados':casosConfirmados,
            'Decesos x Mill.': muertosXmillon}
    
    dfPaises = pd.DataFrame(data)   
        
            
    return dfPaises 

dataSetFinal = obtenerTabla(listaPaisesScrapingFormat, listaPaises)

dataSetFinal.to_excel("Covid19yML.xlsx", sheet_name='Covid19yML', index=False)  

        