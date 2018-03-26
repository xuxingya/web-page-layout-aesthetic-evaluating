// Hello World! example user script
// version 0.1 BETA!
// 2005-04-22
// Copyright (c) 2005, Mark Pilgrim
// Released under the GPL license
// http://www.gnu.org/copyleft/gpl.html
//
// --------------------------------------------------------------------
//
// This is a Greasemonkey user script.
//
// To install, you need Greasemonkey: http://greasemonkey.mozdev.org/
// Then restart Firefox and revisit this script.
// Under Tools, there will be a new menu item to "Install User Script".
// Accept the default configuration and install.
//
// To uninstall, go to Tools/Manage User Scripts,
// select "Hello World", and click Uninstall.
//
// --------------------------------------------------------------------
//
// ==UserScript==
// @name          Hello World
// @namespace     http://diveintogreasemonkey.org/download/
// @description   example script to alert "Hello world!" on every page
// @include       http://www.baidu.com/s*
// @exclude       http://diveintogreasemonkey.org/*
// @exclude       http://www.diveintogreasemonkey.org/*
// ==/UserScript==

GM_addStyle('#s_tab a.i {width: 108px; color: blue; font-size: 18px; font-weight: bold; }');
GM_addStyle('.result-op { display: none; }');	
GM_addStyle('.result { position: relative; }');
GM_addStyle('.result .score-container { width: 300px; height: 240px; display: none; border: 1px solid #eee; position: absolute; left: 550px; top: 0px; box-shadow: 1px 1px 1px #ccc; padding: 10px; background: white}');
GM_addStyle('.result .score-container .score { font-size: 18px; color: #666; }');
GM_addStyle('.result .score-container img { width: 100% }');
GM_addStyle('.result.down:before { content: "▲";color: red;position: absolute;left: -19px; }');
GM_addStyle('.result.up:before { content: "▼";color: green;position: absolute;left: -19px; }');
GM_addStyle('.hide { display: none!important }');
GM_addStyle('.result:hover .score-container { display: block; }');
GM_addStyle('#loading { display: none; position: fixed; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; top:0; left:0; text-align: center; text-align: center; }');
GM_addStyle('#loading .load { display: inline-block; background: white; border: 1px solid #ccc; border-radius: 3px; width: 120px; height: 50px; padding: 15px; text-align: center; margin-top: 30% }');
GM_addStyle('#loading .load p { font-size: 12px; margin-top: 5px }');

$('#s_tab').append($('<a>').text('点此重排！').addClass('i').attr('href', 'javascript:void(0);').click(get_score));
if($('.leftBlock').length){
    $('<div>').addClass('anchor').insertAftger('.leftBlock');
}else{
    $('#content_left').prepend($('<div>').addClass('anchor'));
}


results = [];
scores = [];

$('.result').each(function(ind, item){
    results.push($(item).find('.t a').attr('href'));
    html = "<div>得分:<span class='score'></span></div>"+
        "<div class='img-container'><img></div>";
    $(item).append($('<div>').addClass('score-container hide').attr('id', 'score-'+ind).html(html));
});

load_html = "<div class='load'>评分中...<img src='http://jimpunk.net/Loading/wp-content/uploads/loading3.gif' width=15><p>已完成：<span class='done'>0</span>/"+results.length+"</p></div>"
$('body').append($('<div></div>').attr('id', 'loading').html(load_html));

function show_loading(){
    $('#loading').show();
    update_loading(0);
}

function hide_loading(){
    $('#loading').hide();
}

function update_loading(x){
    x = x===undefined? (parseInt($('#loading .done').text()) + 1): x;
    $('#loading .done').text(x);
    if(x==results.length){   
	    hide_loading();
        resort();
    }
}

function resort(){
    sorted = scores.sort(function(a, b){
        return parseFloat(a.score) - parseFloat(b.score);
    });
    GM_log(sorted);
    for(i=0;i<sorted.length;i++){
       	s = sorted[i];
    	$('#score-'+s.id).parents('.result').addClass('new-'+i).insertAfter('#content_left .anchor');
        if(parseInt(s.id)>i){
       		$('#score-'+s.id).parents('.result').addClass('up');
        };
        if(parseInt(s.id)<i){
            $('#score-'+s.id).parents('.result').addClass('down');
        }
    }
}

function get_score(){
    show_loading();
    $('.result .score-container').removeClass('hide');
    for(i=0;i<results.length;i++){
      (function(ii){
        $.ajax({
            url: 'http://192.168.1.101:7009/e?url=' + results[i]+'&id='+i,
            dataType: 'json',
            type: 'get',
            success: function(data){
                scores.push(data);
                update_loading();
                sf = parseFloat(data.score);
                score = (sf*100).toFixed(2);
                id = data.id;
                $('#score-'+id+' .score').text(score);
                $('#score-'+id+' img').attr('src', 'http://192.168.1.101:8801/exp3/sc/'+encodeURIComponent(data.img)+'?r='+Math.random());
            },
            error: function(){
                update_loading();
                $('#score-'+ii+' .score').text('评分出现了错误');
            }
        });
       })(i);
    }
};