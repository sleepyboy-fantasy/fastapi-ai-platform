import {
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import request from "../api/request";


function Login() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");


    async function handleLogin() {

        try {

            const params = new URLSearchParams();

            params.append("username", username);
            params.append("password", password);


            const res =
                await request.post(
                    "/users/login",
                    params,
                    {
                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded"
                        }
                    }
                );


            console.log("登录成功：", res.data);


            localStorage.setItem(
                "token",
                res.data.access_token
            );


            alert("登录成功");

            navigate("/dashboard");


        } catch (error) {

            console.log("登录失败：", error);

            if (error.response) {

                console.log(
                    "状态码：",
                    error.response.status
                );

                console.log(
                    "后端返回：",
                    error.response.data
                );

                alert(
                    "登录失败：" +
                    JSON.stringify(error.response.data)
                );

            } else {

                alert(
                    "登录失败：" +
                    error.message
                );

            }

        }

    }


    return (

        <div className="auth-page">

            <h1>
                AI知识库平台
            </h1>


            <h2>
                用户登录
            </h2>


            <input
                placeholder="用户名"
                value={username}
                onChange={
                    e => setUsername(e.target.value)
                }
            />


            <br />


            <input
                placeholder="密码"
                type="password"
                value={password}
                onChange={
                    e => setPassword(e.target.value)
                }
            />


            <br />


            <button
                onClick={handleLogin}
            >
                登录
            </button>
            <br />
            <br />

            <p>
                还没有账号？
                <button
                    onClick={() => navigate("/register")}
                >
                    立即注册
                </button>
            </p>


        </div>

    );

}

export default Login;
