# keyring-subprocess
A minimal dependency keyring backend for lean virtual environments.

This is achieved by locating a virtual environment which has
`keyring-subprocess[landmark]` installed whose `keyring-subprocess` can be found
on the PATH. `keyring-subprocess` is effectively a renamed `keyring`
executable and serves as a more unique landmark file.

The virtual environment that is found this way should have the actual
`keyring` backend(s) you need installed into it.

## Pros
- Minimal dependencies for a clean `pip list` command and to always be
  compatible with the rest of your dependencies. Which makes it more
  suitable to be added to `PYTHONPATH` after installing with Pip's
  `--target` flag.
- Has [keyring](https://pypi.org/project/keyring) and the minimal required
  dependencies vendored to make the `chainer` and `null` backends work.
  - It uses the ModuleSpec apis provided by [PEP451](https://peps.python.org/pep-0451/)
    to make the vendored `keyring` importable.
- Provices an extra named `landmark` that will provide the
  `keyring-subprocess` executable.
- Provides a `virtualenv` [Seeder](https://virtualenv.pypa.io/en/latest/user_guide.html#seeders)
  named `keyring-subprocess`.
  - Set `VIRTUALENV_SEEDER` to `keyring-subprocess` or set `seeder` in the
    config file to the same value.
- Provides a `sitecustomize` entry point for the `sitecustomize-entrypoints`
  package. This can be useful if you install it somewhere that is not a
  so-called site directory by using Pip's `--target` flag.
  - You can install both `keyring-subprocess` and `sitecustomize-entrypoints`
    in one go by executing `pip install keyring-subprocess[sitecustomize]`.
    - `sitecustomize-entrypoints` is required if you if `keyring-subprocess`
      is installed into a `PYTHONPATH` location.

## Cons
- It does require `keyring-subprocess[landmark]` to be installed into a virtual
  environment whose `keyring-subprocess` can be found on the PATH.
- Adds, or replaces, points of failures. Depending on how you look at it.
- Being able to import `keyring`, `importlib_metadata` and `zipp` but
  `pip list` not listing them might be confusing and not very helpful during
  debugging.

# Example on Windows

This is a Powershell script which installs [Pipx](https://pypa.github.io/pipx/)
into `C:\Users\Public\.local\pipx`.
- First it sets some environment variables, including `VIRTUALENV_SEEDER`.
- Then it installs keyring via Pipx and injects artifacts-keyring and
  keyring-subprocess[landmark] into the virtual environment of keyring.
- Lastly it installs keyring-subprocess and sitecustomize-entrypoints into
  Pipx's shared virtualenv which Pipx makes sure is available to all virtual
  environments it manages.

When using your new Pipx installation to install Poetry or Pipenv the virtual
environment created by virtualenv will contain keyring-subprocess. This should
cause installing the project dependencies from your private repository to
succeed!

Assuming of couse that your private repository requires artifacts-keyring to
authenticate, and is therefor a Azure DevOps Artifact Feed. If this is not the
case this should be easily fixed by replacing artifacts-keyring by the
package that provides the keyring backend that you actually need.

```powershell
$EnvironmentVariableTarget = $(Read-Host "Target environment (User/Machine) [Machine]").Trim(); `
if ($EnvironmentVariableTarget -eq "") {
  $EnvironmentVariableTarget = "Machine";
} `
if ($EnvironmentVariableTarget -inotin @("User", "Machine")) {
  Write-Host "Invalid option.";
} else {
  try {
    $PATH = $env:PATH;
    $PIP_NO_INPUT = $env:PIP_NO_INPUT;
    $PIP_INDEX_URL = $env:PIP_INDEX_URL;
    $ExecutionPolicy = Get-ExecutionPolicy;

    try {
      if (!$env:PIPX_HOME) {
        $env:PIPX_HOME = [Environment]::GetEnvironmentVariable("PIPX_HOME", $EnvironmentVariableTarget);
      };
      if (!$env:PIPX_HOME) {
        [Environment]::SetEnvironmentVariable("PIPX_HOME", "C:\Users\Public\.local\pipx", $EnvironmentVariableTarget);
        $env:PIPX_HOME = [Environment]::GetEnvironmentVariable("PIPX_HOME", $EnvironmentVariableTarget);
      };

      if (!$env:PIPX_BIN_DIR) {
        $env:PIPX_BIN_DIR = [Environment]::GetEnvironmentVariable("PIPX_BIN_DIR", $EnvironmentVariableTarget);
      };
      if (!$env:PIPX_BIN_DIR) {
        [Environment]::SetEnvironmentVariable("PIPX_BIN_DIR", "C:\Users\Public\.local\bin", $EnvironmentVariableTarget);
        $env:PIPX_BIN_DIR = [Environment]::GetEnvironmentVariable("PIPX_BIN_DIR", $EnvironmentVariableTarget);
      };

      if (!$env:VIRTUALENV_SEEDER) {
        $env:VIRTUALENV_SEEDER = [Environment]::GetEnvironmentVariable("VIRTUALENV_SEEDER", $EnvironmentVariableTarget);
      };
      if (!$env:VIRTUALENV_SEEDER) {
        [Environment]::SetEnvironmentVariable("VIRTUALENV_SEEDER", "keyring-subprocess", $EnvironmentVariableTarget);
        $env:VIRTUALENV_SEEDER = [Environment]::GetEnvironmentVariable("VIRTUALENV_SEEDER", $EnvironmentVariableTarget);
      };

      if (Test-Path "C:\Users\Public\.local\bin\pipx.exe") {
        try {
          $env:PATH = [Environment]::GetEnvironmentVariable("PATH", $EnvironmentVariableTarget);

          Get-Command -Name pipx -OutVariable pipx > $null;
        } catch {
        } finally {
          $env:PATH = $PATH
        }

        if (-not $pipx) {
          $env:PATH = $PATH = "C:\Users\Public\.local\bin;"+$env:PATH;
        };
        return
      };

      [Environment]::SetEnvironmentVariable("Path", "C:\Users\Public\.local\bin;" + [Environment]::GetEnvironmentVariable("Path", $EnvironmentVariableTarget), $EnvironmentVariableTarget);
      $env:PATH = $PATH = "C:\Users\Public\.local\bin;"+$env:PATH;

      $env:PIP_NO_INPUT = '1';
      $env:PIP_INDEX_URL = 'https://pypi.org/simple/';
    } catch {
      throw "Run as Administrator or choose `"User`" as the target environment"
    };

    $venv = Join-Path $env:TEMP ".venv"

    <# Use the py executable if it can be found and default to the python executable #>
    Get-Command -Name py, python -OutVariable py 2>&1 > $null;
    $py = $py[0];
    $env:PATH = $(& $py -c "import sys; import sysconfig; import os; from pathlib import Path; from itertools import chain; print(os.pathsep.join(chain(set([str(Path(sys.executable).parent), sysconfig.get_path(`"`"scripts`"`")]), [os.environ[`"`"PATH`"`"]])))");

    & $py -m venv "$venv";

    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force;
    . "$venv\Scripts\Activate.ps1";

    & $py -m pip install -qqq --no-input --isolated pipx;
    pipx install --pip-args="--no-input --isolated" pipx;
    pipx install --pip-args="--no-input --isolated" keyring;
    pipx inject --pip-args="--no-input --isolated" keyring artifacts-keyring;
    pipx inject --pip-args="--no-input --isolated" --include-apps --include-deps keyring keyring-subprocess[landmark];
    pipx install --pip-args="--no-input --isolated" virtualenv;

    <# Minor hack since Pipx does not allow us to do this via the cli #>
    & "$env:PIPX_HOME\shared\Scripts\pip.exe" install --no-input --isolated keyring-subprocess[sitecustomize];

    deactivate;
    if (Test-Path -Path $venv) {
      Remove-Item -Path "$venv" -Recurse -Force;
    }

    <# Fill virtualenv's wheel cache with keyring-subprocess and up-to-date versions of the embeded wheels #>
    <# I might take a stab at making keyring-subprocess a Quine at some point... #>
    <# Update: I started and figured out that the size of the vendored dependencies are a problem #>
    <# DEFLATE uses a 32KiB sliding window so the size of the .whl before making it a quine should definately be below 64KiB #>
    <# Maybe I can get Pip to vendor keyring and keyring-subprocess? #>
    virtualenv --upgrade-embed-wheels;
    virtualenv --seeder keyring-subprocess --download $venv;

  } catch {
    $Error;
    $env:PATH = $PATH;
  } finally {
    if ($venv -and (Test-Path -Path $venv)) {
      Remove-Item -Path "$venv" -Recurse -Force;
    }

    $env:PIP_NO_INPUT = $PIP_NO_INPUT;
    $env:PIP_INDEX_URL = $PIP_INDEX_URL;
    if ($ExecutionPolicy) {
      Set-ExecutionPolicy -ExecutionPolicy $ExecutionPolicy -Scope Process -Force;
    }
  }
}
```
