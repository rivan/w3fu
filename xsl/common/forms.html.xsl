<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:edit-login">
		<div class="top-label">
			<div class="title">Логин</div>
		</div>
		<input type="text" name="login" maxlength="32">
			
			<w3fu:attribute name="value">
				<w3fu:value-of select="*/form/source/@login" />
			</w3fu:attribute>
									
			<w3fu:attribute name="class">									
				<w3fu:if test="not(*/form/errors/login)">
					<w3fu:text>val-required val-login def </w3fu:text>
				</w3fu:if>
										
				<w3fu:if test="*/form/errors/login">
					<w3fu:text>val-required val-login err </w3fu:text>
				</w3fu:if>										
			</w3fu:attribute>
		</input>
	</w3fu:template> 
	
	<w3fu:template name="w3fu:val-login-msg">
		<span class="val-login-msg">	
			<w3fu:if test="*/form/errors/login/argsizeerror">
				<w3fu:text>Недостаточная длина</w3fu:text>
			</w3fu:if>
			<w3fu:if test="*/form/errors/login/argtypeerror">
				<w3fu:text>Проверьте формат</w3fu:text>
			</w3fu:if>
		</span>
	</w3fu:template>
	<w3fu:template name="w3fu:login-label">
		<div class="bottom-label">4-32 символа: буквы, цифры, ( - ) , ( _ ) , ( . )</div>
	</w3fu:template> 
	
	<w3fu:template name="w3fu:edit-password">
		<div class="top-label">
			<div class="title">Пароль</div>
			<div class="toggle-display">показать</div>
			<div class="toggle-hide">скрыть</div>
		</div>
		<input type="text" value="" class="val-required val-password def display-monitor" style="display: none;" maxlength="32" />
		<input type="password" name="password" maxlength="32">
			
			<w3fu:attribute name="class">
				<w3fu:if test="not(*/form/errors/password)">
					<w3fu:text>val-required val-password def display-element </w3fu:text>	
				</w3fu:if>
				
				<w3fu:if test="*/form/errors/password">
					<w3fu:text>val-required val-password err display-element </w3fu:text>	
				</w3fu:if>			
			</w3fu:attribute>
		</input>
	</w3fu:template>
	
	<w3fu:template name="w3fu:val-password-msg">	
				
		<span class="val-password-msg">
			<!-- <w3fu:if test="*/form/errors/password/argsizeerror">
				<w3fu:text>Недостаточная длина</w3fu:text>
			</w3fu:if>
			<w3fu:if test="*/form/errors/password/argtypeerror">
				<w3fu:text>Проверьте формат</w3fu:text>
			</w3fu:if> -->
		</span>
	</w3fu:template>
	
	<w3fu:template name="w3fu:password-label">
		<div class="bottom-label">4-32 символа: любые, кроме пробела</div>
	</w3fu:template> 
	
	<w3fu:template name="w3fu:edit-firm">	
		<div class="top-label">
			<div class="title">Название</div>
		</div>
		<input type="text" name="name" maxlength="100">
			
			<w3fu:attribute name="class">
				<w3fu:if test="not(*/form/errors/name/argsizeerror)">
					<w3fu:text>val-required val-firm def</w3fu:text>	
				</w3fu:if>
				
				<w3fu:if test="*/form/errors/name/argsizeerror">
					<w3fu:text>val-required val-firm err</w3fu:text>	
				</w3fu:if>			
			</w3fu:attribute>
		</input>
		<span class="val-firm-msg">	
			<w3fu:if test="*/form/errors/name/argsizeerror">
				<w3fu:text>Недостаточная длина</w3fu:text>
			</w3fu:if>
		</span>
		
		<div class="bottom-label">1-100 символов: любые</div>
	</w3fu:template>
	
	<w3fu:template name="w3fu:error-auth">
		<div class="error-auth">
			<w3fu:if test="login/error/auth">
				<w3fu:text>Неудачная попытка авторизации.</w3fu:text>
				<br /><br />
				<w3fu:text>Проверьте правильность логина и/или пароля и повторите попытку.</w3fu:text>	
			</w3fu:if>
			<w3fu:if test="register/error/exists">
				<w3fu:text>Неудачная попытка регистрации.</w3fu:text>
				<br /><br />
				<w3fu:text>Учетная запись с таким логином существует. Выберите другой логин.</w3fu:text>	
			</w3fu:if>	
		</div>
	</w3fu:template>

</w3fu:stylesheet>