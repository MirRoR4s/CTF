FROM node:18-alpine

#设定工作目录，以后各层的目录从此处开始。
WORKDIR /app 

#将主机 package开头的文件复制到 /app 下
COPY package* ./

#RUN指令用来执行命令行命令
RUN npm ci

#将 web.js 文件复制到 /app 下
COPY web.js ./

#指定当前用户为 node
USER node

#容器主进程的启动命令
CMD node web.js