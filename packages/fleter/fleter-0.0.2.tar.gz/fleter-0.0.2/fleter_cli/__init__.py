import argparse


def cli():
    parser = argparse.ArgumentParser(description='Fleter CLI')
    subparsers = parser.add_subparsers(metavar='Command')

    open_demo = subparsers.add_parser('demo', help='打开示例')
    open_demo.set_defaults(handle=demo)

    # 解析命令
    args = parser.parse_args()
    # 1.第一个命令会解析成handle，使用args.handle()就能够调用
    if hasattr(args, 'handle'):
        args.handle(args)
    # 2.如果没有handle属性，则表示未输入子命令，则打印帮助信息
    else:
        parser.print_help()


def demo(args):
    from os import system
    system("fleter-demo")


if __name__ == '__main__':
    cli()
