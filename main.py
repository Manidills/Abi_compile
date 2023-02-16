from typing import Union
import os

from fastapi import FastAPI
import json
import web3
import requests
#import nft_storage
#from nft_storage.api import nft_storage_api
from io import BytesIO
from fastapi import FastAPI, File, UploadFile
import openai
from solcx import compile_standard, install_solc
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


app = FastAPI( middleware=middleware,)




# def nft_storage_store(file_name):
#         # Defining the host is optional and defaults to https://api.nft.storage
#         # See configuration.py for a list of all supported configuration parameters.
#         configuration = nft_storage.Configuration(
#             host="https://api.nft.storage"
#         )

#         configuration = nft_storage.Configuration(
#             access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE0RkY4NTU4MzVGMDYwZDBCRTk0ZWQyOTBjNTdiODE1YTE5MjQxNUQiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY1NzU2OTU4ODQxOSwibmFtZSI6Ik1BTklESUxMUyJ9.idaK-qJVyOb8WKP1cD0yddE8UJX4zRpBKtX-QqN49fU'
#         )
#         with nft_storage.ApiClient(configuration) as api_client:
#             # Create an instance of the API class
#             api_instance = nft_storage_api.NFTStorageAPI(api_client)
          
#             body = file_name.file.read()
#             body = BytesIO(body)
#             #body = open(file_name, 'rb')  # file_type |


#             # example passing only required values which don't have defaults set
#             try:
#                 # Store a file
#                 api_response = api_instance.store(body, _check_return_type=False)
#                 return (api_response)
#             except nft_storage.ApiException as e:
#                 st.info("Exception when calling NFTStorageAPI->store: %s\n" % e)


@app.get("/")
def read_root():
    return {"Hello": "World"}
    
    
@app.get("/code")
def get_code(data:str):
    openai.api_key = os.getenv('api')
    # Get user input and use OpenAI to generate a response
    user_input = data

    if user_input:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{user_input}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text

        return(response)

@app.get("/compile")
def get_compile_code(code:str):
    openai.api_key = os.getenv('api')
    # Get user input and use OpenAI to generate a response
    user_input = code

    if user_input:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{user_input}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        ).choices[0].text
    print(response)
    data = f"""

    // SPDX-License-Identifier: GPL-3.0

    {response}

    """

    # Install Solidity compiler.
    _solc_version = "0.8.0"
    install_solc(_solc_version)

    # Compile SimpleStorage smart contract with solcx.
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"SimpleStorage.sol": {"content": data}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version=_solc_version,
    )

    # abi = json.dumps(compiled_sol['contracts']['SimpleStorage.sol']['Storage']['abi'])
    # bytecode = compiled_sol['contracts']['SimpleStorage.sol']['Storage']['evm']['bytecode']['object']

    # return({
    #     "abi": abi, "bytecode": bytecode
    # })
    return({
        "code": data.replace('\n',''),
        "compile_data": compiled_sol
    })


