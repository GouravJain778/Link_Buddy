$(document).ready(function(){
    console.log("ready")
    $('#login-btn').click(function(){
        var username=$("#username").val();
        var password=$("#password").val();
        if ( username != "" && password != ""){
            var body= {username:username, password:password}
            $.ajax({
                type:"POST", 
                url:"http://127.0.0.1:5000/api/login",
                data:JSON.stringify(body),
                async:false,
                contentType: "application/json",
                success:function(data){
                    console.log(data["access_token"])
                    localStorage.setItem("access_token", data["access_token"])
                    var token= localStorage.getItem("access_token") 
                
                
                    console.log(data)
                    
                    console.log("success")
                    console.log(token)
                    window.location.href= "http://localhost:5000/getall"
                }
        
            })
        }

            
        
    })
}
)