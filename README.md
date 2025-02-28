# Grocery Store Management System

## Project Description  
The **Grocery Store Management System** helps users **browse and purchase grocery items** efficiently. Users can select items from various categories, add them to a shopping cart, and proceed to checkout. The system also stores order details in a database.

This web application is built using **Flask** and provides an intuitive user interface for grocery shopping.

### Features  
- **User Input Form**: Users can select a **category**, choose an **item**, and specify the **quantity**.  
- **Shopping Cart**: Users can **add, remove, and clear** items from their cart.  
- **Checkout System**: Users can enter **shipping details** and place an order.  
- **Database Integration**: Data is stored in **MySQL**, using tables such as `Users`, `Orders`, `OrderItems`, and `SearchHistory`.  

## Tech Stack  
- **Flask** – Web framework for handling requests and rendering HTML templates.  
- **MySQL** – Database for storing and retrieving user data.  
- **Jinja2** – Templating engine for rendering dynamic HTML in Flask.  
- **Python** – The primary language for backend logic.  
- **HTML/CSS/Bootstrap** – Used for designing the front-end interface and user input form.  

## Setup Instructions  

### Prerequisites  
Ensure you have the following installed:  

- **Python 3.12.3**  
- **MySQL Server**  

#### [Python 3.12 Setup Guide](https://www.python.org/downloads/release/python-3123/)  
- Follow the link for installation instructions.  
- Ensure **Python is added to your system's PATH** during installation.  

#### [MySQL Setup Guide](https://dev.mysql.com/doc/refman/8.0/en/installing.html)  
- Follow the link to install and set up **MySQL Server** on your system.  

### Create a Python Virtual Environment & Install Flask  
1. Open the command line and navigate to the project folder.  
2. Create a virtual environment:  
   ```bash
   python -m venv env
   ```  
3. Activate the virtual environment:  
   - On **Windows**:  
     ```bash
     env\Scripts\activate
     ```  
4. Install the required Python packages:  
   ```bash
   pip install -r requirements.txt
   ```  

### Database Setup in MySQL  
1. Open **MySQL Workbench**.  
2. In the **Menu bar**, click on **Database** → **Connect to Database**, then click **OK**.  
3. In the **Schemas** panel (left side), click the **+** button to create a new schema.  
4. Enter the desired **database name** and click **Apply**.  
5. Once created, **right-click** on the schema and select **Set as Default Schema**.  

### Update Database Credentials  
1. Open the `config.json` file in the project folder.  
2. Update the database credentials with your MySQL details:  

   ```json
   {
       "username": "your-mysql-username",
       "password": "your-mysql-password",
       "host": "localhost",
       "database": "grocery_store"
   }
   ```  

### Create Database Tables  
1. Ensure the **Python virtual environment** is activated:  
   ```bash
   env\Scripts\activate
   ```  
2. Run the following script to create the necessary tables:  
   ```bash
   python create_tables.py
   ```  

### Running the Project  
Once the setup is complete, start the Flask application:  

1. Ensure the **virtual environment** is activated.  
2. Run the application:  
   ```bash
   python app.py
   ```  
3. Open your browser and go to `http://127.0.0.1:5000` to access the **Grocery Store Management System**.  

## Usage  
1. Select a **category**, choose an **item**, and specify the **quantity**.  
2. Add items to the **shopping cart**.  
3. Proceed to **checkout**, enter shipping details, and place an order.  
4. View the **order confirmation page** with details of the purchase.  

## Future Enhancements  
- Add **user authentication** for personalized shopping experiences.  
- Implement **payment integration** for online transactions.  
- Improve **search functionality** with advanced filtering options.  

## Contributing  
We welcome contributions! Feel free to **fork the repository**, submit **issues**, and open **pull requests** with any improvements or features.  

## License  
This project is licensed under the **MIT License**.  

## Acknowledgments  
- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)  
- **MySQL Documentation**: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)  

