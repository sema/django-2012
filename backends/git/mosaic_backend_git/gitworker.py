from gitmanager import GitManager
from mosaic_backend.worker import Worker
import sys
import logging

logging.basicConfig()
logging.root.setLevel(logging.DEBUG)

def run(mosaic_url, repository_dir, api_key):
    Worker(mosaic_url, GitManager(repository_dir), api_key).run()

if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2], sys.argv[3])

