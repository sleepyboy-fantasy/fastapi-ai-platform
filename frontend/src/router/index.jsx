import {
    createBrowserRouter
} from "react-router-dom";

import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import Documents from "../pages/Documents";
import QA from "../pages/QA";
import AdminUsers from "../pages/AdminUsers";


const router = createBrowserRouter([
    {
        path: "/",
        element: <Login />
    },
    {
        path: "/register",
        element: <Register />
    },
    {
        path: "/dashboard",
        element: <Dashboard />
    },
    {
        path: "/documents",
        element: <Documents />
    },
    {
        path: "/qa",
        element: <QA />
    },
    { 
        path: "/admin/users", 
        element: <AdminUsers /> 
    }
]);


export default router;