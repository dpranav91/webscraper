import pyzillow
from pyzillow.pyzillow import ZillowWrapper, ZillowResults, GetDeepSearchResults
from pprint import pprint

ZWSID = r'X1-ZWz190x3nag8i3_6wmn8'

# --------------------------------------------
# OVER RIDE ZillowWrapper
# --------------------------------------------
class ZillowWrap(ZillowWrapper):
    def get_zestimate(self, zpid):
        """
        GetUpdatedPropertyDetails API
        """
        url = 'http://www.zillow.com/webservice/GetZestimate.htm'

        params = {
            'zpid': zpid,
            'zws-id': self.api_key,
            'rentzestimate': True
        }
        return self.get_data(url, params)


class GetZestimateDetails(ZillowResults):
    """
    Parse GetZestimateDetails
    """
    attribute_mapping = {
        'zillow_id': 'zpid',

        # 'zestimate_amount': 'zestimate/amount',
        # 'zestimate_lastupdated': 'zestimate/last-updated',
        'zestmate_oneweekchange': 'zestimate/oneWeekChange',
        # 'zestimate_value_change': 'zestimate/valueChange',
        'zestimate_valuation_range': 'zestimate/valuationRange',
        # 'zestimate_percentile': 'zestimate/percentile',

        'rentzestimate_amount': 'rentzestimate/amount',
        'rentzestimate_last_updated': 'rentzestimate/last-updated',
        'rentzestimate_oneweekchange': 'rentzestimate/oneWeekChange',
        'rentzestimate_value_change': 'rentzestimate/valueChange',
        'rentzestimate_valuation_range': 'rentzestimate/valuationRange'

    }

    def __init__(self, data, *args, **kwargs):
        """
        Creates instance of GeocoderResult from the provided XML data array
        """
        self.data = data.findall('response')[0]

        for attr in self.attribute_mapping.__iter__():
            try:
                self.__setattr__(attr, self.get_attr(attr))
            except AttributeError:
                print('AttributeError with %s' % attr)


# ----------------------------------------------
# MAIN
# ----------------------------------------------

def parse_zestimate_attributes(address, zillow_attrs):
    zipcode = address.split()[-1]  # address.split()[-1].split('-')[0]
    zillow_data = ZillowWrap(ZWSID)
    print("zestimate for address:{}, zipcode:{}".format(address, zipcode))
    try:
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
    # except pyzillow.pyzillowerrors.ZillowError:
    #     return
    except Exception:
        print("Error while parsing zillow attributes for {}".format(address))
        return {'zillow': False}
    deep_search = GetDeepSearchResults(deep_search_response)
    # **************************************
    # GetZestimate
    # **************************************
    try:
        resp = zillow_data.get_zestimate(deep_search.zillow_id)
    except Exception:
        print("Error while parsing zillow attributes for {}".format(address))
        return {'zillow': False}
    zestimate_result = GetZestimateDetails(resp)
    # pprint(zestimate_result.__dict__)
    zillow_res = {}
    for attr in zillow_attrs:
        key = 'zillow_bedrooms' if attr =='bedrooms' else attr
        if attr in deep_search.__dict__:
            attr_value = deep_search.get_attr(attr)
            if attr_value:
                zillow_res[key] = attr_value
        elif attr in zestimate_result.__dict__:
            attr_value = zestimate_result.get_attr(attr)
            if attr_value:
                zillow_res[key] = attr_value
    zillow_res['zillow'] = True
    return zillow_res

#
# def get_rent_attributes_from_zillow(address):
#     zillow_attrs = {'zestimate_amount': 'Zillow Rent',
#                     'zestimate_valuationRange_low': 'Rent Bottom',
#                     'zestimate_valuation_range_high': 'Rent Best',
#                     'zestimate_last_updated': 'Rent Last Updated'}
#
#     result = parse_zestimate_attributes(address)
#     if result:
#         zillow_result = {}
#         for attr, other_name in zillow_attrs.items():
#             try:
#                 attr_value = result.get_attr(attr)
#             except AttributeError:
#                 attr_value = 'Attribute Unavailable'
#             zillow_result[other_name] = attr_value
#         return zillow_result
#     else:
#         return {'Zillow Error': 'Zillow Error'}


if __name__ == '__main__':
    addressList = [
        '4916 Laborde Street Charlotte, NC 28269',
                   '7318 MIDDLEBURY PL, CHARLOTTE, NC 28212',
                   '2150 Pheasant Glen Road Charlotte, NC 28214',
                   '254 Lucky Drive Way Northwest Concord, NC 28027'
    ]
    attrs = ['bathrooms', 'bedrooms', 'home_size', 'home_type',
             'property_size', 'tax_value', 'year_built', 'zestimate_amount',
             'zestimate_valuationRange_low', 'zestimate_valuation_range_high',
             'rentzestimate_amount', 'rentzestimate_last_updated',
             'zestimate_valuation_range']
    for address in addressList:
        res = parse_zestimate_attributes(address, attrs)
        print(res)

    '''
    ************************************
    result.__dict__ SAMPLE
    ************************************
    {>'bathrooms': '2.5',
     >'bedrooms': '4',
     'data': <Element 'results' at 0x7f73a8fd7098>,
     'graph_data_link': 'http://www.zillow.com/homedetails/13506-Kibworth-Ln-Charlotte-NC-28273/6308261_zpid/#charts-and-data',
     'home_detail_link': 'http://www.zillow.com/homedetails/13506-Kibworth-Ln-Charlotte-NC-28273/6308261_zpid/',
     ^'home_size': '2638',
     ^'home_type': 'SingleFamily',
     'last_sold_date': '02/28/2006',
     'last_sold_price': '161500',
     'latitude': '35.109349',
     'longitude': '-80.965557',
     'map_this_home_link': 'http://www.zillow.com/homes/6308261_zpid/',
     >'property_size': '8712',
     >'tax_value': '182900.0',
     'tax_year': '2017',
     >'year_built': '1995',
     >'zestimate_amount': '239991',
     'zestimate_last_updated': '09/16/2017',
     'zestimate_percentile': '0',
     >'zestimate_valuationRange_low': '227991',
     >'zestimate_valuation_range_high': '251991',
     'zestimate_value_change': '2202',
     'zillow_id': '6308261'}
     '''
