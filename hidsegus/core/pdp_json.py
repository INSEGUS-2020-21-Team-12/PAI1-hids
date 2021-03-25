import json
from datetime import datetime
from hidsegus.core import pdp_protocol, utils

def rsa_hash(filepath, outfile, key_bitsize=2048):
    if key_bitsize is None: key_bitsize = 2048
    if outfile is None: outfile = f'{utils.filename(filepath)}.json'
    hmorph_hash, n_modulo = pdp_protocol.rsa_hash(filepath, key_bitsize)
    
    pdp_hashdata = {
        "filepath": filepath,
        "n_modulo": n_modulo,
        "rsahash": hmorph_hash
    }

    with open(outfile, "w") as write_file:
        json.dump(pdp_hashdata, write_file, indent=2)
    
    return f'{outfile}'

def request(json_hashdata, outfile):

    pdp_hashdata = None
    with open(json_hashdata) as read_file:
        pdp_hashdata = json.load(read_file)
    
    if outfile is None: outfile = f"{utils.generate_jsonfilename(pdp_hashdata['filepath'], 'pdp_req')}"
    
    b_token, n_modulo = pdp_protocol.request(pdp_hashdata['n_modulo'])

    pdp_request = {
        "filepath": pdp_hashdata['filepath'],
        "b_token": b_token,
        "n_modulo": n_modulo,
    }

    with open(outfile, "w") as write_file:
        json.dump(pdp_request, write_file, indent=2)
    
    return outfile, pdp_hashdata['filepath']

def response(json_request, outfile):

    pdp_request = None
    with open(json_request) as read_file:
        pdp_request = json.load(read_file)
    
    if outfile is None: outfile = f"{json_request.replace('pdp_req', 'pdp_resp')}"

    pdp_result = pdp_protocol.response(pdp_request['filepath'], pdp_request['b_token'], pdp_request['n_modulo'])

    pdp_response = {
        "filepath": pdp_request['filepath'],
        "b_token": pdp_request['b_token'],
        "n_modulo": pdp_request['n_modulo'],
        "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "pdp_result": pdp_result
    }

    with open(outfile, "w") as write_file:
        json.dump(pdp_response, write_file, indent=2)
    
    return outfile, pdp_request['filepath']

def verification(json_response, json_hashdata):
    pdp_response = None
    with open(json_response) as read_file:
        pdp_response = json.load(read_file)

    pdp_hashdata = None
    with open(json_hashdata) as read_file:
        pdp_hashdata = json.load(read_file)

    pdp_expected_result = pdp_protocol.verification(pdp_response['b_token'], pdp_hashdata['rsahash'], pdp_response['n_modulo'])    

    return pdp_expected_result == pdp_response['pdp_result'], pdp_response['filepath']




    


    




