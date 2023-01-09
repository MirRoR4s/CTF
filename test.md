### 记录一下 git 相关操作

#### 新建分支 a 

```
git branch a
```

#### 切换到分支 a

```
git checkout a
```

#### 拉取远程分支到本地（本地没有这个分支）

如果远程分支有个 develop,而本地没有，你想把远程的 develop 分支迁到本地：

```
git branch develop origin/develop
```

如果你想拉取的同时切换到该分支，那么输入如下命令

```
git checkout -b develop origin/develop
```

#### 把 develop 分支推送到远程仓库

```
git push origin develop
```

如果你远程的分支想取名叫 develop2,那执行以下代码：

```
git push origin develop:develop2
```

但是强烈不建议这么做，这会导致混乱并难以管理，所以建议本地分支跟远程分支名要保持一致。

