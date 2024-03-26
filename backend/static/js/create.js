$(document).ready(function () {
    console.log("ready")
    var access_token = localStorage.getItem("access_token");
    console.log(access_token)
    if(access_token == "" || access_token==null || access_token == undefined){
        alert("you are not loggedin please login please")
        window.location.href = "http://localhost:5000/login"
    };
    $("#create-btn").on("click" , function(){
        var data={
            name: $("#name").val(),
            description:$("#description").val(),
            url:$("#url").val()
            

        }
        console.log(data)
        $.ajax({
            type: "POST",
            url: "http://localhost:5000/api/create",
            headers:{
                "Content-Type": "application/json",
                "Authorization": "Bearer " + access_token
            },
            data: JSON.stringify(data),
    
            success: function (response) {
                console.log("create sussessful")
                window.location.href= "http://localhost:5000/getall"
                
            }
        });
    })

    
   
    
});