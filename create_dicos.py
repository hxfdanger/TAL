import sys
from Dicos import Dicos


# if len(sys.argv) < 3 :
#     print('usage:', sys.argv[0], 'conllu_file (input) dico_file (output)')
#     exit(1)


if(__name__ == "__main__"):

	mcd = (('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))


	FilenameConllu = "test.txt"

	print('populating dicos from file ',FilenameConllu)
	dicos = Dicos(mcd)
	dicos.populateFromConlluFile(FilenameConllu, verbose=False)

	for dico in dicos.content.keys():
		print(dico)
		if dico == 'LABEL':
			labels = dicos.content[dico]
	print(labels)
	print(labels[5])
	print(len(labels))


	dicos.lock()


#print('saving dicos in file ', sys.argv[2])
#dicos.printToFile(sys.argv[2])
#dicos.print()


