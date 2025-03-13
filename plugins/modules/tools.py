#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: duo_mfa

short_description: Manages Duo Security MFA actions (enroll, bypass, delete)

version_added: "1.2.0"

description:
    - This module allows enrolling a user into Duo Security, bypassing them, or deleting them.
    - It sends API requests to the Duo authentication endpoints.

options:
    username:
        description: Username of the user to be enrolled, bypassed, or deleted.
        required: true
        type: str
    host:
        description: The Duo API hostname (e.g., api-XXXXXXXX.duosecurity.com).
        required: true
        type: str
    ikey:
        description: Duo API integration key.
        required: true
        type: str
        no_log: true
    skey:
        description: Duo API secret key.
        required: true
        type: str
        no_log: true
    action:
        description: The action to perform ('enroll', 'bypass', or 'delete').
        required: false
        type: str
        default: "enroll"

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Enroll User To DUO
  duo_mfa:
    username: "kdalphas"
    host: "api-XXXXXXXX.duosecurity.com"
    ikey: "{{ ikey_password_var }}"
    skey: "{{ skey_password_var }}"
    action: "enroll"

- name: Bypass User In DUO
  duo_mfa:
    username: "kdalphas"
    host: "api-XXXXXXXX.duosecurity.com"
    ikey: "{{ ikey_password_var }}"
    skey: "{{ skey_password_var }}"
    action: "bypass"

- name: Delete User In DUO
  duo_mfa:
    username: "kdalphas"
    host: "api-XXXXXXXX.duosecurity.com"
    ikey: "{{ ikey_password_var }}"
    skey: "{{ skey_password_var }}"
    action: "delete"
'''

RETURN = r'''
original_message:
    description: The original username passed in.
    type: str
    returned: always
response:
    description: The response from the Duo API.
    type: dict
    returned: always
'''

import json
import subprocess
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        host=dict(type='str', required=True),
        ikey=dict(type='str', required=True, no_log=True),
        skey=dict(type='str', required=True, no_log=True),
        action=dict(type='str', required=False, default="enroll", choices=["enroll", "bypass", "delete"])
    )

    result = dict(
        changed=False,
        original_message='',
        response={}
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        module.exit_json(**result)

    username = module.params['username']
    host = module.params['host']
    ikey = module.params['ikey']
    skey = module.params['skey']
    action = module.params['action']

    if action in ["bypass", "delete"]:
        # Step 1: Get user ID
        get_user_command = [
            "python3", "-m", "duo_client.client",
            "--ikey", ikey,
            "--skey", skey,
            "--host", host,
            "--method", "GET",
            "--path", "/admin/v1/users",
            f"username={username}"
        ]
        
        try:
            user_process = subprocess.run(get_user_command, capture_output=True, text=True, check=True)
            user_output = user_process.stdout.strip()
            
            json_start = user_output.find('{')
            json_data = user_output[json_start:] if json_start != -1 else '{}'
            user_data = json.loads(json_data)
            
            if "response" in user_data and isinstance(user_data["response"], list) and len(user_data["response"]) > 0:
                user_id = user_data["response"][0].get("user_id")
            else:
                raise KeyError("User ID not found in response")
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError) as e:
            module.fail_json(msg=f"Failed to retrieve user ID for {username}: {str(e)}", **result)
    
    if action == "enroll":
        path = "/auth/v2/enroll"
        method = "POST"
        command = [
            "python3", "-m", "duo_client.client",
            "--ikey", ikey,
            "--skey", skey,
            "--host", host,
            "--method", method,
            "--path", path,
            f"username={username}"
        ]
    elif action == "bypass":
        path = f"/admin/v1/users/{user_id}"
        method = "POST"
        command = [
            "python3", "-m", "duo_client.client",
            "--ikey", ikey,
            "--skey", skey,
            "--host", host,
            "--method", method,
            "--path", path,
            "status=bypass"
        ]
    elif action == "delete":
        path = f"/admin/v1/users/{user_id}"
        method = "DELETE"
        command = [
            "python3", "-m", "duo_client.client",
            "--ikey", ikey,
            "--skey", skey,
            "--host", host,
            "--method", method,
            "--path", path
        ]
    
    try:
        process = subprocess.run(command, capture_output=True, text=True, check=True)
        output = process.stdout.strip()
        
        json_start = output.find('{')
        json_data = output[json_start:] if json_start != -1 else '{}'
        response = json.loads(json_data)
        
        result['response'] = response
        result['changed'] = True
    except subprocess.CalledProcessError as e:
        module.fail_json(msg=f"Duo API call failed: {e.stderr}", **result)
    except json.JSONDecodeError:
        module.fail_json(msg=f"Failed to parse Duo API response: {output}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
