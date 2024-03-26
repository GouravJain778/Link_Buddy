$(document).ready(function () {
    var access_token = localStorage.getItem("access_token");
    console.log(access_token);
    if (access_token == "" || access_token == null || access_token == undefined) {
        alert("you are not loggedin please login again")
        window.location.href = "http://localhost:5000/login"
    };

    $.ajax({
        type: "GET",
        url: "http://localhost:5000/api/getall",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token
        },

        success: function (links) {
            var linksContainer = $('#links');
            linksContainer.empty(); // Clear existing content
            var htmlTable  = '<table class="table table-bordered border-primary table-striped" style="width: 100%;">';
            htmlTable += '<thead><tr><th scope="col">ID</th><th scope="col">Name</th><th scope="col">Description</th><th scope="col">Link</th><th scope="col">Delete</th><th scope="col">Create</th><th scope="col">Update</th></tr></thead>';
            htmlTable += '<tbody">';
            $.each(links, function (index, link) {
                htmlTable += '<tr>';
                htmlTable += '<td>' + link.id + '</td>';
                htmlTable += '<td>' + link.name + '</td>';
                htmlTable += '<td>' + link.description + '</td>';
                htmlTable += '<td><a href="' + link.url + '" target="_blank">' + link.url + '</a></td>';
                htmlTable += '<td><button class="btn btn-primary" type="submit" id="delete-btn" value="' + link.id + '">Delete</button></td>';
                htmlTable += '<td><button class="btn btn-primary" type="submit" id="create-btn" >Create</button></td>';
                htmlTable += '<td><button class="btn btn-primary" type="submit" id="update-btn" >Update</button></td>';
                htmlTable += '</tr>';
            });

            // Close the tbody and table tags
            htmlTable += '</tbody></table>';
            linksContainer.append(htmlTable)

        },

        error: function () {
            console.log("get error");
        },

    });
   
    $(document).on("click","#delete-btn",function(){
        var id= $(this).val()
        console.log(id)
        $.ajax({
            url:"http://127.0.0.1:5000/api/delete/"+id,
            type:"DELETE",
            headers:{
                "Content-Type": "application/json",
                "Authorization": "Bearer " + access_token
            },

            success:function(){
                alert("deleted")
                location.reload()
            }

        });
    });


    $(document).on("click" ,"#create-btn" ,function() {
        $.ajax({
            success: function (response) {
                // console.log("create sussessful")
                window.location.href= "http://localhost:5000/create"
                
            }
        });
        
    });

    $(document).on("click" ,"#update-btn" ,function(){
        $.ajax({
            success: function(response){
                // console.log("updated successfully")
                window.location.href ="http://localhost:5000/update"

            }
        });
    });





});


