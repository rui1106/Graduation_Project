var vm = new Vue({
    el: "#app",
    data:{
        host: host,
        token: localStorage.token,
        username: localStorage.username,
        user: {
            email: "1105407264@qq.com",
            phone: "15340851024",
            avatar_url: "http://r7pjj3wfv.bkt.clouddn.com/LPP1.jpg"
        }
    },
    mounted(){

    },
    methods:{
        GetUser(){
            axios.get(this.host+"/getuser/", {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                response: "json"
            })
        }
    }
})