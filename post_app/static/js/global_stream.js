$('h1').click(function(){
    alert('this is global stream js')
})

var cnt = 0;
//$().ready(function(){
   $('button').click(function(){
        $('#prevented').unbind().on('submit',function(event){
            // prevent the default submit of form, using ajax
            cnt += 1;
            console.log(cnt);
            event.preventDefault();
            console.log('prevent success!');
            var new_post = $('#id_post').val();
            console.log(new_post);
            $.ajax({
                type: "POST",
                url: "/global/",
                // the key-'post’ must be the same key in form, otherwise it cannot be saved in database
                data: {'post':new_post},
                datatype: "json",
                success: function(data){
                    console.log('success!')},
                error: function(){
                    console.log('fail!')},
                // clearForm: true,
                // resetFrom: true,
            })
        })
   })
// })

// define the global time variable
var latest_post_time = "1970-01-01 00:00:00"

function getUpdatePost() {
    console.log("trigger getUpdatePost")
    // $.ajax({
    //     type: "POST",
    //     url: "/update_post/"+latest_post_time,
    //     datatype: "json",
    // })
    $.get( "/update_post/"+latest_post_time).done(function (data) {
        //3. get posts in json format. print them out.
        //https://stackoverflow.com/questions/42570854/how-to-output-json-array-value-in-ajax-success
        console.log(data);
        console.log(typeof(data));
        // data is already a jsonObject
        console.log("get test pass");
        latest_post_time = data.timestamp;
        latest_post = data.posts;
        console.log(latest_post_time)
        console.log(latest_post)
        
        var post_html = "";
        for (var i = 0; i<latest_post.length; i++){
            var new_post = latest_post[i];
            post_html +=
                '<li class="list-group-item">'
                +'<div class="card w-90">' 
                    +'<div class="card-body">'
                        +'<a href=http://127.0.0.1:8000/personal/'+ new_post["user_id"]+'>'
                            +'<h5 class="card-title" username_id='+new_post["user"]+'>'+new_post["user"]+'</h5>'
                            +'</a>'
                        +'<div class="container">'
                            +'<div class="row">'
                                +'<div class="col-2">'
                                    +'<a href="#">'
                                        +'<img src="C:\Users\\xucha\Documents\前端网课\17-437\hwk1\素材\\user3.jpg" width="col-3" height="col-3" class="card-img-top" alt="User2">'
                                    +'</a>'
                                +'</div>'
                                +'<div class="col-10">'
                                    +new_post["post"]
                                +'</div>'
                            +'</div>'
                        +'</div>'
                        +'<p class="card-text text-right"><small class="text-muted" id="postTime">'+ new_post["timestamp"]+ '</small></p>'
                    +'</div>'
                +'</div>'
            +'</li>'
        };
        console.log(post_html)
        $("#postPool").prepend(post_html);
    });
}

$(document).ready(function(){
    window.setInterval(getUpdatePost, 3000);
})

$('#follow').click(function(){
    alert('You click the follow button!')
    // var to_user = $('#follow').prev().children().attr('username_id');
    // console.log(to_user);
    // $.ajax({
    //     type: "POST",
    //     url: "/follow/",
    //     data: {'to_user':to_user},
    //     datatype: "json",
    //     success: function(data){
    //         console.log(data)
    //         console.log('success!')},
    //     error: function(){
    //         console.log(data)
    //         console.log('fail!')},
    // })
})
