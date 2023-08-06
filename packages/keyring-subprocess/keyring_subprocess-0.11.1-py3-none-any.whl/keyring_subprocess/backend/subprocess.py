import base64
import json
import os
import sys
import shutil
import subprocess
from typing import Optional

from keyring import credentials, errors
from keyring.util import properties
from keyring.backend import KeyringBackend
from keyring.backends.chainer import ChainerBackend

EXECUTABLE = "keyring-subprocess"
SERVICE_NAME = "keyring-subprocess"
ENV_VAR_RECURSIVE = "KEYRING_SUBPROCESS_RECURSIVE"


class SubprocessBackend(KeyringBackend):
    recursive = False

    @properties.ClassProperty
    @classmethod
    def priority(cls):
        if not shutil.which(EXECUTABLE):
            raise RuntimeError(f"No {EXECUTABLE} executable found")

        if sys.version_info > (3, 10):
            from importlib import metadata
        else:
            import importlib_metadata as metadata

        if any(metadata.distributions(name="keyring_subprocess_landmark")):
            version = tuple(
                int(digit)
                for digit in metadata.version("keyring_subprocess_landmark").split(".")
            )
            if version >= (0, 3, 0):
                raise RuntimeError(
                    "keyring-subprocess-landmark 0.3.0 and up no longer require"
                    " the backend to be viable for the chainer backend"
                )

        return 100

    @properties.ClassProperty
    @classmethod
    def recursive(cls):
        return bool(os.getenv(ENV_VAR_RECURSIVE))

    def _env(self):
        env = os.environ.copy()
        env[ENV_VAR_RECURSIVE] = "1"

        return env

    def get_password(self, service: str, username: str) -> Optional[str]:
        if self.recursive:
            return self._recursive_get_password(service, username)

        executable = shutil.which(EXECUTABLE)
        if executable is None:
            return None

        payload = {
            "method": "get_password",
            "service": service,
            "username": username,
        }
        result = self._run_subprocess(executable, "get", payload)

        if result.returncode:
            return None

        password = result.stdout.splitlines()[-1]
        return password

    def get_credential(
        self,
        service: str,
        username: Optional[str],
    ) -> Optional[credentials.Credential]:
        if self.recursive:
            return None

        executable = shutil.which(EXECUTABLE)
        if not self.recursive and executable is None:
            return None

        payload = {
            "method": "get_credential",
            "service": service,
            "username": username,
        }
        result = self._run_subprocess(executable, "get", payload)

        if result.returncode:
            return None

        credential = json.loads(base64.b64decode(result.stdout.splitlines()[-1]))

        return credentials.SimpleCredential(**credential)

    def _recursive_get_password(self, service: str, username: str) -> Optional[str]:
        if not self.recursive or service != SERVICE_NAME:
            return None

        params = json.loads(base64.b64decode(username))

        if params["method"] == "get_credential":
            return self._recursive_get_credential(params["service"], params["username"])

        return ChainerBackend().get_password(params["service"], params["username"])

    def _run_subprocess(self, executable, operation: str, payload: any):
        payload = json.dumps(payload)
        payload = base64.b64encode(payload.encode(encoding="utf-8")).decode(
            encoding="utf-8"
        )
        result = subprocess.run(
            [executable, operation, SERVICE_NAME, payload],
            env=self._env(),
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
        return result

    def _recursive_get_credential(self, service: str, username: str) -> Optional[str]:
        if not self.recursive:
            return None

        credential = ChainerBackend().get_credential(service, username)
        if not credential:
            return None

        credential = {
            "username": credential.username,
            "password": credential.password,
        }

        return base64.b64encode(json.dumps(credential).encode(encoding="utf-8")).decode(
            encoding="utf-8"
        )

    def set_password(self, service: str, username: str, password: str) -> None:
        if self.recursive:
            return self._recursive_set_password(service, username, password)

        executable = shutil.which(EXECUTABLE)
        if not self.recursive and executable is None:
            return None

        payload = {
            "service": service,
            "username": username,
            "username": password,
        }
        result = self._run_subprocess(executable, "set", payload)

        if result.returncode:
            raise errors.PasswordSetError(
                f"Subprocess returned with code {result.returncode}"
            )

    def _recursive_set_password(self, service: str, username: str) -> Optional[str]:
        assert self.recursive, "Please don't call this internal method directly"
        if service != SERVICE_NAME:
            raise NotImplementedError()

        params = json.loads(base64.b64decode(username))

        return ChainerBackend().set_password(
            params["service"], params["username"], params["password"]
        )

    def delete_password(self, service: str, username: str) -> None:
        if self.recursive:
            return self._recursive_delete_password(service, username)

        executable = shutil.which(EXECUTABLE)
        if not self.recursive and executable is None:
            return None

        payload = {
            "service": service,
            "username": username,
        }
        result = self._run_subprocess(executable, "del", payload)

        if result.returncode:
            raise errors.PasswordDeleteError(
                f"Subprocess returned with code {result.returncode}"
            )

    def _recursive_delete_password(self, service: str, username: str) -> Optional[str]:
        assert self.recursive, "Please don't call this internal method directly"
        if service != SERVICE_NAME:
            raise NotImplementedError()

        params = json.loads(base64.b64decode(username))

        return ChainerBackend().delete_password(params["service"], params["username"])
