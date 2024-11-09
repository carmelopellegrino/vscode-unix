import os
import shutil
from typing import Any, Dict, List

def vscode_cmd(executable: str, socket_path: str) -> List[str]:
    if not os.path.isfile(executable):
        if not shutil.which(executable):
            raise FileNotFoundError(f"Can not find {executable}")

    cmd = [
        executable,
        "--auth", "none",
        "--disable-telemetry",
    ]

    working_dir = os.getenv("CODE_WORKINGDIR", ".")

    extensions_dir = os.getenv("CODE_EXTENSIONSDIR", None)

    # --socket-path <path>           The path to a socket file for the server to listen to.
    cmd.append("--socket=" + socket_path)
    cmd.append("--socket-mode=700")

    if extensions_dir:
        cmd += ["--extensions-dir", extensions_dir]

    cmd.append(working_dir)
    return cmd


def setup_vscode() -> Dict[str, Any]:
    executable = os.getenv("CODE_EXECUTABLE", "code-server")
    icon = "vscode.svg"

    socket_path = f'/tmp/code-server_{os.getuid()}'

    def command() -> List[str]:
        return vscode_cmd(executable, socket_path)

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
