'''
Created: 19.03.2015
@author: Dennis Ligtenberg
Views for request handling
'''
from flask import Blueprint, jsonify, request, abort
from datetime import datetime
from config import api_config
from config.ext_config import FORECAST_INTERVAL
from datetime import timedelta

from .models import Peak, PublicTransport
from .update_fog_height import UpdateFogHeightForecast
from .crossdomain import crossdomain
from .query_issuer import get_peaks, get_heights, get_stops_within_bounds, \
    get_max_forecasted_height_by_time

webservice = Blueprint("webservice", __name__)


def round_timestamp(timestamp):
    if timestamp.hour % FORECAST_INTERVAL != 0:
        timestamp += timedelta(hours=1)
    return timestamp


@webservice.route(api_config.UPDATE_URL)
@crossdomain(origin='*')
def update():
    UpdateFogHeightForecast().update()
    return 'Data Updated'


@webservice.route(api_config.HEIGHTS_FORECAST_URL)
@crossdomain(origin='*')
def heights():
    return jsonify(heights=get_heights())


@webservice.route(api_config.FORECASTED_PEAKS_URL)
@crossdomain(origin='*')
def peaks():
    try:
        forecasted_height = float(request.args.get('height'))
        results = get_peaks()
        return jsonify(Peak.to_geojson(results, forecasted_height))
    except TypeError:
        abort(400)


@webservice.route(api_config.FORECASTED_PUBLIC_TRANSPORT_URL)
@crossdomain(origin='*')
def get_public_transport():
    # Dict with Bounds (minx, miny, maxx, maxy from the GET parameters)
    try:
        forecasted_height = float(request.args.get('height'))
        bounds = {
            'minx': float(request.args.get('minx')),
            'miny': float(request.args.get('miny')),
            'maxx': float(request.args.get('maxx')),
            'maxy': float(request.args.get('maxy'))
        }
        stops = get_stops_within_bounds(bounds)

        return jsonify(PublicTransport.to_geojson(stops, forecasted_height))

    except TypeError:
        abort(400)


@webservice.route(api_config.FORECASTED_HEIGHTS_URL)
@crossdomain(origin='*')
def get_height_at_time():
    try:
        year = request.args.get('y')
        month = request.args.get('m')
        day = request.args.get('d')
        hour = request.args.get('h')
        timestamp = datetime.strptime(
            year + "-" + month + "-" + day + " " + hour, '%Y-%m-%d %H')
        return jsonify({'height': get_max_forecasted_height_by_time(timestamp)})
    except TypeError:
        abort(400)


@webservice.route(api_config.HOME_URL)
@crossdomain(origin='*')
def home():
    return 'Server is up'
