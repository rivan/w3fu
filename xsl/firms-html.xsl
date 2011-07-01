<w3fu:stylesheet version="1.0"
	xmlns:w3fu="http://www.w3.org/1999/XSL/Transform">

	<w3fu:include href="common/head.html.xsl" />
	<w3fu:include href="common/footer.html.xsl" />
	<w3fu:include href="common/nav.html.xsl" />
<!-- 	<w3fu:include href="common/errors.html.xsl" /> -->
	<w3fu:include href="common/user.html.xsl" />
	<w3fu:include href="common/forms.html.xsl" />
	
	<w3fu:template match="/">
		<html>
			<head>
			<title>Вход на сайт</title>
			<meta name="keywords" content="войти, вход, залогиниться" />
    		<meta name="description" content="Вход на сайт" />
			<w3fu:call-template name="w3fu:links" />
			</head>
			
			<body>
				<w3fu:call-template name="w3fu:statnav" />
			
				<div class="container_16">
				<div class="grid_12 l-header">
					<p>Заголовок</p>
				</div>
				<div class="grid_4 l-header">
					<w3fu:call-template name="w3fu:user-login" />
				</div>
				
				<div class="clear"></div>
				
					<div class="grid_3 l-main"><br/></div>	
					<div class="grid_10">
					<div>Создать компанию</div>						
						
						<form method="post" action="/admin/firms" class="firm-create">												
							<w3fu:call-template name="w3fu:edit-firm" />
							<input type="submit" class="button-enter" value="Создать" />
							
						</form>
					</div>
					<div class="grid_3 l-main"><br/></div>
					<div class="clear"></div>

				<div class="grid_16 l-footer">
					<w3fu:call-template name="w3fu:footer" />
				</div>
				<div class="clear"></div>
				<w3fu:call-template name="w3fu:user-not-login" />
				</div>
			</body>
		</html>
		
	</w3fu:template>

</w3fu:stylesheet>