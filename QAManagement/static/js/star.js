;+function($){
	
	//星星构造函数
	function Star(options){
		//如果大小不带单位转换为px
		var size = options.size + (isNaN(options.size) ? '' : 'px');
		//创建星星元素
		this.$element = $(
			'<li class="star" style="max-width:'+size+';width:'+size+';height:'+size+';" data-prompt="'+(options.prompt || '无')+'" >'+
				'<img src="'+options.emptyImgUrl+'" style="width:'+size+';height:'+size+';" />'+
				'<span><img src="'+options.fullImgUrl+'" style="width:'+size+';height:'+size+';" /></span>'+
			'</li>'
		);
		//星星的评分间隔
		this.step = options.step;
		//整颗星星表示的分数
		this.sumScore = options.sumScore;
	}
	//星星原型
	Star.prototype = {
		//构造指向
		constructor : Star,
		setFullPosition : function(score){
			this.$element.find('span').width(score/this.sumScore*100+'%');
		}
	};
	
	
	//星星(图片)评分构造函数
	function StarScore(options){
		//星星input
		this.$element = $(options.element);
		//容器
		this.$container = $('<ul class="star-score"></ul>').insertBefore(this.$element);
		//显示分数的元素
		this.$showScoreElement = $(options.showScoreElement);
		//一共几颗星星
		this.length = Math.max(options.length,1);
		//每颗星星的大小
		this.size = options.size;
		//初始分数
		this.score = Number(options.score) || 0;
		//总分
		this.sumScore = options.sumScore;
		//评分间隔
		this.step = options.step > 0 ? options.step : 0.1;
		//获得有几位小数
		var stepStr = String(Number(this.step));
		this.decimal = stepStr.substring(stepStr.lastIndexOf('.')+1).length;
		//未打分的图片url
		this.emptyImgUrl = options.emptyImgUrl;
		//已打分的图片的url
		this.fullImgUrl = options.fullImgUrl;
		//每颗星星提示文本数组
		this.prompts = options.prompts;
		//只读
		this.readonly = options.readonly;
		//星星数组
		this.stars = [];
		//显示的分数
		this.virtualScore = 0;
		//每颗星星表示的分数
		this.oneScore = this.sumScore / this.length;
		this.init();
	}
	//星星评分原型
	StarScore.prototype = {
		//构造指向
		constructor : StarScore,
		//控件名字
		NAME : 'starScore',
		//开启选择器
		ENABLED_SELECTOR : 'input[data-star="true"]',
		//dataset获取值后对dataset进行操作
		GET_DATASET : function(dataset){
			if(dataset.prompts){
				var dataSet = $.extend({},dataset);
				dataSet.prompts = dataSet.prompts.split(',');
				return dataSet;
			}
			return dataset;
		},
		//默认值
		defaultParams : {
			length : 5,
			size : '20px',
			sumScore : 5,
			step : .1,
			emptyImgUrl : '/static/img/star-empty.png',
			fullImgUrl : '/static/img/star-full.png',
			prompts : ['很差!','差!','一般!','还可以!','非常好!'],
			readonly : false
		},
		//初始化
		init : function(){
			//星星对象
			var star;
			//遍历向容器中添加星星
			for(var i = 0; i < this.length; ++i){
				//实例化星星对象
				star = new Star({
					size : this.size,
					step : this.step,
					//计算出每颗星星表示的分数
					sumScore : this.oneScore,
					emptyImgUrl : this.emptyImgUrl,
					fullImgUrl : this.fullImgUrl,
					prompt : this.prompts[i]
				});
				//将星星加入数组与容器
				this.stars.push(star);
				this.$container.append(star.$element);
			}
			this.$element.css('display','none');
			this.bindMouseEvent();
			this.updateScore(this.score);
		},
		//绑定鼠标事件
		bindMouseEvent : function(){
			//获得鼠标在页面中的位置
			function getMousePosition(ev){
				if(ev.pageX || ev.pageY){
					return {
						x:ev.pageX, 
						y:ev.pageY
					};
				}
				return {
					x:ev.clientX + document.body.scrollLeft - document.body.clientLeft,
					y:ev.clientY + document.body.scrollTop - document.body.clientTop
				};
			}
			//获得元素在页面中的位置
			function getElementPosition(element){
				var pos = {
					x : 0,
					y : 0
				};
				for(element; element;element = element.offsetParent){
					pos.y += element.offsetTop;
					pos.x += element.offsetLeft;
				}
				return pos;
			}
			
			var scope = this;
			//循环为每个星星绑定鼠标事件
			for(var i = 0; i < this.stars.length; ++i){
				(function(i){
					scope.stars[i].$element.mousemove(function(e){
						if(scope.readonly) return;
						
						var ePos = getElementPosition(this),
							mPos = getMousePosition(e),
							width = $(this).width(),
							score = i*scope.oneScore+scope.oneScore*((mPos.x-ePos.x)/width);
						//设置分数
						if(i === scope.length - 1 && mPos.x - ePos.x >= width-width/5){
							scope.showScore(scope.sumScore);
						}else if(i === 0 && mPos.x - ePos.x <= width/5){
							scope.showScore(0);
						}else{
							scope.showScore(parseFloat(score % scope.step === 0 ? score : score + (scope.step - score % scope.step),10));
						}
				
					}).mouseleave(function(){
						if(scope.readonly) return;
						
						scope.showScore(scope.score);
					}).click(function(){
						if(scope.readonly) return;
						
						scope.updateScore();
					});
				})(i);
			}
			
		},
		//设置分数
		showScore : function(score){
			//小数位数
			var length,index = String(score).lastIndexOf('.');
			if(index === -1){
				length = 0;
			}else{
				length = String(score).substring(index+1).length;
			}
			//正则匹配小数点后面的位数  如果小数位数超过指定  保留指定的	位数
			score = Math.min(this.sumScore, length < this.decimal ? score : score.toFixed(this.decimal));
			//如果小于等于0分 清空星星 退出方法
			if(score <= 0){
				this.setEmptyStars(0);
				this.virtualScore = 0;
				return;
			}
			//算出要设置满的星星个数
			var fullLength = Math.ceil(score/this.oneScore) - 1;
		
			//将要清空的星星清空
			this.setEmptyStars(fullLength);
			//将要设满的星星设满
			this.setFullStars(fullLength);
			
			//设置非填满的那个星星
			this.stars[fullLength].setFullPosition(score-(fullLength)*this.oneScore);
			this.virtualScore = score;
		},
		updateScore : function(score){
			this.$element.trigger({
				type : 'changeScore',
				//设置评分和input的值      如果点击分数等于现在的实际分数则清零
				score : this.$element.val(this.score = isNaN(score) ? (this.score === this.virtualScore ? 0 : this.virtualScore) : (this.showScore(score) || score)).val()
			});

			if(this.$showScoreElement[0]){
				if('value' in this.$showScoreElement[0]){
					this.$showScoreElement.val(this.score);
				}else{
					this.$showScoreElement.html(this.score);
				}
			}
			
			//执行动画
			if(this.score <= 0){
				this.$container.removeClass('active');
			}else{
				this.$container.addClass('active');
			}
		},
		//设置要填满的星星 根据个数
		setFullStars : function(fullLength){
			for(var i = 0; i < fullLength; ++i){
				this.stars[i].setFullPosition(this.oneScore);
			}
		},
		//设置要清空的星星 从开始下标
		setEmptyStars : function(emptyIndex){
			for(var i = emptyIndex; i < this.stars.length; ++i){
				this.stars[i].setFullPosition(0);
			}
		}
	};
	
	
	$.control(StarScore);
	
}(jQuery);