# apaato
This application allows you to see the probability of you getting an accommodation on studentbostader.se. The probabilities are based on a simulation of how they probably (I think) distribute the accommodations.

## Example
![Example usage](https://i.imgur.com/dxcroLd.png)

## Installing
Dependencies: `selenium` and `sqlite3`.

## Usage
Run `python3 -i main.py` and call `load_accommodations()`.

After that you can either list the accommodations, `list_accommodations(your_queue_points)` or run the simulation, `simulate(your_queue_points)`. When the simulation is finished, call `list_probabilites()` to see the result.
