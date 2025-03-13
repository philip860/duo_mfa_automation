# Ansible Collection - philip860.duo_mfa

## Overview
This Ansible collection provides a custom module, `duo_mfa`, which allows managing Duo Security Multi-Factor Authentication (MFA) actions such as enrolling, bypassing, and deleting users.

## Requirements

Before using this module, ensure you have the following installed on your Ansible control node:

- **Python 3** (Required for running the module)
- **Duo Security Python SDK (`duo_client`)**
  
  Install it using:
  ```bash
  pip install duo_client
  ```

## Module: `duo_mfa.tools`

### Description
This module enables interaction with the Duo Security API to:
- Enroll a user into Duo Security.
- Set a user’s status to "bypass."
- Delete a user from Duo Security.

This module is useful for automating user management within Duo Security when integrating with Ansible playbooks.

### Parameters

| Parameter  | Required | Type | Description |
|------------|----------|------|-------------|
| `username` | Yes | String | The username of the user to manage in Duo Security. |
| `host` | Yes | String | The Duo API hostname (e.g., `api-XXXXXXXX.duosecurity.com`). |
| `ikey` | Yes | String | Duo API integration key (Stored securely and should not be hardcoded). |
| `skey` | Yes | String | Duo API secret key (Stored securely and should not be hardcoded). |
| `action` | No | String | The action to perform (`enroll`, `bypass`, `delete`). Defaults to `enroll`. |

### Usage

This module can be used within an Ansible playbook to perform actions on Duo Security users. The playbook should reference the `philip860.duo_mfa` collection and call the `duo_mfa.tools` module.

### Example Playbooks

#### 1. Enroll a User in Duo Security
This playbook enrolls a user in Duo Security. The `ikey` and `skey` values should be securely stored using Ansible Vault or environment variables.
```yaml
- name: Enroll User in Duo
  hosts: localhost
  tasks:
    - name: Enroll User To DUO
      philip860.duo_mfa.tools:
        username: "kdalphas"
        host: "api-XXXXXXXX.duosecurity.com"
        ikey: "{{ ikey_password_var }}"
        skey: "{{ skey_password_var }}"
        action: "enroll"
```

#### 2. Bypass MFA for a User
This playbook sets the Duo user’s status to `bypass`, which allows them to authenticate without completing MFA.
```yaml
- name: Bypass User in Duo
  hosts: localhost
  tasks:
    - name: Bypass User To DUO
      philip860.duo_mfa.tools:
        username: "kdalphas"
        host: "api-XXXXXXXX.duosecurity.com"
        ikey: "{{ ikey_password_var }}"
        skey: "{{ skey_password_var }}"
        action: "bypass"
```

#### 3. Delete a User from Duo Security
This playbook deletes a user from Duo Security, removing them completely from the system.
```yaml
- name: Delete User from Duo
  hosts: localhost
  tasks:
    - name: Delete User In DUO
      philip860.duo_mfa.tools:
        username: "kdalphas"
        host: "api-XXXXXXXX.duosecurity.com"
        ikey: "{{ ikey_password_var }}"
        skey: "{{ skey_password_var }}"
        action: "delete"
```

### Installation

To use this collection, install it using Ansible Galaxy:
```bash
ansible-galaxy collection install philip860.duo_mfa
```

Then, include the module in your playbooks using the `philip860.duo_mfa.tools` namespace.

### Additional Notes
- Ensure that your Duo Security account has API access enabled and that the `ikey` and `skey` credentials are properly configured.
- Use Ansible Vault to securely store API keys instead of hardcoding them in playbooks.
- The `duo_client` Python module must be installed on the Ansible control node for this module to function correctly.
- When deleting a user, be cautious as this action is irreversible.

### License
This collection is licensed under the MIT License.

### Author
**Philip860** (@philipduncan860@gmail.com)
