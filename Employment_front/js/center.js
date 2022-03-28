var vm = new Vue({
    el: "#app",
    data: {
        host: host,
        token: localStorage.token,
        username: localStorage.username,
        img_url: "",
        old_password: "",
        new_password: "",
        new_password2: "",
        user: {
            username: localStorage.username,
            email: "1105407264@qq.com",
            phone: "15340851024",
            avatar_url: "http://r7pjj3wfv.bkt.clouddn.com/LPP1.jpg",
            sex: 0,
        }
    },
    mounted() {
        this.GetUser();
    },
    methods: {
        GetUser() {
            axios.get(this.host + "/getuser/", {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    this.user = response.data.results[0];
                    if (this.user.avatar_url === "") {
                        this.user.avatar_url = "http://r7pjj3wfv.bkt.clouddn.com/LPP1.jpg"
                    }
                    console.log(this.user)
                })
                .catch(error => {
                    location.href = "login.html"
                    console.log("获取失败");
                })
        },
        upload(e) {
            // 上传照片
            let self = this;
            let file = e.target.files[0];
            /* eslint-disable no-undef */
            let param = new FormData(); // 创建form对象
            param.append("file", file); // 通过append向form对象添加数据
            param.append("chunk", "0"); // 添加form表单中其他数据
            console.log(param.get("file")); // FormData私有类对象，访问不到，可以通过get判断值是否传进去
            console.log(param)
            axios.post(this.host + '/upload/', param, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    },
                    response: "json"
                })
                .then(response => {
                    if (response.data.code === 0) {
                        img_url = response.data.file_url
                        // console.log(img_url)
                        alert("上传成功")
                    } else {
                        alert("上传失败")
                    }
                })
                .catch(error => {
                    console.log("网络错误")
                })
        },
        // 修改头像
        ChangeImg(e) {
            e.preventDefault();
            axios.post(this.host + "/changeimg/", {
                    "file_url": img_url
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    if (response.data.code === 0) {
                        this.user.avatar_url = response.data.avatar_url
                        console.log("修改成功")
                    } else {
                        console.log(response.data.message);
                    }
                })
                .catch(error => {
                    // location.href = "login.html"
                    console.log("网络错误");
                })
        },
        // 修改个人信息
        ChangeInfo(e) {
            e.preventDefault();
            axios.put(this.host + "/changeinfo/", {
                    "username": this.user.username,
                    "phone": this.user.phone,
                    "email": this.user.email,
                    "sex": this.user.sex
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    if (response.data.code === 0) {
                        alert("修改成功")
                    } else {
                        // console.log("修改失败")
                        alert(response.data.errmsg)
                    }
                })
                .catch(error => {
                    // location.href = "login.html"
                    console.log("网络错误");
                })
        },

        // 修改密码
        changepwd(e) {
            e.preventDefault();
            axios.put(this.host + "/changepwd/", {
                    "old_password": this.old_password,
                    "new_password": this.new_password,
                    "new_password2": this.new_password2,
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    if (response.data.code === 0) {
                        localStorage.clear();
                        location.href = '/login.html';
                    } else {
                        // console.log("修改失败")
                        alert(response.data.message)
                    }
                })
                .catch(error => {
                    // location.href = "login.html"
                    console.log("网络错误");
                })
        }
    }
})