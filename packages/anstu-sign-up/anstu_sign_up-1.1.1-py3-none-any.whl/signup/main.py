import shutil
import sys
from pathlib import Path

import requests
import requests.cookies

import signup._config as _config
import signup.login as login
import signup.temperature as temperature
import signup.info as info
import signup.utils as utils


def run(config):
    sess = requests.Session()
    sess.headers = utils.default_header()

    login.main(sess, config)

    sess.headers["Referer"] = utils.Url.CHOOSE_SYS
    temperature.main(sess)

    info.main(sess, config)
    sess.close()


def sign_all(configs):
    for cfg in configs:
        print(f"--------------User: {cfg['Common']['txtUid']}----------------")
        run(cfg)


def sign_user(ident: str, cfgs_path: Path | str):
    # 身份标识只能为学号，且如需使用定向填报则配置文件名应为 {身份标识符}.ini
    for cfg in cfgs_path.glob("*.ini"):
        if ident == cfg.stem:
            run(_config.read_cfg(cfg))
            return

    raise FileNotFoundError(f"cannot find config file for user {ident}")


def main(tgt: str = None, cfgs_path: Path | str = None):
    orig_cfgs_path = Path(__file__).parent.parent.joinpath("./conf")
    if cfgs_path is None:
        path = orig_cfgs_path
    else:
        path = Path(cfgs_path)

    if not path.is_dir():
        shutil.copytree(orig_cfgs_path, path.parent)

    try:
        cfgs = _config.config(path)
    except FileNotFoundError:
        print(f"no valid configure file found in path {path}")

        # review: b5a27eb4
        # pyinstaller在打包时不会import内置的site module(可能使用了自己的)，故在builtins里找不到exit符号
        sys.exit(1)
    else:
        if tgt is not None:
            sign_user(tgt, path)
        else:
            sign_all(cfgs)


if __name__ == '__main__':
    main()
