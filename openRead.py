# Import libraries
from tkinter import *
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
from google.cloud import texttospeech
import pygame
from google.cloud import translate_v3beta1 as translate
from ibm_watson import LanguageTranslatorV3
import glob
from tkinter import ttk
import tkinter
from functools import partial
import PyPDF2


def play(PDF_file, l4ng, transl, n_pag, entry):

	s_pag = int(entry.get())

	# Converting PDF to images
	pages = convert_from_path(PDF_file, first_page=s_pag, last_page=s_pag)

	# Counter to store images of each page of PDF to image
	image_counter = 1

	# Iterate through all the pages stored above
	for page in pages:

		# Declaring filename for each page of PDF as JPG
		# For each page, filename will be:
		# PDF page 1 -> page_1.jpg
		filename = "page_"+str(image_counter)+".jpg"

		# Save the image of the page in system
		page.save(filename, 'JPEG')

		# Increment the counter to update filename
		image_counter = image_counter + 1

	# Recognizing text from the images using OCR

	if l4ng == "por":
		# Variable to get count of total number of pages
		filelimit = image_counter-1

		# Creating a text file to write the output
		outfile = "out_text.txt"

		# Reset the file
		f = open(outfile, "w")
		f.write("")
		f.close()

		# Open the file in append mode so that
		# All contents of all images are added to the same file
		f = open(outfile, "a")

		# Iterate from 1 to total number of pages
		for i in range(1, filelimit + 1):

			# Set filename to recognize text from
			# Again, these files will be:
			# page_1.jpg
			# page_2.jpg
			# ....
			# page_n.jpg
			filename = "page_"+str(i)+".jpg"

			# Recognize the text as string in image using pytesserct
			text = str(((pytesseract.image_to_string(Image.open(filename), lang="por"))))

			# The recognized text is stored in variable text
			# Any string processing may be applied on text
			# Here, basic formatting has been done:
			# In many PDFs, at line ending, if a word can't
			# be written fully, a 'hyphen' is added.
			# The rest of the word is written in the next line
			# Eg: This is a sample text this word here GeeksF-
			# orGeeks is half on first line, remaining on next.
			# To remove this, we replace every '-\n' to ''.
			text = text.replace('-\n', '')

			# Write the processed text to the file.
			f.write(text)

		# Close the file after writing all the text.
		f.close()

	elif l4ng == "eng":
		# Variable to get count of total number of pages
		filelimit = image_counter-1

		# Creating a text file to write the output
		outfile = "out_text.txt"

		# Reset the file
		f = open(outfile, "w")
		f.write("")
		f.close()

		# Open the file in append mode so that
		# All contents of all images are added to the same file
		f = open(outfile, "a")

		# Iterate from 1 to total number of pages
		for i in range(1, filelimit + 1):

			# Set filename to recognize text from
			# Again, these files will be:
			# page_1.jpg
			# page_2.jpg
			# ....
			# page_n.jpg
			filename = "page_"+str(i)+".jpg"

			# Recognize the text as string in image using pytesserct
			text = str(((pytesseract.image_to_string(Image.open(filename), lang="eng"))))

			# The recognized text is stored in variable text
			# Any string processing may be applied on text
			# Here, basic formatting has been done:
			# In many PDFs, at line ending, if a word can't
			# be written fully, a 'hyphen' is added.
			# The rest of the word is written in the next line
			# Eg: This is a sample text this word here GeeksF-
			# orGeeks is half on first line, remaining on next.
			# To remove this, we replace every '-\n' to ''.
			text = text.replace('-\n', '')

			# Write the processed text to the file.
			f.write(text)

		# Close the file after writing all the text.
		f.close()

	path = 'out_text.txt'
	txt_file = open(path,'r')
	text_read = txt_file.read()

	print(text_read)
	print("\n \n"+"Idioma original:"+l4ng+"\n"+"Idioma traduzido:"+transl)

	# Translate
	if l4ng == "por" and transl == "eng":
		client = translate.TranslationServiceClient()
		project_id = "tesseract-248321"
		text = text_read
		location = 'global'

		parent = client.location_path(project_id, location)

		response = client.translate_text(
		    parent=parent,
		    contents=[text],
		    mime_type='text/plain',  # mime types: text/plain, text/html
		    source_language_code='pt-BR',
		    target_language_code='en-US')

		for translation in response.translations:
			format(translation)
		text_read = str(translation)
		text_read = text_read.replace("\\n"," ")
		text_read = text_read.replace("translated_text:","")
		print('\n'+'Texto Traduzido: \n \n'+text_read)

	elif l4ng == "eng" and transl == "por":
		client = translate.TranslationServiceClient()
		project_id = "tesseract-248321"
		text = text_read
		location = 'global'

		parent = client.location_path(project_id, location)

		response = client.translate_text(
		    parent=parent,
		    contents=[text],
		    mime_type='text/plain',  # mime types: text/plain, text/html
		    source_language_code='en-US',
		    target_language_code='pt-BR')

		text_read = str(response.translations)
		# Fix the special characteres
		text_read = text_read.replace("\\303\\241","á")
		text_read = text_read.replace("\\303\\251","é")
		text_read = text_read.replace("\\303\\255","í")
		text_read = text_read.replace("\\303\\252","ê")
		text_read = text_read.replace("\\303\\263","ó")
		text_read = text_read.replace("\\303\\243","ã")
		text_read = text_read.replace("\\303\\247","ç")
		text_read = text_read.replace("\\303\\265","õ")
		text_read = text_read.replace("\\303\\272","ú")
		text_read = text_read.replace("\\342\\200","'")
		text_read = text_read.replace("\\303\\211","")
		text_read = text_read.replace("\\230",",")
		text_read = text_read.replace("\\231",",")
		text_read = text_read.replace("\\234"," ")
		text_read = text_read.replace("\\n"," ")
		text_read = text_read.replace("[translated_text:","")
		print('\n'+'Texto Traduzido: \n \n'+text_read)

	# Inicialize text to speech
	# Instantiates a client
	client = texttospeech.TextToSpeechClient()

	# Set the text input to be synthesized
	synthesis_input = texttospeech.types.SynthesisInput(text=text_read)

	# Build the voice request, select the language code ("en-US") and the ssml
	# voice gender ("neutral")
	if transl == "por":
		voice = texttospeech.types.VoiceSelectionParams(
		    language_code='pt-BR',
		    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
	else:
		voice = texttospeech.types.VoiceSelectionParams(
		    language_code='en-US',
		    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

	# Select the type of audio file you want returned
	audio_config = texttospeech.types.AudioConfig(
	    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

	# Perform the text-to-speech request on the text input with the selected
	# voice parameters and audio file type
	response = client.synthesize_speech(synthesis_input, voice, audio_config)

	# The response's audio_content is binary.
	with open('output.mp3', 'wb') as out:
	    # Write the response to the output file.
	    out.write(response.audio_content)
	    print('Audio content written to file "output.mp3"')

	# Inicialize PyGame
	pygame.init()

	# Loading the MP3 file and running
	if os.path.exists('output.mp3'):
	    pygame.mixer.music.load('output.mp3')
	    pygame.mixer.music.play()
	    pygame.mixer.music.set_volume(1)

	    clock = pygame.time.Clock()
	    clock.tick(10)

def translEng():
	transl = "eng"
	print("Váriavel transl setada para:"+transl)
	inicio(caminho,transl)

def translPor():
	transl = "por"
	print("Váriavel transl setada para:"+transl)
	inicio(caminho,transl)

#---------- Third window
def inicio(caminho):

	livro = caminho.replace("/home/dario/openRead/", "")

	print("Idioma de origem: "+origem)
	print("Idioma de leitura:"+destino)
	print("Livro escolhido: "+livro.replace("arquivos/", ""))

	pdf = livro
	l4ng = origem
	transl = destino
	PDF_file = pdf
	pdf2_file = open(PDF_file,'rb')
	pdf_reader = PyPDF2.PdfFileReader(pdf2_file)
	n_pag = pdf_reader.numPages

	player = Tk();

	def entry_sum_args(n_pag):
		if(entry.get() == ""):
			entry.insert(0,"1")
		elif(str(entry.get()) == str(n_pag)):
			print("Valor ultrapassa o Nº máximo de páginas")
		elif(int(entry.get()) >=1 and int(entry.get()) < int(n_pag)):
			new_entry = int(entry.get())
			new_entry = new_entry+1
			entry.delete(0,tkinter.END)
			entry.insert(0,new_entry)

	def entry_sub_args(n_pag):
		if(entry.get() == ""):
			entry.insert(0,"1")
		elif(entry.get() == "1"):
			print("Nº mínimo de páginas atingido")
		elif(int(entry.get()) >1):
			new_entry = int(entry.get())
			new_entry = new_entry-1
			print(new_entry)
			entry.delete(0,tkinter.END)
			entry.insert(0,new_entry)


	lb1 = Label(player, text="Selecione a página: (O livro tem: "+str(n_pag)+" páginas)").place(x = 0, y = 5, width=390, height=40)
	#validate = player.register(validate_input)
	for i in range(10):
		#entry = Entry(player, validate="key", validatecommand=(validate, "%P", n_pag))
		entry = Entry(player, validate="key")
		entry.place(x = 170, y = 65, width=45, height=30)
	entry_sum = partial(entry_sum_args, n_pag)
	entry_sub = partial(entry_sub_args, n_pag)
	bt2 = Button(player, text='<', command=entry_sub).place(x = 140, y = 65, width=25, height=30)
	bt3 = Button(player, text='>', command=entry_sum).place(x = 220, y = 65, width=25, height=30)

	def toggle():
		if bt4.config('relief')[-1] == 'sunken':
			pygame.mixer.music.unpause()
			bt4.config(relief="raised")
		else:
			pygame.mixer.music.pause()
			bt4.config(relief="sunken")

	play_args = partial(play, PDF_file, l4ng, transl, n_pag, entry)
	bt1 = Button(player, text='Play', command=play_args).place(x = 95, y = 140, width=90, height=30)
	bt4 = Button(player, text='Pause')
	bt4.place(x = 195, y = 140, width=90, height=30)
	bt4['command'] = toggle

	#LxA+E+T
	#500x500+150+300
	player.geometry("390x200+480+50")
	player.title('OpenRead - Player')
	player.mainloop()

def set_ori_por():
	global origem
	origem = "por"
def set_ori_eng():
	global origem
	origem = "eng"
def set_des_por():
	global destino
	destino = "por"
def set_des_eng():
	global destino
	destino = "eng"

#---------- Second window
def linguagem(caminho):

	janela2 = Tk()

	lb1 = Label(janela2, text="      Selecione a linguagem de origem").grid(row=1,columnspan=5)
	lb_espaco = Label(janela2, text="                             ").grid(row=0,column=1)
	lb2 = Label(janela2, text="      Selecione a linguagem de leitura").grid(row=5,columnspan=5)
	lb_espaco2 = Label(janela2, text="                             ").grid(row=4,column=1)

	ori = tkinter.IntVar()
	rb1 = Radiobutton(janela2, text="Português", variable=ori, value=0, command=set_ori_por).grid(row=3, column=1)
	rb2 = Radiobutton(janela2, text="Inglês", variable=ori, value=1, command=set_ori_eng).grid(row=3, column=2)

	des = tkinter.IntVar()
	rb3 = Radiobutton(janela2, text="Português", variable=des, value=0, command=set_des_por).grid(row=6, column=1)
	rb4 = Radiobutton(janela2, text="Inglês", variable=des, value=1, command=set_des_eng).grid(row=6, column=2)

	lb_espaco3 = Label(janela2, text="                             ").grid(row=7,column=1)
	translArg = partial(inicio, caminho)
	bt1 = Button(janela2, text='Confirmar', command=translArg).grid(row=8,column=1, columnspan=5)

	#LxA+E+T
	#500x500+150+300
	janela2.geometry("280x200+510+50")
	janela2.title('OpenRead - Seletor de linguagens')
	janela2.mainloop()

#---------- First window
janela = Tk()

# Auxiliary functions ..........................
def populate_janela(tree):
	dir = os.path.abspath('/home/dario/openRead/arquivos').replace('\\', '/')
	node = tree.insert('', 'end', text=dir, values=[dir, "directory"])
	populate_tree(tree, node)

# Insert file paths in Treeview widget
def populate_tree(tree, node):
	if tree.set(node, "type") != 'directory':
		return

	path = tree.set(node, "fullpath")
	tree.delete(*tree.get_children(node))

	parent = tree.parent(node)
	special_dirs = [] if parent else glob.glob('.') + glob.glob('..')

	for p in special_dirs + os.listdir(path):
		ptype = None
		p = os.path.join(path, p).replace('\\', '/')
		if os.path.isdir(p): ptype = "directory"
		elif os.path.isfile(p): ptype = "file"

		fname = os.path.split(p)[1]
		id = tree.insert(node, "end", text=fname, values=[p, ptype])

		if ptype == 'directory':
			if fname not in ('.', '..'):
				tree.insert(id, 0, text="dummy")
				tree.item(id, text=fname)
		elif ptype == 'file':
			size = os.stat(p).st_size
			tree.set(id, "size", "%d bytes" % size)

# Update the tree when the user opens a directory
def update_tree(event):
	tree = event.widget
	populate_tree(tree, tree.focus())

# Update tree when directory double-clicks mouse
def change_dir(event):
	tree = event.widget
	node = tree.focus()
	if tree.parent(node):
		path = os.path.abspath(tree.set(node, "fullpath"))
		if os.path.isdir(path):
			os.chdir(path)
			tree.delete(tree.get_children(''))
			populate_janela(tree)

def autoscroll(sbar, first, last):
	"""Hide and show scrollbar as needed."""
	first, last = float(first), float(last)
	if first <= 0 and last >= 1:
		sbar.grid_remove()
	else:
		sbar.grid()
	sbar.set(first, last)

#----------------- Main program body

# Horizontal bars
vsb = ttk.Scrollbar(orient="vertical")
hsb = ttk.Scrollbar(orient="horizontal")

# Creating a Treeview obje
tree = ttk.Treeview(columns=("fullpath", "type", "size"),
	displaycolumns="size", yscrollcommand=lambda f, l: autoscroll(vsb, f, l),
	xscrollcommand=lambda f, l:autoscroll(hsb, f, l))

# Associate the scrollbars with the x and y views of the Treeview object
vsb['command'] = tree.yview
hsb['command'] = tree.xview

# Define the headers of the different columns
tree.heading("#0", text="Directory Structure", anchor='w')
tree.heading("size", text="File Size", anchor='w')
tree.column("size", stretch=0, width=100)

# Inicialize Treeview
populate_janela(tree)

# Associates Treeview events with specific methods
tree.bind('<<TreeviewOpen>>', update_tree)
tree.bind('<Double-Button-1>', change_dir)

# Arrange the tree and its scrollbars in the toplevel
tree.grid(column=0, row=0, sticky='nswe')
vsb.grid(column=1, row=0, sticky='ns')
hsb.grid(column=0, row=1, sticky='ew')
janela.grid_columnconfigure(0, weight=1)
janela.grid_rowconfigure(0, weight=1)

def selectItem(a):
	curItem = tree.focus()
	itemValue = tree.item(curItem).get("values")[0]
	linguagem_arg = partial(linguagem, itemValue)
	bt5 = Button(janela, text='Escolher', command=linguagem_arg)
	bt5['width'] = 15
	#Play
	bt5.grid(row=40, column=0, columnspan=2)

tree.bind('<ButtonRelease-1>', selectItem)

# Choice pdf window
lb1 = Label(janela, text="Selecione um arquivo PDF")
lb_espaco = Label(janela, text="                            ")
lb_espaco2 = Label(janela, text="                            ")
lb_espaco.grid(row=38,column=0)
lb_espaco2.grid(row=41,column=0)
lb1.grid(row=39,column=0, columnspan=5)

#LxA+E+T
#500x500+150+300
janela.geometry("700x420+300+50")
janela.title('OpenRead - Selecione um arquivo PDF')
janela.call('wm', 'iconphoto', janela._w, PhotoImage(file='icon.png'))
janela.mainloop()
