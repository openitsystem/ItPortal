import json

from django.http import HttpResponse
from datetime import datetime

from Thr.Ther import flow_agree
from adapi.ad_api import adapi
from adapi.dbinfo import showid, updatepumailuser_allow, updatepumailuser
from dfs.dbinfo import directorapproval, relationapprovaldb, operate, sel_folder_dfs_flow_id
from dfs.thr_re_sucapproval import thr_all_process_sucapproval
from logmanager.views import logmanager


def approvalapi (request):
    try:
        id = request.POST.get("id") #审批ID
        types = request.POST.get("types") #类型 (DFS 或者非DFS)
        status = request.POST.get("status")  #审批意见（1：同意，0：不同意）
        if id == None or types == None or status == None:
            isSuccess = False
            message = "参数不完整"
        else:
            log = logmanager()
            if types == "DFS":
                # DFS审批同意方法
                if status ==1 or status == "1":
                    thr_all_process_sucapproval(id)
                # DFS 主管审批不同意方法
                else:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    approvalresult = directorapproval('0', now, '4', id)
            else:
                if status == 1 or status == "1":
                    folowvalue = showid(id)[0]
                    if folowvalue['flowstatus'] == 0:
                        updatepumailuser(id, 0)
                        flow_agree(folowvalue)
                else:
                    updatepumailuser_allow(id, 3)
            if status == 1 or status == "1":
                log.log(returnid=1, username="外部审批接口", message="同意申请单ID" + str(id)+"，类型"+ str(types), issuccess=1,
                        methodname="approvalapi", types="other")
            else:
                log.log(returnid=1, username="外部审批接口",message="拒绝申请单ID" + str(id)+"，类型"+ str(types), issuccess=1,
                methodname="approvalapi", types="other")
            isSuccess = True
            message = "审批意见已提交"
    except Exception as e:
        isSuccess = False
        message = str(e)
    result = {"isSuccess": isSuccess, "message": message}
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(json.dumps(result))
    return response
