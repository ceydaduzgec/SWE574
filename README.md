
<div id="top"></div>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/swe574-spring23/SWE574">
    <img src="docs/boun.png" alt="Logo" width="380" height="200">
  </a>

<h3 align="center">SWE 574 Software Development Practice</h3>

  <p align="center">
    Boğaziçi University Spring'23 Software Development Course Project
    <br />
    <a href="https://github.com/swe574-spring23/SWE574/wiki"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/swe574-spring23/SWE574">View Demo</a>
    ·
    <a href="https://github.com/swe574-spring23/SWE574/issues/new">Report Bug</a>
    ·
    <a href="https://github.com/swe574-spring23/SWE574/issues/new">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
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
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This projects is for the SWE 574 Software Development Practice course of Boğaziçi University on Spring'23 and supervised by [Suzan Uskudarlı](https://github.com/uskudarli). It will be updated each week in order to reflect projects process which is divided into 3 Milestones. You can find out more about it on the [wiki](https://github.com/swe574-spring23/SWE574/wiki).

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

- [![Django][django-image]][django-url]
- [![Bootstrap][Bootstrap.com]][Bootstrap-url]
- [![Postgresql][Postgresql.org]][Postgresql-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Download Docker from [here](https://www.docker.com/products/docker-desktop/)


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/swe574-spring23/SWE574.git
   ```
2. Create a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments
   "Official documentation") in the project folder:

    `python -m venv venv`

3. [Activate](https://docs.python.org/3/library/venv.html#creating-virtual-environments:~:text=Command%20to%20activate%20virtual%20environment
   "Official documentation") the virtual environment:

    `source venv/bin/activate`

4. Install the requirements:

    `pip install -r requirements/local.txt`

5. Compose Docker or run the stack if it already exists.

    `docker-compose -f local.yml build` or `docker-compose -f local.yml up`

6. Migrate models.

    `python manage.py migrate`

7. Run on your local.

    `python manage.py runserver 0.0.0.0:8000`

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- DOCUMENTATION -->
### Create Mock Data

To generate mock data for your local, you can use the following command, after the installation steps:
  `python manage.py generate_data`

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

See the [open issues](https://github.com/swe574-spring23/SWE574/issues) for a full list of proposed features (and known issues).
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "Type: Enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/SWE574`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/SWE574`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/swe574-spring23/SWE574](https://github.com/swe574-spring23/SWE574)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Suzan Uskudarlı](https://github.com/uskudarli)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/swe574-spring23/SWE574.svg?style=for-the-badge
[contributors-url]: https://github.com/swe574-spring23/SWE574/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/swe574-spring23/SWE574.svg?style=for-the-badge
[forks-url]: https://github.com/swe574-spring23/SWE574/network/members
[stars-shield]: https://img.shields.io/github/stars/swe574-spring23/SWE574.svg?style=for-the-badge
[stars-url]: https://github.com/swe574-spring23/SWE574/stargazers
[issues-shield]: https://img.shields.io/github/issues/swe574-spring23/SWE574.svg?style=for-the-badge
[issues-url]: https://github.com/swe574-spring23/SWE574/issues
[license-shield]: https://img.shields.io/github/license/swe574-spring23/SWE574.svg?style=for-the-badge
[license-url]: https://github.com/swe574-spring23/SWE574/LICENSE.txt


[product-screenshot]: images/screenshot.png

[Django-image]: https://img.shields.io/badge/Django-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[Django-url]: https://nextjs.org/

[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Postgresql.org]: https://img.shields.io/badge/Postgresql-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[Postgresql-url]: https://www.postgresql.org/