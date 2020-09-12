<!-- PROJECT LOGO -->
<br />

<p align="center">
  <h3 align="center">Mail Cheker</h3>

  <p align="center">
    
  </p>
</p>

<!-- ABOUT THE PROJECT -->

## About The Project

基于 SMS Spam 邮箱分类课题所制作的集 Web 与 AIsolution 于一体的项目

所使用的前端框架为 Vue，位于 frontend 目录之中，
所使用的后端框架为 Flask，文件为 app.py，接洽模型的业务定义在 backend 之中

<!-- GETTING STARTED-->

## Developing

### 1.目录架设

项目分成两部分，上半部为 web 部分，下半部为解题算法部分。
之所以没有将下半部份算作 backend 的一部分是因为如此的分隔能体现二元性。

```
.
├── backend
│   └── ...
├── dist      ——front build for backend
│   └── ...
├── frontend
│   └── ...
├─---------------------------------------
├── data
│   └── ...
├── dataset
│   └── ...
├── checkpoints
│   └── ...
├── models
│   └── ...
├── utils
│   └── ...
├── display
│   └── ...
├── README.md
├── requirements.txt
├── run.py   --starter of flask | entry of project
├── main.py  --train model
└── test
    └── ...

```

### 2.Prerequisites

#### For web-frontend development

-   yarn

```sh
Sea for https://yarn.bootcss.com/
```

-   vue-cli

```sh
yarn global add @vue/cli
```

#### For solution development

-   python3 env
    -   scipy==1.4.1
    -   joblib==0.16.0
    -   Flask_Cors==3.0.9
    -   matplotlib==3.2.1
    -   pandas==1.0.3
    -   nltk==3.5
    -   torchvision==0.7.0
    -   Flask==1.1.2
    -   numpy==1.16.4
    -   torch==1.6.0
    -   ipython==7.18.1
    -   scikit_learn==0.23.2

### 3.Installation

1. Clone the repo

```sh
git clone https://https://github.com/Peviroy/MailChecker.git
cd MailChcker
```

2. Install python package

```sh
pip install -r requirements.txt
```

3. Install python package

```sh
cd frontend
yarn
```

### 4. Start

#### Web part:

虽然预计采用的是静态网页，但在开发过程中利用 flask-cors 能做到前后端的实时交互。同时开启前后端服务即可。

1. Flask：

```sh
FLASK_APP=run.py flask run
```

2. Vue end:

```sh
cd frontend
yarn run serve
```

3. Build test:
   使用`yarn run build`生成 dist 目录，此时单独启动 flask 便是最终的 web 效果

#### Solution part:

针对于邮箱分类，我们设计了朴素贝叶斯分类器、BiLSTM-Attention 分类器以及 LSTM 生成器共计三种模型。
模型位于 model 文件夹之中，根目录下的 main.py 负责了后两者的训练以及预测等开发环境所需的功能

### Deploy

1. Gunicorn
   Gunicorn 为一个轻量级高性能的 Web 服务。之所以不选择 flask 直接用于生产环境的原因在于 flask 毕竟主要是作为一个框架而存在，虽然有服务端配备，但并不出彩。
   而 Gunicorn 采用纯 python 构造，能够快速通过 pip 安装

```sh
pip install gunicorn
```

2. Nginx
   Nginx 在此处起到的作用为处理高并发情况，并且进行反向代理

```
server {
    listen <监听的端口>;

    server_name <监听的域名>;

    access_log  /var/log/nginx/access.log;
    error_log  /var/log/nginx/error.log;

    location / {
        proxy_pass         http://127.0.0.1:5000/ ; # 中转向的url
        proxy_redirect     off;

        proxy_set_header   Host             $http_host;
        proxy_set_header   X-Real-IP        $remote_addr;
        proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;

    }

    location /media  {
        alias /usr/share/nginx/html/media;
    }

    location /static  {
        alias /usr/share/nginx/html/static;
    }
}

```

<!-- USAGE EXAMPLES
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_


<!-- CONTRIBUTING -->

## Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE

## License

Distributed under the MIT License. See `LICENSE` for more information.
-->

<!-- CONTACT

## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email

Project Link: [https://github.com/github_username/repo](https://github.com/github_username/repo)

-->
