import requests
import json
import base64
import pandas
import glob

url = "https://vendor.alliedfit.com/api/User/Authenticate"

payload = json.dumps({
  "user": "RNGupta",
  "password": "@llied202E"
})
headers = {
  'Content-Type': 'application/json'
}

def login_api_call():
  response = requests.request("POST", url, headers=headers, data=payload, verify=False)
  
  json_resp = json.loads(response.text)
  global token
  token = json_resp['token']

    
excel_data_df = pandas.read_excel('23-2073.xlsx', sheet_name='Template')
excel_data_df = excel_data_df.fillna('')
excel_data_df.columns = [x[0].lower() + x[1:] for x in excel_data_df.columns]
json_str = excel_data_df.to_json(orient='split')

with open(glob.glob("*.pdf")[0], "rb") as pdf_file:
  global byte_array
  byte_array = base64.b64encode(pdf_file.read())

s = ""
req_body_dict = {"linesBundles": [], "mtrsToUpload": []}
for i in excel_data_df.index:
  json_row = excel_data_df.loc[i].to_dict()
  req_body_dict["linesBundles"].append(json_row)
  req_body_dict["mtrsToUpload"].append({
    "partNumber": json_row["partNumber"],
    "manufacturerCode": json_row["manufacturerCode"],
    "heat": json_row["heat"],
    "lot": json_row["lot"],
    "test": json_row["test"],
    "heatTreatmentCode": json_row["heatTreatmentCode"],
    "fileName": glob.glob("*.pdf")[0],
    "fileContent": str(byte_array)[2: -1]
  })


  # print("----------------------------------")

json_object = json.dumps(req_body_dict, indent=4, allow_nan=False)

login_api_call()
print(token)

headers = {
  'Authorization': f'Bearer {token}',
  'Content-Type': 'application/json'
}

response = requests.request("POST", "https://vendor.alliedfit.com/api/PreReception/ImportLineBundles", headers = headers, data=json_object, verify=False)
print(response)

# Writing to sample.json
with open("sample.json", "w") as outfile:
  outfile.write(json_object)


#test

