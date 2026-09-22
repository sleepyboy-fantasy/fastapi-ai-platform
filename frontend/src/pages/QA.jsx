import { useState } from "react";
import { useNavigate } from "react-router-dom";
import request from "../api/request";

function QA() {
    const navigate = useNavigate();

    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [sources, setSources] = useState([]);
    const [loading, setLoading] = useState(false);

    async function handleAsk() {
        if (!question.trim()) {
            alert("请输入问题");
            return;
        }

        setLoading(true);
        setAnswer("");
        setSources([]);

        try {
            const res = await request.post("/qa/ask", {
                question: question
            });

            setAnswer(res.data.answer || "");
            setSources(res.data.sources || []);
        } catch (error) {
            console.log("问答失败：", error);

            if (error.response) {
                console.log("状态码：", error.response.status);
                console.log("后端返回：", error.response.data);

                if (error.response.status === 401) {
                    localStorage.removeItem("token");
                    navigate("/");
                    return;
                }

                alert(
                    "问答失败：" +
                    JSON.stringify(error.response.data)
                );
            } else {
                alert("问答失败：" + error.message);
            }
        } finally {
            setLoading(false);
        }
    }

    function handleKeyDown(event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            handleAsk();
        }
    }

    return (
        <div>
            <header>
                <h1>AI 知识库平台</h1>

                <button onClick={() => navigate("/dashboard")}>
                    返回首页
                </button>
            </header>

            <main>
                <h2>AI 智能问答</h2>

                <p>
                    基于知识库中的文档内容进行智能问答。
                </p>

                <div>
                    <textarea
                        rows="5"
                        cols="60"
                        placeholder="请输入你的问题，例如：第三个知识库测试文档是用来做什么的？"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                </div>

                <br />

                <button
                    onClick={handleAsk}
                    disabled={loading}
                >
                    {loading ? "正在思考..." : "发送问题"}
                </button>

                {answer && (
                    <div>
                        <hr />

                        <h3>AI 回答</h3>

                        <p>
                            {answer}
                        </p>
                    </div>
                )}

                {sources.length > 0 && (
                    <div>
                        <h3>参考资料</h3>

                        {sources.map((source) => (
                            <div
                                key={source.id}
                                style={{
                                    border: "1px solid #ddd",
                                    padding: "10px",
                                    marginBottom: "10px"
                                }}
                            >
                                <p>
                                    <strong>
                                        来源 #{source.id}
                                    </strong>
                                </p>

                                <p>
                                    {source.content}
                                </p>

                                <p>
                                    相似度距离：
                                    {source.distance.toFixed(4)}
                                </p>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

export default QA;