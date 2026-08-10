# Safe Coding Agent Harness

这是一个面向编程任务的命令行 Coding Agent Harness。它提供文件读写、命令执行、反馈和记忆，并在工具执行前检查危险操作。

## 安装与运行

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
agent-harness demo
pytest
```

也可以直接运行：

```bash
python -m agent_harness.cli demo
```

## 分发

```bash
python -m pip install build
python -m build
python -m pip install dist/safe_coding_agent_harness-0.1.0-py3-none-any.whl
```

当前 Release：<https://github.com/killyagt/AI4SE/releases/tag/v0.1.0>

本项目是 CLI-only 原型，不提供 WebUI。真实 API key 应通过环境变量或操作系统凭据管理器配置，不能写入源码或 Git。

## 安全边界

- 文件工具不能访问工作区之外的路径。
- `read_file` 默认拒绝 `.env`、`.env.*`、`credentials` 和 `secrets`。
- `rm`、`del`、`format`、关机、重启等危险命令会被拦截。
- mock LLM 演示不需要网络和 API key。
- 当前版本不是完整的操作系统级 sandbox，命令执行仍依赖宿主系统。

## 目录结构

```text
src/agent_harness/  核心代码
tests/              自动化测试
demo/               机制演示
```

## 已知限制

当前版本是单进程、单 agent、CLI 原型，使用 mock LLM 进行离线测试。真实 LLM、交互式人工审批和完整 sandbox 仍需后续实现。
