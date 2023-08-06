# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['keyring_subprocess',
 'keyring_subprocess._internal',
 'keyring_subprocess._vendor',
 'keyring_subprocess._vendor.importlib_metadata',
 'keyring_subprocess._vendor.keyring',
 'keyring_subprocess._vendor.keyring.backends',
 'keyring_subprocess._vendor.keyring.backends.macOS',
 'keyring_subprocess._vendor.keyring.util',
 'keyring_subprocess.backend']

package_data = \
{'': ['*'], 'keyring_subprocess._internal': ['wheels/*']}

extras_require = \
{'landmark': ['keyring-subprocess-landmark'],
 'sitecustomize': ['sitecustomize-entrypoints']}

entry_points = \
{'keyring.backends': ['keyring-subprocess = '
                      'keyring_subprocess.backend:SubprocessBackend'],
 'sitecustomize': ['keyring-subprocess = '
                   'keyring_subprocess._internal:sitecustomize'],
 'virtualenv.seed': ['keyring-subprocess = '
                     'keyring_subprocess._internal.seeder:KeyringSubprocessFromAppData']}

setup_kwargs = {
    'name': 'keyring-subprocess',
    'version': '0.11.1',
    'description': '',
    'long_description': '# keyring-subprocess\nA minimal dependency keyring backend for lean virtual environments.\n\nThis is achieved by locating a virtual environment which has\n`keyring-subprocess[landmark]` installed whose `keyring-subprocess` can be found\non the PATH. `keyring-subprocess` is effectively a renamed `keyring`\nexecutable and serves as a more unique landmark file.\n\nThe virtual environment that is found this way should have the actual\n`keyring` backend(s) you need installed into it.\n\n## Pros\n- Minimal dependencies for a clean `pip list` command and to always be\n  compatible with the rest of your dependencies. Which makes it more\n  suitable to be added to `PYTHONPATH` after installing with Pip\'s\n  `--target` flag.\n- Has [keyring](https://pypi.org/project/keyring) and the minimal required\n  dependencies vendored to make the `chainer` and `null` backends work.\n  - It uses the ModuleSpec apis provided by [PEP451](https://peps.python.org/pep-0451/)\n    to make the vendored `keyring` importable.\n- Provices an extra named `landmark` that will provide the\n  `keyring-subprocess` executable.\n- Provides a `virtualenv` [Seeder](https://virtualenv.pypa.io/en/latest/user_guide.html#seeders)\n  named `keyring-subprocess`.\n  - Set `VIRTUALENV_SEEDER` to `keyring-subprocess` or set `seeder` in the\n    config file to the same value.\n- Provides a `sitecustomize` entry point for the `sitecustomize-entrypoints`\n  package. This can be useful if you install it somewhere that is not a\n  so-called site directory by using Pip\'s `--target` flag.\n  - You can install both `keyring-subprocess` and `sitecustomize-entrypoints`\n    in one go by executing `pip install keyring-subprocess[sitecustomize]`.\n    - `sitecustomize-entrypoints` is required if you if `keyring-subprocess`\n      is installed into a `PYTHONPATH` location.\n\n## Cons\n- It does require `keyring-subprocess[landmark]` to be installed into a virtual\n  environment whose `keyring-subprocess` can be found on the PATH.\n- Adds, or replaces, points of failures. Depending on how you look at it.\n- Being able to import `keyring`, `importlib_metadata` and `zipp` but\n  `pip list` not listing them might be confusing and not very helpful during\n  debugging.\n\n# Example on Windows\n\nThis is a Powershell script which installs [Pipx](https://pypa.github.io/pipx/)\ninto `C:\\Users\\Public\\.local\\pipx`.\n- First it sets some environment variables, including `VIRTUALENV_SEEDER`.\n- Then it installs keyring via Pipx and injects artifacts-keyring and\n  keyring-subprocess[landmark] into the virtual environment of keyring.\n- Lastly it installs keyring-subprocess and sitecustomize-entrypoints into\n  Pipx\'s shared virtualenv which Pipx makes sure is available to all virtual\n  environments it manages.\n\nWhen using your new Pipx installation to install Poetry or Pipenv the virtual\nenvironment created by virtualenv will contain keyring-subprocess. This should\ncause installing the project dependencies from your private repository to\nsucceed!\n\nAssuming of couse that your private repository requires artifacts-keyring to\nauthenticate, and is therefor a Azure DevOps Artifact Feed. If this is not the\ncase this should be easily fixed by replacing artifacts-keyring by the\npackage that provides the keyring backend that you actually need.\n\n```powershell\n$EnvironmentVariableTarget = $(Read-Host "Target environment (User/Machine) [Machine]").Trim(); `\nif ($EnvironmentVariableTarget -eq "") {\n  $EnvironmentVariableTarget = "Machine";\n} `\nif ($EnvironmentVariableTarget -inotin @("User", "Machine")) {\n  Write-Host "Invalid option.";\n} else {\n  try {\n    $PATH = $env:PATH;\n    $PIP_NO_INPUT = $env:PIP_NO_INPUT;\n    $PIP_INDEX_URL = $env:PIP_INDEX_URL;\n    $ExecutionPolicy = Get-ExecutionPolicy;\n\n    try {\n      if (!$env:PIPX_HOME) {\n        $env:PIPX_HOME = [Environment]::GetEnvironmentVariable("PIPX_HOME", $EnvironmentVariableTarget);\n      };\n      if (!$env:PIPX_HOME) {\n        [Environment]::SetEnvironmentVariable("PIPX_HOME", "C:\\Users\\Public\\.local\\pipx", $EnvironmentVariableTarget);\n        $env:PIPX_HOME = [Environment]::GetEnvironmentVariable("PIPX_HOME", $EnvironmentVariableTarget);\n      };\n\n      if (!$env:PIPX_BIN_DIR) {\n        $env:PIPX_BIN_DIR = [Environment]::GetEnvironmentVariable("PIPX_BIN_DIR", $EnvironmentVariableTarget);\n      };\n      if (!$env:PIPX_BIN_DIR) {\n        [Environment]::SetEnvironmentVariable("PIPX_BIN_DIR", "C:\\Users\\Public\\.local\\bin", $EnvironmentVariableTarget);\n        $env:PIPX_BIN_DIR = [Environment]::GetEnvironmentVariable("PIPX_BIN_DIR", $EnvironmentVariableTarget);\n      };\n\n      if (!$env:VIRTUALENV_SEEDER) {\n        $env:VIRTUALENV_SEEDER = [Environment]::GetEnvironmentVariable("VIRTUALENV_SEEDER", $EnvironmentVariableTarget);\n      };\n      if (!$env:VIRTUALENV_SEEDER) {\n        [Environment]::SetEnvironmentVariable("VIRTUALENV_SEEDER", "keyring-subprocess", $EnvironmentVariableTarget);\n        $env:VIRTUALENV_SEEDER = [Environment]::GetEnvironmentVariable("VIRTUALENV_SEEDER", $EnvironmentVariableTarget);\n      };\n\n      if (Test-Path "C:\\Users\\Public\\.local\\bin\\pipx.exe") {\n        try {\n          $env:PATH = [Environment]::GetEnvironmentVariable("PATH", $EnvironmentVariableTarget);\n\n          Get-Command -Name pipx -OutVariable pipx > $null;\n        } catch {\n        } finally {\n          $env:PATH = $PATH\n        }\n\n        if (-not $pipx) {\n          $env:PATH = $PATH = "C:\\Users\\Public\\.local\\bin;"+$env:PATH;\n        };\n        return\n      };\n\n      [Environment]::SetEnvironmentVariable("Path", "C:\\Users\\Public\\.local\\bin;" + [Environment]::GetEnvironmentVariable("Path", $EnvironmentVariableTarget), $EnvironmentVariableTarget);\n      $env:PATH = $PATH = "C:\\Users\\Public\\.local\\bin;"+$env:PATH;\n\n      $env:PIP_NO_INPUT = \'1\';\n      $env:PIP_INDEX_URL = \'https://pypi.org/simple/\';\n    } catch {\n      throw "Run as Administrator or choose `"User`" as the target environment"\n    };\n\n    $venv = Join-Path $env:TEMP ".venv"\n\n    <# Use the py executable if it can be found and default to the python executable #>\n    Get-Command -Name py, python -OutVariable py 2>&1 > $null;\n    $py = $py[0];\n    $env:PATH = $(& $py -c "import sys; import sysconfig; import os; from pathlib import Path; from itertools import chain; print(os.pathsep.join(chain(set([str(Path(sys.executable).parent), sysconfig.get_path(`"`"scripts`"`")]), [os.environ[`"`"PATH`"`"]])))");\n\n    & $py -m venv "$venv";\n\n    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force;\n    . "$venv\\Scripts\\Activate.ps1";\n\n    & $py -m pip install -qqq --no-input --isolated pipx;\n    pipx install --pip-args="--no-input --isolated" pipx;\n    pipx install --pip-args="--no-input --isolated" keyring;\n    pipx inject --pip-args="--no-input --isolated" keyring artifacts-keyring;\n    pipx inject --pip-args="--no-input --isolated" --include-apps --include-deps keyring keyring-subprocess[landmark];\n    pipx install --pip-args="--no-input --isolated" virtualenv;\n\n    <# Minor hack since Pipx does not allow us to do this via the cli #>\n    & "$env:PIPX_HOME\\shared\\Scripts\\pip.exe" install --no-input --isolated keyring-subprocess[sitecustomize];\n\n    deactivate;\n    if (Test-Path -Path $venv) {\n      Remove-Item -Path "$venv" -Recurse -Force;\n    }\n\n    <# Fill virtualenv\'s wheel cache with keyring-subprocess and up-to-date versions of the embeded wheels #>\n    <# I might take a stab at making keyring-subprocess a Quine at some point... #>\n    <# Update: I started and figured out that the size of the vendored dependencies are a problem #>\n    <# DEFLATE uses a 32KiB sliding window so the size of the .whl before making it a quine should definately be below 64KiB #>\n    <# Maybe I can get Pip to vendor keyring and keyring-subprocess? #>\n    virtualenv --upgrade-embed-wheels;\n    virtualenv --seeder keyring-subprocess --download $venv;\n\n  } catch {\n    $Error;\n    $env:PATH = $PATH;\n  } finally {\n    if ($venv -and (Test-Path -Path $venv)) {\n      Remove-Item -Path "$venv" -Recurse -Force;\n    }\n\n    $env:PIP_NO_INPUT = $PIP_NO_INPUT;\n    $env:PIP_INDEX_URL = $PIP_INDEX_URL;\n    if ($ExecutionPolicy) {\n      Set-ExecutionPolicy -ExecutionPolicy $ExecutionPolicy -Scope Process -Force;\n    }\n  }\n}\n```\n',
    'author': 'Dos Moonen',
    'author_email': 'darsstar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://keyring-subprocess.darsstar.dev/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
