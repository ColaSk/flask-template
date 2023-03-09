import os

import click
from flask.cli import with_appcontext

from configs.sysconf import PROJECT_PATH
from flask import Flask


def txt_line_iterator(filepath: str):
    """txt 行迭代器"""
    with open(filepath, 'r', encoding='utf=8') as file:
        while True:
            line = file.readline()
            if not line:
                break
            # 去除末尾换行符
            line = line.strip('\n')
            yield line


def init_command(app: Flask):

    @app.cli.command("init", help="init a project")
    @click.pass_context
    def init(ctx):
        """
        创建一个Flask项目~
        """
        if ".git" in os.listdir(PROJECT_PATH):
            click.echo("看上去你的项目已经初始化过了, 删除.git文件继续")
            return

        project_name = click.prompt('即将创建一个APP, 请输入名字(默认使用文件夹名称)', default="")
        if not project_name:
            project_name = PROJECT_PATH.split("/")[-1].lower()

        with open(os.path.join(PROJECT_PATH, "app/configs/base.py"), "w") as f:
            f.write(f"PROJECT_NAME ='{project_name}'")

        ctx.forward(gen_secret_key)

        # init git
        os.system(f"git init {PROJECT_PATH}")
        with open(os.path.join(PROJECT_PATH, '.gitignore'), 'a') as f:
            f.write('\n#template file\n.template/\n')

    @app.cli.command("gen_secret_key", help="gen a secret key for flask in base.py")
    @click.option('--force', '-f', type=bool, default=False)
    def gen_secret_key(force):
        with open(os.path.join(PROJECT_PATH, "app/configs/base.py"), "r+") as f:
            content = f.read()
            if "SECRET_KEY" in content:
                if not force:
                    click.echo("SECRET_KEY is set, skipping...")
                    return

            f.write(f"\nSECRET_KEY = {os.urandom(24)}\n")

    @app.cli.command("app_name", help="print a app name so that you know it's name")
    def print_app_name():
        click.echo(f"{app.name}")

    @app.cli.command("create_db", help="create a database if not exists")
    @click.option("--drop", help="是否需要删除当前数据库", type=bool, default=False)
    def create_db(drop: bool):
        from pymysql import connect

        from configs.sysconf import (MYSQL_CHARSET, MYSQL_DATABASE, MYSQL_HOST, MYSQL_PASSWD, MYSQL_PORT, MYSQL_USER)
        with connect(user=MYSQL_USER, password=MYSQL_PASSWD,
                     host=MYSQL_HOST, port=MYSQL_PORT, charset=MYSQL_CHARSET) as conn:
            with conn.cursor() as cr:
                conn.begin()
                if drop:
                    res = click.prompt(f"正在删除数据库{MYSQL_DATABASE}是否继续..., y确定", confirmation_prompt=True)
                    if res.lower() != "y":
                        click.echo("ABORT!")
                        return
                    click.echo(f"DROPPING DATABASE {MYSQL_DATABASE}")
                    cr.execute(f"DROP DATABASE {MYSQL_DATABASE}")
                    click.echo(f"{MYSQL_DATABASE} DROPPED")

                click.echo("CREATING DATABASE")
                cr.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHAR SET {MYSQL_CHARSET}")
                conn.commit()
                click.echo("DATABASE CREATED!")

    @app.cli.command("drop_all", help="drop all tables, very! dangerous!")
    @with_appcontext
    def drop_all():
        res = click.prompt("drop table is very dangerous continue?.. y to continue", confirmation_prompt=True)
        if res.upper() != "Y":
            click.echo("abort!")
            return
        from initialization.sqlalchemy_process import db
        click.echo("by you command!")
        db.drop_all()
        return

    @app.cli.command("create_resource",
                     help="""
    create Entity, Model Service and Schema for you!

    example:

        flask create_resource -n config

        flask create_resource -n config -p v1 -s
    """)
    @click.option("--name", "-n", "name", help="需要生成的模块名称，使用小写字母和下划线来链接", required=True)
    @click.option(
        "--prefix",
        "-p",
        "prefix",
        help="前缀，如果写了该值会在resource下创建代表版本的文件夹，如，v1/ v2/ v3/, 如果指定了 prefix 则不会创建 blueprint，而会从上层目录中导入名字为 $prefix 的蓝图对象",
    )
    @click.option("--spec",
                  "-s",
                  "spec",
                  help="是否生成 spec 装饰器，如果需要的话则会在 resource.view 中生成 @bp.doc 等装饰器, 默认为False",
                  is_flag=True,
                  type=click.BOOL)
    def create_bp(name, prefix=None, spec=False):
        from pathlib import Path

        from jinja2 import Template

        from configs.sysconf import PROJECT_PATH
        context = dict(
            bp_name=name,
            bp_classname="".join([word.capitalize() for word in name.split("_")]),
            prefix=prefix,
            need_spec=spec,
        )
        project_path = Path(PROJECT_PATH)

        template_path = project_path / '.template'

        if not template_path.exists():
            click.echo("没有发现 .template 文件夹，请重新下载本模板然后拷贝 .template 文件夹到目录")
            click.Abort()

        # resource
        resource_path = project_path / "app" / "resources"

        bp_dir = (resource_path / prefix / name) if prefix else (resource_path / name)

        try:
            bp_dir.mkdir()
        except OSError:
            click.echo(f"resource {name} has exists, abort")
            click.Abort()

        resource_template = template_path / 'resource'

        for file in resource_template.iterdir():
            source = open(file).read()
            t = Template(source)
            with (bp_dir / file.name.replace(".jinja2", "")).open("w") as f:
                f.write(t.render(**context))

        def make_file(module_dir, module_name):
            dir_path = Path(PROJECT_PATH) / "app" / module_dir
            template = template_path / f"{module_name}.py.jinja2"
            with (dir_path / f"{name}_{module_name}.py").open("w") as f:
                t = Template(template.read_text())
                f.write(t.render(**context))

        # entity
        make_file("entities", "entity")

        # model
        make_file("models", "model")

        # service
        make_file("services", "service")

        # schema
        make_file("schemas", "schema")
