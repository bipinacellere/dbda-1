'''
download_repos.py
Downloads all the repositories listed in repo_names.csv
'''

import os
import csv
from tqdm import tqdm
import shutil
import psutil
from joblib import Parallel, delayed

def get_free_space():
    hdd = psutil.disk_usage('/')
    return hdd.free / (2**30)

def procced_or_break(free_space):
    if free_space > 10.0:
        return True
    else:
        return False

OUTPUT_PATH = 'output/'

def download_repo(repo):
    file_name = repo.split("/")[-1]
    if file_name not in os.listdir("output/"):
        if procced_or_break(get_free_space()):
            os.system('git clone --quiet --depth 1 --single-branch https://github.com/' + repo + ' ' + 'output' + '/' + file_name)
            for root, dirs, files in os.walk(OUTPUT_PATH + file_name):
                for file in files:
                    if file.endswith(".js"):
                        pass
                    else:
                        os.remove(os.path.join(root, file))
        else:
            print("Disk almost Full, breaking.")
            print("Free Space Left: " + str(get_free_space()))
            sys.exit()
    else:
        print("Already downloaded: " + repo)

with open('github_repositories.csv', 'r') as f:
    csv_reader = csv.reader(f)
    repositories = list(map(tuple, csv_reader))

if 'output' not in os.listdir():
    os.makedirs('output')

repo_names = [repo[0] for repo in repositories]
Parallel(n_jobs=80, prefer="threads")(
    delayed(download_repo)(name) for name in tqdm(repo_names))

print("changes")
