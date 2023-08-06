import os
from sys import argv
import requests
import zipfile
import subprocess
import pipreqs
import shutil
import ipynbname
from google.colab import drive

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
  drive.mount('/content/drive')
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
  
  pipes2 = subprocess.Popen(['pipreqs','--force', '--ignore', './drive,./train', './'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes2.communicate()
  
  pipes3 = subprocess.Popen(['sed','-i', '/aifactory/d', './requirements.txt'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes3.communicate()

  # pipes3 = subprocess.Popen(['sed','-i', '/tensorflow/d', './requirements.txt'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  # std_out, std_err = pipes3.communicate()

  filename = os.path.splitext(ipynb_name)[0]
  pipes4 = subprocess.Popen(['sed','-i', 's/main()/#main()/g', './' + filename + '.py'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes4.communicate()

  pipes4 = subprocess.Popen(['sed','-i', 's/def #main()/def main()/g', './' + filename + '.py'], cwd=current_cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
  std_out, std_err = pipes4.communicate()

  zip_file = zipfile.ZipFile("./aif.zip", "w")  # "w": write 모드
  for (path, dir, files) in os.walk("./"):
    for file in files:        
      if "train" not in path and "drive" not in path and "aif.zip" not in file:
        zip_file.write(os.path.join(path, file), compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()

  filename = filename + '.py'
  values = {"key": key, "modelname": filename}
  res = requests.post(api_url_test, files = {'file': open("./aif.zip",'rb', )}, data=values)  
  if res.status_code == 200 or res.status_code == 201: 
    print("success")
    return
  print(res.status_code)  
  print(res.text)