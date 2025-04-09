import os
import shutil
import pytest
from config.config import Config

if __name__ == '__main__':
    if not os.path.exists(Config.report_path):
        os.makedirs(Config.report_path)

    # 运行pytest并生成报告
    pytest.main([f'--alluredir={Config.allure_results}', '--clean-alluredir'])
    # 在测试开始运行，执行了--clean-alluredir的命令行参数后，再将environment.properties文件复制到allure-results目录下
    env_path = os.path.join(Config.allure_results, 'environment.properties')
    shutil.copy("environment.properties", env_path)
    os.system(f"allure generate {Config.allure_results} -o {Config.allure_reports} --clean")
