# PLAN

## 依赖关系

`models/llm` → `tools/guardrail` → `feedback/memory` → `loop/cli` → `tests/docs/package`。

## Tasks

- [x] T1：建立 Python 包、动作模型和 mock LLM；验证 `action_from_json` 与脚本动作。
- [x] T2：实现工作区工具和路径/危险命令护栏；验证危险动作在执行前被拦截。
- [x] T3：实现反馈验证器、记忆和主循环；验证失败反馈能改变下一步动作。
- [x] T4：添加 CLI 机制演示；验证 mock LLM 下可重复复现护栏和反馈闭环。
- [x] T5：补充真实供应商适配、凭据管理说明与最终安全检查。
- [ ] T6：运行最终测试、构建 wheel、配置 CI、创建远程仓库和 Release。

每个未完成 task 都必须在 `AGENT_LOG.md` 中记录实际命令、结果和人工修改。
