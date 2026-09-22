import {
    useEffect,
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import request from "../api/request";


function Documents() {

    const navigate = useNavigate();

    const [documents, setDocuments] = useState([]);

    const [loading, setLoading] = useState(true);

    const [uploading, setUploading] = useState(false);

    const [selectedFile, setSelectedFile] = useState(null);


    // =========================
    // 获取文档列表
    // =========================
    async function loadDocuments() {

        try {

            const res =
                await request.get(
                    "/documents",
                    {
                        params: {
                            page: 1,
                            page_size: 20
                        }
                    }
                );


            console.log(
                "文档列表：",
                res.data
            );


            setDocuments(
                res.data.items || []
            );


        } catch (error) {

            console.log(
                "获取文档失败：",
                error
            );


            if (
                error.response &&
                error.response.status === 401
            ) {

                localStorage.removeItem(
                    "token"
                );

                navigate("/");

            }

        } finally {

            setLoading(false);

        }

    }


    useEffect(() => {

        loadDocuments();

    }, []);


    // =========================
    // 选择文件
    // =========================
    function handleFileChange(event) {

        const file =
            event.target.files[0];

        if (!file) {

            setSelectedFile(null);

            return;

        }


        const fileName =
            file.name.toLowerCase();


        if (
            !fileName.endsWith(".txt") &&
            !fileName.endsWith(".pdf")
        ) {

            alert(
                "目前只支持 TXT 和 PDF 文件"
            );

            event.target.value = "";

            setSelectedFile(null);

            return;

        }


        setSelectedFile(file);

    }


    // =========================
    // 上传文件
    // =========================
    async function handleUpload() {

        if (!selectedFile) {

            alert("请先选择文件");

            return;

        }


        const formData =
            new FormData();

        formData.append(
            "file",
            selectedFile
        );


        try {

            setUploading(true);


            const res =
                await request.post(
                    "/documents/upload",
                    formData
                );


            console.log(
                "上传成功：",
                res.data
            );


            alert("文档上传成功");


            setSelectedFile(null);


            document.getElementById(
                "document-file"
            ).value = "";


            await loadDocuments();


        } catch (error) {

            console.log(
                "上传失败：",
                error
            );


            if (error.response) {

                console.log(
                    "后端返回：",
                    error.response.data
                );


                alert(
                    "上传失败：" +
                    JSON.stringify(
                        error.response.data
                    )
                );

            } else {

                alert(
                    "上传失败：" +
                    error.message
                );

            }

        } finally {

            setUploading(false);

        }

    }


    // =========================
    // 删除文档
    // =========================
    async function handleDelete(
        documentId
    ) {

        const confirmed =
            window.confirm(
                "确定要删除这个文档吗？"
            );


        if (!confirmed) {

            return;

        }


        try {

            await request.delete(
                `/documents/${documentId}`
            );


            alert("删除成功");


            await loadDocuments();


        } catch (error) {

            console.log(
                "删除失败：",
                error
            );


            alert(
                "删除失败：" +
                (
                    error.response?.data
                    ? JSON.stringify(
                        error.response.data
                    )
                    : error.message
                )
            );

        }

    }


    // =========================
    // 页面
    // =========================
    return (

        <div>

            <header>

                <h1>
                    AI 知识库平台
                </h1>


                <button
                    onClick={
                        () => navigate("/dashboard")
                    }
                >
                    返回工作台
                </button>

            </header>


            <main>

                <h2>
                    文档管理
                </h2>


                <p>
                    上传 TXT 或 PDF 文档，建立你的个人知识库
                </p>


                <hr />


                {/* 上传区域 */}

                <section>

                    <h3>
                        上传知识库文档
                    </h3>


                    <input
                        id="document-file"
                        type="file"
                        accept=".txt,.pdf"
                        onChange={
                            handleFileChange
                        }
                    />


                    <br />


                    <br />


                    {
                        selectedFile && (

                            <p>
                                已选择：
                                {selectedFile.name}
                            </p>

                        )
                    }


                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                    >
                        {
                            uploading
                                ? "正在上传..."
                                : "上传文档"
                        }
                    </button>

                </section>


                <hr />


                {/* 文档列表 */}

                <section>

                    <h3>
                        我的文档
                    </h3>


                    {
                        loading ? (

                            <p>
                                正在加载文档...
                            </p>

                        ) : documents.length === 0 ? (

                            <p>
                                暂时还没有文档，请先上传一个 TXT 或 PDF 文件。
                            </p>

                        ) : (

                            <table>

                                <thead>

                                    <tr>

                                        <th>
                                            ID
                                        </th>

                                        <th>
                                            文件名
                                        </th>

                                        <th>
                                            文件类型
                                        </th>

                                        <th>
                                            操作
                                        </th>

                                    </tr>

                                </thead>


                                <tbody>

                                    {
                                        documents.map(
                                            document => (

                                                <tr
                                                    key={
                                                        document.id
                                                    }
                                                >

                                                    <td>
                                                        {
                                                            document.id
                                                        }
                                                    </td>

                                                    <td>
                                                        {
                                                            document.filename
                                                        }
                                                    </td>

                                                    <td>
                                                        {
                                                            document.file_type
                                                        }
                                                    </td>

                                                    <td>

                                                        <button
                                                            onClick={
                                                                () =>
                                                                    handleDelete(
                                                                        document.id
                                                                    )
                                                            }
                                                        >
                                                            删除
                                                        </button>

                                                    </td>

                                                </tr>

                                            )
                                        )
                                    }

                                </tbody>

                            </table>

                        )
                    }

                </section>

            </main>

        </div>

    );

}


export default Documents;
