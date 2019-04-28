# apaato
This application allows you to see the probability of you getting an accommodation on studentbostader.se. The probabilities are based on a simulation of how they probably distribute the accommodations.

## Example
![Example usage](https://i.imgur.com/dxcroLd.png)

## Installing
Download geckodriver from [here](https://github.com/mozilla/geckodriver/releases) and save it to as `~/Documents/apaato/geckodriver`

Copy this repository and install using `pip3 install /path/to/apaato`.

## Usage
`apaato load`: loads all accommodations into a database.

`apaato accommodations`: lists all the accommodations with all earliest latest application acceptance date.

`apaato simulate`: lists the probabilities of getting an accommodation.

For more options, use the `-h` flag.
