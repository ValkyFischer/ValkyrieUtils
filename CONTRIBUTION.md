# Contribution Guidelines

We welcome contributions from the community to improve Valkyrie Utils. By contributing to this project, you help 
make it better and more useful for everyone. Here are a few guidelines to follow:

---

## How to Contribute

1. Fork the repository to your GitHub account.


2. Clone the forked repository to your local machine:

    ```bash
    git clone https://github.com/ValkyFischer/ValkyrieUtils.git
    cd ValkyrieUtils
    ```


3. Create a new branch for your contribution:

    ```bash
    git checkout -b feature/your-feature
    ```

    Please use a descriptive branch name that reflects the contribution you're making (e.g., `feature/new-logger-functionality`).


4. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Add your descriptive commit message here"
    ```


5. Push the changes to your repository:

    ```bash
    git push origin feature/your-feature
    ```


6. Create a pull request (PR) from your branch to the main repository's `develop` or `main` branch.

    - Make sure to describe your changes in the PR and provide any necessary context.
    - If your PR relates to an existing issue, reference the issue in the description (e.g., "Closes #123").


7. Your PR will be reviewed by the maintainers, and feedback or changes may be requested.

---

### Code Style

Please follow the existing code style and structure in the project to maintain consistency.
   - Use 4 spaces for indentation.
   - Use descriptive variable and function names.
   - Use docstrings to document classes and functions.
   - Use type hints for function parameters and return values.
   - Use `camelCase` for function and class names.
   - Use `snake_case` for variable names.
   - Use `ALL_CAPS` for constants and enums.
   - Use `_` as prefix for private variables and functions.

### Testing

If your contribution involves code changes, make sure to add or modify tests where necessary to maintain test coverage.
   - Use the `unittest` module for testing.
   - Use the `test_` prefix for test functions.

### Reporting Issues

If you encounter any issues or have suggestions for improvements, please open an issue in the [GitHub repository](https://github.com/ValkyFischer/ValkyrieUtils/issues).
   - Use a descriptive title and description for the issue.
   - If the issue relates to a specific module, please mention it in the description.

### License

By contributing to this project, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

***Thank you for contributing!***
