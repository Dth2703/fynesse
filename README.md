# Repository overview

`access.py` contains functions to achieve the following:
- Download price data
- Set up the price data database table
- Modify the price data table indices
- Upload price data
- Download postcode data
- Set up the postcode data database table
- Modify the postcode data table indices
- Upload postcode data
- Start a database connection
- Get the bounding coordinates of a bounding box
- Get the points of interest inside a bounding box
- Get the graph of streets inside a bounding box

`assess.py` contains functions to achieve the following:
- Select the top few entries of a database table
- Plot the points of interest within an area

`address.py` has the function `predict_price()` and a few helper functions to help it do that. This includes the function to query the database for data, adding geometries to the data, getting nearby points of interest for both the data and the location to be predicted.
