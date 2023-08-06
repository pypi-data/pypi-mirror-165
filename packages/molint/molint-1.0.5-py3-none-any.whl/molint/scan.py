import os
import subprocess
import shutil
import argparse

create_init_path = []


def set_init(code_hash_path):
    """
        创建init文件
    """
    for file in os.listdir(code_hash_path):
        if not file.startswith('.'):
            file_path = os.path.join(code_hash_path, file)
            if os.path.isdir(file_path):
                init = os.path.join(file_path, "__init__.py")
                if not os.path.exists(init):
                    create_init_path.append(init)
                    with open(init, "a") as file:
                        file.write("")
                set_init(file_path)
    root_init = os.path.join(code_hash_path, "__init__.py")
    if not os.path.exists(root_init):
        create_init_path.append(root_init)
        with open(root_init, "a") as file:
            file.write("")


def create_rcfile(code_path):
    rc_path = os.path.join(code_path, '.pylintrc')
    if not os.path.exists(rc_path):
        shutil.copy(os.path.join(os.path.dirname(__file__), '.pylintrc'), rc_path)
        create_init_path.append(rc_path)


def delete_init():
    """
        删除创建的init文件
    """
    while True:
        if len(create_init_path) == 0:
            break
        work_path = create_init_path.pop()
        if os.path.exists(work_path):
            os.remove(work_path)


def pylint_scan(code_path, lint_rule='', disable=''):
    """
        pylint 扫描后端代码

        :param code_path: 扫描路径
        :param lint_rule: 过滤目录
        :param disable: 过滤条件

    """
    # 处理没有__init__.py 文件时，不扫描目录的问题
    # os.chdir(code_path)
    if code_path in ['./', '.', '/']:
        code_path = os.getcwd()
    set_init(code_path)
    create_rcfile(code_path)
    rc_ptah = os.path.join(code_path, '.pylintrc')
    args = [f'--rcfile={rc_ptah}']
    if lint_rule.strip('"').strip("'"):
        args.append(f'--ignore={lint_rule}')
    if disable.strip('"').strip("'"):
        args.append(f'--disable={disable}')
    cmd = f"pylint {code_path} {' '.join(args)}"
    print(cmd)
    subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for i in iter(subp.stdout.readline, ''):
        if len(i) < 1:
            break
        print(i.strip('\n'))
    delete_init()


def main():
    try:
        parser = argparse.ArgumentParser(prog='python code scan')
        parser.add_argument('code_path', nargs='?', default='./', help='代码路径')
        parser.add_argument('lint_rule', nargs='?', default='', help='过滤目录')
        parser.add_argument('dis', nargs='?', default='', help='过滤条件')
        args = parser.parse_args()
        pylint_scan(args.code_path, args.lint_rule, args.dis)
    except KeyboardInterrupt:
        delete_init()
