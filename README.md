# apaato
This application allows you to see the probability of you getting an accommodation on studentbostader.se. The probabilities are based on a simulation of how they probably distribute the accommodations.

## Example
![Example usage](https://i.imgur.com/EEZbF8s.png)

## Installing

Download this repository and install it using `pip3 install /path/to/apaato`.

Then download geckodriver with these commands:
```
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz -P ~/Documents/apaato
$ tar -xzvf ~/Documents/apaato/geckodriver-v0.26.0-linux64.tar.gz -C ~/Documents/apaato
$ rm ~/Documents/apaato/geckodriver-v0.26.0-linux64.tar.gz
```


## Using

The three main commands are listed below.

`apaato load`: loads all accommodations into a database.

`apaato accommodations`: lists all accommodations.

`apaato simulate`: lists the probabilities of getting the accommodation.

For more options on each of these commands, use the `-h` flag.
