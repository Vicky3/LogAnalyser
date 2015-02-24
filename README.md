# Log Analyser
23/02/2015

## General usage
- Use a browser to go to the set address/port (depending on the mini_httpd configuration, or the -p parameter set in the run_mini_httpd.sh)
- The top area (Search criteria) allows the configuration of filters and the level of detail of the pie charts while the lower area (What statistics..) allows to select the statistics that are to be computed.
- Choose a file (micro1, micro2, small, medium, large) from the dropdown box
- The "Create Statistics"-button will start the computation and show the results upon completion
- The "Reset"-button will clear all filters and category selections

## Requirements and installation
- Adapt the run_mini_httpd.sh:
    - Change the DATADIR to the root directory of the project (where the index.html is located)
    - Change the -c parameter to 'src/*cgi'
- Log files need to be located in the "logs" directory in the root directoy of the project
- matplotlib 1.4.3: Use pip (pip install matplotlib) or download sources: http://matplotlib.org/downloads.html
    - Earlier versions might work, but is not guaranteed.

## Authors
Adriana-Victoria Dreyer | adreyer@techfak.uni-bielefeld.de

Jan Pöppel | jpoeppel@techfak.uni-bielefeld.de

