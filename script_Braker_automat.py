import sys
import os
from subprocess import run

#crear un diccionario con lo que queremos comparar
dictfof = {}
fof = '/data/users/olcinaj/scripts_TFG/fof_Braker.tsv'
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


#Buscar cosas para braker
dictbraker = {}
for mycode in dictfof.keys():
	#Busqueda del fasta del my genome
	nomb = dictspec[mycode]
	routemy = '/data/users/olcinaj/TFGProject/Species/' + nomb + '/10_RepetitiveAnnotation/01_EarlGrey/' + nomb + '_EarlGrey/' + nomb + '_summaryFiles/'
	for name in os.listdir(routemy):
		soft = nomb + '.softmasked.fasta'
		if name == soft:
			fastamygenome = name
	myfasta = routemy + '/' + fastamygenome
	#Busqueda del fasta y del gff del refcode
	for refcode in dictfof[mycode]:
		routeref = '/data/users/olcinaj/TFGProject/Species/' + dictspec[refcode] + '/00_source'
		countfasta = 0
		countgff = 0
		for name in os.listdir(routeref):
			comp = name.split('.')
			if comp[-1] in ('fa', 'fasta', 'fna', 'fas'):
				countfasta += 1
				if countfasta > 1:
					sys.exit('error con el fasta del ref')
				fastarefgenome = name
			elif comp[-1] in ('gff', 'gff3'):
				countgff += 1
				if countgff > 1:
					sys.exit('error con el gff del ref')
				gffrefgenome = name
		reffasta = routeref + '/' + fastarefgenome
		refgff = routeref + '/' + gffrefgenome
	#Poner todo en un diccionario para poder usarlo mas adelante
		dictbraker['{}_{}'.format(mycode, refcode)] = [myfasta, refgff, reffasta, mycode, refcode]

#Funcion para ejecutar gffread
def gffread (routeprot, fastaref, gffref):
	cmdgff = 'gffread -V -y {} -g {} {}'.format(routeprot, fastaref, gffref)
	print(cmdgff)
	resultgff = run(cmdgff, capture_output=True, shell=True, text=True)
	if resultgff.returncode != 0:
		print("Error en gffread:", resultgff.stderr)

def braker (fastamy, nameesp, nameprot, dirbraker, mycode, refcode):
	cmdbraker = 'braker.pl --genome={} --species={} --prot_seq={} --gff3 --threads 8 --workingdir={}'.format(fastamy, nameesp, nameprot, dirbraker)
	print(cmdbraker)
	resultbraker = run(cmdbraker, capture_output=True, shell=True, text=True)
	with open('/data/users/olcinaj/scripts_TFG/Brakerlogs/{}_{}log.txt'.format(mycode, refcode), 'w') as filebraker:
		filebraker.write(resultbraker.stdout)
	print(resultbraker.stderr)
	print(resultbraker.stdout)
	if resultbraker.returncode != 0:
		print("Error en braker:", resultbraker.stderr)

if __name__ == "__main__":
	for caso in dictbraker.keys():
		#Creacion de directorios para meter info
		newdirect = dictbraker[caso][4]
		mycode = dictbraker[caso][3]
		outdir = '/data/users/olcinaj/TFGProject/Species/' + dictspec[mycode] + '/02_ABI_Braker2/' + newdirect
		os.makedirs(outdir, exist_ok=True)
		#Ejecucion de gffread
		docprot = dictbraker[caso][4] + '.protein.fasta'
		routedoc = '/data/users/olcinaj/TFGProject/Species/' + dictspec[dictbraker[caso][4]] + '/02_ABI_Braker2/' + docprot
		if not os.path.exists(routedoc):
			gffread(routedoc, dictbraker[caso][2], dictbraker[caso][1])
		if os.path.exists("stopBraker.txt"):
			sys.exit("Se encontro 'stopBraker.txt'. Finalizando antes del proximo analisis.")
		#Ejecucion de braker
		namespc = dictbraker[caso][3] + '_' + dictbraker[caso][4] + '_braker'
		braker(dictbraker[caso][0], namespc, routedoc, outdir, dictbraker[caso][3], dictbraker[caso][4])