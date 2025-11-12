#!/bin/bash


#Nécessite l'utilitaire pdf2text et d'avoir perl installé
#les lignes latex sont sorties dans le fichier en .extract
#les FDS doivent provenir du site Merck et être en français.

#Le fichier convert-hp.pl doit être exécutable (chmod +x convert-hp.pl)

#Idem pour ce fichier

for i in *.pdf
do
#	echo $i
	mkdir "${i%.pdf}"
	#pdfimages -all $i "${i%.pdf}"/"${i%.pdf}"
	pdftotext -layout $i
	cd "${i%.pdf}"

	cd ..
	./convert-hp.pl "${i%.pdf}".txt >> "${i%.pdf}".extract
	mv "$i" "${i%.pdf}/"
	mv "${i%.pdf}.txt" "${i%.pdf}/"
	rm *.hp
done

