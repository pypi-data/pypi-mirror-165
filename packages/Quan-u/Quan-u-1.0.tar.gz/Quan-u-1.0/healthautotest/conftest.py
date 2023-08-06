# coding=utf-8
# import pytest
# import subprocess
# import time
# import os
# global setupNumber
#
# from components.android.Common import Common
# from tools.LoggerUtil import LoggerUtil
# from tools.ManageAppiumServer import ManageAppiumServer
# from tools.PullAppUtil import PullAppUtil
# from tools.SendEmailUtil import SendEmailUtil
# from tools.YamlUtil import YamlUtil
# from tools import PullAppUtil as Path
#
# logger = LoggerUtil()
# logger.info('开始清除本地数据')
# YamlUtil().clearYaml(r'tools/resource/Result.yaml')
# YamlUtil().clearYaml(r'tools/resource/ReportChecklist.yaml')
# logger.info('清除本地数据完成')
# rootPath = os.path.abspath(os.path.dirname(__file__))
# logPath = os.path.join(rootPath, 'tools\\log\\')
# sn = Common().getSN()  # 获取手机sn号
# terminalModel = Common().getModelNameAndroid(sn)  # 获取手机型号


# #测试结果集
# import pytest
# import time
# results,totalCases,ok,fail,result={},0,0,0,0
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     global results,totalCases,ok,fail,result
#     out = yield
#     res = out.get_result()
#     if res.when == "call":
#         print(res.outcome,9999)
#         if str(res.outcome) == 'passed':
#             ok += 1
#
# print(ok,'haha')
    # if res.when == "call":
    #     times = int(round(time.time() * 1000))
    #     result['case'] = str(item)
    #     result['caseDescribe'] = str(item.function.__doc__)
    #     result['abnormalInfo'] = str(call.excinfo)
    #     result['log'] = str(res.longrepr)
    #     result['testResult'] = str(res.outcome)
    #     result['timeConsuming'] = str(res.duration)
    #     results[times] = result
    #     YamlUtil().writeYaml(r'tools/resource/Result.yaml', data=results)
import time
import pytest

from tools.YamlUtil import YamlUtil

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    result,results = {},{}
    out = yield
    res = out.get_result()
    if res.when == "call":
        times = int(round(time.time() * 1000))
        result['testCaseName'] = str(item)
        result['testResult'] = str(res.outcome)
        result['timeConsuming'] = str(res.duration)
        results[times] = result
        YamlUtil().writeYaml(r'tools/resource/Result.yaml', data=results)



# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     result,results = {},{}
#     out = yield
#     res = out.get_result()
#     if res.when == "call":
#         times = int(round(time.time() * 1000))
#         result['case'] = str(item)
#         result['caseDescribe'] = str(item.function.__doc__)
#         result['abnormalInfo'] = str(call.excinfo)
#         result['log'] = str(res.longrepr)
#         result['testResult'] = str(res.outcome)
#         result['timeConsuming'] = str(res.duration)
#         results[times] = result
#         YamlUtil().writeYaml(r'tools/resource/Result.yaml', data=results)


# setupNumber, teardownNumber = 0, 0
# @pytest.fixture(scope='session', autouse=True)
# def totaExecution(request):
#     import subprocess
#     import time
#     import os
#     global setupNumber
#
#     if not setupNumber:
#         # 开启appium服务
#         ManageAppiumServer.stopAppium(4723)
#         ManageAppiumServer.startAppium(4723)
#         time.sleep(5)
#         # 拉取apk
#         date, version = PullAppUtil().getAppDateAndAppVersion()
#         strs = '/work/data/WATCH/PhoneApp/Health/wsw_master/Health_Dailybuild_{}/OPlus/releaseT/{}'.format(date,
#                                                                                                            version)
#         PullAppUtil().sftpDownloadFile(strs,
#                                        Path.appPath + version)
#         # 安装apk
#         Common().installAppAndroid(sn)
#         result, results, appVersionNumber = {}, {}, []
#         now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))  # 获取当前时间
#         # 获取app版本号
#         iter = 0
#         for root, dirs, files in os.walk(r"{}\testapk".format(rootPath)):
#             iter += 1
#             appVersionNumber.append(files[0])
#         # 写入报告清单
#         result['startTime'] = str(now)
#         result['endTime'] = str(now)
#         result['totalTime'] = str(now)
#         result['terminalModel'] = str(terminalModel)
#         result['appVersionNumber'] = appVersionNumber[0]
#         result['reportAddress'] = 'http://10.114.93.138:8081/job/healthautotest/allure/'
#         result['execute'] = False
#         results['Checklist'] = result
#         YamlUtil().writeYaml(r'tools/resource/ReportChecklist.yaml', data=results)
#         # 开启手机log
#         filename = logPath + now + "_" + sn + "_logcat.txt"  # 日志文件名添加当前时间
#         logcat_file = open(filename, 'w')
#         logcmd = "adb logcat -v time"
#         logger.info('正在开启设备: {} log'.format(sn))
#         Poplog = subprocess.Popen(logcmd, stdout=logcat_file, stderr=subprocess.PIPE)
#         logger.info('成功开启设备: {} log'.format(sn))
#         setupNumber += 1
#     else:
#         pass
#
#     def fin():
#         global teardownNumber
#         if not teardownNumber:
#             logcat_file.close()
#             Poplog.terminate()
#             logger.info('成功结束设备: {} log'.format(sn))
#             # 发送邮件
#             SendEmailUtil().sendEmail()
#             print('-------------发送邮件成功------------')
#             teardownNumber += 1
#         else:
#             pass
#     request.addfinalizer(fin)

