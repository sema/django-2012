from mosaic_backend.worker import Worker
from mosaic_backend.git.gitmanager import GitManager
class GitWorker(object):
    if __name__ == "__main__":
        Worker("http://localhost:8000", GitManager("/home/esbena/tmp/repositories")).run()
