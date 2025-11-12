#!/bin/bash

#N="20 21 11 23 24" # 05 04 07 09 22"
#N="19 30 21 24 05 07 22 26 13 14 12 15 17 17"
N="31 31"
echo $N

path="/home/jeff/Documents/IUTOrsay/1-Cours/3p06-Cours_Batterie/02-TD/"

for n in $N
do
cat > ./test.tex << EOL
\documentclass[a4paper]{article} 
\usepackage[teacher]{Corrections} 
\lhead{Travaux dirigés} \chead{} \rhead{3.06 Propriétés des matériaux}
\lfoot{IUT d'Orsay - BUT 2A - 2023/2024} \cfoot{\includegraphics[height=0.5cm]{cc-by-nc-sa.png}}  \rfoot{Jean-François Olivieri \quad \thepage}

\renewcommand*{\thesubsubsection}{}

\begin{document}
\input{$path/Ex$n}
\end{document}
EOL

pdflatex test.tex
pdflatex test.tex

mv "test.pdf" "./Corrections/Ex$n.pdf"
done
#V\let\subsubsection\section*
