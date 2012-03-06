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

