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
python -r requirements.txt
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

当前一方面是因为尚未完成模型的全面工作，另一方面是因为设计的模式为 api 模式，因而尚未设计 main 入口函数，而单纯是提供了几个简单的 api。
solution 方面的进展可以见 display/data_evaluate.ipynb

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
