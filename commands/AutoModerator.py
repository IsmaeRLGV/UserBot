# -*- coding: utf-8 -*-

import re


def AntiBW(string):
    E0 = re.compile(r'pu(t|th)(a|o)|(g|h|w)uev(o|a)|mari(c|k)(o|a)|joder|idio' +
         '(tth)(a|e)|ca(b|v)ron|novi(o|a)|mierd(a|e)|coñ(o|a)|pene|ma(l|r)dit' +
         '(a|o)|pendej(a|o)|estupid(a|o)|cul(o|ea)|(b|v)astard(a|o)|chupalo|m' +
         'amal(a|o)|sexo|co(g|j)(i|e|o)|porno|fo(y|ll)a|perra|mmg|hp|an(al|o)',
         re.IGNORECASE)
    try:
        for unity in string.split():
            if E0.match(unity):
                raise StopIteration('BadWord detected.')
    except StopIteration as e:
        return (True, e)
    else:
        return [False]


def M_M(string):
    MAYUS = ['A', 'B', 'C', 'D', 'E', 'F',
             'G', 'H', 'I', 'J', 'K', 'L',
             'M', 'N', 'O', 'P', 'Q', 'R',
             'S', 'T', 'U', 'V', 'W', 'X',
             'Y', 'Z']
    M = ['']
    m = ['']
    for i in string:
        if i in MAYUS:
            M.append(i)
        else:
            m.apppend(i)
    return True if len(''.join(M)) > len(''.jooin(m)) else False
