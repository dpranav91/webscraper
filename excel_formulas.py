from collections import OrderedDict as od

formulas_dict = od([
    ('Spread', '=IF(AND(ISNUMBER(E{0}), ISNUMBER(U{0})),U{0}-E{0},"")',),
    ('Spread %', '=IF(AND(ISNUMBER(X{0}), ISNUMBER(U{0}), U{0}<>0), X{0}/U{0}, "")'),
    ('Loan Amount', '=IF(AND(ISNUMBER(E{0})),E{0}*0.75, "")'),
    ('Mortage Princ+Int', '=IF(AND(ISNUMBER(Z{0})),-PMT(4.25/1200,120, Z{0}), "")'),
    ('Property Tax', '=IF(AND(ISNUMBER(U{0})),U{0}*0.0125/12, "")'),
    ('HOA+INS', '=170+(400/12)'),
    ('Final Mortgage',
     '=IF(AND(ISNUMBER(AA{0}), ISNUMBER(AB{0}),  ISNUMBER(AC{0})), AA{0}+AB{0}+AC{0}, "")'),

    ('Rento Meter Avg', ''),
    ('Rent Best', ''),
    ('Rest Bottom', ''),
    ('Break Even', '=IF(AND(ISNUMBER(AE{0}), ISNUMBER(AD{0})), (AE{0}-AD{0}),"")'),
])
