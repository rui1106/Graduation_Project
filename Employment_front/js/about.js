var vm = new Vue({
    el: "#app",
    data: {
        host: host,
        username: localStorage.username,
        work: {
            id: "",
            name: "",
            salary: "",
            location: "",
            company: "",
            degree_required: "",
            number: "",
            request: ""
        }
    },
    mounted(){
        this.showDetail();
    },
    methods:{
        showDetail(){
            var query = window.location.search.substring(1);
            console.log(query)
            axios.get(this.host + "/detail/" + query + "/", {
                response: "json"
            })
            .then(response=>{
                this.work = response.data.work;
            })
            .catch(error =>{
                console.log("获取失败");
            })
        }
    }
})