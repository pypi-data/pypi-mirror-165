import requests
import base64
brr = lambda url, out_file="result.obj": open(out_file, "wb").write(base64.b64decode(requests.post("https://46158.gradio.app/api/predict", json={"data": [x]}).json()["data"][0]["data"].partition(",")[-1]))

