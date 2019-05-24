#coding:utf-8
import watchdog
from watchdog.observers import Observer
from watchdog.events import *
import time
import threading
from folder_api.dbinfo import get_folder_first_chiice
from monitor_file.th_watchdog import thr_watchdog_folder


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
    #重命名
    def on_moved(self, event):
        if event.is_directory:
            thr_watchdog_folder('moved',event.src_path,event.dest_path)
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
    #删除
    def on_deleted(self, event):
        thr_watchdog_folder('deleted', event.src_path, '1')
        print("directory deleted:{0}".format(event.src_path))
    def on_created(self, event):
        if event.is_directory:
            thr_watchdog_folder('created', event.src_path, '2')
            print("directory created:{0}".format(event.src_path))


# if __name__ == "__main__":
class watchdog_start(threading.Thread):
    def __init__(self,monitor):
        self.monitor=monitor
        threading.Thread.__init__(self)  # 异步调用
    def run(self):
        try:
            observer = Observer()
            if self.monitor=="monitor":
                event_handler = FileEventHandler()
                get_folder_first_chiices = get_folder_first_chiice()
                for i in get_folder_first_chiices:
                    if i['watchdog'] == 1:
                        observer.schedule(event_handler, i['folder_path'], True)
                observer.start()
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    observer.stop()
                observer.join()
            else:
                observer.stop()
                observer.join()
            return True
        except Exception as e:
            print(e)
            return False


def thr_watchdog_start(monitor):
        watch_Exc = watchdog_start(monitor)
        watch_Exc.start()


