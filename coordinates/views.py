from django.http import HttpResponse, JsonResponse
from datetime import datetime
import json

from . import data_access
from . import kmeans


def centers(req):
    # TODO: Agregar hora con formato HHMMSS
    if req.method != 'GET':
        resp = JsonResponse(
            {'error': 'method not allowd', 'description':
             'The method ' + req.method + ' is not allowed for centers/.'}
        )
        resp.status_code = 405

        return resp

    print('Obteniendo coordenadas')
    try:
        data = data_access.get_coordinates()
    except Exception:
        return JsonResponse(
            {'message': 'No se pudieron obtener las coordenadas de las denuncias.'},
            status=503
        )
    print('Calculando centros')
    result = kmeans.calcular_centros(data)

    return JsonResponse(
        _create_dict(result),
        safe=False,
        content_type='application/json;charset=UTF-8'
    )


def _create_dict(centers):
    center_list = []
    for c in centers:
        center_object = {}
        center_object['center'] = {}
        center_object['center']['type'] = 'Point'
        center_object['center']['coordinates'] = c[0]

        center_object['radio'] = c[1]
        center_list.append(center_object)
    t = datetime.now().time()
    return {
        'complain-centers': center_list,
        'time': '%02d%02d%02d' % (t.hour, t.minute, t.second)
    }
