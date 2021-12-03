from .config import *

from .access import *

import matplotlib.pyplot as plt
import mlai
import mlai.plot as plot
import pymysql

"""These are the types of import we might expect in this file
import pandas
import bokeh
import matplotlib.pyplot as plt
import sklearn.decomposition as decomposition
import sklearn.feature_extraction"""

"""Place commands in this file to assess the data you have downloaded.
How are missing values encoded, how are outliers encoded?
What do columns represent, makes rure they are correctly labeled.
How is the data indexed?
Create visualisation routines to assess the data (e.g. in bokeh).
Ensure that date formats are correct and correctly timezoned."""

def select_top(conn, table,  n):
    """
    Query n first rows of the table
    :param conn: the Connection object
    :param table: the table to query
    :param n: number of rows to query
    """
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM {table} LIMIT {n}')

    rows = cur.fetchall()
    return rows

def head(conn, table, n=10):
    """
    Prints the first n rows of a table
    """

    rows = select_top(conn, table, n)
    for r in rows:
        print(r)
    
    return

def plot_pois(edges, pois, north, south, east, west):
    fig, ax = plt.subplots(figsize=plot.big_figsize)

    # Plot street edges
    edges.plot(ax=ax, linewidth=1, edgecolor="dimgray")

    ax.set_xlim([west, east])
    ax.set_ylim([south, north])
    ax.set_xlabel("longitude")
    ax.set_ylabel("latitude")
    ax.set_title("Points of interest around the chosen location")

    # Plot all POIs
    pois[pois.amenity.notnull()].plot(ax=ax, color="blue", alpha=0.7, markersize=10)
    pois[pois.leisure.notnull()].plot(ax=ax, color="red", alpha=0.7, markersize=10)
    pois[pois.public_transport.notnull()].plot(ax=ax, color="peru", alpha=0.7, markersize=10)
    pois[pois.shop.notnull()].plot(ax=ax, color="darkviolet", alpha=0.7, markersize=10)
    pois[pois.tourism.notnull()].plot(ax=ax, color="green", alpha=0.7, markersize=10)
    
    plt.tight_layout()
    return


def data():
    """Load the data from access and ensure missing values are correctly encoded as well as indices correct, column names informative, date and times correctly formatted. Return a structured data structure such as a data frame."""
    df = access.data()
    raise NotImplementedError

def query(data):
    """Request user input for some aspect of the data."""
    raise NotImplementedError

def view(data):
    """Provide a view of the data that allows the user to verify some aspect of its quality."""
    raise NotImplementedError

def labelled(data):
    """Provide a labelled set of data ready for supervised learning."""
    raise NotImplementedError
