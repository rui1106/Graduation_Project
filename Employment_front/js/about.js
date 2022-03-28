var vm = new Vue({
    el: "#app",
    data: {
        host: host,
        token: localStorage.token,
        username: localStorage.username,
        work: {
            id: "",
            name: "",
            salary: "",
            location: "",
            company: "",
            degree_required: "",
            number: "",
            request: "",
            collection: true,
        }
    },
    mounted() {
        this.showDetail();
    },
    methods: {
        logout: function(){
            // sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        showDetail() {
            var query = window.location.search.substring(1);
            console.log(query)
            axios.get(this.host + "/detail/" + query + "/", {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    this.work = response.data.work;
                })
                .catch(error => {
                    console.log("获取失败");
                })
        },
        Collect(id) {
            axios.post(this.host + "/collect/", {
                    "job_id": id,
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    if (response.data.code === 0) {
                        this.work.collection = false
                    } else {
                        console.log("收藏失败")
                    }
                })
                .catch(error => {
                    console.log("获取失败");
                })
        },
        CancelCollect(id) {
            axios.post(this.host + "/cancelcollect/", {
                    "job_id": id,
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    response: "json"
                })
                .then(response => {
                    if (response.data.code === 0) {
                        this.work.collection = true
                    } else {
                        console.log("取消收藏失败")
                    }
                })
                .catch(error => {
                    console.log("获取失败");
                })
        }
    }
})