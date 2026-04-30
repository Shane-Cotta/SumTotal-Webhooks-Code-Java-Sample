<p align="center" width="100%">
    <img src="https://marketplace.sumtotalsystems.com/content/images/vendor/SumTotal_logo.png">
</p>

# SumTotal Sample Code to Demonstrate Webhook/Event Usage

This repository contains two equivalent reference implementations of a SumTotal webhook listener:

| Implementation | Location | Stack |
| --- | --- | --- |
| **Java** (original) | repository root ([src/](src/), [pom.xml](pom.xml)) | Java 11, Spring Boot 2.7, Maven |
| **Python** (new port) | [python/](python/) | Python 3.9+, FastAPI, uvicorn, pytest |

Both expose `POST /api/listenevent` on port `8080`, validate the `X-SUMT-Signature` header with HMAC-SHA1, and return identical response strings. Pick whichever stack matches your environment.

---

## Python version (recommended)

Full setup, run, and VS Code instructions live in [python/README.md](python/README.md). Quick start:

```bash
cd python
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env                  # then edit APPLICATION_SECRET_KEY
python run.py
```

The Python project ships with a complete VS Code workflow — `launch.json`, `tasks.json`, `settings.json`, recommended extensions, and a `requests.http` for in-editor REST testing. Open the [python/](python/) folder in VS Code and press `F5` to run.

---

## Java version (original)

### Pre-requisites
1. JDK latest version (Java 11 is used in this project).
2. Tomcat embedded Spring Tool Suite / Eclipse.

### Setup Guide
1. Download the Source Code from GitHub Location.
2. Open SpringToolSuite/Eclipse in administration Mode.
3. Import the Project as Existing Maven Project (From File select Import, select Maven, then select existing Maven projects. After that select project location and project name).
4. Now right click on project and Run the project as Spring Boot App.
5. This will host the webhooklisterner and default browser url will be: [http://localhost:8080/](http://localhost:8080/)
6. Now the project is ready to receive the API calls. You can hit the project using the URL (http://localhost:8080/api/listenevent) or you can give your machinename in place of localhost in URL.

---

## Steps (apply to both implementations)
1. Provide the webhooklisterner URL in the webhooks configuration page, e.g. [http://localhost:8080/api/listenevent](http://localhost:8080/api/listenevent) or `http://machinename/api/listenevent`.
2. If you are using HTTP, make sure the webhooks processor host and this sample project are hosted in the same domain/network — otherwise the URL won't reach the project when an event triggers.
3. Trigger any event. It will call the POST handler at `/api/listenevent`.
4. To validate the payload signature in the request header, copy the `secretKey` from the webhook endpoint UI and update [src/main/resources/application.properties](src/main/resources/application.properties) (Java) or `python/.env` (Python).

Trigger any event and the response body will tell you whether the signature matched:
* **Secret key empty** → `Success and not validated the secret key as secretkey is empty`
* **Secret key set, signature matches** → `Success and validated the secretkey with the payload signature and result is matched and secretkey is : xxxxx`
* **Secret key set, signature mismatch** → `Success and validated the secretkey with the payload signature and result is NOT matched and secretkey is : xxxxx`
