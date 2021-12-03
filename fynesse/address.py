# This file contains code for supporting addressing questions in the data

from .access import *
from shapely.geometry import Point

import numpy as np
import statsmodels.api as sm

def get_properties(conn, north, south, east, west, p_type, year):
    """
    Get all entries in the `pp_data` table that satisfy the search criteria.
    :param conn: the Connection object
    :param north: north bound of the bounding box
    :param south: south bound of the bounding box
    :param east: east bound of the bounding box
    :param west: west bound of the bounding box
    :param p_type: type of property (F, D, S, O)
    :param year: the year to query
    """

    cur = conn.cursor()
    cur.execute(f"""
                SELECT * 
                FROM
                    (SELECT price, date_of_transfer, postcode,
                    property_type, new_build_flag, tenure_type,
                    locality, town_city,
                    district, county FROM pp_data
                    WHERE pp_data.property_type = {p_type}
                    AND YEAR(pp_data.date_of_transfer) = {year}) AS pr
                INNER JOIN 
                    (SELECT postcode, country,
                    latitude, longitude FROM postcode_data 
                    WHERE postcode_data.latitude <= {north} AND 
                    postcode_data.latitude >= {south} AND 
                    postcode_data.longitude <= {east} AND 
                    postcode_data.longitude >= {west} ) po
                ON
                    po.postcode = pr.postcode
                """)

    rows = cur.fetchall()
    return rows

def add_geometry_to_property(results):
    """
    Returns a GeoDataFrame containing the price of each property,
    along with its latitude, longitude and a Geometry object.
    """

    prices = [i[0] for i in results]
    latitudes = [i[12] for i in results]
    longitudes = [i[13] for i in results]
    data = pd.DataFrame(
        {'price': prices,
        'latitude': latitudes,
        'longitude': longitudes}
        )
    
    geo_data = gpd.GeoDataFrame(
        data, geometry=gpd.points_from_xy(data.longitude, data.latitude))
    
    return geo_data

def get_nearby_pois(results, pois, tags):
    """
    Get number of nearby points of interest for each property.
    Returns a list of column names containing that info.
    """

    pois_centroids = []
    col_names = []
    for tag in tags.keys():
        gdf = pois[pois[tag].notnull()]
        pois_centroids.append(gdf['geometry'].centroid)
        col_names.append(f"{tag}_near")
    
    for index, row in results.iterrows():
        for i in range(len(pois_centroids)):
            results.at[index, col_names[i]] = sum(
                pois_centroids[i].geometry.geom_almost_equals(
                    row['geometry'], decimal=2, align=False))
    
    return col_names

def get_nearby_for_prediction(pred_point, pois, tags):
    """
    Get number of each type of nearby points of interest
    for the prediction point
    """

    x_pred = [[]]
    x_pred[0].append(1)
    for tag in tags.keys():
        gdf = pois[pois[tag].notnull()]
        pois_centroid = gdf['geometry'].centroid
        x_pred[0].append(sum(pois_centroid.geom_almost_equals(pred_point, decimal=2, align=False)))
    
    X_pred = np.asarray(x_pred)
    X_pred = sm.add_constant(X_pred)
    return X_pred

def predict_price(latitude, longitude, date, property_type):
    """Price prediction for UK housing."""

    north, south, east, west = get_bounds(latitude, longitude)
    p_type = f"""'"{property_type}"'"""
    print(p_type)

    pois = get_pois(latitude, longitude, box_width, box_height, tags)

    property_results = get_properties(conn, north, south, east, west, p_type, year)

    results_with_geom = add_geometry_to_property(property_results)
    col_names = get_nearby_pois(results_with_geom, pois, tags)

    x = [col_names]
    X = np.asarray(x)
    X = sm.add_constant(X)
    y = np.asarray([house[0] for house in results_with_geom])

    model = sm.OLS(y, X)
    results = model.fit()

    pred_point = Point(latitude, longitude)

    x_pred = get_nearby_for_prediction(pred_point, pois, tags)
    prediction = results.predict(x_pred)

    return round(prediction)

