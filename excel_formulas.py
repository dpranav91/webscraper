from collections import OrderedDict as od

formulas_dict = od([
    ('Spread', '=IF(AND(ISNUMBER(E{0}), ISNUMBER(U{0})),U{0}-E{0},"")',),
    ('Spread %', '=IF(AND(ISNUMBER(X{0}), ISNUMBER(U{0}), U{0}<>0), X{0}/U{0}, "")')
])
