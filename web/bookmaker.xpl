<p:declare-step xmlns:p="http://www.w3.org/ns/xproc"
	            xmlns:html="http://www.w3.org/1999/xhtml"
                name="compose-book-site"
                version="1.0">
    
	<!-- Get the book HTML5 input on STDIN -->
	<p:input port="book" />

	<!-- Split out the book's chapter sections. -->
	<p:for-each name="chapters">
		<p:iteration-source select="fn:subsequence(/xhtml:section/xhtml:section, 2)">
			<p:pipe step="compose-book-site" port="book" />
		</p:iteration-source>

		<!-- Store each chapter to a file. -->
		<p:store>
			<p:input port="source">
				<p:pipe step="chapters" port="current" />
			</p:input>
			<p:with-option name="href" select="fn:concat(fn:replace(xhtml:section/@id, '-', '_'), '.html')">
				<p:pipe step="chapters" port="current" />
			</p:with-option>
		</p:store>
	</p:filter>

</p:declare-step>