import multiprocessing

def get_default_workers():
    try:
        default_workers = multiprocessing.cpu_count() or 1
    except NotImplementedError:
        default_workers = 1
    return default_workers