# Hypercorn waits for one last request before shutting down

I'm not sure if this is intended behavior, but I've run into a scenario where
it seems like `hypercorn` is unable to immediately respond to a shutdown trigger.
Instead, `hypercorn` won't shut down until one last request comes in.

## Reproduction

In one terminal:

```bash
git clone https://github.com/tdg5/hypercorn-needs-one-last-request.git
cd hypercorn-needs-one-last-request
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

After the server is running, notice it has not shutdown even though `SHUTDOWN,
BABY!` has been written to the terminal.

In another terminal:

```bash
curl http://127.0.0.1:8080
```

and that should cause `hypercorn` to exit.

Is this the way it is supposed to work?
