from pathlib import Path
import asyncio
import contextlib
import itertools
import logging.config
import subprocess
import sys
import tempfile
import typing

from hat import aio
from hat import json
import appdirs
import click

from boxhatter import common
import boxhatter.backend
import boxhatter.server
import boxhatter.ui


user_config_dir: Path = Path(appdirs.user_config_dir('boxhatter'))
user_data_dir: Path = Path(appdirs.user_data_dir('boxhatter'))
user_cache_dir: Path = Path(appdirs.user_cache_dir('boxhatter'))

default_conf_path: Path = user_config_dir / 'server.yaml'
default_db_path: Path = user_data_dir / 'server.db'
default_cache_path: Path = user_cache_dir


@click.group()
@click.option('--log-level',
              default=common.settings.log_level,
              type=click.Choice(['CRITICAL', 'ERROR', 'WARNING', 'INFO',
                                 'DEBUG', 'NOTSET']),
              help="log level (default INFO)")
@click.option('--ssh-key', metavar='PATH', type=Path,
              default=common.settings.ssh_key,
              help="private key used for ssh authentication")
@click.option('--engine',
              default=common.settings.engine,
              help="container engine (default podman)")
def main(log_level: str,
         ssh_key: typing.Optional[Path],
         engine: str):
    common.settings = common.Settings(
        log_level=log_level,
        ssh_key=(ssh_key.resolve() if ssh_key else None),
        engine=engine)

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'console': {
                'format': "[%(asctime)s %(levelname)s %(name)s] %(message)s"}},
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
                'level': log_level}},
        'root': {
            'level': log_level,
            'handlers': ['console']},
        'disable_existing_loggers': False})


@main.command()
@click.option('--action', default='.boxhatter.yaml',
              help="action file path inside repository")
@click.option('--env', multiple=True,
              help="environment variables")
@click.option('--cache-src', metavar='PATH', default=None, type=Path,
              help="path to persisted cache folder")
@click.option('--cache-dst', metavar='PATH', default='.boxhatter_cache',
              help="relative path to cache folder inside repository")
@click.argument('url', required=True)
@click.argument('ref', required=False, default='HEAD')
def execute(action: str,
            env: typing.Tuple[str],
            cache_src: typing.Optional[Path],
            cache_dst: str,
            url: str,
            ref: str):
    with contextlib.suppress(Exception):
        path = Path(url)
        if path.exists():
            url = str(path.resolve())

    with tempfile.TemporaryDirectory() as repo_dir:
        repo_dir = Path(repo_dir)

        subprocess.run(['git', 'init', '-q'],
                       cwd=str(repo_dir),
                       check=True)

        subprocess.run(['git', 'remote', 'add', 'origin', url],
                       cwd=str(repo_dir),
                       check=True)

        subprocess.run(['git', 'fetch', '-q', '--depth=1', 'origin', ref],
                       cwd=str(repo_dir),
                       check=True)

        subprocess.run(['git', 'checkout', '-q', 'FETCH_HEAD'],
                       cwd=str(repo_dir),
                       check=True)

        conf = json.decode_file(repo_dir / action)
        common.json_schema_repo.validate('boxhatter://action.yaml#', conf)

        volumes = [f'{repo_dir}:/boxhatter']
        if cache_src:
            volumes.append(f'{cache_src.resolve()}:/boxhatter/{cache_dst}')

        image = conf['image']
        command = conf['command']

        cmd = [common.settings.engine, 'run', '-i', '--rm',
               *itertools.chain.from_iterable(('-v', i) for i in volumes),
               *itertools.chain.from_iterable(('--env', i) for i in env),
               image, '/bin/sh']
        subprocess.run(cmd,
                       input=f'set -e\ncd /boxhatter\n{command}\n',
                       encoding='utf-8',
                       check=True)


@main.command()
@click.option('--host', default='0.0.0.0',
              help="listening host name (default 0.0.0.0)")
@click.option('--port', default=24000, type=int,
              help="listening TCP port (default 24000)")
@click.option('--conf', default=default_conf_path, metavar='PATH', type=Path,
              help="configuration defined by boxhatter://server.yaml# "
                   "(default $XDG_CONFIG_HOME/boxhatter/server.yaml)")
@click.option('--db', default=default_db_path, metavar='PATH', type=Path,
              help="sqlite database path "
                   "(default $XDG_DATA_HOME/boxhatter/server.db")
@click.option('--cache', default=default_cache_path, metavar='PATH', type=Path,
              help="persisted cache path (default $XDG_CACHE_HOME/boxhatter")
def server(host: str,
           port: int,
           conf: Path,
           db: Path,
           cache: Path):
    conf = json.decode_file(conf)
    common.json_schema_repo.validate('boxhatter://server.yaml#', conf)
    cache.mkdir(parents=True, exist_ok=True)

    with contextlib.suppress(asyncio.CancelledError):
        aio.run_asyncio(async_server(host, port, conf, db, cache))


async def async_server(host: str,
                       port: int,
                       conf: json.Data,
                       db_path: Path,
                       cache_path: Path):
    async_group = aio.Group()

    try:
        backend = await boxhatter.backend.create(db_path)
        _bind_resource(async_group, backend)

        server = await boxhatter.server.create(conf, cache_path, backend)
        _bind_resource(async_group, server)

        ui = await boxhatter.ui.create(host, port, server)
        _bind_resource(async_group, ui)

        await async_group.wait_closing()

    finally:
        await aio.uncancellable(async_group.async_close())


def _bind_resource(async_group, resource):
    async_group.spawn(aio.call_on_cancel, resource.async_close)
    async_group.spawn(aio.call_on_done, resource.wait_closing(),
                      async_group.close)


if __name__ == '__main__':
    sys.argv[0] = 'boxhatter'
    main()
