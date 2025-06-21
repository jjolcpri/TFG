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

#coger los nombres del fof
listfof = []
fof = '/data/users/olcinaj/scripts_TFG/fof_earlgrey.txt'
for line in open(fof):
	line = line.strip('\n')
	listfof.append(line)

#hacer un diccionario con toda la info necesaria
dictearlgrey = {}
for code in listfof:
    #buscar el directorio de salida en cada caso
    outdir = '/data/users/olcinaj/TFGProject/Species/' + dictspec[code] + '/10_RepetitiveAnnotation/01_EarlGrey'
    #coger la ruta absoluta del fasta de la especie
    routemy = '/data/users/olcinaj/TFGProject/Species/' + dictspec[code] + '/00_source'
    count = 0
    for name in os.listdir(routemy):
	    comp = name.split('.')
		if comp[-1] in ('fa', 'fasta', 'fna', 'fas'):
		    count += 1
			if count > 1:
				sys.exit('error con el fasta del my')
		    fastamygenome = name
    myfasta = routemy + '/' + fastamygenome
    dictearlgrey[code] = [myfasta, dictspec[code], outdir]


#definir funcion para ejecutar earlgrey
def earlgrey (code, fastamy, name_spec, out):
	cmd = 'earlGrey -g {} -s {} -o {} -t 24 -d yes -e yes'.format(fastamy, name_spec, out)
	print(cmd)
	results = run(cmd, capture_output=True, shell=True, text=True)
	with open('/data/users/olcinaj/scripts_TFG/Earlgreylogs/{}log.txt'.format(code), 'w') as file:
		file.write(results.stdout)

if __name__ == "__main__":
	#ejecutar earlgrey
	for caso in dictearlgrey.keys():
		if os.path.exists("stopEarlgrey.txt"):
			sys.exit("Se encontró 'stopEarlgrey.txt'. Finalizando antes del próximo análisis.")
		else:
			earlgrey(caso, dictearlgrey[caso][0], dictearlgrey[caso][1], dictearlgrey[caso][2])
