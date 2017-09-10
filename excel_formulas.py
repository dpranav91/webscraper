from collections import OrderedDict as od

formulas_dict = od([
    ('Spread', '=IF(AND(ISNUMBER(E{0}), ISNUMBER(U{0})),U{0}-E{0},"")',),
    ('Spread %', '=IF(AND(ISNUMBER(X{0}), ISNUMBER(U{0}), U{0}<>0), X{0}/U{0}, "")'),
    ('Loan Amount', '=IF(AND(ISNUMBER(E2)),E2*0.75, "")'),
    ('Mortage Princ+Int', '=IF(AND(ISNUMBER(Z2)),-PMT(4.25/1200,120, Z2), "")'),
    ('Property Tax', '=IF(AND(ISNUMBER(U2)),U2*0.0125/12, "")'),
    ('HOA+INS', '170+(400/12)'),
    ('Final Mortgage', '=IF(AND(ISNUMBER(AA2), ISNUMBER(AB2),  ISNUMBER(AC2)), AA2+AB2+AC2, "")'),

    ('Rento Meter Avg', ''),
    ('Rent Best', ''),
    ('Rest Bottom', ''),
    ('Break Even', '=IF(AND(ISNUMBER(AE2), ISNUMBER(AD2)), (AE2-AD2),"")'),
])
