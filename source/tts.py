#!/usr/bin/python
from __future__ import division
import re
import sys
import subprocess
import math


def separarEnDifonos(s):
	l = []
	difono_init = "-" + s[:1]
	l.append(difono_init)
	while(len(s) > 1):
		difono = s[:2] #Tomar primer difono
		s = s[1:] # recorto la cadena
		l.append(difono) # agrego difono a una lista
	difono_fin = s[:1] + "-"
	l.append(difono_fin)
	return l 

def generarScriptPraat(ls):
	script = ""
	read = ""
	select = ""
	plus = ""
	i = 0
	for x in ls:
		read = "Read from file... difonos_wav/"
		read += x + ".wav\nselect Sound "
		read += x + "\nRename... " + str(i) + "\n"
		script += " " + read
		i+=1
	i = 0
	for x in ls:
		plus = "plus Sound " + str(i) + "\n"
		script += " " + plus
		i+=1
	script += " Concatenate recoverably\n select Sound chain\n Save as WAV file... chain.wav"
	return script


def asignarTonoDePregunta():
	print 'Extrayendo pitch...'
	bash = "praat extraer-pitch-track.praat chain.wav chain.PitchTier 50 300"
	process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]

	#Me grabe haciendo tres preguntas, y por lo que pude ver en praat
	#El pitch se comporta como una onda senoidal, es decir,
	#Del comienzo de la frase comienza a suvir hasta 1/4 de la frase
	#Luego, pasado ese punto, comienza a disminuir hasta 3/4 y nuevamente sube
	#En algunos casos no es tan marcado, por ejemplo en las preguntas mas largas, pero bueno,
	#eso se ve despues

	num_lines = sum(1 for line in open('chain.PitchTier')) #cuento las lineas, asi aproximo el periodo de mi onda senoidal
	num_lines = num_lines - 6
	num_lines = num_lines/3				


	frecIni = 0
	with open("chain.PitchTier", "r+") as f:
		#consigo el primer pitch para guiarme
		praatPitch = f.readlines()
		for line in praatPitch:
			if "value" in line:
				frecIni = re.findall("\d+.\d+", line)
				frecIni = float(frecIni[0])
				break

	with open("chain.PitchTier", "r+") as f:
		praatPitch = f.readlines()
		f.seek(0)
		i = 1
		for line in praatPitch:
			if "value" in line:
				f.write("    value = ")
				
				#Nota: cuanto mas grande es la amplitud del pitch, mas tono de pregunta tiene la frase
				#Pero tambien mas se rome el sonido
				amplitudDelPitch = 100


				f.write( str( amplitudDelPitch*math.cos((i*2*math.pi)/num_lines) + frecIni )) #esta linea hace toda la magia, genera una onda sinoidal de periodo = largo del sonido y amplitud 100
				f.write("\n")
				i = i + 1
			else:
				f.write(line)
		print i
		f.close()


	print 'Re-insertando pitch...'
	bash = "praat reemplazar-pitch-track.praat chain.wav chain.PitchTier chain-mod.wav 50 300"
	process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]






print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

pregunta = 0
if (sys.argv[1][-1] == "?"):
	print 'Es pregunta!'
	pregunta = 1
	sys.argv[1] = sys.argv[1][:-1]
	#borro el caracter para no buscar su difono

l = separarEnDifonos(sys.argv[1])
for x in l:
	print x
script = generarScriptPraat(l)
print script

text_file = open("praatScript", "w")
text_file.write(script)
text_file.close()

bash = "praat praatScript"

process = subprocess.Popen(bash.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]

if(pregunta == 1):
	print 'Asignando prosodia correcta...'
	asignarTonoDePregunta()

# Read from file... difonos_wav/Al.wav
# Read from file... difonos_wav/Am.wav
# Read from file... difonos_wav/A-.wav
# select Sound A-
# plus Sound Al
# select Sound Al
# plus Sound Am
# plus Sound A-
# Concatenate recoverably
# select Sound chain
# Save as WAV file... /chain.wav
