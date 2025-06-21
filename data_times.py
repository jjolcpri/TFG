import sys

#diccionario para traducir codigo en nombre de la especie
inputcode = '/data/users/olcinaj/scripts_TFG/code_spec.tsv'
dictspec = {}
for line in open(inputcode):
	line = line.strip('\n').split('\t')
	code = line[0]
	spec = line[1]
	dictspec[code] = spec

#crear un diccionario con lo que queremos comparar
dictfof = {}
fof = '/data/users/olcinaj/scripts_TFG/fof_time.tsv'
for line in open(fof):
	line = line.strip('\n').split('\t')
	mycode = line[0]
	refcodes = line[1].split(' ')
	dictfof[mycode] = refcodes

#conversor de tiempo
def convert_to_time (sec):
	hours = sec // 3600
	minutes = (sec % 3600) // 60
	seconds = sec % 60
	return f"{hours}:{minutes:02}:{seconds:02}"

def convert_to_seconds (time_one, time_two, day_one, day_two):
	spliting = time_one.split(':')
	hours = int(spliting[0])
	minutes = int(spliting[1])
	seconds = int(spliting[2])
	#pasar todo a segundos
	total_sec_one = hours * 3600 + minutes * 60 + seconds
	spliting = time_two.split(':')
	hours = int(spliting[0])
	minutes = int(spliting[1])
	seconds = int(spliting[2])
	#pasar todo a segundos
	total_sec_two = hours * 3600 + minutes * 60 + seconds
	dif_days = int(day_two) - int(day_one)
	if dif_days == 0:
		total_sec = total_sec_two - total_sec_one
	elif dif_days == 1 or dif_days == -30 or dif_days == -29:
		total_sec = 86400 - total_sec_one + total_sec_two
	elif dif_days == 2:
		total_sec = 86400 - total_sec_one + total_sec_two + 86400
	return total_sec


for mycode in dictfof.keys():
	for refcode in dictfof[mycode]:
		myspec = dictspec[mycode]
		caso = mycode + '_' + refcode
		print(caso)
		#tiempo gemoma
		#direccion del archivo a analizar
		gemdir = '/data/users/olcinaj/TFGProject/Species/' + myspec + '/01_EVP_GeMoMa/' + refcode + '/' + 'protocol_GeMoMaPipeline.txt'
		#recorrer el archivo y extraer el tiempo
		for line in open(gemdir):
			line = line.strip('\n').split(' ')
			if line[0] == 'Elapsed':
				sec_gemoma = int(line[2])
		#en horas y minutos de manera aproximada:
		final_gemoma = convert_to_time(sec_gemoma)
		print(final_gemoma)
		#guardar en doc
		with open('/data/users/olcinaj/scripts_TFG/TIME/data_time_GeMoMa.txt', 'a') as anyadir:
			anyadir.write(caso + ';' + final_gemoma + '\n')
		#tiempo braker
		brakdir = '/data/users/olcinaj/TFGProject/Species/' + myspec + '/02_ABI_Braker2/' + refcode + '/' + 'braker.log'
		#reocrrer el archivo y extraer el tiempo
		count = 0
		for line in open(brakdir):
			line = line.strip('\n').split(' ')
			if line[0] == '#' and line[-3] == 'braker.pl' and line[-2] == 'version':
				day_one = int(line[-6])
				hours_one = line[-5]
			if line[0] == '#' and line [-6] == 'deleting' and line[-5] == 'job':
				day_two = int(line[-9])
				hours_two = line[-8]
		sec_braker = convert_to_seconds(hours_one, hours_two, day_one, day_two)
		final_braker = convert_to_time(sec_braker)
		print(final_braker)
		with open('/data/users/olcinaj/scripts_TFG/TIME/data_time_Braker.txt', 'a') as anyadir:
			anyadir.write(caso + ';' + final_braker + '\n')