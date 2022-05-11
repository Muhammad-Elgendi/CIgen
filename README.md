<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com//Muhammad-Elgendi/CIgen">
    <img src="staticfiles/img/favicon.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">CIgen</h3>

  <p align="center">
    CIgen is an open-source quizzing software to create and deliver online quizzes, exams, and tests.
    <br />
    <a href="https://github.com//Muhammad-Elgendi/CIgen"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com//Muhammad-Elgendi/CIgen">View Demo</a>
    ·
    <a href="https://github.com//Muhammad-Elgendi/CIgen/issues">Report Bug</a>
    ·
    <a href="https://github.com//Muhammad-Elgendi/CIgen/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


### Built With

* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Install docker engine and docker compose.
* Docker engine
  ```
  https://docs.docker.com/engine/install/
  ```
* Docker compose
  ```
  https://docs.docker.com/compose/install/
  ```
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com//Muhammad-Elgendi/CIgen.git
   ```
2. Go to CIgen directory
   ```sh
   cd CIgen/
   ```
3. Create your own .env files by copying .env.example
   ```sh
   cp .env.example .env.dev
   cp .env.example .env.prod
   ```
4. Go to docker directory
   ```sh
   cd CIgen/docker
   ```
5. Create your own .env file for docker compose by copying .env.example
   ```sh
   cp .env.example .env
   ```
6. Create and start all the containers
   ```sh
   docker-compose up
   ```
7. Generate a new security key

8. Creating a New Administrator Account
    ```sh
   docker-compose exec web bash
   python manage.py createsuperuser
   ```
9. Fill out your credentials

10. Open a new browser tab and Visit localhost:8000




<!-- Use Cases -->
## Use Cases

CIgen could be used for different use cases, here are some examples:

1. Quiz maker software
2. Attendance management software

Additional screenshots, screencasts, and more resources will be soon.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 license. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Muhammad Elgendi- [@gendidev](https://twitter.com/@gendidev)

Project Link: [https://github.com//Muhammad-Elgendi/CIgen](https://github.com//Muhammad-Elgendi/CIgen)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username