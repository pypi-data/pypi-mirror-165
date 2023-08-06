# Development environment for ML projects

## Local environment 

Here are the steps to start developing and run code *locally*
 * Clone this repo
 * If you don't have python installed on your machine, install Python
 * If you don't have poetry installed on your Python environement, type
    ```bash
    pip install poetry
    ```
 * Install the necessary dependencies in a virtual environment
    ```bash
    poetry install
    ```
 * Run the command in the virtual env
    ```bash
    poetry run python -m app
    ```
 * Add dependencies to the project, for example the library requests in this case
    ```bash
    poetry add requests
    ```
## Docker environment 
Here are the steps to start developing and run code *on a Docker image*
 * If you don't have Docker installed on your machine, install Docker
 * Build an image based on the Dockerfile of this repo
    ```bash
    docker build -t ml-env .
    ```
 * Run the image
    ```bash 
    docker run -it ml-env
    ```

## Testing 
The tests are included in the tests folder, and uses pytest as testing library.