from urllib import response
from fastapi import FastAPI, Header, Response, status, HTTPException
import requests

# direct import so we can override in tests later
import settings

app = FastAPI()

"""
demo: User Details.

Access control is managed by the OBLV proxy.
The user name and role of the requester is 
appended to the headers:
    X-OBLV-USER-NAME
    X-OBLV-USER-ROLE
"""
@app.get("/hello")
def get_hello(
    x_oblv_user_name: str = Header(default=None),
    x_oblv_user_role: str = Header(default=None)
):
    return f"hello {x_oblv_user_name}, your role is {x_oblv_user_role}"

"""
demo: Runtime Args

We will create a handle to return the
settings to users who query for it to 
demonstrate it's usage.

The runtime args are in `/usr/runtime.yaml`,
but we'll load them as Pydantic BaseSetting.
"""
@app.get("/settings")
def get_settings():
    return settings.get_settings()

"""
demo: Outbound Calls

We'll create a handle to let users test
outbound calls with different IP adresses
and urls. These will timeout due to not
matching a FQDN on the allow list.
"""
@app.get("/call")
def get_call(
    url: str,
    response: Response
):
    try:
        # adding timeout condition if DNS not found
        r = requests.get(url, allow_redirects=True, timeout=10)
        response.status_code = r.status_code
        return {
            "status": r.status_code,
            "content": r.content
        }
    except Exception as e:
        response.status_code = status.HTTP_408_REQUEST_TIMEOUT
        return str(e)


#
# Simple MPC Application (Yao' Millionaire Problem)
#

YAO_UPLOADED = {}

# first path lets users upload their value
@app.get("/submit_value")
def get_submit_value(
    value: int,
    x_oblv_user_name: str = Header(default=None)
):
    if x_oblv_user_name is None:
        raise HTTPException(401, "No X-OBLV-USER-NAME provided.")

    if x_oblv_user_name in YAO_UPLOADED.keys():
        raise HTTPException(401, f"Path only available for one time use. Value already uploaded by {x_oblv_user_name}.")

    YAO_UPLOADED[x_oblv_user_name] = value

    return f"Successfully saved {value} as value for {x_oblv_user_name}"


# once both have uploaded their respective values
# a comparison can be made
@app.get("/compare")
def compare(
    x_oblv_user_name: str = Header(default=None)
):
    if x_oblv_user_name is None:
        raise HTTPException(401, "No X-OBLV-USER-NAME provided.")

    if len(YAO_UPLOADED) != 2:
        raise HTTPException(401, "Path only available when both parties have uploaded their value.")

    # sort to always be alphabetical
    user_names = list(YAO_UPLOADED.keys())
    user_names.sort()

    result="<"
    if YAO_UPLOADED[user_names[0]] >= YAO_UPLOADED[user_names[1]]:
        result = ">="

    return f"{user_names[0]} {result} {user_names[1]}"
