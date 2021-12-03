from .config import *

from .access import *

import matplotlib.pyplot as plt
import mlai
import mlai.plot as plot
import pymysql


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
