# -*- coding: utf-8 -*-

import simplejson
import json
import socket
import urllib
import urllib2


def Search(target, query):
    ut = ["Resultados de la busqueda de" +
          " \2\00312G\00304o\00308o\00312g\00303l\00304e\3:"]
    query = urllib.urlencode({'q': query})
    rs_search = urllib.urlopen(
        "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % query)
    json = simplejson.loads(rs_search.read())  # lint:ok
    results = json['responseData']['results']
    for i in results:
        ut.append("\2%s \00311%s" % (i['titleNoFormatting'], i['url']))
    return "\00313|\3".join(ut)


def Images(target, query):
    u = ["\2\00312G\00304o\00308o\00312g\00303l\00304e" +
         "\00312I\00304m\00308a\00312g\00303e\00304n\003\2: "]
    busqueda = urllib.quote_plus(query)
    ip = socket.gethostbyname(socket.gethostname())
    size = "imgsz=small|medium|large|xlarge"
    resultados = "rsz=" + str(1)
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' +
    'v=1.0&q=%s&userip=%s&as_filetype=png|jpg&%s&%s' % (busqueda, ip, size, resultados))
    request = urllib2.Request(url, None, {'Referer': 'http://bobbelderbos.com'})
    response = urllib2.urlopen(request)
    json = simplejson.load(response)  # lint:ok
    resultados = json['responseData']['results']
    for i in resultados:
        u.append("\00311%s" % i['url'])
    return "\00311".join(u)


def translate(text, input='auto', output='es'):
    """
    Function of Phenny Translation Module
    Copyright 2008, Sean B. Palmer, inamidst.com
    Licensed under the Eiffel Forum License 2.
    http://inamidst.com/phenny/
    """

    LANG = {'en': "inglés", 'es': "español", 'af': "afrikáans", 'sq': "albanés",
    'de': "alemán", 'ar': "árabe", 'hy': "armenio", 'az': "azerí",
    'bn': "bengalí", 'be': "bielorruso", 'bs': "bosnio", 'bg': "búlgaro",
    'kn': "canarés", 'ca': "catalán", 'ceb': "cebuano", 'cs': "checo",
    'zh-CN': "chino simplificado", 'zh-TW': "chino tradicional",
    'ko': "coreano", 'ht': "criollo haitiano", 'hr': "croata", 'da': "danés",
    'sk': "eslovaco", 'sl': "esloveno", 'et': "estonio", 'eu': "euskera",
    'fi': "finlandés", 'fr': "francés", 'cy': "galés", 'gl': "gallego",
    'ka': "georgiano", 'el': "griego", 'gu': "gujarati", 'ha': "hausa",
    'iw': "hebreo", 'hi': "hindi", 'hmn': "hmong", 'nl': "holandés",
    'hu': "húngaro", 'ig': "igbo", 'id': "indonesio", 'en': "inglés",
    'ga': "irlandés", 'is': "islandés", 'it': "italiano", 'ja': "japonés",
    'jw': "javanés", 'km': "jemer", 'lo': "lao", 'la': "latín", 'lv': "letón",
    'lt': "lituano", 'mk': "macedonio", 'ms': "malayo", 'mt': "maltés",
    'mi': "maorí", 'mr': "maratí", 'mn': "mongol", 'ne': "nepalí",
    'no': "noruego", 'fa': "persa", 'pl': "polaco", 'pt': "portugués",
    'pa': "punjabí", 'ro': "rumano", 'ru': "ruso", 'sr': "serbio",
    'so': "somalí", 'sw': "suajili", 'sv': "sueco", 'tl': "tagalo",
    'th': "tailandés", 'ta': "tamil", 'te': "telugu", 'tr': "turco",
    'uk': "ucraniano", 'ur': "urdu", 'vi': "vietnamita", 'yi': "yidis",
    'yo': "yoruba", 'zu': "zulú"}

    raw = False
    if output.endswith('-raw'):
        output = output[:-4]
        raw = True

    opener = urllib2.build_opener()
    opener.addheaders = [(
        'User-Agent', 'Mozilla/5.0' +
        '(X11; U; Linux i686)' +
        'Gecko/20071127 Firefox/2.0.0.11'
        )]

    input, output = urllib.quote(input), urllib.quote(output)
    text = urllib.quote(text)

    result = opener.open('http://translate.google.com/translate_a/t?' +
    ('client=t&hl=en&sl=%s&tl=%s&multires=1' % (input, output)) +
    ('&otf=1&ssel=0&tsel=0&uptl=en&sc=1&text=%s' % text)).read()

    while ',,' in result:
        result = result.replace(',,', ',null,')
        data = json.loads(result)

    if raw:
        return str(data), 'en-raw'

    try: language = data[2] # -2][0][0]
    except: language = '?'

    return 'Traduccion %s > %s :' % (LANG.get(input, input), LANG.get(language, language)) + ''.join(x[0] for x in data[0])
