// setTimeout(function(){
//     $('#message').alert('slow')
// }, 2000);

setTimeout(fade_out, 3000);
    function fade_out() {
        $(".messages").fadeOut().empty();
    }