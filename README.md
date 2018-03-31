# AI_project
AI project for the course of Artificial Intelligence 2017-2018, University of Florence
---------------------------------------------------------------------------------------------------------------------------------
README ITA:

Codice per l'analisi e lo sviluppo della ricerca informata con il seguente assegnamento:

Sono assegnati n vasi di capacità di ci, inizialmente vuoti, e collocati alle coordinate xi, yi
, i = 1, . . . , n. È disponibile una pompa in xp, yp, con acqua illimitata e si possono eseguire le seguenti azioni:

1. Vuotare il vaso i (sul posto).
2. Portare il vaso i alla pompa, riempirlo completamente (l’agente non può misurare la quantità di acqua erogata) e
ricollocarlo alla sua posizione.
3. Portare il vaso j in xi, yi e riempirlo completamente prendendo quanta acqua necessaria dal vaso i, e riportarlo in xj, yj.
4. Portare il vaso i in xj, yj, trasferire tutta l’acqua nel vaso j, e riportarlo in xi, yi.

L’acqua è gratuita ma le azioni 2,3,4 consumano una quantità di energia proporzionale al
prodotto del volume dell’acqua trasportata per la distanza percorsa. In certe ovvie circostanze,
alcune azioni potrebbero essere impossibili (p.es. l’azione 4 se la somma dei contenuti nei vasi
i e j supera cj). Dati i valori [g1, . . . , gn], gi ≤ ci, si deve determinare la sequenza di azioni
con energia totale minima in modo che ogni vaso sia riempito con il valore desiderato gi per
i = 1, . . . , n.

Sarà poi sviluppata un euristica ammissibile e una non ammissibile da usare con A* e si potrà dunque confrontare sperimentalmente 
il costo del cammino trovato, la penetranza, l'effective branching factor, il numero di nodi espansi rispetto alla ricerca
a costo uniforme.

CODICE:
Il codice è sviluppato con compatibilità per Python 2.7; per poterlo eseguire attraverso Python 3.5 è necessario adattare alcune funzioni.
Sono inoltre necessari alcuni packages esterni quali psutil, math... visibili nelle clausole import dei vari files.
Il codice, eseguito dal file Project.py, permette di poter selezionare tra 4 istanze diverse del problema con, rispettivamente 3,4,5,6 vasi sulla board la quale è configurata di default come una 8x8  con pompa presente in posizione (1,8).
La selezione successiva permette di eseguire sul problema selezionato, una ricerca a costo uniforme oppure 3 diverse ricerche informate A* che sfruttano diverse euristiche tra cui una ampiamente non ammissibile, una non ammissibile solo per pochi casi particolari e una ammissibile in generale.
Eseguito il run sulla funzione trace(), nella console verrà raffigurato, in forma tabellare, lo stato iniziale poi, successivamente, una serie di informazioni sull'andamento della ricerca e un blocco "Stats" dove sono presenti i dati con cui verrà fatto il confronto; infine, verrà raffigurata la successione di stati e azioni dallo stato iniziale fino al goal.

*********************************************************************************************************************************

SOURCES
-
With many changes and additions, this code starts from :

- Russell And Norvig's "Artificial Intelligence - A Modern Approach"  aimacode python repository: 
  https://github.com/aimacode/aima-python  for A* implementation, utils.py, and base class such as Node, Problem...
  
- Paolo Frasconi's implementation of classic 15 puzzle problem with informed search.
  Full Professor of Computer Science at DINFO, University of Florence : http://ai.dinfo.unifi.it/paolo/#paolofrasconi
  
 *********************************************************************************************************************************
