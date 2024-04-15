import requests, os 

  

bcp_login_url = os.environ.get("BCP_LOGIN_URL") 

scoped_token_url = os.environ.get("BCP_AUTHENTICATE_URL") 

detach_ip_url = os.environ.get("DETACH_IP_URL")

attach_ip_url = os.environ.get("ATTACH_IP_URL")

reboot_vm_url = os.environ.get("REBOOT_VM_URL") 

  

 

def main_func(): 

    auth_token = get_auth_token() 

    scoped_token = get_scoped_token(auth_token) 

    detach_status = detach_floating_ip(auth_token, scoped_token) 

    if detach_status =="success": 

        attach_status = attach_floating_ip(auth_token, scoped_token) 

        if attach_status =="success": 

            reboot_vm(auth_token, scoped_token) 

        else: 

            raise Exception 

    else: 

        raise Exception 

    print("Done") 

  

def get_auth_token(): 

    payload = { 

        "email": "mehadihasan.shuvo@brilliant.com.bd", 

        "password": os.environ.get("PASSWORD") 

    } 

    login_resp = requests.post(bcp_login_url, json=payload) 

    login_resp_dict = login_resp.json() 

    if login_resp_dict.get("status")=="success": 

        auth_token = login_resp_dict.get("auth_token") 

    return auth_token 

  

def get_scoped_token(auth_token): 

    headers = {"Authorization": "Bearer "+auth_token} 

    scoped_token_resp = requests.get(scoped_token_url,headers=headers) 

    scoped_token_resp_dict = scoped_token_resp.json() 

    scoped_token = scoped_token_resp_dict.get("data").get("scopedToken") 

    return scoped_token 

  

def detach_floating_ip(auth_token, scoped_token): 

    payload = { 

        "scopedToken": scoped_token, 

        "serverID": os.environ.get("SERVER_TWO_ID"), 

        "uid": os.environ.get("UID") 

    } 

    headers = {"Authorization": "Bearer "+auth_token} 

    detach_ip_resp = requests.post(detach_ip_url, json=payload,headers=headers) 

    if detach_ip_resp.status_code == 200: 

        return "success" 

    else: 

        return "fail" 

     

def attach_floating_ip(auth_token, scoped_token): 

    payload = { 

        "scopedToken": scoped_token, 

        "projectID": os.environ.get("PROJECT_ID"), 

        "serverID": os.environ.get("SERVER_ONE_ID"), 

        "floating_ip_id": os.environ.get("FLOATING_IP_ID"), 

        "uid": os.environ.get("UID") 

    } 

    headers = {"Authorization": "Bearer "+auth_token} 

    attach_ip_resp = requests.post(attach_ip_url, json=payload,headers=headers) 

    if attach_ip_resp.status_code == 200: 

        return "success" 

    else: 

        return "fail" 

     

def reboot_vm(auth_token, scoped_token): 

    payload = { 

        "scopedToken": scoped_token, 

        "serverID": os.environ.get("SERVER_TWO_ID"), 

        "uid": os.environ.get("UID") 

    } 

    headers = {"Authorization": "Bearer "+auth_token} 

    reboot_vm_resp = requests.post(reboot_vm_url, json=payload,headers=headers) 

    if reboot_vm_resp.status_code != 202: 

        raise Exception 

    return 


if __name__=="__main__": 

    main_func() 
  

  

if __name__=="__main__": 

    main_func() 
