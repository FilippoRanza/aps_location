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