# 敏感文件读取保护实施计划

> **给智能体开发者：** 按任务逐项执行，每完成一个小步骤都运行对应验证并记录结果。

**目标：** 阻止 Coding Agent 通过 `read_file` 读取常见的本地凭据文件，同时保持普通文件读取正常。

**架构：** 在现有 `Guardrail.check` 的路径检查之后，增加针对 `read_file` 的文件名策略。策略只负责判断和返回错误，不打开文件；`ToolRegistry` 不需要修改。

**技术栈：** Python、pytest、`pathlib.Path`。

## 全局约束

- 只限制 `read_file`，不改变普通写入和命令执行行为。
- 敏感文件名匹配不区分大小写。
- 必须先看到测试失败，再写生产代码。
- 现有测试必须继续全部通过。

---

### 任务 1：为敏感文件读取定义失败测试

**文件：**

- 修改：`tests/test_harness.py`
- 不修改生产代码。

**接口：**

- 使用现有接口：`Guardrail(tmp_path).check(Action("tool", "read_file", {"path": ...}))`。
- 期望接口：敏感路径返回 `ok == False`，普通文件返回 `ok == True`。

- [ ] **步骤 1：增加三个测试**

```python
def test_guardrail_blocks_sensitive_env_file(tmp_path: Path):
    result = Guardrail(tmp_path).check(Action("tool", "read_file", {"path": ".env"}))
    assert not result.ok
    assert "sensitive" in result.error


def test_guardrail_blocks_nested_sensitive_file(tmp_path: Path):
    result = Guardrail(tmp_path).check(Action("tool", "read_file", {"path": "config/.env.production"}))
    assert not result.ok
    assert "sensitive" in result.error


def test_guardrail_allows_ordinary_config_file(tmp_path: Path):
    result = Guardrail(tmp_path).check(Action("tool", "read_file", {"path": "config.json"}))
    assert result.ok
```

- [ ] **步骤 2：运行新增测试，确认它们按预期失败**

运行：

```bash
pytest tests/test_harness.py -k "sensitive or ordinary_config" -v
```

预期：前两个测试失败，因为当前代码还没有敏感文件规则；普通文件测试通过。

- [ ] **步骤 3：提交测试**

```bash
git add tests/test_harness.py
git commit -m "test: define sensitive file read policy"
```

### 任务 2：实现最小敏感文件策略

**文件：**

- 修改：`src/agent_harness/guardrails.py`
- 测试：`tests/test_harness.py`

**接口：**

- 在 `Guardrail.check` 中继续返回现有的 `ToolResult`。
- 敏感文件返回错误信息：`blocked sensitive file`。

- [ ] **步骤 1：在路径边界检查之后增加文件名判断**

规则：

```python
filename = target.name.lower()
if action.name == "read_file" and (
    filename == ".env"
    or filename.startswith(".env.")
    or filename in {"credentials", "secrets"}
):
    return ToolResult(False, "", "blocked sensitive file")
```

- [ ] **步骤 2：运行新增测试，确认全部通过**

```bash
pytest tests/test_harness.py -k "sensitive or ordinary_config" -v
```

- [ ] **步骤 3：运行完整测试集**

```bash
pytest -q
```

- [ ] **步骤 4：提交实现和测试**

```bash
git add src/agent_harness/guardrails.py tests/test_harness.py
git commit -m "feat: block sensitive file reads"
```

### 任务 3：更新说明并同步仓库

**文件：**

- 修改：`README.md`

- [ ] **步骤 1：在安全边界部分补充敏感文件读取规则**

说明 `.env`、`.env.*`、`credentials` 和 `secrets` 默认不能通过 `read_file` 读取。

- [ ] **步骤 2：重新运行完整测试和 demo**

```bash
pytest -q
PYTHONPATH=src python -m agent_harness.cli demo
```

- [ ] **步骤 3：提交并推送**

```bash
git add README.md
git commit -m "docs: explain sensitive file protection"
git push
```
