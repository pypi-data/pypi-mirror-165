import requests as sync_req
from zrequests import logger
from zrequests.setting import Setting
import time
import json as f_json


def verify_success_text(s_text, response: sync_req.Response):
    if isinstance(s_text, dict):
        r_json = f_json.loads(response.text)
        for k, v in s_text.items():
            if k in r_json and v == r_json[k]:
                continue
            else:
                return False, response
        return True, response

    if isinstance(s_text, str):
        if s_text in response.text:
            return True, response
        else:
            return False, response

    return False, response


# todo remove sensitive info from url
def send_request(method, url, s_codes: list, params, headers, tag='N', json=None, data=None, count=0, sleep=False,
                 s_text=None):
    response = None
    if count < Setting.MAX_RETRY:
        try:
            response = sync_req.request(method, url=url, params=params, data=data, headers=headers, json=json)
            if response.status_code in s_codes:
                if not s_text:
                    return True, response
                return verify_success_text(s_text, response)
            else:
                logger.warning(f'[ZREQUEST] [{tag}][{count}] {url}, e=HTTP code not in s_codes, r={response}')
                count += 1
                if sleep:
                    time.sleep(2 ** count)
                return send_request(method, url, s_codes, params, headers, tag, json, data, count, sleep, s_text)

        except Exception as e:
            logger.warning(f'[ZREQUEST] [{tag}][{count}] {url}, e={e}, r={response}', exc_info=True)
            count += 1
            if sleep:
                time.sleep(2 ** count)
            return send_request(method, url, s_codes, params, headers, tag, json, data, count, sleep, s_text)

    logger.error(f'[ZREQUEST] [{tag}] Failed to get proper response for {url} r={response},', exc_info=True)
    return False, response
