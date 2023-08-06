#!/usr/bin/python3
# PYTHON_ARGCOMPLETE_OK

# versionator
#
# Copyright (C) 2022 Katie Rust (katie@ktpanda.org)
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import re
import time
import os
import argparse
import subprocess
import traceback
import uuid
import shutil
import argcomplete
from collections import deque
from collections.abc import Iterable
from pathlib import Path

RX_VERSION = re.compile(r'^Version (\d+\.\d+\.\d+)')
RX_VERSION_LINK = re.compile(r'^\[Version (\d+\.\d+\.\d+) \([^\)]+\)\]')

RX_VERSION_QUOTE = re.compile(r'^\s*version\s*=\s*"(\d+\.\d+\.\d+)"', re.I|re.M)
RX_VERSION_NOQUOTE = re.compile(r'^\s*version\s*=\s*(\d+\.\d+\.\d+)\s*$', re.I|re.M)

REMOTE_PATHS = (
    (re.compile(r'^git@gitlab\.com:(.*)\.git$'), r'https://gitlab.com/\1/-/commit/'),
    (re.compile(r'https://gitlab.com/(.*)\.git(\?.*)?$'), r'https://gitlab.com/\1/-/commit/'),
    (re.compile(r'^git@github\.com:(.*)\.git$'), r'https://github.com/\1/commit/%s'),
    (re.compile(r'https://github.com/(.*)\.git(\?.*)?$'), r'https://github.com/\1/commit/'),
)

PYPI_TEMPLATE = 'https://pypi.org/project/{project}/{version}/'

class Version:
    def __init__(self, vers:str|Iterable[int]):
        if isinstance(vers, str):
            vers = [int(v) for v in vers.split('.')]
        self.parts = tuple(vers)

    def tag(self):
        return 'version_' + '_'.join(str(v).rjust(i+1 if i < 2 else 4, '0') for i, v in enumerate(self.parts))

    def bump(self, level):
        nparts = list(self.parts)
        idx = len(nparts) - 1 - level
        nparts[idx] += 1
        idx += 1
        while idx < len(nparts):
            nparts[idx] = 0
            idx += 1

        return Version(nparts)

    def __str__(self):
        return '.'.join(str(v) for v in self.parts)

    def __repr__(self):
        return f'Version({str(self)!r})'

def parse_changelog(path):
    '''Parse a changelog into two parts: One with all the lines up to the first version
    header, and the rest. Also returns the version number found'''
    lines = path.read_text().replace('\r', '').split('\n')
    prefix_text = []
    itr = iter(lines)
    for line in itr:
        m = RX_VERSION_LINK.match(line) or RX_VERSION.match(line)
        if m:
            version = m.group(1)
            previous_entries = [line]
            previous_entries.extend(itr)
            return prefix_text, previous_entries, version
    return prefix_text, [], None

def make_version_header(version, date, pkgname):
    version_text = f'[Version {version} ({date})]'
    url = PYPI_TEMPLATE.format(project=pkgname, version=version)
    version_link = version_text + f'({url})'
    return version_link, '=' * len(version_text)

def update_changelog(path, new_version, pkgname, remoteprefix):
    try:
        prefix_text, previous_entries, last_version = parse_changelog(path)
    except FileNotFoundError:
        changelog = [(None, [])]

    delimiter = f'[{uuid.uuid4()}]'
    log_args = ['git', 'log', f'--format={delimiter}%H|%ci|%B']
    if last_version:
        log_args.append(f'{Version(last_version).tag()}..HEAD')

    new_changelog_lines = []

    # If we don't have a new version, skip any commits until we come to a version commit
    skip = new_version is None
    if not skip:
        # Insert the entry that we're about to commit
        new_changelog_lines.extend(make_version_header(new_version, time.strftime("%Y-%m-%d", time.localtime()), pkgname))
        new_changelog_lines.append('')

    p = subprocess.run(log_args, stdout=subprocess.PIPE, encoding='utf8', errors='replace', check=True)
    for entry in p.stdout.split(delimiter):
        lst = entry.split('|', 2)
        if len(lst) < 3:
            continue
        hash, date, text = lst
        date = date[:10]
        m = RX_VERSION.match(text)
        if m:
            version_header = f'Version {m.group(1)} ({date})'
            if not skip:
                new_changelog_lines.extend(['', ''])
            new_changelog_lines.extend(make_version_header(m.group(1), date, pkgname))
            new_changelog_lines.append('')
            skip = False
        elif not skip:
            text = text.strip()
            if not text:
                continue

            if remoteprefix:
                remote_url = remoteprefix + hash
                hash_link = f' ([{hash[:7]}]({remote_url}))'
            else:
                hash_link = f' ({hash[:7]})'
            pfx = '* '
            for line in text.split('\n'):
                if line:
                    new_changelog_lines.append(pfx + line + hash_link)
                    pfx = '  * '
                    hash_link = ''

    if not skip:
        new_changelog_lines.extend(['', ''])


    combined_lines = []
    combined_lines.extend(prefix_text)
    combined_lines.extend(new_changelog_lines)
    combined_lines.extend(previous_entries)

    while combined_lines and combined_lines[-1] == '':
        combined_lines.pop()
    combined_lines.append('')
    return '\n'.join(new_changelog_lines), '\n'.join(combined_lines)

def find_remote_commit_prefix():
    p = subprocess.run(['git', 'remote', '-v'], check=True, encoding='utf8', stdout=subprocess.PIPE)
    for url in p.stdout.split():
        if not '/' in url:
            continue
        for rx, template in REMOTE_PATHS:
            m = rx.match(url)
            if m:
                return m.expand(template)
    return None

def walk_tree(base, filter_dir=None, filter_file=None):
    queue = deque([base])
    while queue:
        path = queue.popleft()

        if path.is_dir():
            if not filter_dir or filter_dir(path):
                queue.extend(sorted(path.iterdir()))
        else:
            if not filter_file or filter_file(path):
                yield path

def find_version_files(base):
    for path in (base / 'pyproject.toml', base / 'setup.cfg'):
        yield path

    yield from walk_tree(base, filter_file=lambda path: path.suffix == '.py')

def find_version_data(base):
    version_file_data = []
    current_version = None
    for path in find_version_files(base):
        try:
            text = path.read_text()
        except FileNotFoundError:
            continue

        m = (RX_VERSION_NOQUOTE if path.name == 'setup.cfg' else RX_VERSION_QUOTE).search(text)
        if m:
            version = m.group(1)
            if current_version is None:
                current_version = version

            if version == current_version:
                version_file_data.append((path, text[:m.start(1)], text[m.end(1):]))

    return (Version(current_version) if current_version is not None else None, version_file_data)

def ask(prompt, choices, default=None):
    choices = set(choices)
    while True:
        choice = input(prompt + ' ').lower()
        if choice in choices:
            return choice
        if not choice and default is not None:
            return default

def grep(path, rx):
    try:
        with path.open('r', encoding='utf8', errors='replace') as fp:
            for line in fp:
                m = rx.search(line)
                if m:
                    return m
    except FileNotFoundError:
        pass
    return None

def find_name(path):
    rx_name_quote = re.compile(r'^\s*name\s*=\s*"([a-zA-Z0-9_-]+)"\s*,?\s*$')
    rx_name_noquote = re.compile(r'^\s*name\s*=\s*([a-zA-Z0-9_-]+)\s*$')
    m = (
        grep(path / 'pyproject.toml', rx_name_quote) or
        grep(path / 'setup.cfg', rx_name_noquote) or
        grep(path / 'setup.py', rx_name_quote)
    )
    return m.group(1) if m else None

def find_dist_files(dist_path, package_name, version):
    files = []
    package_name = package_name.replace('_', '-')
    for path in dist_path.iterdir():
        m = re.search(f'(.*?)-(\d+\.\d+\.\d+)(.*)(\.whl|\.tar\.gz)$', path.name)
        if m:
            pkg, vers, qual, suffix = m.groups()
            if vers != version:
                continue

            if pkg.replace('_', '-') != package_name:
                continue

            files.append(path)
    return files

def main():
    p = argparse.ArgumentParser(description='Increment or set the version number, update CHANGELOG.md, and make a version commit')
    p.add_argument('path', nargs='?', type=Path, default=Path('.'), help='Path to package')
    p.add_argument('-a', '--amend', action='store_true', help='Amend edits to changelog and retag')
    p.add_argument('-v', '--version', help='Set the version number. Can be "+" to increment.')
    p.add_argument('-+', '--increment-version', dest='version', action='store_const', const='+', help='Increment the version number.')
    p.add_argument('-c', '--changelog', action='store_true', help='Update CHANGELOG.md from git commits.')
    p.add_argument('-e', '--edit-changelog', action='store_true', help='Edit changelog before committing')
    p.add_argument('-m', '--commit', action='store_true', help='Make a version commit')
    p.add_argument('-t', '--tag', action='store_true', help='Make a version tag')
    p.add_argument('-b', '--build', action='store_true', help='Build the package')
    p.add_argument('-p', '--publish', action='store_true', help='Publish the package with twine')
    p.add_argument('-u', '--push', action='store_true', help='Push to remote')
    p.add_argument('--all', action='store_true', help='Does everything (increment-version, changelog, commit, tag, build, publish, push)')

    p.add_argument('-s', '--install', action='store_true', help='Install the package using "pip"')
    p.add_argument('--installpy', type=Path, help='Use the specified python to run pip for --install')
    p.add_argument('-i', '--confirm', action='store_true', help='Ask for confirmation before everything')
    p.add_argument('-f', '--force', action='store_true', help='Do not ask for confirmation for anything')

    p.add_argument('--noclean', action='store_true', help='Don\'t clean .egg-info dirs')
    p.add_argument('--changelog-path', type=Path, help='Path to CHANGELOG.md')
    p.add_argument('--package-name', default=None, help='Name of the current package')
    p.add_argument('-r', '--remote', default=None, help='Remote repository URL base for linking commits')
    argcomplete.autocomplete(p, validator=lambda current_input, keyword_to_check_against: True)

    args = p.parse_args()

    if args.installpy:
        args.installpy = args.installpy.parent.resolve() / args.installpy.name

    if args.all:
        if not args.version:
            args.version = '+'
        args.changelog = True
        args.commit = True
        args.tag = True
        args.build = True
        args.publish = True
        args.push = True

    if (args.commit or args.tag) and not args.version:
        print('Cannot commit or tag without a new version')
        return 1

    args.path = args.path.resolve()
    if args.package_name is None:
        args.package_name = find_name(args.path)
        if args.package_name is None:
            print("Cannot determine package name")
            return 1

    print(f'Package name: {args.package_name}')

    if args.changelog_path:
        args.changelog_path = args.changelog_path.resolve()
    else:
        args.changelog_path = args.path / 'CHANGELOG.md'

    os.chdir(args.path)

    python = Path('venv/bin/python')
    if not python.exists():
        python = sys.executable


    if not args.remote:
        args.remote = find_remote_commit_prefix()
        if args.remote:
            print(f'Remote URL: {args.remote}')

    p = subprocess.run(
        ['git', 'log', '-n', '1', '--pretty=%B'], check=False, encoding='utf8',
        stdout=subprocess.PIPE, stdin=subprocess.DEVNULL
    )
    last_commit_message = p.stdout.strip()
    m = RX_VERSION.match(last_commit_message)
    head_commit_version = m.group(1) if m else None

    if args.amend:
        if not head_commit_version:
            print(f'Last commit was not a version bump ({last_commit_message})')
            return 1

        if args.edit_changelog:
            subprocess.run([os.getenv('EDITOR') or 'editor', args.changelog_path], check=True)

        if args.confirm:
            if ask('Continue with amend (Y/n)?', 'yn', 'n') != 'y':
                return 1

        subprocess.run(['git', 'add', args.changelog_path], check=True)
        subprocess.run(['git', 'commit', '--amend', '--no-edit'], check=True)
        subprocess.run(['git', 'tag', '-f', version_tag(head_commit_version)], check=True)
        return

    if args.commit:
        p = subprocess.run(['git', 'status', '--porcelain', '-uno'], check=True, encoding='utf8', stdout=subprocess.PIPE)
        ok = True
        if p.stdout:
            print('Uncommitted changes:')
            print(p.stdout)
            ok = False

        if head_commit_version:
            print(f'Last commit was a version bump ({last_commit_message})')
            ok = False

        if not ok:
            if args.force:
                print('Continuing anyway (--force)')
            elif ask('Continue (y/N)?', 'yn', 'n') != 'y':
                return 1

    current_version, version_file_data = find_version_data(args.path)
    if current_version is None:
        print('Cannot find version in any files!')
        return 1

    git_add_args = []

    new_version = None
    print(f'Current version is: {current_version}')

    if args.version:
        if args.version == '+':
            new_version = current_version.bump(0)
        else:
            new_version = Version(args.version)

        if args.confirm:
            print('Will write new version {new_version} to files:')
            for path, pre_txt, post_txt in version_file_data:
                print(f'   {path}')
            if ask('Continue (Y/n)?', 'yn', 'y') != 'y':
                return 1

        print(f'Writing new version {new_version} to files:')
        for path, pre_txt, post_txt in version_file_data:
            print(f'   {path}')
            path.write_text(pre_txt + str(new_version) + post_txt)
            git_add_args.append(path)

    if args.changelog:
        added, new_content = update_changelog(args.changelog_path, new_version, args.package_name, args.remote)
        if args.confirm:
            print('Will add the following to CHANGELOG.md:')
            print(new_content)
            choice = ask('Write changelog (Y/n/e/c)?', 'ynec', 'y')
            if choice == 'c':
                return 1

            if choice == 'n':
                args.changelog = False

            if choice == 'e':
                args.edit_changelog = True

    if args.changelog:
        args.changelog_path.write_text(new_content)

    if args.edit_changelog:
        subprocess.run([os.getenv('EDITOR') or 'editor', args.changelog_path], check=True)

    if args.changelog or args.edit_changelog:
        git_add_args.append(args.changelog_path)

    if args.commit and args.confirm:
        choice = ask(f'Commit {new_version} (Y/n/c)?', 'ync', 'y')
        if choice == 'c':
            return 1
        if choice == 'n':
            args.commit = False

    if args.commit:
        if git_add_args:
            subprocess.run(['git', 'add'] + git_add_args, check=True)
        subprocess.run(['git', 'commit', '-m', f'Version {new_version}'], check=True)

    if args.tag:
        new_tag = new_version.tag()
        existing_commit = subprocess.run(['git', 'rev-parse', '-q', '--verify', 'refs/tags/' + new_tag], stdout=subprocess.PIPE, check=False).stdout
        if existing_commit:
            if args.force:
                print(f'Tag {new_tag} refers to {existing_commit}, continuing (--force)')
            else:
                choice = ask(f'Tag {new_tag} already refers to {existing_commit}, continue (y/N/c)?', 'ync', 'n')
                if choice == 'c':
                    return 1
                if choice == 'n':
                    args.tag = False
            if args.tag:
                subprocess.run(['git', 'tag', '-f', new_tag], check=True)
        else:
            if args.confirm:
                choice = ask(f'Create tag {new_tag} (Y/n/c)?', 'ync', 'y') == 'c'
                if choice == 'c':
                    return 1
                if choice == 'n':
                    args.tag = False
            if args.tag:
                subprocess.run(['git', 'tag', new_tag], check=True)

    if args.build and args.confirm:
        choice = ask(f'Build {new_version} (Y/n/c)?', 'ync', 'y')
        if choice == 'c':
            return 1
        if choice == 'n':
            args.build = False

    if args.build:
        subprocess.run([python, '-m', 'build', '-n', '-w', '-s'], check=True)
        if not args.noclean:
            def delete_egg(path):
                if path.name.endswith('.egg-info'):
                    print(f'Clean egg {path}')
                    shutil.rmtree(path)
                    return False
                return True
            all(walk_tree(Path('.'), filter_dir=delete_egg))

    if args.push and args.confirm:
        choice = ask(f'Push to remote (Y/n/c)?', 'ync', 'y')
        if choice == 'c':
            return 1
        if choice == 'n':
            args.push = False

    if args.push:
        res = subprocess.run(['git', 'push'], check=False).returncode
        if res != 0:
            if not args.force:
                choice = ask(f'Push failed, continue (y/N/c)?', 'ync', 'n')
                if choice != 'y':
                    return 1

    publish_version = str(new_version or current_version)
    publish_files = find_dist_files(Path('dist'), args.package_name, publish_version)
    if args.install:
        install_files = [f for f in publish_files if f.suffix == '.whl']
        if not install_files:
            print('No files to install!')
            return 1

        if args.confirm:
            choice = ask('Install {", ".join(publish_files)} (Y/n/c)?', 'ync', 'y')
            if choice == 'c':
                return 1
            if choice == 'n':
                args.install = None

        if args.install:
            py = args.installpy or sys.executable
            subprocess.run([py, '-m', 'pip', 'uninstall', '-y', args.package_name], check=True)
            subprocess.run([py, '-m', 'pip', 'install', install_files[0]], check=True)

    if args.publish:
        if not publish_files:
            print('No files to publish!')
            return 1

        if args.confirm:
            choice = ask('Publish {", ".join(publish_files)} (Y/n/c)?', 'ync', 'y')
            if choice == 'c':
                return 1
            if choice == 'n':
                args.publish = False

        if args.publish:
            subprocess.run([sys.executable, '-m', 'twine', 'upload'] + [p for p in publish_files if '-linux_' not in p.name], check=True)

    return 0

if __name__ == '__main__':
    sys.exit(main())
