# API 自动化测试脚手架

pytest + httpx 的 HTTP API 测试脚手架。示例用例打公开演示接口 [JSONPlaceholder](https://jsonplaceholder.typicode.com)，不需要私有密钥，本地和 CI 都可以直接通过。

## 如何本地跑

需要 Python 3.10+（CI 使用 3.12）。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

可选：`cp .env.example .env` 后再跑。不创建 `.env` 时使用公开默认地址。

结果：

- 终端输出 pytest 摘要
- JUnit XML：`reports/junit.xml`（已 gitignore）
- 只跑冒烟：`pytest -m smoke`

## 如何改 BASE_URL

共享客户端在 `tests/conftest.py`，地址和 token 从环境变量读取（`config.py`，自动加载项目根目录的 `.env`）。

1. 复制 `.env.example` 为 `.env`
2. 把 `BASE_URL` 改成测试环境根地址，例如 `https://staging.example.com`
3. 需要鉴权时填写 `API_TOKEN`。非空时请求会带 `Authorization: Bearer <token>`
4. 留空或不设置时，回落到 `https://jsonplaceholder.typicode.com`

当前示例按 JSONPlaceholder 的资源编写：

| 文件 | 覆盖 |
| --- | --- |
| `tests/test_posts.py` | `GET /posts/1`、`GET /posts?userId=1`、`POST /posts`、不存在的资源返回 404 |
| `tests/test_users.py` | `GET /users/1` |
| `tests/test_config.py` | `BASE_URL` / `API_TOKEN` 的空值回落，不访问网络 |

换到真实环境后，保留 `client` fixture，按该环境的路径改这些用例或新增 `tests/test_*.py`。

## CI 做什么

工作流：`.github/workflows/api-tests.yml`

- 触发：`push`、`pull_request`、`workflow_dispatch`，以及每天 02:00 UTC 定时跑一次
- 安装 `requirements.txt`，执行 `pytest`
- `BASE_URL`：手动触发时用输入框；否则用仓库 Secret `BASE_URL`。两者都空则用公开默认地址，空仓库也能绿
- 可选 Secret：`API_TOKEN`
- 无论成功失败，都会在 Job Summary 里列出用例结果，并上传 artifact `pytest-junit`（`reports/junit.xml`）

手动跑：Actions → API tests → Run workflow，可临时填写 BASE_URL。
