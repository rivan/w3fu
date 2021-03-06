(function($) {
$.extend(
		$.fn, {
			valForm : function (type) {
			
				if (!$(this).length) {return;}				
				
				$(this).each (function() {					
					var val = new $.val(this, type);
					$(this).data('validator', val);
					val.init();
				}); 
			}
		}
);

$.val = function (form, type) {
	
	this.form = form;
	//this.email = $(this.form).find($.val.valElements.email);
	//this.integer = $(this.form).find($.val.valElements.integer);
	//this.toggle = $(this.form).find($.val.valElements.toggle);
	this.provider = $(this.form).find($.val.valElements.provider);
	$(this.provider).data('msg', $(this.form).find($.val.valElements.providerMsg));
	this.login = $(this.form).find($.val.valElements.login);
	$(this.login).data('msg', $(this.form).find($.val.valElements.loginMsg));
	this.password = $(this.form).find($.val.valElements.password);
	$(this.password).data('msg', $(this.form).find($.val.valElements.passwordMsg));
	this.showError = this.showValid = this.showDefault = function(){};
	
	if (type == 'default') {
		
		this.showError = function(element){
			
			$(element).removeClass('def');
			$(element).removeClass('val');
			$(element).addClass('err');
			$($(element).data('msg')).text('Проверьте формат');
		}
		
		this.showValid = function(element){
			
			$(element).removeClass('def');
			$(element).removeClass('err');
			$(element).addClass('val');
			$($(element).data('msg')).text('Хорошая работа!');
			
		}
		
		this.showDefault = function(element){
			
			$(element).removeClass('val');
			$(element).removeClass('err');
			$(element).addClass('def');
			$($(element).data('msg')).text('');
		}		
	}	
}

$.extend($.val, {			
						
			valElements: {
				required: "val-required",
				email: "input.val-email",
				integer: "input.val-integer",
				toggle: "input.val-toggle",
				login: "input.val-login",
				loginMsg: ".val-login-msg",
				password: "input.val-password",
				passwordMsg: ".val-password-msg",
				provider:"input.val-provider",
				providerMsg:".val-provider-msg"
			},
			regexp: {
				email: /^[-0-9a-z!#$%&'*+\/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+\/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)+(?:museum|travel|(?:[a-z]{2,4}))$/i,
				integer: /^-?\d+$/,
				login: /^\s*[а-яА-Я\w\.-]{4,32}\s*$/,
				password: /^\s*[№ёа-яЁА-Я\x21-\x7e]{4,32}\s*$/,
				provider: /^\s*[№а-яА-Я\x21-\x7e][№а-яА-Я\x20-\x7e]{0,99}\s*$/
			},
			
			prototype: {
				
				init: function () {
					(function (validator) {
						
						$(validator.form).submit(function(){return validator.submitForm();});						
					/*	
						validator.email.bind('blur', function(){ validator.validateText(this, $.val.regexp.email);});
						validator.email.bind('keyup',function(e){ if (e.keyCode != 9) {validator.validateText(this, $.val.regexp.email);}});
					*/	
						validator.login.bind('blur', function(){ validator.validateLogin(this);});
					//	validator.login.bind('keyup', function(e){ if (e.keyCode != 9) {validator.validateText(this, $.val.regexp.login);}});
						
						validator.password.bind('blur', function(){ validator.validatePassword(this);});
						validator.provider.bind('blur', function(){ validator.validateProvider(this);});
					//	validator.password.bind('keyup', function(e){ if (e.keyCode != 9) {validator.validateText(this, $.val.regexp.password);}});
					/*										
						validator.integer.bind('blur', function(){ validator.validateInteger(this, $.val.regexp.integer,0,2999);});						
						validator.integer.bind('keyup', function(e){ if (e.keyCode != 9) {validator.validateInteger(this, $.val.regexp.integer,0,2999);}});
						
						validator.toggle.click(function(){ validator.validateToggle(this); });
					*/	
						
					})(this);
				},
				reset: function(element) {
					$(element).val('');
					this.showDefault(element);
				},
				validatePassword: function(element) {
					 return this.validateText(element, $.val.regexp.password);
				},
				validateLogin: function(element) {
					 return this.validateText(element, $.val.regexp.login);
				},
				validateProvider: function(element) {
					 return this.validateText(element, $.val.regexp.provider);
				},
				validateText: function(element, regexp) {
					if ($(element).val() == ""){
						if ($(element).hasClass($.val.valElements.required)) {this.showError(element); return false;}	
						else  {this.showDefault(element); return true;}
					}
					if (regexp.test($(element).val())) {this.showValid(element); return true;}
					
					this.showError(element); return false;							
				},				
				validateInteger:function(element, regexp, min, max){
					if (element.value == ""){
						if ($(element).hasClass($.val.valElements.required)) {this.showError(element); return false;}	
						else  {this.showDefault(element); return true;}
					}
					if (regexp.test(element.value)) {	
						if ((element.value >= min) && (element.value <= max)) {
							this.showValid(element); return true;
						}
						else {this.showError(element); return false;}
					}
					this.showError(element); return false;				
				},				
				validateToggle:function(element) {
					if ($(element).hasClass($.val.valElements.required)) {
						if (!$(element).attr('checked')) { this.showError(element); return false;}
						else {this.showValid(element); return true; }
					}
					return true;
				},
				submitForm:function(){
					var send = true;
					(function (validator) {
						
				/*		validator.email.each(function(){
							if (!validator.validateText(this,$.val.regexp.email)){send = false;}
						});
						
						validator.integer.each(function(){
							if (!validator.validateInteger(this,$.val.regexp.integer,0,2999)){send = false;}
						});
						
						validator.toggle.each(function(){
							if (!validator.validateToggle(this)){send = false;}
						});
			*/			
						validator.login.each(function(){
							if (!validator.validateLogin(this)){send = false;}
						});
						
						validator.password.each(function(){
							if (!validator.validatePassword(this)){send = false;}
						});
						
						validator.provider.each(function(){
							if (!validator.validateProvider(this)){send = false;}
						});
						
						/*отладочная функция*/
						//if (!send) {$(validator.form).css('border','3px solid red');}
						/*отладочная функция*/					
					})(this);
					
					return send;
				}
							
			}
		}
);
})(jQuery);