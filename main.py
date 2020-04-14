# https://github.com/jiaaro/pydub

from pydub import AudioSegment
from googletrans import Translator
import sys
import time
import csv

def is_time(s):
	try:
		time.strptime(s, '%H:%M:%S')
		return True
	except:
		try:
			time.strptime(s, '%M:%S')
			return True
		except:
			return False


def extract_part(file, outfile, smin, ssec, emin, esec):
	startMin = smin
	startSec = ssec
	endMin = emin
	endSec = esec

	# Time to miliseconds
	startTime = startMin * 60 * 1000 + startSec * 1000
	endTime = endMin * 60 * 1000 + endSec * 1000

	# Opening file and extracting segment
	song = AudioSegment.from_mp3(file)
	extract = song[startTime:endTime]

	# Saving
	extract.export(outfile, format="mp3")


def extract_sentences(file):
	lines = open(file).readlines()
	sentences = []
	curr_sent = ''
	times = []
	start = None

	for i, line in enumerate(lines):
		line = line.strip()
		
		if is_time(line):			
			if start is None:
				start = line
				times.append(start)
			continue
		else:
			curr_sent+= ' ' + line
			if line.endswith('.'):
				sentences.append(curr_sent)
				curr_sent = ''
				start = None
				
	return sentences, times

if __name__ == '__main__':
	transcript = sys.argv[1]
	audiofile = sys.argv[2]
	outfile = sys.argv[3]
	AUDIO_OUT_PATH = sys.argv[4] # folder to store audios
	AUDIO_OUT_PREFIX = sys.argv[5] # file name prefix
	
	s, t = extract_sentences(transcript)
	print(len(s))
	x=1/0
	delta_end = 0.75
	dados = []
	ID = 0

	SRC = 'fr'
	DEST = 'pt'
	gtranslate = Translator()
	
	for i in range(len(s) - 1):
		start = t[i]
		end = t[i + 1]
		smin = float(start.split(':')[0])
		ssec = float(start.split(':')[1])
		emin = float(end.split(':')[0])
		esec = float(end.split(':')[1]) + delta_end

		if esec >= 60:
			emin+= 1
			esec = 0

		sentence = s[i].strip()

		try:
			time.sleep(1)
			trans = gtranslate.translate(sentence, src=SRC, dest=DEST).text
		except:
			trans = 'no translation'

		audio_out = AUDIO_OUT_PATH +  AUDIO_OUT_PREFIX + str(ID) + '.mp3'
		extract_part(audiofile, audio_out, smin, ssec, emin, esec)		
		dados.append([ID, sentence, trans, '[sound:' + AUDIO_OUT_PREFIX + str(ID) + '.mp3]'])
		ID+= 1

	with open(outfile, 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(dados)
