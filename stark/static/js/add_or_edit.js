    var pop_back_id="";
    function pop(url,id) {
            pop_back_id=id;
            console.log(pop_back_id);
            window.open(url+"?pop=1",url+"?pop=1","width=800,height=500,top=100,left=100")

        }
    //jquery的DOM操作
    function pop_back_func(text,pk) {
        console.log(pop_back_id);
        var $option=$("<option>"); //  <option></option>添加一个option标签
        $option.html(text);  // 文本值
        $option.attr("value",pk);//select的value值
        $option.attr("selected","selected");//选中

        $("#"+pop_back_id).append($option) //往后添加


    }
