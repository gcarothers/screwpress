<xsl:stylesheet version="2.0"
				xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
				xmlns:html="http://www.w3.org/1999/xhtml">
	<xsl:template match="/">
		<html:html>
			<html:head>
			</html:head>
			<html:body>
				<xsl:copy-of select="."/>
			</html:body>
		</html:html>
	</xsl:template>
</xsl:stylesheet>