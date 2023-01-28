from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from datetime import datetime
import pandas as pd

from Mywebapp.db import get_flightdb

bp = Blueprint("flight", __name__)

@bp.route("/flight",methods=['GET', 'POST'])
def flight_index():
    """Show all the posts, most recent first."""
    #today's date
    proc_day = datetime.today()
    proc_day = proc_day.strftime("%Y-%m-%d")
    
    airline = request.values["airline"]

    db = get_flightdb()
    posts = db.execute(
        "select startdate,provider_code,price,airline,max(link) link,predict_purchase_date from flight_itinerary where process_date > ? and airline = ? "
        " group by startdate,price,airline,provider_code order by startdate desc"
        ,(proc_day,airline,)
    ).fetchall()

    print(airline)
    return render_template("flight/index.html", posts=posts,airline=airline)

@bp.route("/flight/low_price")
def flight_lowprice():
    """Show all the posts, most recent first."""
    #today's date
    proc_day = datetime.today()
    proc_day = proc_day.strftime("%Y%m%d")
    proc_file = proc_day + "_flight_data_pivot.csv"
    
    posts = pd.read_csv("C:/Users/dgoma/python/webcrawl/Flight_Data/"+proc_file)
    #posts.drop('Process_date', axis=1, inplace=True)
    #posts = posts.to_dict
    column_names = posts.columns.values
    column_cnt = int(len(column_names))


    return render_template("flight/low_price.html",proc_day=proc_day,column_names=column_names, row_data=list(posts.values.tolist()),zip=zip )