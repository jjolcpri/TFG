import sys
import os
from subprocess import run
import shutil
import time
from datetime import datetime

#crear un diccionario con lo que queremos comparar
dictfof = {}
fof = '/data/users/olcinaj/scripts_TFG/fof_GAQET.tsv'
for line in open(fof):
	line = line.strip('\n').split('\t')
	mycode = line[0]
	refcodes = line[1].split(' ')
	dictfof[mycode] = refcodes

#diccionario para traducir codigo en nombre de la especie
inputcode = '/data/users/olcinaj/scripts_TFG/code_spec.tsv'
dictspec = {}
for line in open(inputcode):
	line = line.strip('\n').split('\t')
	code = line[0]
	spec = line[1]
	dictspec[code] = spec

#diccionario para buscar taxon IDs
#diccionario para traducir codigo en nombre de la especie
inputID = '/data/users/olcinaj/scripts_TFG/code_ID.tsv'
dictID = {}
for line in open(inputID):
	line = line.strip('\n').split('\t')
	code = line[0]
	ID = line[1]
	dictID[code] = ID

#buscar el fasta
dictgaqet = {}
for mycode in dictfof.keys():
	#Busqueda del fasta del genoma
	routemy = '/data/users/olcinaj/TFGProject/Species/' + dictspec[mycode] + '/00_source'
	count = 0
	for name in os.listdir(routemy):
		comp = name.split('.')
		if comp[-1] in ('fa', 'fasta', 'fna', 'fas'):
			count += 1
			if count > 1:
				sys.exit('error con el fasta del my')
			fastamygenome = name
	myfasta = routemy + '/' + fastamygenome
	#Busqueda de los gff del refcode
	for refcode in dictfof[mycode]:
		#ref code de gemoma
		routegemoma = '/data/users/olcinaj/TFGProject/Species/' + dictspec[mycode] + '/01_EVP_GeMoMa/' + refcode + '/' + 'final_annotation.gff'
		#ref code de braker
		routebraker = '/data/users/olcinaj/TFGProject/Species/' + dictspec[mycode] + '/02_ABI_Braker2/' + refcode + '/' + 'braker.gff3'
		dictgaqet['{}_{}'.format(mycode, refcode)] = [myfasta, routegemoma, routebraker, mycode, refcode]

#definir función de gaqet
def gaqet(yaml, esp, fasta, gff, id, outdir, codename, coderef, analis):
	cmd = 'GAQET --yaml {} -s {} -g {} -a {} -t {} -o {}'.format(yaml, esp, fasta, gff, id, outdir)
	print(cmd)
	results = run(cmd, capture_output=True, shell=True, text=True)
	with open('/data/users/olcinaj/scripts_TFG/GAQETlogs/{}_{}_{}log.txt'.format(mycode, refcode, analis), 'w') as filegaqet:
		filegaqet.write(results.stdout)
		filegaqet.write(results.stderr)
	print(results.stdout)
	print(results.stderr)
	if results.returncode != 0:
		print("Error en gaqet:", results.stderr)

if __name__ == "__main__":
	for caso in dictgaqet.keys():
		#poner el yaml
		yaml = '/data/users/olcinaj/scripts_TFG/YAML.txt'
		esp = dictspec[dictgaqet[caso][3]]
		ID = dictID[dictgaqet[caso][3]]
		mycode = dictgaqet[caso][3]
		refcode = dictgaqet[caso][4]
		#GeMoMa
		analis = 'GeMoMa'
		#iniciar contador
		start_time = datetime.now()
		texto_inicial = 'Inicio' + '_' + mycode + '_' + refcode + '_' + analis + ':' + start_time.strftime('%H:%M:%S')
		#Creacion de directorio de gemoma para meter info
		if os.path.exists("stopGAQET.txt"):
			sys.exit("Se encontro 'stopGAQET.txt'. Finalizando antes del proximo analisis.")
		outdirgemoma = 'GAQET2_DATA/GeMoMa/' + mycode + '/' + refcode
		os.makedirs(outdirgemoma, exist_ok=True)
		#correr analisis de genmoma
		gaqet(yaml, esp, dictgaqet[caso][0], dictgaqet[caso][1], ID, outdirgemoma, mycode, refcode, analis)
		#relocalización de la informacion generada por BUSCO para hacer bien el resumen de GAQET
		directbusco = '/data/users/olcinaj/scripts_TFG' + '/' + refcode + '/' + 'BUSCOCompleteness_run'
		directfinal = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/GeMoMa/' + mycode + '/' + refcode + '/' + 'BUSCOCompleteness_run'
		print(directbusco, directfinal)
		if os.path.exists(directfinal):
			shutil.rmtree(directfinal)
		shutil.move(directbusco, directfinal)
		#duplicacion del log del programa por si acaso
		archivo_log = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/GeMoMa/' + mycode + '/' + refcode + '/' + 'GAQET.log.txt'
		copia_log = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/GeMoMa/' + mycode + '/' + refcode + '/' + 'GAQET_analis.log.txt'
		shutil.copy(archivo_log, copia_log)
		gaqet(yaml, esp, dictgaqet[caso][0], dictgaqet[caso][1], ID, outdirgemoma, mycode, refcode, analis)
		#mirar el tiempo
		end_time = datetime.now()
		texto_final = 'Final' + '_' + mycode + '_' + refcode + '_' + analis + ':' + end_time.strftime('%H:%M:%S')
		with open ('/data/users/olcinaj/scripts_TFG/times', 'a') as anyadir:
			anyadir.write(texto_inicial + '\n' + texto_final + '\n')
		#braker
		analis = 'Braker'
		#iniciar nuevo contador
		start_time = datetime.now()
		texto_inicial = 'Inicio' + '_' + mycode + '_' + refcode + '_' + analis + ':' + start_time.strftime('%H:%M:%S')
		#creacion de directorio de braker
		outdirbraker = 'GAQET2_DATA/Braker/' + mycode + '/' + refcode
		os.makedirs(outdirbraker, exist_ok=True)
		#correr analisis para braker
		gaqet(yaml, esp, dictgaqet[caso][0], dictgaqet[caso][2], ID, outdirbraker, mycode, refcode, analis)
		#relocalización de la informacion generada por BUSCO para hacer bien el resumen de GAQET
		directbusco = '/data/users/olcinaj/scripts_TFG' + '/' + refcode + '/' + 'BUSCOCompleteness_run'
		directfinal = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/Braker/' + mycode + '/' + refcode + '/' + 'BUSCOCompleteness_run'
		print(directbusco, directfinal)
		if os.path.exists(directfinal):
			shutil.rmtree(directfinal)
		shutil.move(directbusco, directfinal)
		#duplicacion del log del programa por si acaso
		archivo_log = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/Braker/' + mycode + '/' + refcode + '/' + 'GAQET.log.txt'
		copia_log = '/data/users/olcinaj/scripts_TFG/GAQET2_DATA/Braker/' + mycode + '/' + refcode + '/' + 'GAQET_analis.log.txt'
		shutil.copy(archivo_log, copia_log)
		gaqet(yaml, esp, dictgaqet[caso][0], dictgaqet[caso][2], ID, outdirbraker, mycode, refcode, analis)
		#mirar el tiempo
		end_time = datetime.now()
		texto_final = 'Final' + '_' + mycode + '_' + refcode + '_' + analis + ':' + end_time.strftime('%H:%M:%S')
		with open ('/data/users/olcinaj/scripts_TFG/times', 'a') as anyadir:
			anyadir.write(texto_inicial + '\n' + texto_final + '\n')
