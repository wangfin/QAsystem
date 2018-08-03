$(window).load(function() {
	//页面切换
	$(".left-nav .click-btn").on('click', function() {
			var _index = $(this).index();
			$(this).addClass('active').siblings().removeClass('active');
			$(".right-product").eq(_index).addClass('active').siblings().removeClass('active');
		});
		//page2
		//添加
	$('#btn_add').click(function(){
		console.log("do")
		$(this).attr({
			'data-toggle': 'modal',
			'data-target': '#tianjiaModal'
		});
	});

    $(".save-tianjia").click(function () {
        var post_json = {};
        var len = $("#tianjiaModal .modal-body input").length;
        var tabel_name = $(".th-inner")
        //alert(tabel_name);
        for (var j = 0; j < len; j++) {
            var id_text = $("#tianjiaModal .modal-body input").eq(0).val();
            var tabel_text = $("#tianjiaModal .modal-body input").eq(j).val();
            console.log(tabel_name[j].innerHTML);
            post_json[tabel_name[j+1].innerHTML] = tabel_text;
        }
        console.log(post_json);
        $('#tianjia').removeAttr('data-toggle');
        //ajax将json传递给后台
        $.ajax({
            url: '/Add/',
            type: "POST",
            data: {jsondata: JSON.stringify(post_json)},
            success: function (data) {
                alert("插入成功");
                for (var j = 0; j < len; j++) {
                    $("#tianjiaModal .modal-body input").eq(j).val("");
                }
                $("#mytab").bootstrapTable('refresh');


            }
        });
        // $("#mytab").bootstrapTable('insertRow',post_json);

    });

	//全选
	var door = true;
	$("#quanxuan").click(function() {
			if(door) {
				alert("2");
				$(".bb input[type='checkbox']").attr('checked', true);
				door = false;
			} else {
						alert("1");
				$(".bb input[type='checkbox']").attr('checked', false);
				door = true;
			}
		});
		//批量删除,删除被选中元素
	$("#quanshan").click(function() {
//		console.log($(".table input[type='checkbox']").length)
		var j = 0;
		if($(".table input[type='checkbox']").length == 0) {
			alert('无可删除的元素')
		} else if(choose1()) {
			$(":checked").parent().parent().remove()
		} else {
			alert('请选择要删除的元素')
		}
		function choose() {
			for(var i = 0; i < $(".bb input[type='checkbox']").length; i++) {
//				console.log($(".bb input[type='checkbox']").eq(i).get(0).checked)
				if($(".bb input[type='checkbox']").eq(i).get(0).checked) {
					j++;
				}
			}
			return j;
		}

		function choose1() {
			choose();
			if(j > 0) {
				return true;
			} else {
				return false;
			}
		}


	});
});
	//删除
	function del(obj){
		var $obj = $(obj);
		$obj.attr({
			'data-toggle': 'modal',
			'data-target': '#shanchuModal'
		});
		// var delth = deltr.childNodes;
		// for(var i=0;i<delth.length;i++){
		// 	var node = delth[i];
        	// if(node.nodeType == 3 && !/\S/.test(node.nodeValue))
        	// {
         //   		 //删除空白子节点
         //   		 node.parentNode.removeChild(node);
        	// }
		// }
		// var delid = delth[1].innerHTML;




		$(".sure-shanchu").on('click', function() {

            var ids = $("#mytab").bootstrapTable('getSelections');

            // selectrow.bootstrapTable('remove', {
            //     field: 'id',
            //     values: ids
            // });


			//$obj.parents('tr').remove();
			var removekey = new Array();
			for(var i=0;i<ids.length;i++){
				removekey[i] = ids[i].id;
				console.log(removekey[i]);
			}
			console.log(removekey);
			//按id删除
			$.ajax({
					url:'/delete/',
					type:"POST",
					data:{del_key:JSON.stringify(removekey)},
					success:function (data) {
						alert("删除成功");
						$("#mytab").bootstrapTable('refresh');
					}

				});
		});

}
	//修改
	function modify(obj){
		var $obj = $(obj);
		//得到要修改的那一行
		var trdata = obj.parentNode.parentNode;
        var changedata = {};
        //得到表头
        var tabel_name = $('.th-inner');
		//console.log(trdata.nodeName);
		//得到那一行的原始值
		var defaultdata = trdata.childNodes;
		for(var i = 0;i < defaultdata.length;i++){
			var node = defaultdata[i];
        	if(node.nodeType == 3 && !/\S/.test(node.nodeValue))
        	{
           		 //删除空白子节点
           		 node.parentNode.removeChild(node);
        	}
		}
		//这里得到的是id
		changedata[tabel_name[1].innerHTML] = defaultdata[1].innerHTML;
		console.log(defaultdata[1].innerHTML);
		//将原始值设为默认值 i=0 时为选择框，特殊处理
		 for (var i=0;i< $("#xiugaiModal .modal-body input").length;i++){
			 $("#xiugaiModal .modal-body input").eq(i).attr("placeholder",defaultdata[i+2].innerHTML);
			 //console.log(defaultdata[i].innerHTML.length);
			 //len = defaultdata[i].innerHTML.length/40;
			 //$("#xiugaiModal .modal-body input").eq(i).css("height",len*563);
		 	// if(i == 3){
		 	// 	$("#xiugaiModal .modal-body input").eq(0).attr("placeholder",defaultdata[i].innerHTML);
			// }
		 }
		for(var i = 1; i < $(".bb tr").length; i++) {
			$(".bb tr").eq(i).children('button').eq(0).removeAttr({
				'data-toggle': 'modal',
				'data-target': '#xiugaiModal'
			});
		}

		$obj.attr({
			'data-toggle': 'modal',
			'data-target': '#xiugaiModal'
		});

		$(".save").click(function() {
			var len = $("#xiugaiModal .modal-body input").length;
			for(var j = 0; j < len; j++) {
				//alert($("#myModal .modal-body input").eq(j).val())
				//针对改动的地方做出修改没有改动的即为原始值
				// if($("#xiugaiModal .modal-body input").eq(0).val()=="")
				// 	var id_text = $("#xiugaiModal .modal-body input").eq(0).attr("placeholder");
				// else
				// 	var id_text = $("#xiugaiModal .modal-body input").eq(0).val()
				if($("#xiugaiModal .modal-body input").eq(j).val()==""){
					var tabel_text = $("#xiugaiModal .modal-body input").eq(j).attr("placeholder");
				}
				else {
                    var tabel_text = $("#xiugaiModal .modal-body input").eq(j).val();
                }
					//console.log(tabel_name[j]);
					changedata[tabel_name[j+2].innerHTML] = tabel_text;
				//数据覆盖
					//console.log(tabel_text);
					trdata.childNodes[j+2].innerHTML = tabel_text;
			}
			//ajax将json数据传递给后台
			console.log(JSON.stringify(changedata));
			$.ajax({
				url:'/modify/',
				type:"POST",
				data:{jsondata:JSON.stringify(changedata)},
				success:function (data) {
				    alert('修改成功');
					for (var j = 0; j < len; j++) {
                        $("#xiugaiModal .modal-body input").eq(j).val("");
                    }
					$("#mytab").bootstrapTable('refresh');
                },
                error:function(data){
				    alert('修改失败');
                }

			});
			// $(".bb button[data-target ='#xiugaiModal']").parents('tr').children().eq(len).buttons($(".btn btn-default xiugai"));
			// $(".bb button[data-target ='#xiugaiModal']").parents('tr').children().eq(len).text(show());

			// function show() {
				// 	var mydate = new Date();
				// 	var str = "" + mydate.getFullYear() + "-";
				// 	str += (mydate.getMonth() + 1) + "-";
				// 	str += mydate.getDate();
				// 	return str;
				// }
	});
}

//查找
// function searchData() {
// 	alert("search");
// 	var search_key = $("#seach").val();
// 	$.ajax({
// 		url:'/search/',
// 		type:"POST",
// 		data:{search_key:search_key},
// 		success:function (data) {
// 			alert(data);
//         }
// 	})
//
// }

