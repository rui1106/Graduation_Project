var vm = new Vue({
    el: '#app',
    data: {
        host: host,
        username: localStorage.username,
        works:[
            {
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
        showindex(){
            axios.get(this.host+"/showindex/",{
               response:"json" 
            })
            .then(response=>{
                this.works =  response.data.slice(0,4)
                console.log(this.works)
            })
            .catch(error =>{
                console.log(error.response.data);
            })
        }
    }
})