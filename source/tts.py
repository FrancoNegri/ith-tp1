#!/usr/bin/python

import sys
import subprocess


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



	#aca modifico los values de chain.PitchTier para cambiar el pitch


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