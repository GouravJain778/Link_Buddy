console.log("ready")
$(document).ready(function () {
    
    $("#register-btn").on("click",function(){
        var data={
            username: $("#Username").val(),
            password: $("#psw").val()
        }
        console.log(data)
        $.ajax({
            type: 'POST',
            url: "http://localhost:5000/api/register",
            data: JSON.stringify(data),
            async:false,
            contentType: 'application/json',
            success: function (response) {
                console.log(response)
                window.location.href="http://localhost:5000/login"
                
            },
            
        });
    });
    
});