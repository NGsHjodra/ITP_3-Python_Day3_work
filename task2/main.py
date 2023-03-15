import os
from PIL import Image
import time
import threading
import multiprocessing

directory = os.getcwd()

def clean_folders():
    for filename in os.listdir('thread/'):
        os.remove(os.path.join('thread/', filename))
    for filename in os.listdir('multiprocess'):
        os.remove(os.path.join('multiprocess/', filename))

def resize_image(filename, destination):
    with Image.open(filename) as img:
        width, height = img.size
        resized_img = img.resize((width // 2, height // 2))

        new_filename = os.path.splitext(filename)[0] + "_resized.jpeg"

        resized_img.save(os.path.join(destination, new_filename), "jpeg", quality=50)

def resize_images_thread():
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg"):
            files.append(filename)
    
    cpu_count = threading.active_count()

    threads = []

    for i in range(cpu_count):
        for j in range(i, len(files), cpu_count):
            thread = threading.Thread(target=resize_image, args=(files[j], 'thread/'))
            thread.start()
            threads.append(thread)

    for thread in threads:
        thread.join()

def resize_images_multiprocess():
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cores)

    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg"):
            files.append(filename)
    
    pool.starmap(resize_image, [(filename, 'multiprocess/') for filename in files])

if __name__ == "__main__":
    clean_folders()

    start = time.time()
    resize_images_thread()
    end = time.time()
    print("Time taken for thread: ", end - start)

    start = time.time()
    resize_images_multiprocess()
    end = time.time()
    print("Time taken for multiprocess: ", end - start)

# for 27 images
# Time taken for thread:  0.31544947624206543
# Time taken for multiprocess:  0.5934062004089355

# In this case, multiprocess is slower than thread
# maybe because of the overhead of creating processes
# or threading is faster than multiprocessing in I/O bound tasks
