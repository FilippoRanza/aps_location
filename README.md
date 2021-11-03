# aps_location
An exact solver for a Automatic Parcel Station Location Problem

## Rationale

This project is an implementation of the model described in   
[Solving an Ambulance Location Model by Tabu Search 
by Gendreau, Laporte and Semet ](https://doi.org/10.1016/S0966-8349(97)00015-6).

The script tries with different value of the maximal fraction of customer served in region R1 facilities to open 
from the minimal, 1, to the maximal number, equal to the number of facility nodes in the 
graph. If the fraction is to large (close to 1.0) then the model becomes infeasible.

The model was originally designed to be used to locate emergency centers. In this case the target 
is the location of Automatic Parcel Stations in a public transport system.

## Usage
```asp_loc.py``` is used to determine the maximal portion of customer that 
can be served in R1. 
The syntax is:
```
[python[3]] asp_loc.py instance.json config.json output.json
```

If an instance is already available it is possible to directly use it. Otherwise 
it is possible to create one using ```instance_generator.py```.
Run 
```
[python[3]] instance_generator.py --help 
```
for more information about the usage.

One an instance is available the user must create a configuration file. 
It is a JSON file containing one list of lists. The inner list must contain
exactly two elements. The first one is the value R1 the second is the value R2.
Here is an example:
```json
[
    [10, 20],
    [20, 30],
    [20, 40]
]
```
```asp_loc.py``` will compute the value _alpha_ for each number of possible facility count (from 1 to the 
number of facility location in the instance) for each (R1, R2) couple.

The output is save on the third argument. It is saved as a JSON file.

It is possible to visualize a plot by:
```
[python[3]] visualize.py output.json
```



