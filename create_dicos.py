import sys
from Dicos import Dicos


if len(sys.argv) < 3 :
    print('usage:', sys.argv[0], 'conllu_file (input) dico_file (output)')
    exit(1)


mcd = (('INDEX', 'INT'), ('FORM', 'INT'), ('LEMMA', 'INT'), ('POS', 'SYM'), ('X1', 'INT'), ('MORPHO', 'INT'), ('GOV', 'SYM'), ('LABEL', 'SYM'), ('X2', 'SYM'), ('X3', 'SYM'))


print('populating dicos from file ', sys.argv[1])
dicos = Dicos(mcd)
dicos.populateFromConlluFile(sys.argv[1], verbose=False)

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


