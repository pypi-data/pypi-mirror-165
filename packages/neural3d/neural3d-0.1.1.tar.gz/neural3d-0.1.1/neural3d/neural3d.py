import requests
import base64
brr = lambda text, out_file="result.obj", api_link="https://46158.gradio.app/api/predict": open(out_file, "wb").write(base64.b64decode(requests.post(api_link, json={"data": [text]}).json()["data"][0]["data"].partition(",")[-1]))
