# PI-Pico-L76B
Code for the Raspberry Pi Pico with the Waveshare L76B GPS with GNSS, Beidu and GPS. This code WORKS.

The original for this code was found on Github but was the most bloody awful mess I'd ever seen. I have removed fake references to Baidu, GPS and Google satellites (one version spelt it Goodle). The code has been expanded to give all of the information from the $GNRMC record. I have not bothered including information from $PMTK001, $GNZDA, $GNVTG, $GNGGA, GPGSA, $BDGSA purely because they are outside the scope of what I was achieving. Having said that, editing the l76.py file (not the config file) to add those in is pretty straightforward. For further reference, here are the NMEA satellite codes. https://manualzz.com/doc/23347991/nmea-output-description
