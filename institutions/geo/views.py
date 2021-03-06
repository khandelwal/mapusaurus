from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse
from djgeojson.serializers import Serializer as GeoJSONSerializer

from .models import StateCensusTract


def _paged(queryset, request):
    """Adds a pager around a queryset, using the keys in the request"""
    if 'page_num' in request.GET:
        page_size = 250
        if request.GET.get('page_size', '').isdigit():
            page_size = int(request.GET['page_size'])

        pager = Paginator(queryset, page_size)
        try:
            return pager.page(request.GET.get('page_num')).object_list
        except PageNotAnInteger:
            return pager.page(1).object_list
        except EmptyPage:
            return []
    return queryset


def tracts(request):
    """ Request a list of tracts by provided county/state fips. """
    county_fips = request.GET.get('county_fips', '')
    state_fips = request.GET.get('state_fips', '')

    tracts = StateCensusTract.objects.filter(
        countyfp=county_fips, statefp=state_fips).order_by('geoid')
    tracts = _paged(tracts, request)

    return HttpResponse(
        GeoJSONSerializer().serialize(tracts, use_natural_keys=True),
        content_type='application/json')


def tracts_in_rect(request):
    """ Find all tracts within the provided lat/lon boundaries """
    minlat, maxlat = request.GET.get('minlat'), request.GET.get('maxlat')
    minlon, maxlon = request.GET.get('minlon'), request.GET.get('maxlon')

    try:
        minlat, maxlat = float(minlat), float(maxlat)
        minlon, maxlon = float(minlon), float(maxlon)
    except ValueError:
        raise Http404

    # check that any of the three points are inside the boundary
    query = Q(minlat__gte=minlat, minlat__lte=maxlat,
              minlon__gte=minlon, minlon__lte=maxlon)
    query = query | Q(minlat__gte=minlat, minlat__lte=maxlat,
                      maxlon__gte=minlon, maxlon__lte=maxlon)
    query = query | Q(maxlat__gte=minlat, maxlat__lte=maxlat,
                      minlon__gte=minlon, minlon__lte=maxlon)
    query = query | Q(maxlat__gte=minlat, maxlat__lte=maxlat,
                      maxlon__gte=minlon, maxlon__lte=maxlon)

    tracts = StateCensusTract.objects.filter(query).order_by('geoid')
    tracts = tracts.values_list('geojson')
    tracts = _paged(tracts, request)

    # We already have the json strings per model pre-computed, so just place
    # them inside a static response
    response = '{"crs": {"type": "link", "properties": {"href": '
    response += '"http://spatialreference.org/ref/epsg/4326/", "type": '
    response += '"proj4"}}, "type": "FeatureCollection", "features": [%s]}'
    response = response % ', '.join(t[0] for t in tracts)
    return HttpResponse(response, content_type='application/json')
