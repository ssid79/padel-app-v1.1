Il file `app.py` della versione 1.1 è pronto per il download:

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dati di esempio
partite_settimana_corrente = [
    {'giorno': 'Lunedì', 'squadra1': 'A', 'squadra2': 'B', 'punteggio': None},
    {'giorno': 'Martedì', 'squadra1': 'C', 'squadra2': 'D', 'punteggio': None},
    {'giorno': 'Mercoledì', 'squadra1': 'A', 'squadra2': 'C', 'punteggio': None},
]

classifica = {'A':0, 'B':0, 'C':0, 'D':0}

ordine_giorni = {
    'Lunedì': 1, 'Martedì': 2, 'Mercoledì': 3, 'Giovedì': 4, 'Venerdì': 5, 'Sabato': 6, 'Domenica': 7
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calendario')
def mostra_calendario():
    calendario = sorted(partite_settimana_corrente, key=lambda p: ordine_giorni.get(p['giorno'], 8))
    partita_imminente = None
    for p in calendario:
        if not p['punteggio']:
            partita_imminente = p
            break
    return render_template('calendario.html', calendario=calendario, partita_imminente=partita_imminente)

@app.route('/inserisci_punteggio', methods=['POST'])
def inserisci_punteggio():
    squadra1 = request.form['squadra1']
    squadra2 = request.form['squadra2']
    punteggio = request.form['punteggio']

    for partita in partite_settimana_corrente:
        if partita['squadra1'] == squadra1 and partita['squadra2'] == squadra2:
            partita['punteggio'] = punteggio
            aggiorna_classifica(squadra1, squadra2, punteggio)
            break

    return redirect(url_for('mostra_calendario'))

def aggiorna_classifica(squadra1, squadra2, punteggio):
    punti1, punti2 = map(int, punteggio.split('-'))
    if punti1 > punti2:
        classifica[squadra1] += 3
    elif punti2 > punti1:
        classifica[squadra2] += 3
    else:
        classifica[squadra1] += 1
        classifica[squadra2] += 1

if __name__ == '__main__':
    app.run(debug=True)
```

