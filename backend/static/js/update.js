$(document).ready(function () {
    $("#update-btn").on("click",function(){
        var access_token = localStorage.getItem("access_token")
        if (access_token == "" || access_token == null || access_token == undefined){
            alert("you are not loggedin please login please")
            window.location.href = "http://localhost:5000/login"
        };
        $("#update-btn").on("click" , function(){
            var id =$("#id").val();

            var data ={
                name: $("#name").val(),
                description: $("#description").val(),
                url: $("#url").val()

            }
            console.log(data)
            $.ajax({
                url: "http://localhost:5000/api/update/" + id,
                type: "PUT",
                headers:{
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + access_token
                },
                data: JSON.stringify(data),
                success: function (response) {
                    console.log("updated successfully")
                    window.location.href= "http://localhost:5000/getall"
    
                    
                }
            });
        });

        
    });
    
});