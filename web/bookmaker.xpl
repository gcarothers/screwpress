<p:declare-step xmlns:p="http://www.w3.org/ns/xproc"
	            xmlns:html="http://www.w3.org/1999/xhtml"
	            xmlns:fn="http://www.w3.org/2005/xpath-functions"
	            xmlns:c="http://www.w3.org/ns/xproc-step"
                name="compose-book-site"
                version="1.0">
    
	<p:input port="book_directory" kind="parameter" />

	<p:parameters name="xmlizeparameters">
		<p:input port="parameters">
			<p:pipe step="compose-book-site" port="book_directory" />
		</p:input>
	</p:parameters>

	<!-- Parse the markdown. -->
 	<p:exec name="pandoc" command="pandoc" result-is-xml="false" errors-is-xml="false">
 		<p:input port="source">
 			<p:empty />
 		</p:input>

		<p:with-option name="args" select="fn:concat('-f markdown --html5 --section-divs ', /c:param-set/c:param/@value, '/book.md')">
			<p:pipe step="xmlizeparameters" port="result" />
		</p:with-option>
	</p:exec>

	<!-- Parse the resulting html5 -->
	<p:unescape-markup name="parse_html5" content-type="text/html">
		<p:input port="source">
			<p:pipe step="pandoc" port="result" />
		</p:input>
	</p:unescape-markup>

	<!-- Split out the book's chapters into separate files. -->
 	<p:for-each name="chapters">
		<p:iteration-source select="fn:subsequence(/c:result/html:html/html:body/html:section/html:section, 2)">
			<p:pipe step="parse_html5" port="result" />
		</p:iteration-source>

		<p:variable name="chapter_file_name" select="fn:concat(fn:replace(html:section/@id, '-', '_'), '.html')">
			<p:pipe step="chapters" port="current" />
		</p:variable>

		<p:store name="store-chapters">
			<p:input port="source">
				<p:pipe step="chapters" port="current" />
			</p:input>
			<p:with-option name="href" select="fn:concat(/c:param-set/c:param/@value, '/', $chapter_file_name)">
				<p:pipe step="xmlizeparameters" port="result" />
			</p:with-option>
		</p:store>
	</p:for-each>

</p:declare-step>