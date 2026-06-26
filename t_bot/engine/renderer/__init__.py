from abc import ABC, abstractmethod

from rich.text import Text

from t_bot.transform.vector import Vector2i


class BaseRenderer(ABC):
    """行缓冲渲染器基类。

    buffer 每行存储为 ``rich.text.Text`` 对象，保留富文本样式信息。
    所有对外方法（add_line / append_current / replace_at）均接受 ``str | Text``。
    """

    def __init__(self) -> None:
        self.buffer: list[Text] = []

    @abstractmethod
    def render(self) -> None:
        """子类实现：向 buffer 中填充渲染内容。"""
        pass

    # ------------------------------------------------------------------
    # 行级操作
    # ------------------------------------------------------------------

    def add_line(self, line: str | Text) -> None:
        """向 buffer 末尾追加一行。

        Args:
            line: 纯文本字符串或带样式的 ``Text`` 对象。
        """
        if isinstance(line, str):
            line = Text(line)
        self.buffer.append(line)

    def append_current(self, data: str | Text) -> None:
        """向 buffer 最后一行的末尾追加内容。

        Args:
            data: 纯文本字符串或带样式的 ``Text`` 对象。
        """
        if isinstance(data, str):
            data = Text(data)
        self.buffer[-1] = self.buffer[-1] + data

    # ------------------------------------------------------------------
    # 精确替换
    # ------------------------------------------------------------------

    def replace_at(
        self,
        position: Vector2i,
        new_str: str | Text,
        length_override: int = -1,
    ) -> None:
        """在 buffer 的 (col, row) 位置替换 / 插入一段文本。

        以*可见字符*（``.plain`` 长度）为坐标进行定位和覆盖，
        因此富文本标记不会干扰列对齐。

        Args:
            position: 目标坐标，``x`` 为列，``y`` 为行。
            new_str:  要写入的文本（支持富文本样式）。
            length_override: 覆盖长度；``-1`` 表示使用 ``new_str`` 的可见宽度。
        """
        # ---- 统一为 Text ----
        if isinstance(new_str, str):
            new_str = Text(new_str)

        n = length_override if length_override >= 0 else len(new_str.plain)
        row = position.y
        col = position.x

        # ---- 确保目标行存在 ----
        while len(self.buffer) <= row:
            self.buffer.append(Text(""))

        line = self.buffer[row]

        # ---- 用空格填充到 col ----
        current_len = len(line.plain)
        if current_len < col:
            line = line + Text(" " * (col - current_len))

        # ---- 用空格填充到 col + n ----
        if len(line.plain) < col + n:
            line = line + Text(" " * (col + n - len(line.plain)))

        # ---- 以 plain 坐标为界切分，替换中间段 ----
        parts = line.divide([col, col + n])
        line = parts[0] + new_str + parts[2]
        self.buffer[row] = line

    # ------------------------------------------------------------------
    # 输出
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """清空 buffer。"""
        self.buffer.clear()

    def read(self) -> str:
        """将 buffer 中所有行拼接为带标记的字符串。"""
        return "\n".join(line.markup for line in self.buffer)

    def redraw(self) -> str:
        """清空 → 重新 render → 返回标记字符串。"""
        self.clear()
        self.render()
        return self.read()
