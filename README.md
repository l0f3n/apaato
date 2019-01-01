# apaato
This application allows you to see the probability of you getting an apartment on studentbostader.se. It is not an official and 'true' probability of any kind, just a simulation of how they probably distribute apartments.

## Example
![Example usage](https://i.imgur.com/dxcroLd.png)

## Installing
Dependencies: `selenium` and `sqlite3`.

## Usage
Navigate to this repository on your computer and import main in the python interpreter `python3 -i main.py` and call `load_apartments()`.

After that you can either list the apartments, `list_apartments(your_queue_points)` or run the simulation, `simulate(your_queue_points)`. When the simulation is finished, run `list_probabilites()` to see the result.
