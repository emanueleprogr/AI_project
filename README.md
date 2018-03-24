# AI_project
AI project for the course of Artificial Intelligence 2017-2018, University of Florence

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
