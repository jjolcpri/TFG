import sys
import os
from subprocess import run

#diccionario para traducir codigo en nombre de la especie
inputcode = '/data/users/olcinaj/scripts_TFG/code_spec.tsv'
dictspec = {}
for line in open(inputcode):
	line = line.strip('\n').split('\t')
	code = line[0]
	spec = line[1]
	dictspec[code] = spec

#coger el nombre de la especie a analizar y poner la ruta absoluta de los archivos
code = sys.argv[1]
namespec = dictspec[code]
inputfile = '/data/users/olcinaj/TFGProject/Species/' + namespec + '/10_RepetitiveAnnotation/01_EarlGrey/' + namespec + '_EarlGrey/' + namespec + '_summaryFiles/' + namespec + '.highLevelCount.txt'
permfile = '/data/users/olcinaj/scripts_TFG/Data_Earlgrey.tsv'

#Lista para tener los organismos ya probados
listperm = []
for lines in open(permfile):
	lines = lines.strip('\n')
	if lines[0] == '>':
		nameperm = lines[1:]
		listperm.append(nameperm)

#Prcesado de datos de EarlGrey.
#Diccionario para guardar info
dictspe = {}
#Ir cogiendo y poniendo los datos en terminal y doc
count = 0
for line in open(inputfile):
	count += 1
	if count > 1:
		line = line.strip('\n')
		line = line.split('\t')
		name = line[0]
		cpnumb = line[2]
		genomsize = line[4]
		gencov = float(line[3])
		gencovred = round(gencov, 3)
		gencovgood = format(gencovred, '.3f').replace('.', ',')
		dictspe[name] = [cpnumb, gencovred, gencovgood]
dictspe['Genome Size'] = [genomsize]

#Recorrer diccionario para poner en terminal
for cosa in dictspe.keys():
	if cosa == 'Genome Size':
		print('{:<50} {:<50}'.format('Genome size', dictspe[cosa][0]))
		continue
	print('{:<50} {:<50}'.format(cosa, dictspe[cosa][0] + '; ' + dictspe[cosa][2] + '%'))

#Poner en doc final de guardado si hiciera falta
if namespec in listperm:
	sys.exit()
#Poner nombre
with open('/data/users/olcinaj/scripts_TFG/Data_Earlgrey.tsv', 'a') as anyadir:
	anyadir.write('>' + namespec + '\n')
#Recorrer dicc
for cosa in dictspe.keys():
	if cosa == 'Genome Size':
		with open('/data/users/olcinaj/scripts_TFG/Data_Earlgrey.tsv', 'a') as anyadir:
			anyadir.write('Genome size' + '\t' +  dictspe[cosa][0] + '\n')
			anyadir.write('----' + '\n')
		continue
	with open('/data/users/olcinaj/scripts_TFG/Data_Earlgrey.tsv', 'a') as anyadir:
		anyadir.write(cosa + '\t' + dictspe[cosa][0] + '\t' + str(dictspe[cosa][1]) + '\n')