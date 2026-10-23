"""Exercise launcher lifecycle decisions without claiming the real UI port."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys

import pytest


pytestmark = pytest.mark.skipif(
    os.name != "posix" or shutil.which("bash") is None,
    reason="The Bash launcher requires macOS/Linux; use direct Streamlit on Windows.",
)


@pytest.fixture
def launcher(tmp_path):
    project = tmp_path / "project with spaces"
    project.mkdir()
    shutil.copyfile(Path(__file__).parents[1] / "run.sh", project / "run.sh")
    (project / "app.py").touch()
    (project / ".venv/bin").mkdir(parents=True)
    helper = project / "server.py"
    helper.write_text(
        """import json, os, pathlib, signal, sys, time
root = pathlib.Path(os.environ['LAUNCHER_FIXTURE_DIR'])
if (root / 'fail_start').exists():
    print('simulated startup failure', flush=True)
    sys.exit(3)
(root / 'server.json').write_text(json.dumps({'pid': os.getpid(), 'command': ' '.join(sys.argv)}))
(root / 'ready').touch()
def stop(*args):
    (root / 'ready').unlink(missing_ok=True)
    sys.exit(0)
signal.signal(signal.SIGTERM, stop)
while True:
    time.sleep(0.05)
"""
    )
    python = project / ".venv/bin/python"
    python.write_text(
        f"#!{sys.executable}\n"
        """import os, pathlib, sys
root = pathlib.Path(os.environ['LAUNCHER_FIXTURE_DIR'])
if sys.argv[1] == '-c':
    code = sys.argv[2]
    if 'subprocess.Popen' in code:
        import subprocess
        real_popen = subprocess.Popen
        def private_app(command, **options):
            return real_popen([sys.executable, str(root / 'server.py'), *command[1:]], **options)
        subprocess.Popen = private_app
        sys.argv = [sys.argv[0], *sys.argv[3:]]
        exec(code)
        sys.exit(0)
    if 'sys.version_info' in code:
        sys.exit(int((root / 'old_python').exists()))
    if 'import streamlit' in code:
        (root / 'dependencies_checked').touch()
        sys.exit(int((root / 'missing_dependencies').exists()))
    if 'urllib.request' in code:
        sys.exit(int(not (root / 'ready').exists() or (root / 'unhealthy').exists()))
    if 'import socket' in code:
        sys.exit(int((root / 'occupied').exists()))
    raise AssertionError(code)
if (root / 'foreground_exit').exists():
    (root / 'foreground_args.json').write_text(__import__('json').dumps(sys.argv[1:]))
    sys.exit(0)
os.execv(sys.executable, [sys.executable, str(root / 'server.py'), *sys.argv[1:]])
"""
    )
    python.chmod(0o755)
    bin_dir = project / "test-bin"
    bin_dir.mkdir()
    ps = bin_dir / "ps"
    ps.write_text(
        f"#!{sys.executable}\n"
        """import json, os, pathlib, sys
root = pathlib.Path(os.environ['LAUNCHER_FIXTURE_DIR'])
record = root / 'server.json'
if record.exists() and (root / 'ready').exists():
    server = json.loads(record.read_text())
    if str(server['pid']) == sys.argv[2]:
        print(server['command'])
        sys.exit(0)
print('python unrelated-server.py')
"""
    )
    ps.chmod(0o755)
    env = dict(os.environ, LAUNCHER_FIXTURE_DIR=str(project))
    env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]

    def run(*args):
        # Each call is a fresh shell; the private background process must persist.
        return subprocess.run(
            ["bash", str(project / "run.sh"), *args],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=15,
        )

    yield project, run
    record = project / "server.json"
    if record.exists():
        pid = json.loads(record.read_text())["pid"]
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass


def test_start_status_repeat_and_stop_across_fresh_shells(launcher):
    project, run = launcher
    started = run()
    assert started.returncode == 0, started.stderr
    assert "Running (PID" in started.stdout
    pid = (project / ".runtime/server.pid").read_text()
    assert os.getsid(int(pid)) == int(pid)
    assert run("status").returncode == 0
    assert "Already running" in run("start").stdout
    assert (project / ".runtime/server.pid").read_text() == pid
    stopped = run("stop")
    assert stopped.returncode == 0, stopped.stderr
    assert "Stopped this project's" in stopped.stdout
    assert not (project / ".runtime/server.pid").exists()
    assert run("status").returncode == 1
    assert run("stop").returncode == 0


def test_missing_dependencies_are_actionable_and_stop_still_works(launcher):
    project, run = launcher
    assert run("start").returncode == 0
    (project / "dependencies_checked").unlink()
    (project / "missing_dependencies").touch()
    assert run("status").returncode == 0
    assert run("stop").returncode == 0
    assert not (project / "dependencies_checked").exists()
    missing = run("start")
    assert missing.returncode == 1
    assert "python -m pip install -r requirements.txt" in missing.stderr
    assert not (project / ".runtime/server.pid").exists()


def test_unrelated_pid_and_occupied_port_are_left_alone(launcher):
    project, run = launcher
    unrelated = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        (project / ".runtime").mkdir()
        (project / ".runtime/server.pid").write_text(str(unrelated.pid))
        assert "No running preview" in run("stop").stdout
        assert unrelated.poll() is None
        (project / "occupied").touch()
        blocked = run("start")
        assert blocked.returncode == 1
        assert "Port 8501 is already in use" in blocked.stderr
        assert "No process was stopped" in blocked.stderr
        assert unrelated.poll() is None
        assert not (project / ".runtime/server.pid").exists()
    finally:
        unrelated.terminate()
        unrelated.wait(timeout=5)


def test_unhealthy_owned_process_keeps_its_pid_for_safe_stop(launcher):
    project, run = launcher
    assert run("start").returncode == 0
    pid = (project / ".runtime/server.pid").read_text()
    (project / "unhealthy").touch()
    assert "health check failed" in run("status").stderr
    restarted = run("start")
    assert restarted.returncode == 1
    assert "running but unhealthy" in restarted.stderr
    assert (project / ".runtime/server.pid").read_text() == pid
    assert run("stop").returncode == 0


def test_failed_launch_does_not_leave_a_stale_pid(launcher):
    project, run = launcher
    (project / "fail_start").touch()
    failed = run("start")
    assert failed.returncode == 1
    assert "simulated startup failure" in failed.stderr
    assert not (project / ".runtime/server.pid").exists()


def test_invalid_modes_and_address_overrides_fail_before_dependency_checks(launcher):
    project, run = launcher
    assert run("unknown").returncode == 2
    overridden = run("start", "--server.port=8502")
    assert overridden.returncode == 2
    assert "run python -m streamlit run app.py directly" in overridden.stderr
    assert not (project / "dependencies_checked").exists()


def test_stopped_status_does_not_require_an_environment(launcher):
    project, run = launcher
    shutil.rmtree(project / ".venv")
    status = run("status")
    assert status.returncode == 1
    assert "not running" in status.stdout
    assert run("stop").returncode == 0


def test_foreground_preserves_app_path_and_non_address_options(launcher):
    project, run = launcher
    (project / "foreground_exit").touch()
    result = run("foreground", "--theme.base", "dark")
    assert result.returncode == 0, result.stderr
    args = json.loads((project / "foreground_args.json").read_text())
    assert args[:4] == ["-m", "streamlit", "run", str(project / "app.py")]
    assert args[-2:] == ["--theme.base", "dark"]
    assert not (project / ".runtime/server.pid").exists()


def test_unsupported_python_version_has_setup_guidance(launcher):
    project, run = launcher
    (project / "old_python").touch()
    result = run("start")
    assert result.returncode == 1
    assert "Python 3.12 or later is required" in result.stderr
    assert "Recreate .venv" in result.stderr
    assert not (project / "dependencies_checked").exists()
