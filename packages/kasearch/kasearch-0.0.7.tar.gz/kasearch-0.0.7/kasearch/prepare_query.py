from dataclasses import dataclass
from multiprocessing import Pool

import numpy as np

from kasearch.species_anarci import number
from kasearch.canonical_alignment import canonical_alignment, canonical_numbering_len

class AlignSequences:
    """
    Align sequences for KA-Search. 
    """
    def __init__(self, seqs, allowed_species=['Human', 'Mouse'], n_jobs=1):
        
        self.n_jobs = n_jobs
        self._unusual_sequence = np.zeros(canonical_numbering_len, np.int8)
        
        if allowed_species:
            self.allowed_species = [i.lower() for i in allowed_species]
        else:
            self.allowed_species = None
        
        self.db = self._many_canonical_alignment(seqs)
        
    def _canonical_alignment(self, seq):
        """
        Alignment of a single sequence.
        """
        
        try:
            numbered_sequence, _ = number(seq, allowed_species=self.allowed_species)
            return canonical_alignment(numbered_sequence)
        except Exception:
            return self._unusual_sequence
    
    def _many_canonical_alignment(self, seqs):
        """
        Alignment of multiple sequences.
        """
        
        n_jobs = len(seqs) if len(seqs) <  self.n_jobs else self.n_jobs
        chunksize=len(seqs) // n_jobs

        with Pool(processes=n_jobs) as pool:
            return Sequences(np.array(pool.map(self._canonical_alignment, seqs, chunksize=chunksize)))
        
        
@dataclass   
class Sequences:
    """
    Sequence data class.
    """
    aligned_seqs: None
