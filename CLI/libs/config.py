import requests
import json
import os
import yaml
from libs.utils import generate_respons,get_url,get_time,get_idkey,dictcleanup
from libs.auth import get_headers, get_user_id
import copy

with open('libs/templates/endpoints.json', 'r') as f :
    jsonmodel = json.load(f)
    f.close()

DUMP_FOLDER = os.path.expanduser("~")

def send_request(endpoint,data):
    headers = get_headers()
    headers = headers['data']
    url = get_url(endpoint)
    try :
        result = requests.post(
            url = url,
            data = json.dumps(data),
            headers = headers
        )
        respons = result.json()
    except Exception as e:
        respons=generate_respons(False,str(e))
    return respons

def searchId(endpoint,name):
    data = dict()
    data = jsonmodel['search'][endpoint]['data']
    url = get_url(endpoint)
    keys = list(data['where']['tags'].keys())
    headers = get_headers()
    headers = headers['data']
    for i in keys:
        if 'id' not in i:
            key = i
    data['where']['tags'][key] = str(name)
    try :
        res = requests.post(url = url,
        data = json.dumps(data),
        headers=headers)
        res = res.json()
        res = res['data']
        respons = res[0][get_idkey(endpoint, headers=headers)]
    except Exception as e:
        return generate_respons(False,str(e))     
    return generate_respons(True,'success',respons)

def setDefaultDns(name):

    
    header = (get_headers())['data']
    header['user_id'] = (get_user_id())['data']
    res = requests.post("http://103.89.5.121:6968/api/user/dnscreate",
    data = {'domain' : str(name)}
    ,headers=header)
    print(res)
    res = res.json()
    if 'code' not in res :
        print(res['message'])
        return False
    
    tying_zone(header['user_id'],res['data']['data']['id_zone'])

    tags = res['data']['data']['id_zone']
    syncdat = {"command" : "conf-insert", "tags" : str(tags)}
    res=sync(syncdat)
    syncdat = {"command" : "zone-soa-insert", "tags" : str(tags)}
    res=sync(syncdat)
    syncdat = {"command" : "zone-ns-insert", "tags" : str(tags)}
    res=sync(syncdat)

def tying_zone(user_id,id_zone):
    header = (get_headers())['data']
    header['user-id'] = str(user_id)
    data = {"id_zone" : str(id_zone)}
    url = get_url('userzone')
    res = requests.post(url = url, data = data, headers = header)

def setRecord(obj):
    from libs.list import check_zone_authorization
    with open('libs/templates/endpoints.json', 'r') as f :
        jsonmodel = json.load(f)


        temp = copy.deepcopy(obj)
        
        check = check_zone_authorization([obj['--nm-zn']])
        if not check['status']:
            return generate_respons(True,'Authorization failure')
        
        try :
            data = searchId('zone',obj['--nm-zn'])
            temp['--id-zone'] = data['data']
            data = searchId('type',obj['--type'].upper())
            temp['--id-type'] = data['data']
            data = searchId('ttl',obj['--ttl'])
            temp['--id-ttl'] = data['data']
        
        except Exception as e:
            return generate_respons(False,"Zone/Type/TTL doesn't exist\n" + str(e))
        
        #insert Record
        json_data = copy.deepcopy(jsonmodel['create']['record']['data'])
        for i in json_data['insert']['fields']:
            json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
        
        res = send_request('record',json_data)
        temp['--id-record'] = res['message']['id']


        #insert ttldata
        json_data = jsonmodel['create']['ttldata']['data']
        for i in json_data['insert']['fields']:
            json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
        res = send_request('ttldata',json_data)
        temp['--id-ttldata'] = res['message']['id']
        
        #insert content
        
        json_data = jsonmodel['create']['content']['data']
        for i in json_data['insert']['fields']:
            json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
        res = send_request('content',json_data)
        temp['--id-content'] = res['message']['id']

        #insert content serial
        record_type = obj['--type'].upper()

        if record_type == 'SRV' or record_type == 'MX':
            json_data = jsonmodel['create']['content_serial']['data']
            for i in json_data['insert']['fields']:
                json_data['insert']['fields'][i] = temp[json_data['insert']['fields'][i]]
            res = send_request('content_serial',json_data)
            temp['--id-content-serial'] = res['message']['id']
        f.close()

    if record_type == 'MX':
        cmd = 'zone-mx-insert'
        datasync = {"command" : cmd, "tags" : temp['--id-zone']}
    elif record_type == 'SRV':
        cmd = 'zone-srv-insert'
        datasync = {"command" : cmd, "tags" : temp['--id-zone']}
    else :
        cmd = 'zone-insert'
        datasync = {"command" : cmd, "tags" : temp['--id-record']}

    try:
        sync(datasync)
    except Exception as e:
        print("Error \n",str(e))
        return generate_respons(False,'Sync failure')

    return generate_respons(True,'success',data)


# def remove_data(name,endpoint):
#     json_data = jsonmodel['rm'][endpoint]['data']
#     url = get_url(endpoint)
#     key = get_idkey(endpoint, headers=get_headers())
#     delid = searchId(endpoint,name)
#     json_data['remove']['tags'][key] = delid
#     try :
#         requests.post(url, data = json.dumps(json_data)
#         , headers=get_headers())
#     except Exception as e:
#         respons = str(e)
#         print(respons)
#     return

def sync(obj):
    cmd = obj['command']
    tags = obj['tags']
    data_send = {cmd : {"tags" : ''}}
    
    if cmd != 'zone-insert':
        data_send[cmd]['tags'] =  {"id_zone" : tags}
    else :
        data_send[cmd]['tags'] = {"id_record" : tags}
        
    res=send_request('command', data_send)
    
    return res
    
def check_yaml(filename):
    path = ("{}/restknot/"+filename).format(DUMP_FOLDER)
    return os.path.isfile(path)

def load_yaml(filename):
    if check_yaml(filename):
        data = None
        try:
            with open(("{}/restknot/"+filename).format(DUMP_FOLDER),'r') as f :
                data = yaml.load(f)
            return generate_respons(True,'success',data)
        except Exception as e:
            return generate_repons(False,str(e))
    else:
        return util.generate_respons(False,"File doesn't exist")

def parse_yaml(data):
    data_list = list()
    try :
        for i in data:
            for j in data[i]:
                    for k in data[i][j]:
                            data_dict = dict()
                            data_dict['--nm-zn']=i
                            data_dict['--nm'] = j
                            key = list(k.keys())
                            key = key[0]
                            data_dict['--type'] = key.upper()
                            data_dict['--ttl'] = k[key]['ttl']
                            data_dict['--nm-con'] = k[key]['content']
                            data_dict['--date'] = get_time()
                            if 'content-serial' in k[key]:
                                    data_dict['--nm-con-ser']=k[key]['content-serial']
                            data_list.append(data_dict)
        for i in data_list:
            if i['--type'] == 'SRV' or i['--type']=='MX':
                    if not '--nm-con-ser' in i:
                            data_list.remove(i)
            else :
                    if '--nm-con-ser' in i:
                            data_dict.remove(i)
        
        respon = generate_respons(True,'success',data_list)
    except Exception as e:
        respon = generate_respons(False,str(e))
    finally :
        return respon