import re


def clean_text(text: str) -> str:
    """
    清洗文档文本。
    """

    if not text:
        return ""

    # =========================
    # 统一换行符
    # =========================

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # =========================
    # 清理每一行两端空白
    # =========================

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    # =========================
    # 重新组合文本
    # =========================

    text = "\n".join(lines)

    # =========================
    # 压缩连续空格
    # =========================

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    return text.strip()


def split_sentences(text: str) -> list[str]:
    """
    按照中文和英文标点切分句子。
    """

    if not text:
        return []

    paragraphs = text.split("\n")

    sentences = []

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        parts = re.split(
            r"(?<=[。！？!?；;])\s*|(?<=[.!?;])\s+",
            paragraph
        )

        for part in parts:

            part = part.strip()

            if part:
                sentences.append(part)

    return sentences


def split_long_text(
    text: str,
    chunk_size: int
) -> list[str]:
    """
    对超过 chunk_size 的长句进行切分。

    英文：
        优先按照单词边界切分。

    中文：
        按字符切分。

    注意：
        长句切分时不强制 overlap，
        优先保证 Chunk 的完整性。
    """

    chunks = []

    # =========================
    # 英文文本
    # =========================

    if " " in text:

        words = text.split()

        current_chunk = ""

        for word in words:

            if not current_chunk:

                current_chunk = word

                continue

            candidate = (
                current_chunk
                + " "
                + word
            )

            if len(candidate) <= chunk_size:

                current_chunk = candidate

            else:

                chunks.append(
                    current_chunk
                )

                current_chunk = word

        if current_chunk:

            chunks.append(
                current_chunk
            )

        return chunks

    # =========================
    # 中文文本
    # =========================

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[
            start:end
        ].strip()

        if chunk:

            chunks.append(
                chunk
            )

        start = end

    return chunks


def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> list[str]:
    """
    将文档切分成适合 Embedding / RAG 的 Chunk。

    切分策略：

    1. 清洗文本
    2. 按句子切分
    3. 尽量组合完整句子
    4. 超长英文句子按照单词切分
    5. 超长中文句子按照字符切分
    6. 优先保证语义完整性

    chunk_overlap 参数暂时保留，
    用于保持原有服务接口兼容。
    """

    # =========================
    # 参数检查
    # =========================

    if not text:
        return []

    if chunk_size <= 0:

        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if chunk_overlap < 0:

        raise ValueError(
            "chunk_overlap cannot be negative"
        )

    if chunk_overlap >= chunk_size:

        raise ValueError(
            "chunk_overlap must be smaller than chunk_size"
        )

    # =========================
    # 清洗文本
    # =========================

    text = clean_text(text)

    if not text:
        return []

    # =========================
    # 句子切分
    # =========================

    sentences = split_sentences(text)

    if not sentences:
        return []

    chunks = []

    current_chunk = ""

    # =========================
    # 逐句组合
    # =========================

    for sentence in sentences:

        # =========================
        # 超长句子
        # =========================

        if len(sentence) > chunk_size:

            # 保存当前 Chunk
            if current_chunk:

                chunks.append(
                    current_chunk.strip()
                )

                current_chunk = ""

            # 切分超长句子
            long_chunks = split_long_text(
                sentence,
                chunk_size
            )

            chunks.extend(
                long_chunks
            )

            continue

        # =========================
        # 当前没有 Chunk
        # =========================

        if not current_chunk:

            current_chunk = sentence

            continue

        # =========================
        # 尝试加入下一句
        # =========================

        candidate = (
            current_chunk
            + "\n"
            + sentence
        )

        if len(candidate) <= chunk_size:

            current_chunk = candidate

            continue

        # =========================
        # 超过 Chunk 大小
        # 保存当前 Chunk
        # =========================

        chunks.append(
            current_chunk.strip()
        )

        # =========================
        # 开始新的 Chunk
        # =========================

        current_chunk = sentence

    # =========================
    # 保存最后一个 Chunk
    # =========================

    if current_chunk:

        chunks.append(
            current_chunk.strip()
        )

    # =========================
    # 删除空 Chunk
    # =========================

    chunks = [
        chunk
        for chunk in chunks
        if chunk
    ]

    return chunks