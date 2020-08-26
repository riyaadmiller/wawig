import requests
# import json
import datetime

from django.conf import settings
from .           import maths_utils as mu_lib


# owm = open weather map

def owm_request(city, days):

    api_key = settings.API_KEY
    owm_url = settings.OWM_URL
    period  = int(days) * 8  # 24/3, weather is updated every 3 hours, refer api docs

    request_url = f"{ owm_url }q={ city }&appid={ api_key }&units=metric&cnt={ period }"

    response  = requests.get(request_url)
    resp_json = response.json()
    cod_tag   = resp_json.get('cod')

    results_dict = {}
    results_dict['error']   = '0'
    results_dict['detail']  = {}
    results_dict['summary'] = {}

    results_dict['summary']['min_max']  = []
    results_dict['summary']['min']      = {}
    results_dict['summary']['max']      = {}
    results_dict['summary']['med']      = {}
    results_dict['summary']['hum']      = []

    if cod_tag == '200':

        # phase 1: get data from request, build results_dict

        for item in (resp_json.get('list')):

            dt_tag	  = item.get('dt')  # returns epoch formatted datetime
            main_tag  = item.get('main')
            temp_min  = main_tag.get('temp_min')
            temp_max  = main_tag.get('temp_max')
            humidity  = main_tag.get('humidity')

            dt_key = datetime.datetime.fromtimestamp(dt_tag).strftime('%Y-%m-%d')   # we drop %T

            if dt_key not in results_dict['detail']:
                results_dict['detail'][dt_key]              = {}
                results_dict['detail'][dt_key]['ave']       = {}
                results_dict['detail'][dt_key]['min']       = {}
                results_dict['detail'][dt_key]['max']       = {}
                results_dict['detail'][dt_key]['med']       = {}
                results_dict['detail'][dt_key]['hum']       = []
                results_dict['detail'][dt_key]['min_max']   = []

            results_dict['detail'][dt_key]['min_max'].append([temp_min, temp_max])
            results_dict['summary']['min_max'].append([temp_min, temp_max])
            results_dict['detail'][dt_key]['hum'].append(humidity)
            results_dict['summary']['hum'].append(humidity)
        
        # phase 2: process results_dict, build html table rows

        for i in results_dict['detail']:
            results_dict['detail'][i]['max'] = mu_lib.get_max(results_dict['detail'][i]['min_max'])
            results_dict['detail'][i]['min'] = mu_lib.get_min(results_dict['detail'][i]['min_max'])
            results_dict['detail'][i]['ave'] = mu_lib.get_ave(results_dict['detail'][i]['min_max'])
            results_dict['detail'][i]['med'] = mu_lib.get_median(results_dict['detail'][i]['min_max'])
            results_dict['detail'][i]['hum'] = mu_lib.get_ave(results_dict['detail'][i]['hum'])

        results_dict['summary']['min'] = mu_lib.get_min(results_dict['summary']['min_max'])
        results_dict['summary']['max'] = mu_lib.get_max(results_dict['summary']['min_max'])
        results_dict['summary']['ave'] = mu_lib.get_ave(results_dict['summary']['min_max'])
        results_dict['summary']['med'] = mu_lib.get_median(results_dict['summary']['min_max'])
        results_dict['summary']['hum'] = mu_lib.get_ave(results_dict['summary']['hum'])

    else:
        results_dict['error'] = resp_json.get('message')

    return results_dict
