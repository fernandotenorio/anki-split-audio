import multiprocessing as mp
import csv
import random
from subprocess import call

def sayit(arg):
	#call(['say', '-f', arg[0], '-v', arg[1], '-o', arg[2]])
	call(['say', arg[0], '-v', arg[1], '-o', arg[2]])

if __name__ == '__main__':
    N_CPU = 4
    pool = mp.Pool(N_CPU)

    with open('ru_eng.csv') as f:
    	reader = csv.reader(f)
    	arg_list = []
    	voices = ['yuri', 'milena', 'katya']

        for line in reader:
    	   ru_text = line[0].decode('utf-8', 'ignore')
    	   audio_file = line[-1][1:-1].split(':')[1]
    	   #args = (ru_text, random.choice(voices), 'audio/'+ audio_file)
           args = (ru_text, random.choice(voices), "/Users/fernandomiranda/Library/Application Support/Anki2/User 1/collection.media/"+ audio_file)
           arg_list.append(args)

	pool.imap(sayit, arg_list)
    pool.close()
    pool.join()