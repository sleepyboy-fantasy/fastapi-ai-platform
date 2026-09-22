import axios from "axios";


const request = axios.create({

    baseURL:"http://localhost:8000",

    timeout:10000

});



// 请求自动携带token

request.interceptors.request.use(
    config=>{


        const token =
            localStorage.getItem(
                "token"
            );


        if(token){

            config.headers.Authorization =
                `Bearer ${token}`;

        }


        return config;

    }
);



export default request;