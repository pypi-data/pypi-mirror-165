#!/usr/bin/python3
import sys
import re
import time
import os
import argparse
import subprocess
import traceback
import uuid
from pathlib import Path

RX_VERSION = re.compile(r'^Version (\d+\.\d+\.\d+)')
RX_VERSION_LINK = re.compile(r'^\[Version (\d+\.\d+\.\d+) \([^\)]+\)\]')

VCS_PATHS = (
    (re.compile(r'^git@gitlab\.com:(.*)\.git$'), r'https://gitlab.com/\1/-/commit/'),
    (re.compile(r'https://gitlab.com/(.*)\.git(\?.*)?$'), r'https://gitlab.com/\1/-/commit/'),
    (re.compile(r'^git@github\.com:(.*)\.git$'), r'https://github.com/\1/commit/%s'),
    (re.compile(r'https://github.com/(.*)\.git(\?.*)?$'), r'https://github.com/\1/commit/'),
)

PYPI_TEMPLATE = 'https://pypi.org/project/{project}/{version}/'

def version_tag(vers):
    version_parts = [int(v) for v in vers.split('.')]
    return f'version_{version_parts[0]}_{version_parts[1]:02d}_{version_parts[2]:04d}'

def parse_changelog(path):
    lines = path.read_text().replace('\r', '').split('\n')
    current_section = (None, [])
    version_sections = [current_section]
    for line in lines:
        m = RX_VERSION_LINK.match(line)
        if m:
            current_section = m.group(1), []
            version_sections.append(current_section)
        current_section[1].append(line)
    return version_sections

def make_version_header(version, date, pkgname):
    version_text = f'[Version {version} ({date})]'
    url = PYPI_TEMPLATE.format(project=pkgname, version=version)
    version_link = version_text + f'({url})'
    return version_link, '=' * len(version_text)

def update_changelog(path, new_version, pkgname, vcsprefix):
    try:
        changelog = parse_changelog(path)
    except FileNotFoundError:
        changelog = [(None, [])]

    prefix_text = changelog[0][1]
    delimiter = f'[{uuid.uuid4()}]'
    log_args = ['git', 'log', f'--format={delimiter}%H|%ci|%B']
    if len(changelog) >= 2:
        last_version = changelog[1][0]
        log_args.append(f'{version_tag(last_version)}..HEAD')

    new_changelog_lines = list(prefix_text)
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
            new_changelog_lines.extend(['', ''])
            new_changelog_lines.extend(make_version_header(m.group(1), date, pkgname))
            new_changelog_lines.append('')
        else:
            text = text.strip()
            if not text:
                continue

            vcs_url = vcsprefix + hash
            hash_link = f' ([{hash[:7]}]({vcs_url}))'
            pfx = '* '
            for line in text.split('\n'):
                if line:
                    new_changelog_lines.append(pfx + line + hash_link)
                    pfx = '  * '
                    hash_link = ''

    new_changelog_lines.extend(['', ''])
    for version, section in changelog[1:]:
        new_changelog_lines.extend(section)

    while new_changelog_lines and new_changelog_lines[-1] == '':
        new_changelog_lines.pop()
    new_changelog_lines.append('')
    path.write_text('\n'.join(new_changelog_lines))

def find_vcs_template():
    p = subprocess.run(['git', 'remote', '-v'], check=True, encoding='utf8', stdout=subprocess.PIPE)
    for url in p.stdout.split():
        if not '/' in url:
            continue
        for rx, template in VCS_PATHS:
            m = rx.match(url)
            if m:
                return m.expand(template)
    return None

def main():
    p = argparse.ArgumentParser(description='Increment or set the version number, update CHANGELOG.md, and make a version commit')
    p.add_argument('path', nargs='?', type=Path, default=Path('.'), help='Path to package')
    p.add_argument('-p', '--package-name', default=None, help='Name of the current package (default: name of package directory)')
    p.add_argument('-v', '--version-file', default=Path('pyproject.toml'), type=Path, help='Path to the file containing the version')
    p.add_argument('-c', '--changelog-file', default=Path('CHANGELOG.md'), type=Path, help='Path to the changelog file')
    p.add_argument('-f', '--force', action='store_true', help='Force run even with uncommitted changes')
    p.add_argument('-a', '--amend', action='store_true', help='Amend edits to changelog and retag')
    p.add_argument('-e', '--edit-changelog', action='store_true', help='Edit changelog before committing')
    p.add_argument('-n', '--new-version', help='Override the new version')
    p.add_argument('-r', '--remote', default=None, help='Remote repository URL base')
    args = p.parse_args()

    args.path = args.path.resolve()
    if args.package_name is None:
        args.package_name = args.path.name.replace('_', '-')

    os.chdir(args.path)

    if not args.remote:
        args.remote = find_vcs_template()
        if not args.remote:
            print('Could not determine remote url!')
            return 1
        print(f'Remote URL: {args.remote}')

    p = subprocess.run(['git', 'log', '-n', '1', '--pretty=%B'], check=True, encoding='utf8', stdout=subprocess.PIPE)
    last_commit_message = p.stdout.strip()
    m = RX_VERSION.match(last_commit_message)
    head_commit_version = m.group(1) if m else None

    if args.amend:
        if not head_commit_version:
            print(f'Last commit was not a version bump ({last_commit_message})')
            return 1

        if args.edit_changelog:
            subprocess.run([os.getenv('EDITOR') or 'editor', args.changelog_file], check=True)

        subprocess.run(['git', 'add', args.changelog_file], check=True)
        subprocess.run(['git', 'commit', '--amend', '--no-edit'], check=True)
        subprocess.run(['git', 'tag', '-f', version_tag(head_commit_version)], check=True)
        return

    if not args.force:
        p = subprocess.run(['git', 'status', '--porcelain', '-uno'], check=True, encoding='utf8', stdout=subprocess.PIPE)
        if p.stdout:
            print('Uncommitted changes:')
            print(p.stdout)
            return 1

        if head_commit_version:
            print(f'Last commit was a version bump ({last_commit_message})')
            return 1

    old_version = None
    new_version = None
    version_parts = None
    if args.new_version:
        new_version = args.new_version
        version_parts = [int(v) for v in new_version.split('.')]

    git_add_args = []


    text = args.version_file.read_text()
    m = re.search(r'version\s*=\s*"(.*?)"', text, re.I)

    old_version = m.group(1)

    if new_version is None:
        version_parts = [int(v) for v in old_version.split('.')]
        version_parts[-1] += 1
        new_version = '.'.join(str(v) for v in version_parts)

        print(f'new version = {new_version}')


    update_changelog(args.changelog_file, new_version, args.package_name, args.remote)
    git_add_args.append(args.changelog_file)

    if args.edit_changelog:
        subprocess.run([os.getenv('EDITOR') or 'editor', args.changelog_file], check=True)

    new_text = text[:m.start(1)] + new_version + text[m.end(1):]
    if text != new_text:
        args.version_file.write_text(new_text)
        git_add_args.append(args.version_file)

    if git_add_args:
        subprocess.run(['git', 'add'] + git_add_args, check=True)
    subprocess.run(['git', 'commit', '-m', f'Version {new_version}'], check=True)
    new_tag = version_tag(new_version)
    if args.force:
        subprocess.run(['git', 'tag', '-f', new_tag], check=True)
    else:
        subprocess.run(['git', 'tag', new_tag], check=True)

    return 0

if __name__ == '__main__':
    sys.exit(main())
