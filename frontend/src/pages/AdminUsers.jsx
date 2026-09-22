import {
    useEffect,
    useState
} from "react";

import {
    useNavigate
} from "react-router-dom";

import request from "../api/request";


function AdminUsers() {

    const navigate = useNavigate();

    const [users, setUsers] = useState([]);

    const [loading, setLoading] = useState(true);

    const [editingUser, setEditingUser] = useState(null);

    const [editUsername, setEditUsername] = useState("");

    const [editEmail, setEditEmail] = useState("");

    const [editPassword, setEditPassword] = useState("");

    const [editIsAdmin, setEditIsAdmin] = useState(false);

    const [editIsActive, setEditIsActive] = useState(true);

    const [saving, setSaving] = useState(false);


    async function loadUsers() {

        try {

            const res =
                await request.get("/admin/users");

            setUsers(res.data);

        } catch (error) {

            console.log("获取用户列表失败：", error);

            if (error.response) {

                if (error.response.status === 401) {

                    localStorage.removeItem("token");

                    navigate("/");

                    return;

                }

                if (error.response.status === 403) {

                    alert("没有管理员权限");

                    navigate("/dashboard");

                    return;

                }

            }

            alert("获取用户列表失败");

        } finally {

            setLoading(false);

        }

    }


    useEffect(() => {

        const token =
            localStorage.getItem("token");

        if (!token) {

            navigate("/");

            return;

        }

        loadUsers();

    }, [navigate]);


    function openEdit(user) {

        setEditingUser(user);

        setEditUsername(user.username);

        setEditEmail(user.email);

        setEditPassword("");

        setEditIsAdmin(user.is_admin);

        setEditIsActive(user.is_active);

    }


    function closeEdit() {

        if (saving) {

            return;

        }

        setEditingUser(null);

        setEditUsername("");

        setEditEmail("");

        setEditPassword("");

        setEditIsAdmin(false);

        setEditIsActive(true);

    }


    async function saveUser() {

        if (!editUsername.trim()) {

            alert("用户名不能为空");

            return;

        }

        if (!editEmail.trim()) {

            alert("邮箱不能为空");

            return;

        }


        setSaving(true);


        try {

            const data = {

                username: editUsername.trim(),

                email: editEmail.trim(),

                is_active: editIsActive,

                is_admin: editIsAdmin

            };


            if (editPassword) {

                data.password = editPassword;

            }


            await request.patch(
                `/admin/users/${editingUser.id}`,
                data
            );


            alert("用户信息修改成功");

            closeEdit();

            await loadUsers();

        } catch (error) {

            console.log("修改用户信息失败：", error);

            alert(
                error.response?.data?.detail ||
                "修改用户信息失败"
            );

        } finally {

            setSaving(false);

        }

    }


    async function toggleUserStatus(user) {

        try {

            await request.patch(
                `/admin/users/${user.id}/status`,
                {
                    is_active: !user.is_active
                }
            );

            await loadUsers();

        } catch (error) {

            console.log("修改用户状态失败：", error);

            alert(
                error.response?.data?.detail ||
                "修改用户状态失败"
            );

        }

    }


    async function deleteUser(user) {

        const confirmed =
            window.confirm(
                `确定要删除用户「${user.username}」吗？`
            );

        if (!confirmed) {

            return;

        }


        try {

            await request.delete(
                `/admin/users/${user.id}`
            );

            alert("删除成功");

            await loadUsers();

        } catch (error) {

            console.log("删除用户失败：", error);

            alert(
                error.response?.data?.detail ||
                "删除用户失败"
            );

        }

    }


    if (loading) {

        return (
            <div>
                正在加载用户列表...
            </div>
        );

    }


    return (

        <div>

            <header>

                <h1>
                    用户管理
                </h1>

                <button
                    onClick={() => navigate("/dashboard")}
                >
                    返回首页
                </button>

            </header>


            <main>

                <h2>
                    系统用户
                </h2>


                {users.length === 0 ? (

                    <p>
                        暂无用户
                    </p>

                ) : (

                    <table
                        border="1"
                        cellPadding="8"
                        cellSpacing="0"
                    >

                        <thead>

                            <tr>

                                <th>
                                    ID
                                </th>

                                <th>
                                    用户名
                                </th>

                                <th>
                                    邮箱
                                </th>

                                <th>
                                    角色
                                </th>

                                <th>
                                    状态
                                </th>

                                <th>
                                    操作
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {users.map(user => (

                                <tr key={user.id}>

                                    <td>
                                        {user.id}
                                    </td>

                                    <td>
                                        {user.username}
                                    </td>

                                    <td>
                                        {user.email}
                                    </td>

                                    <td>
                                        {user.is_admin
                                            ? "管理员"
                                            : "普通用户"}
                                    </td>

                                    <td>
                                        {user.is_active
                                            ? "正常"
                                            : "已禁用"}
                                    </td>

                                    <td>

                                        <button
                                            onClick={() =>
                                                openEdit(user)
                                            }
                                        >
                                            编辑
                                        </button>


                                        {" "}


                                        <button
                                            onClick={() =>
                                                toggleUserStatus(user)
                                            }
                                        >
                                            {user.is_active
                                                ? "禁用"
                                                : "启用"}
                                        </button>


                                        {" "}


                                        <button
                                            onClick={() =>
                                                deleteUser(user)
                                            }
                                        >
                                            删除
                                        </button>

                                    </td>

                                </tr>

                            ))}

                        </tbody>

                    </table>

                )}


                {editingUser && (

                    <div>

                        <hr />

                        <h2>
                            编辑用户
                        </h2>


                        <p>
                            用户 ID：{editingUser.id}
                        </p>


                        <div>

                            <label>
                                用户名：
                            </label>

                            <input
                                value={editUsername}
                                onChange={e =>
                                    setEditUsername(e.target.value)
                                }
                            />

                        </div>


                        <br />


                        <div>

                            <label>
                                邮箱：
                            </label>

                            <input
                                type="email"
                                value={editEmail}
                                onChange={e =>
                                    setEditEmail(e.target.value)
                                }
                            />

                        </div>


                        <br />


                        <div>

                            <label>
                                新密码：
                            </label>

                            <input
                                type="password"
                                value={editPassword}
                                placeholder="留空表示不修改"
                                onChange={e =>
                                    setEditPassword(e.target.value)
                                }
                            />

                        </div>


                        <br />


                        <div>

                            <label>
                                角色：
                            </label>

                            <select
                                value={editIsAdmin ? "admin" : "user"}
                                onChange={e =>
                                    setEditIsAdmin(
                                        e.target.value === "admin"
                                    )
                                }
                            >

                                <option value="user">
                                    普通用户
                                </option>

                                <option value="admin">
                                    管理员
                                </option>

                            </select>

                        </div>


                        <br />


                        <div>

                            <label>
                                状态：
                            </label>

                            <select
                                value={editIsActive ? "active" : "disabled"}
                                onChange={e =>
                                    setEditIsActive(
                                        e.target.value === "active"
                                    )
                                }
                            >

                                <option value="active">
                                    正常
                                </option>

                                <option value="disabled">
                                    已禁用
                                </option>

                            </select>

                        </div>


                        <br />


                        <button
                            onClick={saveUser}
                            disabled={saving}
                        >
                            {saving
                                ? "正在保存..."
                                : "保存修改"}
                        </button>


                        {" "}


                        <button
                            onClick={closeEdit}
                            disabled={saving}
                        >
                            取消
                        </button>

                    </div>

                )}

            </main>

        </div>

    );

}


export default AdminUsers;