# Graphanator

Graphanator is a powerful and flexible LLM graph generation tool designed to help you create, and visualize complex graphs with ease.

![Graphanator Example](https://github.com/Deckel/graphanator/blob/master/static/images/readme_example.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Graphanator is designed to simplify the process of generating and working with graphs. Whether you are a data scientist, a researcher, or a developer, Graphanator provides the tools you need to create and manipulate graphs efficiently.

## Features

- Reads a CSV and generates context for an LLM
- Auto generate graphs using test prompt input
- Graphical interface to generate graphs

## Installation

To install Graphanator, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/graphanator.git
    ```
2. Navigate to the project directory:
    ```bash
    cd graphanator
    ```
3. Install the required dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```
4. Follow the instructions in these [docs](https://platform.openai.com/docs/quickstart) to get an openai api key 

5. Add your OPENAI_API_KEY to a .env file

## Usage

To start using Graphanator, follow these steps:

1. Run the application:
    ```bash
    flask run
    ```
2. Open your browser and navigate to `http://127.0.0.1:5000`.

3. Press start to initate a conversation and ask questions!

## Contributing

We welcome contributions to Graphanator! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add your commit message"
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.