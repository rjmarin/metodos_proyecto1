import requests 
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
import scipy.stats as st
from scipy.stats import chisquare
from scipy.stats import chi2_contingency
#####OJO estos valoress pueden cambiar ya que consultan directamente a la base de datos######
#####Tomar en cuenta que los valores de españa solo llegaron al 29 de abril

#consulta de datos
URL = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
r = requests.get(url = URL) 
data = r.json() 
esp = 0
ita = 0
deaths_ita = []
deaths_esp =[] 
days = []
total_deaths_days = []
poblacionesp = 0
poblacionita = 0
for d in data["records"]:
        if d['countryterritoryCode'] == 'ITA' and int(d['month']) >2 and int(d['month']) <5 : 
            ita += int(d['deaths'])
            poblacion_ita = int(d['popData2018'])
            deaths_ita.append(int(d['deaths']))
            days.append(d['dateRep'])
                     
        if d['countryterritoryCode'] == 'ESP' and int(d['month']) >2  and int(d['month']) <5:
            esp += int(d['deaths'])
            poblacion_esp = int(d['popData2018'])
            deaths_esp.append(int(d['deaths']))

total_deaths = ita + esp
deaths_ita.extend(deaths_esp) #total de datos
columns = int(len(deaths_ita)**(1/2)) # cantiadad de columnas

#datos generales
print("Data of deaths:\n", deaths_ita) 
print("              porcentaje             muertes     poblacion")
print(" Deaths ESP",100*esp/poblacion_esp, esp, poblacion_esp )
print(" Deaths ITA",100*ita/poblacion_ita, ita, poblacion_ita )
print(" Deaths total",100*(ita +esp)/(poblacion_ita + poblacion_esp), ita +esp, poblacion_ita + poblacion_esp )


#histograma
counts, bins, bars =plt.hist(deaths_ita, density=True, bins=columns)
mn, mx = plt.xlim()
plt.xlim(mn, mx)
kde_xs = np.linspace(mn, mx, 1000)
kde = st.gaussian_kde(deaths_ita)
plt.plot(kde_xs, kde.pdf(kde_xs), label="curva")
plt.legend(loc="upper left")
plt.ylabel('Frecuencia en la Cantidad de dias')
plt.xlabel('cantidad de Muertos')
plt.title("Histograma de las muertes en Marzo y Abril\nmuertos totales:"+ str(total_deaths))
plt.show()

#limites de valores de las columnas
binlist = np.c_[bins[:-1],bins[1:]]


#datos por columna
d = np.array(deaths_ita)
mean = d.sum()/len(d) #promedio
stdev = np.std(d)#desviacion
map_data = []


for i in range(len(binlist)):
    if i == len(binlist)-1:
        l = d[(d >= binlist[i,0]) & (d <= binlist[i,1])]
    else:
        l = d[(d >= binlist[i,0]) & (d < binlist[i,1])]
    map_data.append(list(l))


print("Promedio",mean)
print("desviacion", stdev)
observed_frecuency = []
excepted_frecuency = []
for i in binlist:
    if i.any() == 0.0:
        expect =st.norm(mean, stdev).cdf(i[0])
    else:  
        expect =expect =st.norm(mean, stdev).cdf(i[1]) -st.norm(mean, stdev).cdf(i[0])
    print(expect)
    excepted_frecuency.append(expect*len(deaths_ita))
#limites de valores de las columnas y sus frecuencias
print("\nTabla de frecuencias")
print("        Rango        | Observada  |   Esperada ")
for frec in range(len(map_data)):
    observed_frecuency.append(len(map_data[frec]))
    print(binlist[frec], len(map_data[frec]),excepted_frecuency[frec] )

chi2 = chisquare(observed_frecuency, excepted_frecuency)
print(chi2)
