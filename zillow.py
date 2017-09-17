import pyzillow
from pyzillow.pyzillow import ZillowWrapper, GetDeepSearchResults

ZWSID=r'X1-ZWz190x3nag8i3_6wmn8'

def parse_zestimate_attributes(address):
    zipcode = address.split()[-1] #address.split()[-1].split('-')[0]
    zillow_data = ZillowWrapper(ZWSID)
    try:
        deep_search_response = zillow_data.get_deep_search_results(address, zipcode)
    except pyzillow.pyzillowerrors.ZillowError:
        return
    return GetDeepSearchResults(deep_search_response)

def get_rent_attributes_from_zillow(address):
    zillow_attrs = {'zestimate_amount': 'Zillow Rent',
                    'zestimate_valuationRange_low': 'Rent Bottom',
                    'zestimate_valuation_range_high': 'Rent Best',
                    'zestimate_last_updated': 'Rent Last Updated'}

    result = parse_zestimate_attributes(address)
    if result:
        zillow_result = {}
        for attr, other_name in zillow_attrs.items():
            try:
                attr_value = result.get_attr(attr)
            except AttributeError:
                attr_value = 'Attribute Unavailable'
            zillow_result[other_name] = attr_value
        return zillow_result
    else:
        return {'Zillow Error': 'Zillow Error'}


        #
    # result_attrs = result.__dict__
    # print(result.get_attr('zestimate_amount'))
    # return result_attrs

if __name__ == '__main__':
    addressList = '''4916 Laborde Street Charlotte, NC 28269
7318 MIDDLEBURY PL, CHARLOTTE, NC 28212
9521 LOBLOLLY LN, CHARLOTTE, NC 28210
5124 QUEEN ANNE RD, CHARLOTTE, NC 28217
2839 SOUTHWEST BLVD, CHARLOTTE, NC 28216
717 Peachtree Road Charlotte, NC 28216
6720 FORTESCUE DR, CHARLOTTE, NC 28213
2008 Toddville Road Charlotte, NC 28214
2430 Rice Planters Road Charlotte, NC 28273
1115 Village Lake Drive Monroe, NC 28110-9664
203 Ross Moore Avenue Charlotte, NC 28205
7323 STRIPES CT, CHARLOTTE, NC 28217
10421 MOORES CHAPEL RD, CHARLOTTE, NC 28214
9271 MEADOW VISTA RD, CHARLOTTE, NC 28213
8611 MISSION HILLS RD, CHARLOTTE, NC 28227
13506 Kibworth Lane Charlotte, NC 28273
14902 Hawick Manor Lane Pineville, NC 28134-6406'''.splitlines()
    zillow_attrs = ['zestimate_amount',
                    'zestimate_valuationRange_low',
                    'zestimate_valuation_range_high',
                    'zestimate_last_updated']
    for address in addressList:
        res = get_rent_attributes_from_zillow(address)
        print(res)
#
# 'zestimate_amount': '239991',
# 'zestimate_last_updated': '09/16/2017',
# 'zestimate_percentile': '0',
# 'zestimate_valuationRange_low': '227991',
# 'zestimate_valuation_range_high': '251991',
# 'zestimate_value_change': '2202',
#
#
# {'bathrooms': '2.5',
#  'bedrooms': '4',
#  'data': <Element 'results' at 0x7f73a8fd7098>,
#  'graph_data_link': 'http://www.zillow.com/homedetails/13506-Kibworth-Ln-Charlotte-NC-28273/6308261_zpid/#charts-and-data',
#  'home_detail_link': 'http://www.zillow.com/homedetails/13506-Kibworth-Ln-Charlotte-NC-28273/6308261_zpid/',
#  'home_size': '2638',
#  'home_type': 'SingleFamily',
#  'last_sold_date': '02/28/2006',
#  'last_sold_price': '161500',
#  'latitude': '35.109349',
#  'longitude': '-80.965557',
#  'map_this_home_link': 'http://www.zillow.com/homes/6308261_zpid/',
#  'property_size': '8712',
#  'tax_value': '182900.0',
#  'tax_year': '2017',
#  'year_built': '1995',
#  'zestimate_amount': '239991',
#  'zestimate_last_updated': '09/16/2017',
#  'zestimate_percentile': '0',
#  'zestimate_valuationRange_low': '227991',
#  'zestimate_valuation_range_high': '251991',
#  'zestimate_value_change': '2202',
#  'zillow_id': '6308261'}