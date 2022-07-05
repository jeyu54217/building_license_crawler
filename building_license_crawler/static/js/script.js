
// DataTable
$(document).ready(function () {
    $('#example').DataTable();
});


$('#Select_Date_Submit').click(function(){
    var date_arr = Array();  

    // Date - ['start_date','end_date']
    date_arr = date_arr.concat($('[id^="Select_from_date"]').map(function(){
        return this.value
    }).get());
    date_arr = date_arr.concat($('[id^="Select_to_date"]').map(function(){
        return this.value
    }).get());

    // jQuery post(URL,data,function(data,status,xhr),dataType) - https://api.jquery.com/jquery.post/
    var post_all = $.post(
        'http://127.0.0.1:8000/result_page/',
        {
            'date_ary[]' : date_arr,
        });

    // jQuery.when() 
    $.when(post_all).done(function(){
        // https://ithelp.ithome.com.tw/articles/10242483
        window.location.href="http://127.0.0.1:8000/result_page"
    });
});


//  search-table
$('#addRowChild').click(function(){
    // window.alert('GO!');
    $('#search-table tbody').append(`<tr>${$('#default-row').html()}</tr>`);
});


 $('#btn_search_submit').click(function(){
    // get all keyword value from html class name
    var kwyword_ary = Array();
    var id_ary = Array();

    kwyword_ary = kwyword_ary.concat($('.form-control').map(function(){
        return this.value
    }).get());

    
    id_ary = id_ary.concat($('#detail_page_id').map(function(){
        return this.value
    }).get());

    var post_all = $.post(
        'http://127.0.0.1:8000/search_g0v/',
        {
            'kwyword_ary[]' : kwyword_ary,
            'id_ary[]' : id_ary,
        });

    // redirect current page
    $.when(post_all).done(function(){
        window.location.href="http://127.0.0.1:8000/search_g0v";
    });
 });

 $('#btn_send_mail').click(function(){
    var checked_ary = Array();

    checked_ary = checked_ary.concat($('[name^="checkbox_"]:checked').map(function(){
        return $(this).attr('name')
    }).get());

    var post_all = $.post(
        'http://127.0.0.1:8000/send_email/',
        {
            'checked_ary[]' : checked_ary,
        });

    $.when(post_all).done(function(){
        window.location.href="http://127.0.0.1:8000/result_page/"
    });
});
