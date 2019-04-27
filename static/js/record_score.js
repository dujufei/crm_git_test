$(function () {
    // 修改成绩事件
    $(".score").change(function () {
        var sid = $(this).attr("sid");
        var val = $(this).val();
        var csrfToken = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url:"",
            type:'post',
            data:{
                csrfmiddlewaretoken:csrfToken,
                sid:sid,
                val:val,
                action:"score"
            },
            success:function (data) {
                console.log(data)
            }
        })
    });
    //修改评语事件
    $(".note").change(function () {
        var sid = $(this).attr("sid");
        var val = $(this).val();
        var csrfToken = $("[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url:"",
            type:'post',
            data:{
                csrfmiddlewaretoken:csrfToken,
                sid:sid,
                val:val,
                action:"homework_note",
                },
            success:function (data) {
                console.log(data)
            }
        })
    })
});