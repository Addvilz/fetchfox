import argparse
import os
import shutil
import tarfile
from tempfile import TemporaryDirectory
import json
import urllib.request
import configparser

import wget

desktop_entry = """
# Managed by Fetchfox - do not edit.
[Desktop Entry]
Name=Firefox {{suffix}}
Comment=Browse the World Wide Web (Fetchfox)
GenericName=Web Browser (Fetchfox)
X-GNOME-FullName=Firefox Web Browser{{suffix}}
Exec={{executable}} --class {{instance_class}} %u
Terminal=false
X-MultipleArgs=false
Type=Application
Icon=firefox
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/vnd.mozilla.xul+xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;
StartupWMClass={{instance_class}}
StartupNotify=true
"""


def fetch_name_suffix(target):
    resolve_keys = {
        'dev': ' Dev',
        'stable': ' Stable',
        'devedition': ' Developer',
        'esr': ' ESR',
        'nightly': ' Nightly',
    }
    return resolve_keys[target]


def fetch_local_version(platform_ini_path):
    if not os.path.isfile(platform_ini_path):
        return None

    config = configparser.ConfigParser()
    config.read(platform_ini_path)
    return config['Build']['Milestone']


def fetch_remote_version(target):
    resolve_keys = {
        'dev': 'LATEST_FIREFOX_DEVEL_VERSION',
        'stable': 'LATEST_FIREFOX_VERSION',
        'devedition': 'FIREFOX_DEVEDITION',
        'esr': 'FIREFOX_ESR',
        'nightly': 'FIREFOX_NIGHTLY',
    }

    api_url = 'https://product-details.mozilla.org/1.0/firefox_versions.json'

    with urllib.request.urlopen(api_url) as url:
        api_data = json.loads(url.read().decode())

    return api_data[resolve_keys[target]]


def get_download_url(release, remote_version, locale, arch):
    if arch == 'linux64':
        r_arch = 'linux-x86_64'
    elif arch == 'linux':
        r_arch = 'linux-i686'
    else:
        raise RuntimeError('Unknown arch - %s' % arch)

    if release == 'devedition':
        r_root = 'devedition'
    else:
        r_root = 'firefox'

    return 'https://ftp.mozilla.org/pub/%s/releases/%s/%s/%s/firefox-%s.tar.bz2' % (
        r_root,
        remote_version,
        r_arch,
        locale,
        remote_version
    )


def install_do(args):
    local_dir = os.path.expanduser('~/.local/share/fetchfox/%s-%s-%s' % (args.release, args.arch, args.locale))
    local_version_path = os.path.join(local_dir, 'firefox/platform.ini')
    local_bin_path = os.path.join(local_dir, 'firefox/firefox')
    local_version = fetch_local_version(local_version_path)

    if not args.pin:
        remote_version = fetch_remote_version(args.release)
    else:
        remote_version = args.pin

    if local_version == remote_version:
        if not args.force:
            print('Local version is up to date (%s)' % local_version)
            return

        print('Local version is up to date (%s) but will force reinstall' % local_version)

    print('Will install %s at %s' % (args.release, remote_version))

    url = get_download_url(args.release, remote_version, args.locale, args.arch)

    print('Downloading from %s' % url)

    with TemporaryDirectory() as tmpdir:
        # Download to tmp
        archive_path = os.path.join(tmpdir, 'download.tar.bz2')
        wget.download(url, archive_path)
        print()

        # Remove previous
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir, ignore_errors=True)

        # Create fresh dir
        os.makedirs(local_dir, 0o755)

        # Extract
        archive = tarfile.open(archive_path)
        archive.extractall(local_dir)
        archive.close()

        instance_class = 'Fetchfox-%s-%s-%s' % (args.release, args.arch, args.locale)
        name_suffix = fetch_name_suffix(args.release)
        desktop_entry_text = desktop_entry \
            .replace('{{executable}}', local_bin_path) \
            .replace('{{instance_class}}', instance_class) \
            .replace('{{suffix}}', name_suffix)

        desktop_entry_dir = os.path.expanduser('~/.local/share/applications/')
        desktop_path = os.path.expanduser('~/.local/share/applications/%s.desktop' % instance_class)

        with open(desktop_path, 'w') as desktop_file:
            desktop_file.write(desktop_entry_text)

        os.system('update-desktop-database %s' % desktop_entry_dir)

    print('Done')


def main():
    parser = argparse.ArgumentParser(description='Fetch and install Firefox official binary build for current user.')

    parser.add_argument(
        'release',
        help='Release to install - stable, dev, devedition, esr, nightly'
    )

    parser.add_argument(
        '--locale',
        help='Locale to use, by default - en-US.',
        default='en-US'
    )

    parser.add_argument(
        '--arch',
        help='Arch to use. `linux` for Linux i686, `linux64` for Linux x86_64.',
        default='linux64'
    )

    parser.add_argument(
        '--pin',
        help='Specific version to use, for example 78.0.2. Defaults to latest version.',
        default=None
    )

    parser.add_argument(
        '--force',
        help='Force (re)install, even if local version is the same.',
        action='store_true'
    )

    args = parser.parse_args()

    if args.arch != 'linux' and args.arch != 'linux64':
        raise RuntimeError('Unsupported arch')

    if args.release != 'stable' and args.release != 'dev' and args.release != 'devedition' \
            and args.release != 'esr' and args.release != 'nightly':
        raise RuntimeError('Unsupported arch')

    install_do(args)
