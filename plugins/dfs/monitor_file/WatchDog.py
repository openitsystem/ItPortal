# from watchdog.observers import Observer
# from watchdog.events import *
# import time
# from datetime import datetime
#
#
# from monitor_file.dbinfo import *
# from monitor_file.folderapi import *
#
#
# class FileEventHandler(FileSystemEventHandler):
#     def __init__(self):
#         FileSystemEventHandler.__init__(self)
#
# # 修改
#     def on_moved(self, event):
#         if event.is_directory:
#             print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
#             createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             appname = 'DFS'
#             oprationname = '修改目录'
#             opsdetail = 'directory moved from {0} to {1}'.format(event.src_path, event.dest_path)
#             opsdetail = opsdetail.replace('\\', '\\\\')
#             createdirectorylog(createtime, appname, oprationname, opsdetail)
#         else:
#             print("file moved from {0} to {1}".format(event.src_path,event.dest_path))
#             createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             appname = 'DFS'
#             oprationname = '修改文件'
#             opsdetail = 'directory moved from {0} to {1}'.format(event.src_path, event.dest_path)
#             opsdetail = opsdetail.replace('\\', '\\\\')
#             createfilelog(createtime, appname, oprationname, opsdetail)
#
# # 创建
#     def on_created(self, event):
#         if event.is_directory:
#             print("directory created:{0}".format(event.src_path))
#             createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             appname = 'DFS'
#             oprationname = '创建目录'
#             opsdetail = 'directory created:{0}'.format(event.src_path)
#             opsdetail = opsdetail.replace('\\', '\\\\')
#             createdirectorylog(createtime, appname, oprationname, opsdetail)
#         else:
#             print("file created:{0}".format(event.src_path))
#             createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             appname = 'DFS'
#             oprationname = '创建文件'
#             opsdetail = 'directory created:{0}'.format(event.src_path)
#             opsdetail = opsdetail.replace('\\', '\\\\')
#             createfilelog(createtime, appname, oprationname, opsdetail)
#
# # 删除
#     def on_deleted(self, event):
#         if event.is_directory:
#             print("directory deleted:{0}".format(event.src_path))
#             createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             appname = 'DFS'
#             oprationname = '删除目录'
#             opsdetail = 'directory created:{0}'.format(event.src_path)
#             opsdetail = opsdetail.replace('\\', '\\\\')
#             createdirectorylog(createtime, appname, oprationname, opsdetail)
#
#         else:
#             print("file deleted:{0}".format(event.src_path))
#             createtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             appname = 'DFS'
#             oprationname = '删除文件'
#             opsdetail = 'directory created:{0}'.format(event.src_path)
#             opsdetail = opsdetail.replace('\\', '\\\\')
#             createfilelog(createtime, appname, oprationname, opsdetail)
#
# # 打开
#     def on_modified(self, event):
#         if event.is_directory:
#             print("directory modified:{0}".format(event.src_path))
#         else:
#             print("file modified:{0}".format(event.src_path))
#
# if __name__ == "__main__":
#     observer = Observer()
#     event_handler = FileEventHandler()
#     observer.schedule(event_handler,"Z:\\02.研发中心",True)
#     observer.start()
#     # observer1 = Observer()
#     # observer1.schedule(event_handler, "Y:\\01.2财务中心", True)
#     # observer1.start()
#     # observer1.join()
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()