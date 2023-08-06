import os
from sys import argv
import requests
import zipfile
import subprocess
import pipreqs
import shutil
from google.colab import drive
drive.mount('/content/drive')

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

def submit_test_colab(key, ipynb_name, func):
  values = {"key": key}

  current_cwd = os.getcwd()

  ipynb_file = '/content/drive/MyDrive/Colab Notebooks/' + ipynb_name
  # pipes1 = subprocess.Popen(['!cp',ipynb_file, './'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  # std_out, std_err = pipes1.communicate()
  source=r'/content/drive/MyDrive/Colab Notebooks/' + ipynb_name
  destination=r'./' + ipynb_name
  shutil.copyfile(source, destination)

  pipes1 = subprocess.Popen(['jupyter','nbconvert', '--to','python', ipynb_name], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes1.communicate()
  
  drive.flush_and_unmount()
  
  pipes = subprocess.Popen(['pipreqs','--ignore', './drive,', '/train', './'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes.communicate()

  zip_file = zipfile.ZipFile("./submit.zip", "w")  # "w": write 모드
  for (path, dir, files) in os.walk("./"):
    for file in files:        
      if "train" not in path and "drive" not in path and "submit.zip" not in file:
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()