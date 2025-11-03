# 主动回复插件 (ActiveReplyPlugin)

## 功能说明

当机器人被拉入群聊时，自动发送包含AI助手功能介绍的富文本欢迎消息。

## 特性

- ✅ 自动检测机器人加入群聊事件
- ✅ 发送富文本欢迎消息（包含图片、格式化文本）
- ✅ 可配置欢迎消息内容
- ✅ 可配置发送延迟时间
- ✅ 支持启用/禁用功能

## 工作原理

1. 监听 `group_increase` 通知事件
2. 检查加入群聊的用户是否为机器人本身
3. 延迟指定时间后发送欢迎消息

## 配置方法

### 基本配置

插件默认配置:
- **机器人QQ**: 自动从框架获取，或使用默认值 `xxx`
- **回复消息**: 富文本欢迎消息（包含AI功能介绍和使用教程）
- **延迟时间**: `1` 秒
- **启用状态**: `True`

### 欢迎消息内容

默认欢迎消息包含:
- 🤖 机器人自我介绍
- ✨ 功能列表（）
- 📖 使用示例
- 🖼️ 配图（pictures/tx1.png）
- 💡 使用提示

### 自定义配置

在代码中修改 `plugins/active_reply_plugin/plugin.py`:

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.bot_id = "你的机器人QQ号"
    self.enabled = True
    self.delay_seconds = 1
    
    # 自定义欢迎消息
    self.reply_message = self._create_welcome_message()
```

### 自定义欢迎消息

修改 `_create_welcome_message` 方法来自定义消息内容:

```python
def _create_welcome_message(self):
    return MessageArray([
        "你的欢迎文字\n",
        Text("格式化文本\n"),
        Image(r"你的图片路径.png"),
        Text("更多内容...")
    ])
```

### 动态配置（通过插件API）

```python
from ncatbot.core import MessageArray, Text, Image

# 获取插件实例
plugin = status.plugin_manager.get_plugin("ActiveReplyPlugin")

# 设置简单文本消息
plugin.set_reply_message("欢迎来到本群！")

# 设置富文本消息
custom_message = MessageArray([
    "欢迎！\n",
    Text("这是一个学习群\n"),
    Image(r"your_image.png")
])
plugin.set_reply_message(custom_message)

# 设置延迟时间（秒）
plugin.set_delay(2)

# 启用/禁用插件
plugin.set_enabled(True)  # 或 False
```

## 日志示例

### 成功运行
```
[11:19:40] INFO - 主动回复插件已加载，机器人QQ: xxx
[11:20:24] INFO - 检测到机器人被拉入群 xxxxx
[11:20:25] INFO - 已向群 XXXX 发送欢迎消息
```

### 其他用户加入
```
[11:20:24] DEBUG - 群成员增加，但不是机器人: 用户=xxxxx
```

## 技术细节

- **事件类型**: `ncatbot.notice_event`
- **通知类型**: `group_increase`
- **优先级**: `10`
- **框架**: NcatBot
- **版本**: `1.0.1`

## 常见问题

### Q: 为什么机器人没有自动回复？

A: 检查以下几点:
1. 插件是否正确加载（查看启动日志）
2. `bot_id` 是否正确设置
3. 插件是否被禁用（`self.enabled = False`）

### Q: 如何修改欢迎消息？

A: 修改 `__init__` 方法中的 `self.reply_message`，或使用 `set_reply_message()` 方法。

### Q: 延迟时间有什么用？

A: 确保机器人完全加入群聊后再发送消息，避免消息发送失败。

## 更新日志

### v1.0.1 (2025-10-03)
- 优化代码结构，移除调试日志
- 简化事件处理逻辑
- 改进错误处理
- 添加配置方法

### v1.0.0 (2025-10-03)
- 初始版本
- 基本的自动回复功能
