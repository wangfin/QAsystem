;+function($){

	//正则表达式变换首字母大写  
	 function replaceReg(str){   
		   var reg = /\b(\w)|\s(\w)/g;   
		   str = str.toLowerCase();   
		   return str.replace(reg,function(m){return m.toUpperCase()})   
	 }  
	//带兼容的函数  
	$.getDataset = function(ele){  
		if(ele.dataset)  
			return ele.dataset;  
		else{  
		//一下是兼容代码  
			var dataset = {};  
			var ele_split = ele.outerHTML.split(" "); 
			for(var i = 0,element; i < ele_split.length; i++)      
			{  
				element = ele_split[i];  
				if (element.substring(0,4) == "data") {
					if (element.indexOf("/>") !=  -1) {   
						element = element.split("/>")[0];  
					}; 
					ele_key=element.split("=")[0].slice(5);  
					ele_value=element.split("=")[1].slice(1,-1);  
					if(ele_key.indexOf("-") ==  -1){  
						dataset[ele_key] = ele_value;  
					}else{  
						ele_keys=ele_key.split("-");  
						ele_key=ele_keys[0];  
						for(j=1;j<ele_keys.length;j++){  
							ele_key+=replaceReg(ele_keys[j]);  
						}
						dataset[ele_key] = ele_value;
					}  
				};  
			}
			return dataset;  
		}  

	};
	

	//控件工厂
	function ControlFactory(){}
	//控件工厂原型
	ControlFactory.prototype = {
		//构造指向
		constructor : ControlFactory,
		//将一个构造函数变为控件
		control : function(Constructor){
			var scope = this,
				control = {};
			control[Constructor.prototype.NAME] = function(options){
				//如果传入参数是string
				if(typeof options === 'string'){
					//返回值
					var result,
						//给result赋值的标识,如果调用多次方法只在第一次给result赋值
						flag = true,
						//参数数组,从参数第二位起
						argumentsArray = Array.prototype.slice.call(arguments,1);
					//循环调用方法
					this.each(function(){
						//获得控件对象
						var control = $(this).data(Constructor.prototype.NAME);
						//如果控件对象不存在
						if(!control){
							//创建控件对象
							scope.createExample(this,options,Constructor);
							control = $(this).data(Constructor.prototype.NAME);
						}
						//如果是第一次
						if(flag){
							//调用方法给result赋值
							result = control[options].apply(control,argumentsArray);
							flag = false;
						}else{
							//调用方法
							control[options].apply(control,argumentsArray);
						}
					});
					//如果result为null返回自己用于链式编程
					return result == null ? this : result;
				}
				
				//如果传入不是string则循环创建控件对象
				this.each(function(){
					scope.createExample(this,options,Constructor);
				});
				return this;
			};
			$.fn.extend(control);
			//开启
			if(Constructor.prototype.ENABLED_SELECTOR){
				$(function(){

					$(Constructor.prototype.ENABLED_SELECTOR).each(function(){
						var data = $.getDataset(this);
						if(typeof Constructor.prototype.GET_DATASET === 'function') data = Constructor.prototype.GET_DATASET(data);
						$(Constructor.prototype.ENABLED_SELECTOR)[Constructor.prototype.NAME]($.extend(Constructor.defaultParams,data,{element:this}));
					});
				});
			}
		},
		//创建控件实例
		createExample : function(element,options,Constructor){
			$(element).data(
				Constructor.prototype.NAME,
				new Constructor($.extend({element:element},Constructor.prototype.defaultParams,options))
			);
		}
	};
	
	$.extend({
		control : function(Constructor){
			ControlFactory.prototype.control(Constructor);
		}
	});
}(jQuery);
