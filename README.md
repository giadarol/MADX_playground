# MADX_playground

needs
* Python 2
* [MAD-X](http://mad.web.cern.ch/mad/)
* [NAFFLib](https://github.com/kparasch/NAFFlib)
* [tune_diagram](https://github.com/PyCOMPLETE/tune_diagram)
* [pyoptics](https://github.com/rdemaria/pyoptics)

(NAFFlib and tune_diagram are assumed to be included in PYTHONPATH)

First run 
```madx < toyLHC_beambeam.seq```  
which creates and saves the ```toy.seq``` MAD-X sequence file,
where ```madx``` is the MAD-X executable.

Running
```python plot_tunes.py```  
will import the mad-x sequence, create an grid of $x-y$ points and uses it to track particles with MAD-X.
Finally, it reads the tfs files and produces the footprint.
