var $uid = "";

function toggleLogin(){
  $('#toggle-login').change(function(e){
    if($(this).attr('checked')){
      $('.gender').hide();
      $('.age').hide();
      $('.start').addClass('hidden');
      $('.continue').removeClass('hidden');
    }else{
      $('.gender').show();
      $('.age').show();
      $('.continue').addClass('hidden');
      $('.start').removeClass('hidden');

    }
  })

  $('#login .btn').click(function(){
    if(!$('#username').val().match(/\w+/)){
      alert('请填写完整用户名,而且不要有空格和特殊符号');
    }else{
      $.get(
        '/start?un='+$('#username').val()+'&age='+$('#age').val()+'&gender='+$('#gender').val(),
        function(data){
          $uid = data.uid;
          $('#container').html(ich.loading()); 
          $.get(
            '/work?uid='+$uid,
            function(data){ 
              start_surver(data);
            }, 'json');
        },
        'json').error(function(){
          alert('发生错误，请联系问卷制作者');
        });
    }
  })
}

function start_surver(data){
  surver = null;
  console.log(data);
  if ( Object.prototype.toString.call( data ) === '[object Array]'){
    // surver is finished
    $(document).unbind('keydown');
    surver = ich.result({
      uid: $uid,
      data: data
    })
  }else{
    surver = ich.surver({
      cid:data.cid, 
      type:(function(t){if(t==0){return '美';}return '复杂';})(data.type),
      subj_url: data.subj.path,
      obj_url: data.obj.path,
      });
  }
  $('#container').html(surver);
  $('.load-img').hide();
}

function set_order(order){
  if (order!=1){
    $('.order-'+order).css('background-color', '#FFC7EE');
  }else{
    $('.order-1 .btn').addClass('active');
  }

  $('.load-img').show();
  $.get(
    '/set?uid='+$uid+'&sid='+$('#container .sv').data('cid')+'&order='+order,
    function(data){
      start_surver(data);
    },
    'json'
  )
}

$(document).ready(function(){
  toggleLogin();
  $(document).keydown(function(event){
    switch( event.keyCode){
      case 37: set_order(0); break;
      case 38: set_order(1); break;
      case 39: set_order(2); break;
    }
  });
})
