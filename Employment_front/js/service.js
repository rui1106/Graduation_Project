var vm = new Vue({
    el: "#app",
    data: {
        host: host,
        username: localStorage.username,
        page: 1,
        page_size: 6,
        count: 0,
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
        this.showservice();
    },
    methods:{
        showservice(){
            axios.get(this.host+"/showservice/", {
                params:{
                    page: this.page,
                    page_size: this.page_size,
                },
                response:"json"
            })
            .then(response=>{
                this.works = response.data.results;
                this.count = response.data.count
            })
            .catch(error =>{
                console.log(error.response.data)
            })
        },
        // 点击页数
        on_page: function(num){
            if (num != this.page){
                this.page = num;
                this.showservice();
            }
        },
    },
    computed:{
        total_page: function(){  // 总页数
            return Math.ceil(this.count/this.page_size);
        },
        next: function(){  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function(){  // 上一页
            if (this.page <= 0 ) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums: function(){  // 页码
            // 分页页数显示计算
            // 1.如果总页数<=5
            // 2.如果当前页是前3页
            // 3.如果当前页是后3页,
            // 4.既不是前3页，也不是后3页
            var nums = [];
            if (this.total_page <= 5) {
                for (var i=1; i<=this.total_page; i++){
                    nums.push(i);
                }
            } else if (this.page <= 3) {
                nums = [1, 2, 3, 4, 5];
            } else if (this.total_page - this.page <= 2) {
                for (var i=this.total_page; i>this.total_page-5; i--) {
                    nums.push(i);
                }
            } else {
                for (var i=this.page-2; i<this.page+3; i++){
                    nums.push(i);
                }
            }
            return nums;
        }
    }
})