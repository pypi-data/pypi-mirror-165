import json
import os
import pytest
from common.common.constant import Constant

from common.autotest.handle_allure import convert_severity
from common.config.config import LOG_PATH_FILE, TEST_PATH, TEST_TARGET_RESULTS_PATH, TEST_TARGET_REPORT_PATH
from loguru import logger
from common.data.handle_common import get_system_key
from common.file.handle_system import del_file


class PytestPlugin(object):

    @classmethod
    def pytest_run_case(cls, _deleteResult:bool= True):
        """
        运行自动化用例
        :return:
        """
        logger.add(LOG_PATH_FILE, enqueue=True, encoding='utf-8')
        TEST_CASE_PATH = cls._convert_case_path(get_system_key(Constant.TEST_CASE_PATH))
        if _deleteResult:
            del_file(TEST_TARGET_RESULTS_PATH)
        if get_system_key(Constant.TEST_CASE_MARK) is None or get_system_key(Constant.TEST_CASE_MARK).strip() == '':
            TEST_CASE_PATH_ARR = TEST_CASE_PATH.split(',')
            for case_path in TEST_CASE_PATH_ARR:
                logger.info("开始执行脚本的路径:" + case_path)
                pytest.main(
                    args=[case_path, f'--alluredir={TEST_TARGET_RESULTS_PATH}'])
                logger.info("执行脚本成功:" + case_path)
        else:
            TEST_CASE_MARK = convert_severity(get_system_key(Constant.TEST_CASE_MARK))
            logger.info("执行用例的优先级:" + TEST_CASE_MARK)
            pytest.main(
                args=[TEST_CASE_PATH, '--alluredir', f'{TEST_TARGET_RESULTS_PATH}', '--allure-severities', f'{TEST_CASE_MARK}'])

    @classmethod
    def allure_report(cls):
        """
        生成测试报告
        :return:
        """

        if get_system_key(Constant.ALLURE_PATH) is not None:
            ALLURE_PATH = get_system_key(Constant.ALLURE_PATH)
        else:
            ALLURE_PATH = ''
        if get_system_key(Constant.RUN_TYPE) is None or get_system_key(Constant.RUN_TYPE) != 'jenkins' or get_system_key(Constant.RUN_TYPE) == '':
            os.system(f'{ALLURE_PATH}allure generate {TEST_TARGET_RESULTS_PATH} -o {TEST_TARGET_REPORT_PATH} --clean')
            logger.success('Allure测试报告已生成')


    @classmethod
    def change_allure_title(cls,report_html_path: str = TEST_TARGET_REPORT_PATH):
        """
        修改Allure标题
        :param name: 
        :param report_html_path: 
        :return: 
        """
        dict = {}
        # 定义为只读模型，并定义名称为f
        with open(f'{report_html_path}/widgets/summary.json', 'rb') as f:
            # 加载json文件中的内容给params
            params = json.load(f)
            # 修改内容
            params['reportName'] = get_system_key("JOB_NAME")
            # 将修改后的内容保存在dict中
            dict = params
            logger.info("修改测试报告名称："+get_system_key(Constant.PROJECT_NAME))
            with open(f'{report_html_path}/widgets/summary.json', 'w', encoding="utf-8") as r:
                # 将dict写入名称为r的文件中
                json.dump(dict, r, ensure_ascii=False, indent=4)

            # 关闭json读模式
            f.close()
            logger.info("修改测试报告完成")

    @classmethod
    def _convert_case_path(cls,_str):
        _path=''
        if _str is None or _str.strip()=='':
            _path = os.path.join(TEST_PATH, 'test_single')+','+os.path.join(TEST_PATH, 'test_scene')
        else:
            _arr = _str.split(',')
            for _temp in _arr:
                _path = _path+os.path.join(TEST_PATH, _temp)+","
            _path = _path[0:len(_path)-1]
        return _path




if __name__ == '__main__':
    print(PytestPlugin._convert_case_path('test_scene/test_upgrade/test_WebRT_upgrade_Direct_Cny_integral_Vip_one.py,test_scene/test_upgrade/test_WebRT_upgrade_Direct_Cny_integral_Vip_one2.py'))