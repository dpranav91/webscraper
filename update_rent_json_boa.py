import json
import os
from load_parse_boa import (load_boa,
                            parse_boa,
                            get_rent_attributes_from_boa)
from utils import load_json, dump_json, load_json_or_create_if_empty

CWD = os.path.split(os.path.abspath(__file__))[0]
database_path = os.path.join(CWD, 'database')
rent_json_file = os.path.join(database_path, 'rent.json')
TRIGGER_LIMIT = 50

def update_rent_json_by_parsing_boa(rent_json_file):
    rent_dict = load_json_or_create_if_empty(rent_json_file)
    counter = 0
    for address, attrs_map in rent_dict.items():
        # error in loading/parsing boa url
        if attrs_map.get('Error'):
            pass
        # attributes exists already for address
        elif attrs_map:
            pass
        # // update rent attributes by rendering boa url and parsing
        # // only when mapping is empty and no error
        else:
            print("Updating rent attributes for address: {}".format(address))
            attrs_map.update(get_rent_attributes_from_boa(address))
            counter += 1
            if counter >= TRIGGER_LIMIT: break

    dump_json(rent_json_file, rent_dict)
    return rent_dict


if __name__ == '__main__':
    from pprint import pprint

    rents_attr = update_rent_json_by_parsing_boa(rent_json_file)
    # pprint(rents_attr)
