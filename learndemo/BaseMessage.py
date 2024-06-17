#
# class BaseMessage(Serializable):
#     """基本抽象消息类。
#
#     消息是聊天模型的输入和输出。
#     """
#
#     content: Union[str, List[Union[str, Dict]]]
#     """消息的字符串内容。"""
#
#     additional_kwargs: dict = Field(default_factory=dict)
#     """保留用于消息相关的额外负载数据。
#
#     例如，对于来自 AI 的消息，这可能包括工具调用。"""
#
#     response_metadata: dict = Field(default_factory=dict)
#     """响应元数据。例如：响应头、日志概率、令牌计数。"""
#
#     type: str
#
#     name: Optional[str] = None
#
#     id: Optional[str] = None
#     """消息的可选唯一标识符。理想情况下，应由创建消息的提供者/模型提供。"""
#
#     class Config:
#         extra = Extra.allow
#
#     def __init__(
#             self, content: Union[str, List[Union[str, Dict]]], **kwargs: Any
#     ) -> None:
#         """以位置参数形式传入内容。"""
#         return super().__init__(content=content, **kwargs)
#
#     @classmethod
#     def is_lc_serializable(cls) -> bool:
#         """返回此类是否可序列化。"""
#         return True
#
#     @classmethod
#     def get_lc_namespace(cls) -> List[str]:
#         """获取 langchain 对象的命名空间。"""
#         return ["langchain", "schema", "messages"]
#
#     def __add__(self, other: Any) -> ChatPromptTemplate:
#         from langchain_core.prompts.chat import ChatPromptTemplate
#
#         prompt = ChatPromptTemplate(messages=[self])
#         return prompt + other
#
#     def pretty_repr(self, html: bool = False) -> str:
#         """以漂亮的格式返回消息的表示形式。"""
#         title = get_msg_title_repr(self.type.title() + " Message", bold=html)
#         if self.name is not None:
#             title += f"\nName: {self.name}"
#         return f"{title}\n\n{self.content}"
#
#     def pretty_print(self) -> None:
#         """打印消息的漂亮表示形式。"""
#         print(self.pretty_repr(html=is_interactive_env()))
#
#
# def merge_content(
#         first_content: Union[str, List[Union[str, Dict]]],
#         second_content: Union[str, List[Union[str, Dict]]]
# ) -> Union[str, List[Union[str, Dict]]]:
#     """合并两个消息内容。
#
#     Args:
#         first_content: 第一个内容。
#         second_content: 第二个内容。
#
#     Returns:
#         合并后的内容。
#     """
#     if isinstance(first_content, str):
#         if isinstance(second_content, str):
#             return first_content + second_content
#         else:
#             return_list: List[Union[str, Dict]] = [first_content]
#             return return_list + second_content
#     elif isinstance(second_content, List):
#         merged_list = merge_lists(first_content, second_content)
#         return cast(list, merged_list)
#     else:
#         if isinstance(first_content[-1], str):
#             return first_content[:-1] + [first_content[-1] + second_content]
#         else:
#             return first_content + [second_content]
#
#
# class BaseMessageChunk(BaseMessage):
#     """消息块，可以与其他消息块连接。"""
#
#     @classmethod
#     def get_lc_namespace(cls) -> List[str]:
#         """获取 langchain 对象的命名空间。"""
#         return ["langchain", "schema", "messages"]
#
#     def __add__(self, other: Any) -> BaseMessageChunk:
#         if isinstance(other, BaseMessageChunk):
#             return self.__class__(
#                 id=self.id,
#                 content=merge_content(self.content, other.content),
#                 additional_kwargs=merge_dicts(
#                     self.additional_kwargs, other.additional_kwargs
#                 ),
#                 response_metadata=merge_dicts(
#                     self.response_metadata, other.response_metadata
#                 ),
#             )
#         else:
#             raise TypeError(
#                 'unsupported operand type(s) for +: "'
#                 f"{self.__class__.__name__}"
#                 f'" and "{other.__class__.__name__}"'
#             )
#
#
# def message_to_dict(message: BaseMessage) -> dict:
#     """将消息转换为字典。
#
#     Args:
#         message: 要转换的消息。
#
#     Returns:
#         消息的字典表示形式。
#     """
#     return {"type": message.type, "data": message.dict()}
#
#
# def messages_to_dict(messages: Sequence[BaseMessage]) -> List[dict]:
#     """将一系列消息转换为字典列表。
#
#     Args:
#         messages: 要转换的消息序列（作为 BaseMessages）。
#
#     Returns:
#         消息的字典列表。
#     """
#     return [message_to_dict(m) for m in messages]
#
#
# def get_msg_title_repr(title: str, *, bold: bool = False) -> str:
#     """获取消息的标题表示形式。
#
#     Args:
#         title: 标题。
#         bold: 是否加粗标题。
#
#     Returns:
#         标题的表示形式。
#     """
#     padded = " " + title + " "
#     sep_len = (80 - len(padded)) // 2
#     sep = "=" * sep_len
#     second_sep = sep + "=" if len(padded) % 2 else sep
#     if bold:
#         padded = get_bolded_text(padded)
#     return f"{sep}{padded}{second_sep}"
