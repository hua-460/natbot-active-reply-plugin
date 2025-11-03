"""
主动回复插件 - 核心实现
"""

import asyncio
from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.core.event import NoticeEvent
from ncatbot.core import MessageArray, Text, Image
from ncatbot.utils import get_log, status

LOG = get_log(__name__)


class ActiveReplyPlugin(NcatBotPlugin):
    """主动回复插件 - 当机器人被拉入群聊时自动发送欢迎消息"""
    
    name = "ActiveReplyPlugin"
    author = "Ray."
    desc = "当机器人被拉进群里时自动回复"
    version = "1.0.1"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot_id = "xxx"  # 机器人QQ号（默认值）
        self.enabled = True  # 是否启用主动回复
        self.delay_seconds = 1  # 延迟发送时间（秒）
        
        # 创建富文本欢迎消息
        self.reply_message = self._create_welcome_message()
    
    async def on_load(self):
        """插件加载时的初始化"""
        try:
            # 优先使用框架提供的bot_id，否则使用默认值
            bot_id_from_status = getattr(status, 'bot_id', None) or getattr(status, 'self_id', None)
            if bot_id_from_status:
                self.bot_id = str(bot_id_from_status)
            
            LOG.info(f"主动回复插件已加载，机器人QQ: {self.bot_id}")
            
            # 注册通知事件处理器
            self.register_handler(
                "ncatbot.notice_event",
                self._handle_notice_event,
                priority=10
            )
            
        except Exception as e:
            LOG.error(f"主动回复插件初始化失败: {str(e)}")
    
    async def _handle_notice_event(self, event):
        """处理通知事件"""
        try:
            notice_data = event.data
            
            # 只处理群成员增加事件
            if notice_data.notice_type != 'group_increase':
                return
            
            # 检查是否是机器人自己被拉入群聊
            if str(notice_data.user_id) != str(self.bot_id):
                LOG.debug(f"群成员增加，但不是机器人: 用户={notice_data.user_id}")
                return
            
            LOG.info(f"检测到机器人被拉入群 {notice_data.group_id}")
            
            # 延迟发送，确保机器人完全加入群聊
            await asyncio.sleep(self.delay_seconds)
            
            # 发送欢迎消息
            await self._send_group_reply(notice_data.group_id)
                
        except Exception as e:
            LOG.error(f"处理通知事件时出错: {str(e)}")
    
    def _create_welcome_message(self):
        """创建富文本欢迎消息"""
        try:
            return MessageArray([
                "🤖 大家好！我是通义千问驱动的协作学习AI助手\n",
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n",
                
                Text("📱 如何与我对话？\n"),
                Text("方法1：长按我的头像 → 选择\"@Ta\" → 输入问题\n"),
                Text("方法2：手动输入 @机器人昵称 + 空格 + 问题\n"),
                Text("💡 提示：必须@我才能触发对话哦！\n\n"),
                
                Text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"),
                Text("✨ 我的核心功能：\n\n"),
                
                Text("1️⃣ 智能对话（支持多轮对话）\n"),
                Text("   用法：@我 + 你的问题\n"),
                Text("   示例：@Napcat-Robot 什么是人工智能？\n"),
                Text("   特点：自动记住上下文，支持连续提问\n\n"),
                
                Text("2️⃣ 反思式学习（深度思考模式）\n"),
                Text("   用法：@我 反思：+ 你的思考问题\n"),
                Text("   示例：@Napcat-Robot 反思：今天学到了什么？\n"),
                Text("   流程：\n"),
                Text("   → 提出反思问题\n"),
                Text("   → 我引导你分享初步想法\n"),
                Text("   → 你回复时带上\"我的想法\"\"我认为\"等字眼\n"),
                Text("   → 我提供深度分析和知识拓展\n"),
                Text("   特点：支持多人协作反思，对比不同观点\n\n"),
                
                Text("3️⃣ 群聊讨论整合（智能总结）\n"),
                Text("   用法：@我 整合\n"),
                Text("   示例：@Napcat-Robot 整合\n"),
                Text("   功能：总结最近100条群聊消息\n"),
                Text("   包含：主要话题、重要信息、关注问题\n\n"),
                
                Text("4️⃣ 图片识别理解\n"),
                Text("   用法：发送图片 + @我 + 问题\n"),
                Text("   示例：[发送图片] @Napcat-Robot 这张图讲的是什么？\n"),
                Text("   支持：图表、截图、手写笔记等\n\n"),
                
                Text("5️⃣ 文件解析（文档理解）\n"),
                Text("   用法：发送文件 → @我 解析文件+问题\n"),
                Text("   支持：PDF、Word、Excel等\n"),
                Text("   功能：提取关键信息、总结内容\n\n"),
                
                Text("6️⃣ 联网搜索（实时信息）\n"),
                Text("   自动触发：检测到需要最新信息时自动联网\n"),
                Text("   功能：获取最新资讯、实时数据\n\n"),
                
                Text("7️⃣ 对话管理\n"),
                Text("   清空历史：@我 清空历史\n"),
                Text("   结束反思：@我 结束本轮REFLECT\n\n"),
                
                Image(r"pictures/tx1.png"),
                
                Text("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"),
                Text("🎯 协作学习最佳实践：\n\n"),
                
                Text("✅ 请立即修改群昵称\n"),
                Text("   格式：班级+姓名（如：教育1班-张三）\n"),
                Text("   作用：方便协作学习，我能更好地记录和对比大家的观点\n\n"),
                
                Text("✅ 请将本消息设置为精华\n"),
                Text("   操作：长按本消息 → 设为精华\n"),
                Text("   作用：方便随时查阅使用教程\n\n"),
                
                Text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"),
                Text("📚 完整使用示例：\n\n"),
                
                Text("场景1：普通提问\n"),
                Text("学生：@Napcat-Robot 什么是机器学习？\n"),
                Text("我：[详细解答]\n"),
                Text("学生：@Napcat-Robot 能举个例子吗？\n"),
                Text("我：[基于上下文继续解答]\n\n"),
                
                Text("场景2：反思学习\n"),
                Text("学生A：@Napcat-Robot 反思：编程的本质是什么？\n"),
                Text("我：请分享您的初步想法...\n"),
                Text("学生A：@Napcat-Robot 我认为编程是解决问题的工具\n"),
                Text("学生B：@Napcat-Robot 我觉得编程是一种思维方式\n"),
                Text("我：[综合分析两位同学的观点，提供深度见解]\n\n"),
                
                Text("场景3：图文理解\n"),
                Text("学生：[发送流程图] @Napcat-Robot 帮我分析这个算法流程\n"),
                Text("我：[识别图片内容并详细分析]\n\n"),
                
                Text("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"),
                Text("💡 温馨提示：\n"),
                Text("• 我会记住每次对话的上下文\n"),
                Text("• 多人可以同时向我提问，共享知识\n"),
                Text("• 反思模式特别适合深度学习和小组讨论\n"),
                Text("• 遇到问题随时@我，让我们一起学习进步！\n\n"),
                
                Text("🌟 开始你的协作学习之旅吧！")
            ])
        except Exception as e:
            LOG.error(f"创建欢迎消息失败: {str(e)}")
            # 如果富文本创建失败，使用简单文本
            return "🤖 大家好！我是AI助手，@我即可开始对话！"
    
    async def _send_group_reply(self, group_id: int):
        """发送群聊回复消息"""
        try:
            if not self.enabled:
                LOG.debug("主动回复功能已禁用")
                return
            
            # 如果是MessageArray对象，需要转换为列表
            if isinstance(self.reply_message, MessageArray):
                message_to_send = self.reply_message.to_list()
            else:
                message_to_send = self.reply_message
            
            await status.global_api.send_group_msg(
                group_id=group_id,
                message=message_to_send
            )
            LOG.info(f"已向群 {group_id} 发送欢迎消息")
                
        except Exception as e:
            LOG.error(f"发送群聊消息失败: {str(e)}")
            import traceback
            LOG.error(f"错误详情: {traceback.format_exc()}")
    
    # ==================== 配置方法 ====================
    
    def set_reply_message(self, message):
        """
        设置回复消息内容
        
        Args:
            message: 可以是字符串或MessageArray对象
        """
        self.reply_message = message
        LOG.info("已更新回复消息")
    
    def set_enabled(self, enabled: bool):
        """设置是否启用主动回复"""
        self.enabled = enabled
        LOG.info(f"主动回复已{'启用' if enabled else '禁用'}")
    
    def set_delay(self, seconds: int):
        """设置延迟发送时间（秒）"""
        self.delay_seconds = max(0, seconds)
        LOG.info(f"已设置延迟时间: {self.delay_seconds}秒")

