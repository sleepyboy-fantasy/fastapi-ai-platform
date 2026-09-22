import {
    useEffect,
    useState
} from "react";

import request from "../api/request";

import {
    useNavigate
} from "react-router-dom";


function Dashboard() {

    const navigate = useNavigate();

    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);


    useEffect(() => {

        async function loadUser() {

            const token =
                localStorage.getItem("token");

            if (!token) {

                navigate("/");

                return;

            }


            try {

                const res =
                    await request.get("/users/me");

                setUser(res.data);

            } catch (error) {

                console.log(error);

                localStorage.removeItem("token");

                navigate("/");

            } finally {

                setLoading(false);

            }

        }


        loadUser();

    }, [navigate]);


    function handleLogout() {

        localStorage.removeItem("token");

        navigate("/");

    }


    if (loading) {

        return (
            <div>
                正在加载...
            </div>
        );

    }


    return (

        <div>

            <header>

                <h1>
                    AI 知识库平台
                </h1>

                <button
                    onClick={handleLogout}
                >
                    退出登录
                </button>

            </header>


            <main>

                <h2>
                    欢迎回来，{user?.username}
                </h2>


                <p>
                    这里是你的 AI 知识库工作台
                </p>


                <hr />


                <div>

                    <h3>
                        文档管理
                    </h3>

                    <p>
                        上传、查看和管理知识库文档
                    </p>

                    <button onClick={() => navigate("/documents")}>
                        我的文档
                    </button>

                </div>


                <div>

                    <h3>
                        AI 智能问答
                    </h3>

                    <p>
                        基于知识库内容进行智能问答
                    </p>

                    <button onClick={() => navigate("/qa")}>
                        开始提问
                    </button>

                </div>

                {user?.is_admin && (
                    <div>
                        <h3>
                            用户管理
                        </h3>

                        <p>
                            管理系统用户及用户权限
                        </p>

                        <button
                            onClick={() => navigate("/admin/users")}
                        >
                            用户管理
                        </button>
                    </div>
                )}


            </main>

        </div>

    );

}


export default Dashboard;
