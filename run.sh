#!/usr/bin/env bash
# Start a persistent local preview: bash run.sh
# Other commands: bash run.sh status | stop | foreground
set -euo pipefail

project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_dir"
runtime_dir="$project_dir/.runtime"
pid_file="$runtime_dir/server.pid"
log_file="$runtime_dir/streamlit.log"
site_url="http://127.0.0.1:8501/"
mode="${1:-start}"
if (( $# > 0 )); then shift; fi

case "$mode" in
    start|status|stop|foreground) ;;
    *) echo "Usage: bash run.sh [start|status|stop|foreground]" >&2; exit 2 ;;
esac
# Lifecycle checks use this fixed local address, so don't let extra Streamlit
# options silently move the server away from the URL that is being checked.
for argument in "$@"; do
    case "$argument" in
        --server.address|--server.address=*|--server.port|--server.port=*|--server.baseUrlPath|--server.baseUrlPath=*|--server.sslCertFile|--server.sslCertFile=*|--server.sslKeyFile|--server.sslKeyFile=*)
            echo "This launcher uses $site_url. To change the server address, port, path or TLS settings, run python -m streamlit run app.py directly." >&2
            exit 2 ;;
    esac
done

our_server_running() {
    [[ -f "$pid_file" ]] || return 1
    server_pid="$(cat "$pid_file")"
    [[ "$server_pid" =~ ^[1-9][0-9]*$ ]] || return 1
    kill -0 "$server_pid" 2>/dev/null || return 1
    process_command="$(ps -p "$server_pid" -o args= 2>/dev/null)" || return 1
    [[ "$process_command" == *"streamlit run $project_dir/app.py "* ||
       "$process_command" == *"streamlit run $project_dir/app.py" ]]
}

# Stopping an owned process must still work if its environment was removed or
# damaged after launch. Never infer ownership from a listener on port 8501.
if [[ "$mode" == stop ]]; then
    if our_server_running; then
        kill "$server_pid"
        for attempt in {1..40}; do
            if ! our_server_running; then
                rm -f "$pid_file"
                echo "Stopped this project's local preview."
                exit 0
            fi
            sleep 0.1
        done
        echo "The preview has not stopped yet. Check $log_file and retry bash run.sh stop." >&2
        exit 1
    fi
    rm -f "$pid_file"
    echo "No running preview belonging to this launcher was found."
    exit 0
fi

if [[ "$mode" == status ]] && ! our_server_running; then
    echo "The local preview is not running. Start it with: bash run.sh"
    exit 1
fi

python_bin=""
if [[ -x "$project_dir/.venv/bin/python" ]]; then
    python_bin="$project_dir/.venv/bin/python"
elif [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
    python_bin="$VIRTUAL_ENV/bin/python"
else
    for candidate in python3 python; do
        if command -v "$candidate" >/dev/null 2>&1; then
            python_bin="$(command -v "$candidate")"
            break
        fi
    done
fi
if [[ -z "$python_bin" ]]; then
    echo "Python 3.12 or later is required. Follow README.md to create .venv and install requirements.txt." >&2
    exit 1
fi
healthy() {
    "$python_bin" -c 'import urllib.request; r = urllib.request.urlopen("http://127.0.0.1:8501/_stcore/health", timeout=0.5); assert r.status == 200 and r.read().strip() == b"ok"' >/dev/null 2>&1
}

if [[ "$mode" == status ]]; then
    if healthy; then
        echo "Running (PID $server_pid): $site_url"
        echo "Log: $log_file"
        exit 0
    fi
    echo "This project's preview (PID $server_pid) is running but its health check failed. Check $log_file or run bash run.sh stop before restarting." >&2
    exit 1
fi

if ! "$python_bin" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' >/dev/null 2>&1; then
    echo "Python 3.12 or later is required; the selected interpreter is: $python_bin" >&2
    echo "Recreate .venv with Python 3.12 or later using the commands in README.md." >&2
    exit 1
fi
if ! "$python_bin" -c 'import streamlit, numpy, pandas, plotly, scipy' >/dev/null 2>&1; then
    echo "Required Python packages are missing or could not be imported using: $python_bin" >&2
    echo "Activate the intended environment and run: python -m pip install -r requirements.txt" >&2
    echo "See README.md for the complete setup commands, then retry: bash run.sh" >&2
    exit 1
fi
server_args=(-m streamlit run "$project_dir/app.py" --server.address 127.0.0.1
             --server.port 8501 --server.headless true --browser.gatherUsageStats false)
if [[ "$mode" == foreground ]]; then
    exec "$python_bin" "${server_args[@]}" "$@"
fi

if our_server_running; then
    if healthy; then
        echo "Already running: $site_url"
        exit 0
    fi
    echo "This project's preview (PID $server_pid) is running but unhealthy. Check $log_file or run bash run.sh stop before restarting." >&2
    exit 1
fi
# Test availability without inspecting or stopping any unrelated process.
if ! "$python_bin" -c 'import socket; s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(("127.0.0.1", 8501)); s.close()' >/dev/null 2>&1; then
    echo "Port 8501 is already in use or unavailable. No process was stopped. Close the other server yourself or run Streamlit directly with another --server.port." >&2
    exit 1
fi
mkdir -p "$runtime_dir"
rm -f "$pid_file"
# Python creates a separate session on both macOS and Linux. In particular,
# macOS usually has no setsid executable; nohup alone leaves the session shared.
server_pid="$("$python_bin" -c 'import subprocess, sys
with open(sys.argv[1], "ab", buffering=0) as log:
    process = subprocess.Popen([sys.executable, *sys.argv[2:]], stdin=subprocess.DEVNULL,
                               stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
print(process.pid)' "$log_file" "${server_args[@]}" "$@")"
echo "$server_pid" > "$pid_file"
for attempt in {1..30}; do
    if our_server_running && healthy; then
        echo "Running (PID $server_pid): $site_url"
        echo "Log: $log_file"
        exit 0
    fi
    if ! kill -0 "$server_pid" 2>/dev/null; then break; fi
    sleep 0.25
done
# Clean up only the process started above; leave unrelated port owners alone.
if our_server_running; then kill "$server_pid" 2>/dev/null || true; fi
rm -f "$pid_file"
echo "The preview did not become healthy. Last log messages:" >&2
tail -n 20 "$log_file" >&2
exit 1
