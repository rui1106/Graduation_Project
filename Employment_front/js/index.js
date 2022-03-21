var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        username: localStorage.username,
        works:[
            {
                id: "",
                name: "",
                salary: "",
                location: "",
                company: "",
                degree_required: "",
                number: ""
            }
        ]

    },
    mounted(){
        this.showindex()
    },
    methods:{
        logout: function(){
            // sessionStorage.clear();
            localStorage.clear();
            location.href = '/login.html';
        },
        Detail(id){
            // this.$router.push({ path: "/about.html", query: { id: id } });
            location.href = "about.html?" + id 
        },
        showindex(){
            axios.get(this.host+"/showindex/",{
               response:"json" 
            })
            .then(response=>{
                this.works =  response.data.results;
                console.log(this.works)
            })
            .catch(error =>{
                console.log(获取失败);
            })
        }
    }
})