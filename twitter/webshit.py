search_form = """
    <form action="/query" method="post">
      <input type="text" name="query" size=100/>
      <input type="submit" value="Search Twitter!"/>
    </form>
"""


wordle_applet = unicode("""
    <applet 
        name="wordle" 
        mayscript="mayscript" 
        code="wordle.WordleApplet.class"
        codebase="http://wordle.appspot.com" 
        archive="/j/v1356/wordle.jar" 
        width="100%" height="600">
        <param name="font" value="Kenyan Coffee"/>
        <param name="background" value="0x000000"/>
        <param name="color" value="Organic Carrot"/>
        <param name="text" value="{text}"/>
        <param name="java_arguments" value="-Xmx256m -Xms64m">
        Your browser doesn't seem to understand the APPLET tag.
        You need to install and enable the <a href="http://java.com/">Java</a> plugin.
    </applet>
""")

style_info = unicode("""
    /* ------------------
 styling for the tables 
   ------------------   */


body
{
    color: navy;
    background-color: #c0deed;
	line-height: 1.6em;
	width: 900px;
	margin: 45px;
    font-family: 'Open Sans Condensed', sans-serif;
}

h, h1, h2
{
text-transform:capitalize;
}
table
{

	font-size: 12px;
	margin: 45px;
	width: 900px;
	text-align: left;
	border-collapse: collapse;
	background-color: #fff;
}

tr
{
	padding: 8px 2px;
	font-weight: normal;
	font-size: 14px;
	border-bottom: 2px solid #6678b1;
	border-right: 30px solid #fff;
	border-left: 30px solid #fff;
	color: #039;
}

td
{
	padding: 12px 2px 0px 2px;
	border-right: 30px solid #fff;
	border-left: 30px solid #fff;
	color: #669;
}
""")
    

