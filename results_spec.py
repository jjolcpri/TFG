import sys
from subprocess import run

#diccionario para traducir codigo en nombre de la especie
inputcode = '/data/users/olcinaj/scripts_TFG/code_spec.tsv'
list_code = []
dictspec = {}
for line in open(inputcode):
	line = line.strip('\n').split('\t')
	code = line[0]
	spec = line[1]
	list_code.append(code)
	dictspec[code] = spec

#crear un doc con las relaciones a analizar
dictresults = {}
count = 0
order = '/data/users/olcinaj/scripts_TFG/order_results.txt'
for line in open(order):
	count += 1
	if count == 1:
		analis = line.strip('\n')
	else:
		line = line.strip('\n').split('\t')
		mycode = line[0]
		refcodes = line[1]
		dictresults[mycode] = refcodes

dictfinal = {}
for my_code in dictresults.keys():
	#coger los datos de gaqet
	ref_code = dictresults[my_code]
	inputcode = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/' + analis + '/' + my_code + '/' + ref_code + '/' + dictspec[my_code] + '_GAQET.stats.tsv'
	dictvar = {}
	dictdata = {}
	dictnum = {}
	#hacer contador para recoger info
	countline = 0
	countvar = 0
	countdata = 0
	for line in open(inputcode):
		countline += 1
		line = line.strip('\n').split('\t')
		if countline == 1:
			for elem in line:
				countvar += 1
				dictvar[countvar] = elem
		if countline == 2:
			for elem in line:
				countdata += 1
				dictdata[countdata] = elem
	for numb in dictvar.keys():
		dictnum[numb] = [dictvar[numb], dictdata[numb]]
	#crear el diccionario con toda la info de interés:
	dictfinal['{}_{}'.format(my_code, ref_code)] = [dictnum]

#hacer listas para guardar la informacion
list_var = []
list_data = []
#contador para poner los datos de interes en el doc final
count = 0
filefinal = '/data/users/olcinaj/scripts_TFG/RESULTADOS.txt'
with open(filefinal, 'w') as file:
	file.write('Analisis de:' + analis + '\n')
for code in dictfinal.keys():
	#ir cogiendo por el numero que son los datos mas interesentas
	numb_int = [5, 6, 7, 8, 12, 14, 15, 16, 17, 18, 31, 37, 38]
	numb_busco_omark = [29, 30, 34]
	numb_detenga = [32, 33]
	numb_omark_esp = 35
	numb_omark_otro = 36
	for data in dictfinal[code]:
		count_omark = 0
		variables = 'Variables:' + '/'
		datos = ''
		for pos_num in data.keys():
			if pos_num in numb_int:
				variables += data[pos_num][0] + '/'
				datos += data[pos_num][1] + '/'
			elif pos_num in numb_busco_omark:
				variables += data[pos_num][0] + '/'
				datos += 'Result:' + '/'
				result_varios = data[pos_num][1].split('%')
				result_varios = [x for x in result_varios if x.strip() != '']
				for caso in result_varios:
					caso = caso.split(':')
					variables += caso[0] + '/'
					datos += caso[1] + '/'
			elif pos_num in numb_detenga:
				variables += data[pos_num][0] + '/'
				if data[pos_num][1] == 'FAILED':
					datos += 'FAILED' + '/' + 'FAILED' + '/'
				else:
					datos += 'Result:' + '/'
					caso = data[pos_num][1].split(';')[5]
					caso = caso.split(': ')
					variables += caso[0] + '/'
					datos += caso[1] + '/'
			elif pos_num == numb_omark_otro:
				variables += data[pos_num][0] + '/' + data[pos_num][0] + '/'
				dada = data[pos_num][1].split(': ')
				datos += dada[0] + '/' + dada[1] + '/'
			elif pos_num == numb_omark_esp:
				variables += data[pos_num][0] + '/'
				datos += 'Result:' + '/'
				result_varios = data[pos_num][1].split('; ')
				result_uno = result_varios[0].split(': ')
				variables += result_uno[0] + '/'
				datos += result_uno[1] + '/'
				result_dos = result_varios[1].split('%')
				result_dos = [x for x in result_dos if x.strip() != '']
				for caso in result_dos:
					caso = caso.split(':')
					variables += caso[0] + '/'
					datos += caso[1] + '/'
		count += 1
		with open(filefinal, 'a') as file:
			if count == 1:
				file.write(variables + '\n')
				file.write(code + '/' + datos + '\n')
			else:
				file.write(code + '/' + datos + '\n')