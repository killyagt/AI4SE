# Safe Coding Agent Harness

一个面向软件开发任务的、可测试的 Coding Agent Harness。它把 LLM 的决策放在确定性的工程控制层之后：工具分发、危险动作护栏、客观反馈、记忆和停机条件都由本项目代码实现。

## 为什么有人会用

普通 LLM 只能提出下一步建议，不能安全、稳定地读写项目和运行测试。本工具提供一个小而清晰的运行时，让 coding agent 可以执行工具、接收测试反馈，并在危险动作处暂停。它支持 mock LLM 离线运行，便于测试和审计。

## 安装与运行

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
agent-harness demo
pytest
```

## 分发

```bash
python -m pip install build
python -m build
python -m pip install dist/safe_coding_agent_harness-0.1.0-py3-none-any.whl
```

发布时将 `dist/` 中的 wheel 上传到 GitHub/NJU Git Release。CLI-only 项目使用 Release 链接作为发布入口，不需要 WebUI。

## 安全边界

- 默认工作区边界阻止文件工具访问工作区之外的路径。
- `rm`、`del`、`format`、关机、重启等危险命令由代码护栏拦截。
- mock LLM 演示不访问网络，也不需要 API key。
- 真实供应商适配器必须从环境或操作系统凭据管理器读取 key，不得写入源码、日志或 Git。
- 运行命令仍应在隔离的测试仓库中使用；本项目不是完整的操作系统级 sandbox。

## 目录结构

```text
src/agent_harness/  harness 内核
tests/              mock 驱动的确定性测试
demo/               机制演示
```

## 已知限制

当前版本是单进程、单 agent、CLI 原型；命令执行依赖宿主操作系统，真实 LLM 供应商适配和完整 OS sandbox 需要后续扩展。

运行时规则也可以放在 JSON 配置中，例如 `{"max_steps": 3, "blocked_commands": ["custom-danger"]}`，再通过 `HarnessConfig.from_json()` 加载。

可选的真实 API key 管理：

```bash
python -m pip install ".[credentials]"
python -c "from agent_harness.credentials import set_api_key; set_api_key('provider')"
```

key 写入操作系统凭据管理器，不会在终端回显；环境变量仅作为兼容性兜底，并明确存在进程可见风险。
