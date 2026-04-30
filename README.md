<p align="center" width="100%">
    <img src="https://marketplace.sumtotalsystems.com/content/images/vendor/SumTotal_logo.png">
</p>

# SumTotal Webhook Listener — Python (FastAPI) Sample

A reference implementation of a SumTotal webhook listener in **Python 3.9+ / FastAPI**. Exposes `POST /api/listenevent` on port `8080`, validates the `X-SUMT-Signature` header with HMAC-SHA1, and ships with a complete VS Code workflow.

The original **Java / Spring Boot** sample is preserved unchanged in [java/](java/) — see [java/README notes](#java-reference-implementation) below.

## Layout

```
.
├── .vscode/                    # launch, tasks, settings, recommended extensions
├── app/
│   ├── main.py                 # FastAPI app entry
│   ├── config.py               # env-driven settings
│   ├── controllers/
│   │   └── listener_controller.py   # POST /api/listenevent
│   └── services/
│       └── listener.py         # signature validation
├── tests/
│   └── test_listener.py        # pytest suite (unit + endpoint)
├── java/                       # original Java/Spring Boot sample (reference)
├── .env.example                # copy to .env and fill in your secret
├── pyproject.toml              # pytest config
├── requirements.txt            # pinned runtime + test deps
├── requests.http               # REST Client examples for VS Code
└── run.py                      # local dev entry point
```

## Pre-requisites

1. **Python 3.9+** (tested on 3.10).
2. **VS Code** with the recommended Python extensions — VS Code will prompt you when you open this folder; see [.vscode/extensions.json](.vscode/extensions.json).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                  # then edit APPLICATION_SECRET_KEY
```

Or in VS Code: **Terminal → Run Task… → `setup: venv + install`**.

## Run

**Command line:**

```bash
python run.py
```

**VS Code:** open the **Run and Debug** panel and pick **`Run: Webhook Listener (uvicorn reload)`**, or hit `F5`.

The server listens on [http://localhost:8080](http://localhost:8080):

- `GET /` — health check
- `POST /api/listenevent` — webhook receiver (point your SumTotal webhook endpoint here)
- `GET /docs` — auto-generated OpenAPI / Swagger UI (FastAPI bonus)

## Configure the SumTotal webhook

1. In your SumTotal webhooks configuration page, set the listener URL to `http://<host>:8080/api/listenevent`.
2. Copy the **secretKey** shown in the SumTotal UI for that endpoint into your local `.env`:

   ```
   APPLICATION_SECRET_KEY=<value-from-sumtotal-ui>
   ```

3. If you use plain HTTP, the listener and the SumTotal webhooks processor must reach each other on the same network.
4. Trigger any event — it will hit `POST /api/listenevent` and return a status string:

   - **Secret unset** → `Success and not validated the secret key as secretkey is empty`
   - **Secret set + signature matches** → `Success and validated the secretkey with the payload signature and result is matched and secretkey is :<secret>`
   - **Secret set + signature mismatch** → `Success and validated the secretkey with the payload signature and result is NOT matched and secretkey is : <secret>`

## How signature validation works

The `X-SUMT-Signature` header looks like `t=<unix-timestamp>,v1=<hex-digest>`. The listener:

1. Splits out the timestamp.
2. Computes `HMAC-SHA1(secret, "<timestamp>.<raw-body>")` and hex-encodes it.
3. Rebuilds `t=<timestamp>,v1=<digest>` and compares it to the header value with a constant-time comparison.

See [app/services/listener.py](app/services/listener.py).

## Tests

```bash
pytest -v
```

Or in VS Code: open the **Testing** panel (pytest is preconfigured) or run the **`test: pytest`** task.

## VS Code tooling included

| File | Purpose |
| --- | --- |
| [.vscode/launch.json](.vscode/launch.json) | Debug configs for running the app and pytest |
| [.vscode/tasks.json](.vscode/tasks.json) | One-click venv setup, run, and test tasks |
| [.vscode/settings.json](.vscode/settings.json) | Interpreter path, pytest discovery, format-on-save |
| [.vscode/extensions.json](.vscode/extensions.json) | Recommended extensions (Python, Pylance, debugpy, Black, Ruff, REST Client) |
| [requests.http](requests.http) | REST Client requests you can fire from inside the editor |

---

## Java reference implementation

The original Spring Boot sample lives in [java/](java/) for reference. To run it:

```bash
cd java
./mvnw spring-boot:run         # or import as a Maven project in IntelliJ / STS / Eclipse
```

Mapping between the two implementations:

| Java | Python |
| --- | --- |
| `java/src/main/java/.../WebhookListenerJavaApplication.java` | [app/main.py](app/main.py) |
| `java/src/main/java/.../controller/ListenerController.java` | [app/controllers/listener_controller.py](app/controllers/listener_controller.py) |
| `java/src/main/java/.../service/Listener.java` | [app/services/listener.py](app/services/listener.py) |
| `java/src/main/resources/application.properties` | [.env](.env) (via [app/config.py](app/config.py)) |
| `java/src/test/.../WebhookListenerJavaApplicationTests.java` | [tests/test_listener.py](tests/test_listener.py) |
| `java/pom.xml` | [requirements.txt](requirements.txt) + [pyproject.toml](pyproject.toml) |
| `./mvnw spring-boot:run` | `python run.py` (uvicorn) |

Both expose the same `POST /api/listenevent` route on port `8080` and return identical response strings.
