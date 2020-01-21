# apaato
This application allows you to see the probability of you getting an accommodation on studentbostader.se. The probabilities are based on a simulation of how they probably distribute the accommodations.

## Example
![Example usage](https://i.imgur.com/EEZbF8s.png)

## Installing
Navigate to the folder where you want to install it and type (or just copy) the following commands:
```
git clone https://github.com/l0f3n/apaato.git
pip3 install ./apaato/
cd ./apaato/
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xzvf geckodriver-v0.26.0-linux64.tar.gz
rm ./geckodriver-v0.26.0-linux64.tar.gz
```

## Using

The three main commands are listed below.

`apaato load`: loads all accommodations into a database.

`apaato accommodations`: lists all accommodations.

`apaato simulate`: lists the probabilities of getting the accommodation.

For more options on each of these commands, use the `-h` flag.
