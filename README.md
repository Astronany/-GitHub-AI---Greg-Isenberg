# API 自动化测试脚手架

pytest + httpx 的 HTTP API 测试脚手架。被测系统是本仓库里的**演示业务 API**（一个迷你商店：用户、商品、订单），不是第三方生产系统，也不依赖 JSONPlaceholder 或付费托管。

本地和 GitHub Actions 默认在进程内挂载这个应用，不需要先启动服务，也不需要仓库 Secret。以后如果有真实测试环境，用 `BASE_URL` 和 `API_TOKEN` 把同一套客户端指过去。

## 演示 API 是什么

`app/` 是一个 FastAPI 应用，数据在进程内存里，退出即丢。它专门给这套云测试环境当可控的被测系统：路径、状态码和鉴权都由我们决定。

| 方法 | 路径 | 鉴权 | 说明 |
| --- | --- | --- | --- |
| GET | `/health` | 否 | 存活检查 |
| GET | `/users`、`/users/{id}` | 否 | 用户列表 / 详情，未知 id 返回 404 |
| POST | `/users` | Bearer | 创建用户，重复邮箱返回 409 |
| GET | `/items`、`/items/{id}` | 否 | 商品目录，未知 id 返回 404 |
| GET | `/orders`、`/orders/{id}` | Bearer | 订单列表 / 详情，未知 id 返回 404 |
| POST | `/orders` | Bearer | 创建订单；用户或商品不存在返回 400 |

种子数据（进程启动或进程内测试重置后）：

| 资源 | 数据 |
| --- | --- |
| 用户 | `1` Ada Lovelace `ada` / `ada@example.com`；`2` Grace Hopper `grace` / `grace@example.com` |
| 商品 | `1` Field notebook `NB-100` 1299 分；`2` Graphite pencil `PN-010` 199 分 |
| 订单 | `1` 用户 1、商品 1、数量 2、状态 `placed` |

交互文档在服务启动后的 `/docs`。

### 演示 token

公开默认值是 **`demo-token`**。`API_TOKEN` 留空时，服务端和测试客户端都用这个值，所以本地和 CI 不用配置 GitHub Secrets。

这是写在仓库里的演示口令，不是任何第三方产品的凭证。接到真实环境时改掉它，不要把生产密钥提交进仓库。

## 如何启动 API

需要 Python 3.10+（CI 使用 3.12）。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/users/1
curl -s -H "Authorization: Bearer demo-token" http://127.0.0.1:8000/orders
```

只想跑测试的话可以跳过这一步。pytest 默认不监听端口。

## 如何跑测试

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

不创建 `.env`、不设置 `BASE_URL` 时，`tests/conftest.py` 用 httpx 的 `ASGITransport` 在进程内调用 `app.main:app`（异步客户端）。每条用例开始前会重置内存种子数据。

结果：

- 终端输出 pytest 摘要
- JUnit XML：`reports/junit.xml`（已 gitignore）
- 只跑冒烟：`pytest -m smoke`

对着已经启动的 uvicorn 跑（验证真实 HTTP，而不是进程内传输）：

```bash
BASE_URL=http://127.0.0.1:8000 API_TOKEN=demo-token pytest
```

## 如何改 BASE_URL / API_TOKEN

配置在 `config.py`，自动加载项目根目录的 `.env`。已经导出的环境变量优先于 `.env`。

1. 复制 `.env.example` 为 `.env`
2. `BASE_URL` 留空：进程内演示 API。填写则请求该根地址，例如 `http://127.0.0.1:8000`，或将来的 `https://staging.example.com`
3. `API_TOKEN` 留空：使用 `demo-token`。填写则请求带 `Authorization: Bearer <token>`，演示 API 也用同一个值校验
4. 地址末尾的 `/` 会被去掉

将来换成契约不同的环境时，保留 `client` fixture，按那个环境的路径改 `tests/test_*.py`。当前用例描述的是本仓库演示 API 的合同（种子 id、状态码、Bearer 鉴权）。

## CI 做什么

工作流：`.github/workflows/api-tests.yml`

- 触发：`push`、`pull_request`、`workflow_dispatch`，以及每天 02:00 UTC 定时跑一次
- 安装 `requirements.txt`（含 FastAPI / uvicorn），执行 `pytest`
- 默认 `BASE_URL` 为空，在 runner 进程内挂载演示 API，不另起服务，也不访问外网
- 未配置 Secret 时 `API_TOKEN` 使用 `demo-token`，空仓库也能绿
- 手动触发可临时填写 `BASE_URL`。仓库 Secret `BASE_URL` / `API_TOKEN` 留给以后的真实测试环境
- 无论成功失败，都会在 Job Summary 里列出用例结果，并上传 artifact `pytest-junit`（`reports/junit.xml`）

手动跑：Actions → API tests → Run workflow，可临时填写 BASE_URL。
