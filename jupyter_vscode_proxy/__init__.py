import os
import shutil
from typing import Any, Dict, List

def vscode_cmd(executable: str, socket_path: str) -> List[str]:
    if not os.path.isfile(executable):
        if not shutil.which(executable):
            raise FileNotFoundError(f"Can not find {executable}")

    get_inner_cmd = [
        executable,
        "--auth", "none",
        "--disable-telemetry",
        "--without-connection-token",
    ]

    working_dir = os.getenv("CODE_WORKINGDIR", ".")

    extensions_dir = os.getenv("CODE_EXTENSIONSDIR", None)

    cmd = get_inner_cmd()

    # --socket-path <path>           The path to a socket file for the server to listen to.
    cmd.append("--socket-path=" + socket_path)

    if extensions_dir:
        cmd += ["--extensions-dir", extensions_dir]

    cmd.append(working_dir)
    return cmd


def setup_vscode() -> Dict[str, Any]:
    executable = os.getenv("CODE_EXECUTABLE", "code-server")
    icon = "code-server.svg" if executable == "code-server" else "vscode.svg"

    path = f'/tmp/vscode_sockets_{os.getuid()}'

    try:
        os.mkdir(path, mode = 0o700)
    except FileExistsError:
        os.chmod(path, 0o700)

    socket_path = f'{path}/code-server'

    def command() -> List[str]:
        return vscode_cmd(executable, socket_path),

    return {
        "command": command,
        "timeout": 300,
        "unix_socket": socket_path,
        "new_browser_tab": True,
        "launcher_entry": {
            "title": "VS Code",
            "icon_path": os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "icons", icon
            ),
        },
    }
