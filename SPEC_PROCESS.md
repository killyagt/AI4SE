# SPEC_PROCESS

本文件记录本项目真实的设计过程。反思报告仍需学生本人根据实际体验重新组织和撰写。

## 设计迭代

1. 从“做一个复杂 coding agent”收缩为“可测试的最小 harness”；原因是截止时间和评分重点都要求机制深度而非代码量。
2. 从 WebUI 改为 CLI + Release；原因是 QQ 通知明确允许 CLI-only 项目提供 Release 链接。
3. 将主要贡献确定为“治理护栏 + 反馈闭环”；原因是二者能脱离真实 LLM 进行确定性单元测试。

## 真实决策记录

- 2026-08-09：学生确认选择作业 A，并确认在 2026-08-11 中午前按 CLI 方案完成。
- 2026-08-09：学生确认上述设计，允许继续实现。
- 2026-08-09：由于时间限制，明确不加入 WebUI、多 Agent、向量数据库和云服务。

## TDD 证据

在已有最小护栏草稿基础上，新增 PowerShell 删除命令的安全回归测试：

- RED：`pytest -q tests/test_harness.py::test_guardrail_blocks_powershell_delete_command` 输出 `F`。
- GREEN：加入 `remove-item` 和 `clear-content` 规则后，`pytest -q --basetemp D:\AI4SE\pytest-temp-green` 输出 `.... [100%]`。

## 尚需补充的过程证据

正式提交前请补充真实 brainstorming 对话节选、每轮提问、采纳/否决决策，以及第二种智能体仅阅读 SPEC + PLAN 后的冷启动反馈。不要编造尚未发生的冷启动结果。
