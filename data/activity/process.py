import numpy as np
import pandas as pd
from molecules.interface import load
from molecules.molecule import circular_fingerprint
import editdistance

MAX_LENGTH = 120
def process(filename, out, threshold=100, random_state=42, max_length=MAX_LENGTH):
    rng = np.random.RandomState(random_state)
    df = pd.read_table(filename)
    df = df[['CANONICAL_SMILES', 'PUBLISHED_VALUE']]
    df = df.dropna(axis=0)
    df = df[df['CANONICAL_SMILES'].apply(len) <= max_length]
    smiles = df['CANONICAL_SMILES']
    active = df['PUBLISHED_VALUE'] < threshold 
    rows = []
    X = []
    y = []
    for i in range(len(smiles)):
        s = smiles.iloc[i]
        vect = circular_fingerprint(s)
        X.append(vect)
        is_active = int(active.iloc[i])
        y.append(is_active)
    X = np.array(X)
    y = np.array(y)
    ind = np.arange(len(X))
    rng.shuffle(ind)
    X = X[ind]
    y = y[ind]
    np.savez(out, X=np.array(smiles.tolist()), V=X, y=y)

if __name__ == '__main__':
    # source : https://www.ebi.ac.uk/chembl/target/inspect/CHEMBL224
    process('5ht2a_ic50.txt', '5ht2a_ic50.npz', threshold=100)#100nM as in the paper[1](section 2.4)

    # source : https://www.ebi.ac.uk/chembl/target/inspect/CHEMBL364
    process('plasmodium_falciparum_ic50.txt', 'plasmodium_falciparum_ic50.npz', threshold=10)#calculated as 10**(9-x) where x=8 in the paper [1](section 3.2.2)

    #[1] Generating Focussed Molecule Libraries for Drug Discovery with Recurrent Neural Networks,
    #    Marwin H.S. Segler, Thierry Kogej, Christian Tyrchan, Mark P. Waller
