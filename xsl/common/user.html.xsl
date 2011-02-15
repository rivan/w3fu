<w3fu:stylesheet version="1.0" xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">
	
	<w3fu:template name="w3fu:user-login">
	
	<w3fu:if test="not(*/user)">	
	
		<div class="popup-user-login">
		<a class="dropdown-button"><span>Войти</span></a>		
		<div class="dropdown-content">
			<form method="post" action="/login" class="validate">
				<p>Логин:<input type="text" name="login" maxlength="32" class="val-required val-login" /></p> 
				<p>Пароль:<input type="text" name="password" maxlength="32" class="val-required val-password" /></p>
				<p><input type="submit" class="button" value="ОК" /></p>
			</form>
			<w3fu:apply-templates select="document('../conf/providers.xml')/*" />
			</div>
		</div>
		
	</w3fu:if> 
		
	<w3fu:if test="*/user">
		<div class="popup-user-login">
			<w3fu:value-of select="*/user/login" />
		</div>
	</w3fu:if>
	
	</w3fu:template>
	
	<w3fu:template match="providers/provider">
		<div >
			<w3fu:value-of select="." />
		</div>
	</w3fu:template>

</w3fu:stylesheet>