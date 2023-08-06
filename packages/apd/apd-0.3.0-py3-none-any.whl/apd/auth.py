###############################################################################
# (c) Copyright 2022 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
__all__ = ("get_api_token", "wipe_token_cache")

import base64
import hashlib
import secrets
import sys
import time
import warnings

import requests

from .keyring import KeyringItem, KeyringSpec, LinuxKeyring

OIDC_BASE_URL = "https://auth.cern.ch/auth/realms/cern/protocol/openid-connect"


def get_api_token(clientid, test_url):
    """Get an OIDC token by using Device Authorization Grant.

    On Linux tokens are stored in the kernel keyring.

    :param clientid: Client ID of a public client with device authorization grant enabled.
    """
    if sys.platform == "linux":
        keyring = LinuxKeyring.persistent_keyring(KeyringSpec.PROCESS)
    else:
        if not hasattr(get_api_token, "keyring"):
            warnings.warn(
                "Unsupported platform, login will be requested every time.",
            )
            get_api_token.keyring = {}
        keyring = get_api_token.keyring

    id_token = keyring.get(f"lbap-id-{clientid}")
    if id_token:
        response = requests.get(
            test_url, headers={"Authorization": f"Bearer {id_token}"}, timeout=30
        )
        if response.ok:
            return id_token

    refresh_token = keyring.get(f"lbap-refresh-{clientid}")
    token_response = None
    if refresh_token:
        token_response = _use_refresh_token(clientid, refresh_token)
    if not token_response:
        token_response = device_authorization_login(clientid)

    keyring[f"lbap-id-{clientid}"] = token_response["access_token"]
    keyring[f"lbap-refresh-{clientid}"] = token_response["refresh_token"]

    if sys.platform == "linux":
        item = KeyringItem.from_name(keyring.keyring_id, f"lbap-id-{clientid}")
        item.set_timeout(token_response["expires_in"] - 300)
        item = KeyringItem.from_name(keyring.keyring_id, f"lbap-refresh-{clientid}")
        item.set_timeout(token_response["refresh_expires_in"] - 2 * 60 * 60)

    return keyring[f"lbap-id-{clientid}"]


def wipe_token_cache(clientid):
    """Clear the token cache for a given client ID."""
    if sys.platform == "linux":
        keyring = LinuxKeyring.persistent_keyring(KeyringSpec.PROCESS)
    else:
        keyring = getattr(get_api_token, keyring, {})
    keyring.pop(f"lbap-id-{clientid}", None)
    keyring.pop(f"lbap-refresh-{clientid}", None)


def device_authorization_login(clientid):
    """Get an OIDC token by using Device Authorization Grant.

    :param clientid: Client ID of a public client with device authorization grant enabled.
    """
    random_state = secrets.token_hex(8)
    code_verifier = secrets.token_hex(96)
    code_hash = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(code_hash).decode()

    r = requests.post(
        f"{OIDC_BASE_URL}/auth/device",
        data={
            "client_id": clientid,
            "state": random_state,
            "code_challenge_method": "S256",
            "code_challenge": code_challenge,
        },
        verify=True,
        timeout=30,
    )

    if not r.ok:
        print(r.text)
        raise Exception(
            "Authentication request failed: Device authorization response was not successful."
        )

    auth_response = r.json()

    print("CERN SINGLE SIGN-ON\n")
    print("On your tablet, phone or computer, go to:")
    print(auth_response["verification_uri"])
    print("and enter the following code:")
    print(auth_response["user_code"])
    print()
    print("You may also open the following link directly and follow the instructions:")
    print(auth_response["verification_uri_complete"])
    print()
    print("Waiting for login...")

    signed_in = False
    while not signed_in:
        time.sleep(5)
        r_token = requests.post(
            f"{OIDC_BASE_URL}/token",
            data={
                "client_id": clientid,
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": auth_response["device_code"],
                "code_verifier": code_verifier,
            },
            verify=True,
            timeout=30,
        )
        signed_in = r_token.ok

    token_response = r_token.json()
    return token_response


def _use_refresh_token(clientid, refresh_token):
    r_token = requests.post(
        f"{OIDC_BASE_URL}/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": clientid,
        },
        timeout=30,
    )
    if not r_token.ok:
        return None
    return r_token.json()
