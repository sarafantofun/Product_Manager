# Product Manager Project

Product Manager is a FastAPI-based application built with Poetry for dependency management and Alembic for database migrations. This project allows for creating, retrieving, updating, and deleting products, along with user management and authentication functionalities.

## Project Structure

- **FastAPI**: A Python web framework for building APIs.
- **Poetry**: A dependency manager for Python, managing both project dependencies and environment.
- **Alembic**: A tool for database migrations, integrated with SQLAlchemy for schema management.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sarafantofun/Product_Manager.git
    cd Product_Manager
    ```

2. Install dependencies using Poetry:
    ```bash
    poetry install
    ```

3. Configure environment variables in a `.env` file:
    ```
    POSTGRES_DB=<your_database>
    POSTGRES_USER=<your_user>
    POSTGRES_PASSWORD=<your_password>
    POSTGRES_HOST=<your_host>
    POSTGRES_PORT=<your_port>
    SECRET_KEY=<your_secret_key>
    ```

4. Run database migrations:
    ```bash
    alembic upgrade head
    ```

## Endpoints

### Product Endpoints

- **Create Product**  
  **POST** `/api/product/`
  - Creates a new product with the given details.
  - Body: `{"title": str, "price": float, "count": int}`
  - Response: JSON with the created product details or error if price is negative.

- **Get Product by ID**  
  **GET** `/api/product/{product_id}/`
  - Retrieves a product by its ID.
  - Response: JSON with the product details or 404 if not found.

- **Update Product**  
  **PUT** `/api/product/{product_id}/`
  - Updates a product’s information.
  - Body: `{"title": str, "price": float, "count": int, "description": Optional[str]}`
  - Response: JSON with updated product details or 404 if product is not found.

- **Delete Product**  
  **DELETE** `/api/product/{product_id}/`
  - Deletes a product by its ID.
  - Response: Success message or 404 if product not found.

### User Endpoints

- **Create User**  
  **POST** `/api/users/create_user`
  - Registers a new user.
  - Body: `{"username": str, "password": str, "role": str}`
  - Response: JSON with user details.

Note: Allowed values for role are "admin", "user", or "guest".

### Authentication Endpoints

- **Login for Access Token**  
  **POST** `/api/auth/login`
  - Authenticates the user and returns an access token.
  - Body: `{"username": str, "password": str}`
  - Response: JSON with access token and token type.

## Testing

Tests are written using pytest and pytest-asyncio.

- **Run Tests**:

    ```bash
    pytest
    ```

- **Example Test Cases**:

  - test_create_product_success: Tests successful product creation.
  - test_create_product_negative_price: Tests creating a product with a negative price.
  - test_get_product_by_id: Tests retrieving a product by ID. 

Additional tests cover updating, deleting products, and creating users.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License.

## Author

This project, **Product Manager**, was developed by **Tanya Sarafanova**.

Feedback and suggestions are always welcome!