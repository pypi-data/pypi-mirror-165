import click
import os
from core.utils import mkdirAfterCheck,mkfileAfterCheck
"""
this is test framework base on pytest and pytest-bdd
try to improve the feeling of using test framework

try to improve:
1. require user to follow the rule of this framework, enhance internal-understander in the test team
2. improve the way of parameterize 
3. using common used library to faster the script developing
4. re-org the test case, test suite, log, parameter, comander
5. union the report data and generate report
6. 

"""


@click.command()
@click.option('--name',default='kframe_proj',help='input name of the this project, default is kframe')
@click.option('--top_dir',default='.',help='input top directory of the this project, default is current directory')
def kframe_startProject(name,top_dir):
    cur_dir=os.path.abspath(top_dir)
    proj_dir=cur_dir+os.sep+name
    log_dir=proj_dir+os.sep+'logs'
    data_dir=proj_dir+os.sep+'datas'
    case_dir=proj_dir+os.sep+'cases'
    suite_dir=proj_dir+os.sep+'suites'
    report_dir=proj_dir+os.sep+'reports'
    config_dir=proj_dir+os.sep+'configs'
    mkdirAfterCheck(proj_dir)
    mkdirAfterCheck(log_dir)
    mkdirAfterCheck(data_dir)
    mkdirAfterCheck(case_dir)
    mkdirAfterCheck(suite_dir)
    mkdirAfterCheck(report_dir)
    mkdirAfterCheck(config_dir)

    print('init project done....')

@click.command()
@click.option('--name',default='test_case1',help='input name of testcase, default is test_case1')
@click.option('--top_dir',default='.',help='input top directory of the this project, default is current directory')
def kframe_createCase(name,default):
    cur_dir=os.path.abspath(top_dir)
    proj_dir=cur_dir+os.sep+name
    data_dir=proj_dir+os.sep+'datas'
    case_dir=proj_dir+os.sep+'cases'
    suite_dir=proj_dir+os.sep+'suites'
    config_dir=proj_dir+os.sep+'configs'
    mkfileAfterCheck(path)

    print('test case created....')


kframe_startProject()