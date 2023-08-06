import os
from sys import argv
import requests
import zipfile
import subprocess

api_url_test= "https://grade-bridge-test.aifactory.space/grade"
api_url = "https://grade-bridge.aifactory.space/grade"

def submit(key, submit_file_path):
  values = {"key": key}
  res = requests.post(api_url, files = {'file': open(submit_file_path,'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)

def submit_test(key, submit_file_path):
  values = {"key": key}
  res = requests.post(api_url_test, files = {'file': open(submit_file_path,'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)

def submit_test_new(key, func):
  values = {"key": key}
  os.chdir("./")
  current_cwd = os.getcwd()
  pipes = subprocess.Popen(['pipreqs','./'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes.communicate()

  zip_file = zipfile.ZipFile("./submit.zip", "w")  # "w": write 모드
  for (path, dir, files) in os.walk("./"):
    for file in files:        
      if "train" not in path:
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()