import {
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import request from "../api/request";


function Register() {

    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [loading, setLoading] = useState(false);


    async function handleRegister() {

        // =========================
        // 基础校验
        // =========================

        if (!username.trim()) {
            alert("请输入用户名");
            return;
        }

        if (!email.trim()) {
            alert("请输入邮箱");
            return;
        }

        if (!password) {
            alert("请输入密码");
            return;
        }

        if (password !== confirmPassword) {
            alert("两次输入的密码不一致");
            return;
        }


        setLoading(true);


        try {

            const res = await request.post(
                "/users/register",
                {
                    username: username.trim(),
                    email: email.trim(),
                    password: password
                }
            );


            console.log(
                "注册成功：",
                res.data
            );


            alert("注册成功，请登录");


            navigate("/");


        } catch (error) {

            console.log(
                "注册失败：",
                error
            );


            if (error.response) {

                console.log(
                    "状态码：",
                    error.response.status
                );

                console.log(
                    "后端返回：",
                    error.response.data
                );


                let message = "注册失败";


                if (
                    error.response.data &&
                    error.response.data.message
                ) {

                    message =
                        error.response.data.message;

                } else if (
                    error.response.data &&
                    error.response.data.detail
                ) {

                    message =
                        error.response.data.detail;

                }


                alert(
                    message
                );


            } else {

                alert(
                    "注册失败：" +
                    error.message
                );

            }


        } finally {

            setLoading(false);

        }

    }


    return (

        <div className="auth-page">

            <h1>
                AI知识库平台
            </h1>


            <h2>
                用户注册
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
                placeholder="邮箱"
                type="email"
                value={email}
                onChange={
                    e => setEmail(e.target.value)
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


            <input
                placeholder="确认密码"
                type="password"
                value={confirmPassword}
                onChange={
                    e => setConfirmPassword(e.target.value)
                }
            />


            <br />


            <button
                onClick={handleRegister}
                disabled={loading}
            >
                {
                    loading
                        ? "正在注册..."
                        : "注册"
                }
            </button>


            <br />
            <br />


            <button
                onClick={() => navigate("/")}
            >
                返回登录
            </button>

        </div>

    );

}


export default Register;
