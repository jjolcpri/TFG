import sys
import os
from subprocess import run

#crear un diccionario con lo que queremos comparar
dictfof = {}
fof = '/data/users/olcinaj/scripts_TFG/fof_GeMoMa.tsv'
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

#Buscar cosas para gemoma
dictgemoma = {}
for mycode in dictfof.keys():
	#Busqueda del fasta del my genome
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
		dictgemoma['{}_{}'.format(mycode, refcode)] = [myfasta, refgff, reffasta, mycode, refcode]

#Funcion para ejecutar gemoma
def gemoma (outdir, tfasta, agff, gfasta, mycode, refcode):
	cmd = 'GeMoMa -Xmx64g GeMoMaPipeline threads=12 outdir={} GeMoMa.Score=ReAlign AnnotationFinalizer.r=NO o=true t={} a={} g={}'.format(outdir, tfasta, agff, gfasta)
	print(cmd)
	results = run(cmd, capture_output=True, shell=True, text=True)
	print(results.stdout)
	with open('/data/users/olcinaj/scripts_TFG/GeMoMalogs/{}_{}log.txt'.format(mycode, refcode), 'w') as file:
		file.write(results.stdout)
	if results.returncode != 0:
		print("Error en gemoma:", results.stderr)

#Ejecucion de todo junto
if __name__ == "__main__":
	for caso in dictgemoma.keys():
		#Creacion de directorios para meter info
		newdirect = dictgemoma[caso][4]
		mycode = dictgemoma[caso][3]
		outdir = '/data/users/olcinaj/TFGProject/Species/' + dictspec[mycode] + '/01_EVP_GeMoMa/' + newdirect
		os.makedirs(outdir, exist_ok=True)
		if os.path.exists("stopGemoma.txt"):
			sys.exit("Se encontro 'stopGemoma.txt'. Finalizando ante del proximo analisis.")
		else:
			#Ejecucion de gemoma
			gemoma(outdir, dictgemoma[caso][0], dictgemoma[caso][1], dictgemoma[caso][2], dictgemoma[caso][3], dictgemoma[caso][4])
