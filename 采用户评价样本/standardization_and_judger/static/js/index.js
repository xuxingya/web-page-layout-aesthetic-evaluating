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
	      applyReward();
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

var rewards = ["Nothing", "棒棒糖一支", "士力架一条（大）", "德芙巧克力一袋","光明 金丝肉松饼一盒", "口水娃 xo酱沙嗲牛肉粒230g*2袋", "Razer 地狱狂蛇(镜面版)", "1T移动硬盘"]

if(localStorage.count == undefined){
	localStorage.count = 0;
}
if(localStorage.level == undefined){
	localStorage.level = 0;
}

function applyReward(){
	$('#count').text(localStorage.count).removeClass().addClass('level-'+localStorage.level);
	$('#reward').text(rewards[localStorage.level]).removeClass().addClass('level-'+localStorage.level);
}


function clear(){
	localStorage.count = 0;
	localStorage.level = 0;
	applyReward();
}

function add(){
	localStorage.count = parseInt(localStorage.count) + 1;
	if (localStorage.count>100){
		localStorage.level = 1;
	};
	if (localStorage.count>500){
		localStorage.level = 2;
	}
	if (localStorage.count>1500){
		localStorage.level = 3;
	}
	if(localStorage.count>3000){
		localStorage.level = 4;
	}
	if(localStorage.count>5000){
		localStorage.level = 5;
	}
	if(localStorage.count>9000){
		localStorage.level = 6;
	}
	if(localStorage.count>30000){
		localStorage.level = 7;
	}
	applyReward();
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
      add();
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
