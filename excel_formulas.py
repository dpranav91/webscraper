from collections import OrderedDict as od

excel_columns_mapping = {
    'estimate': 'V',
    'price': 'T',
    'spread': 'Y',
    'loan_amount': 'AA',
    'mortage_price_int': 'AB',
    'property_tax': 'AC',
    'hoa_ins': 'AD',
    'rent_meter_avg': 'AF',
    'final_mortgage': 'AE'}

formulas_dict = od([
    ('Spread',
     '=IF(AND(ISNUMBER({price}{{0}}), ISNUMBER({estimate}{{0}})),'
     '{estimate}{{0}}-{price}{{0}},"")'.format(**excel_columns_mapping)),
    ('Spread %',
     '=IF(AND(ISNUMBER({spread}{{0}}), ISNUMBER({estimate}{{0}}), {estimate}{{0}}<>0), '
     '{spread}{{0}}/{estimate}{{0}}, "")'.format(**excel_columns_mapping)),
    ('Loan Amount',
     '=IF(AND(ISNUMBER({price}{{0}})),{price}{{0}}*0.75, "")'.format(**excel_columns_mapping)),
    ('Mortage Princ+Int',
     '=IF(AND(ISNUMBER({loan_amount}{{0}})),'
     '-PMT(4.25/1200,120, {loan_amount}{{0}}), "")'.format(**excel_columns_mapping)),
    ('Property Tax',
     '=IF(AND(ISNUMBER({estimate}{{0}})),'
     '{estimate}{{0}}*0.0125/12, "")'.format(**excel_columns_mapping)),
    ('HOA+INS', '=170+(400/12)'),
    ('Final Mortgage',
     '=IF(AND(ISNUMBER({mortage_price_int}{{0}}), '
     'ISNUMBER({property_tax}{{0}}),  ISNUMBER({hoa_ins}{{0}})), '
     '{mortage_price_int}{{0}}+{property_tax}{{0}}+{hoa_ins}{{0}}, '
     '"")'.format(**excel_columns_mapping)),
    ('Break Even',
     '=IF(AND(ISNUMBER({rent_meter_avg}{{0}}), ISNUMBER({final_mortgage}{{0}})), '
     '({rent_meter_avg}{{0}}-{final_mortgage}{{0}}),"")'.format(**excel_columns_mapping)),
])
