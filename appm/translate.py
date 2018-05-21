import json

import requests
from flask import current_app

url = 'https://api.microsofttranslator.com/v2/Ajax.svc/Translate'


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translator service not configured.')
    params = {'text': text, 'from': source_language, 'to': dest_language}
    headers = {'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    r = requests.get(url, params=params, headers=headers)
    if r.status_code != 200:
        return _('Error: translator service failed.')
    return json.loads(r.content.decode('utf-8-sig'))
