# CoquiGames
ICOM 5016 Project

By

Jesmarie Hernandez, Heriberto Bourdon, Abisai Ramos

{jesmarie.hernandez, heriberto.bourdon1, abisai.ramos}@upr.edu

#1. Introduction

There is a lack of competition in the video game store market and a lack of options for customers to purchase their favorite video games and accessories, particularly in the island of Puerto Rico. In the island there is a absence of stores whose primary selling point is video games. Therefore, the gaming community in Puerto Rico are forced to choose between buying their video games online or in the island’s chain stores, which don’t offer a variety of prices.
CoquiGames is a web store that will offer a viable solution to the gaming community in Puerto Rico by offering weekly deals, variety in titles available, optional payment methods etc. 
CoquiGames will be implemented as a responsive web application; it will be designed to be viewed appropriately as desktop and as a mobile website. As a responsive web application, clients who either own a phone or a computer will be able to access it without the need of downloading and installing an application. 
CoquiGames will be implemented using the following technologies 
Client Side Tools: AngularJS, HTML/CSS (Bootstrap).
Server Side Tools: JavaPlay, PostgreSQL.

#2. Client App Description

CoquiGames will be implemented using HTML5, CSS, Bootstrap, JavaScript and AngularJS. Will have two kinds of users the regular users (viewers or customers) and administrators. The Regular users are persons that can browse for merchandise and place purchase orders. The Administrators are the IT personnel in charge of supporting and maintaining the database.
A regular user will be able to perform the following tasks: create, login, view, and modify the account information. Account information will consist of: customer name, mailing address, billing address, credit card information. A customer without an account can only browse and view items, and place them in the shopping cart. However, at the moment of placing an order, the customer must be logged on to the account. 
It will be able to browse the following categories of products: video games, platforms and accessories; also browse products available within the categories. There will be an option to allow the products to appear in increasing order of price, or sorted by platform, or sorted by product name. There will be means to search for a product. 
It will be able to view the details of a product. Details will consist of product name, instant price, description, photo of product, reviews. There will be means to place, view and update a shopping cart. Place an order for items in the shopping cart. Get an invoice of an order that has been placed by email. Also the app will keep the invoice in the records for future reference. Order status information will be shown in the following format: open, closed, in transit, cancelled, pre-ordered. Finally review products using a 5-star rating system and a comment. 
An administrator of the CoquiGames will be able to create, view, and modify customer
and administrator accounts also export sales data to a CSV file for reporting purposes

#3. Server Side Description

The store data will be obtained from a Flask (Python) server using REST calls and encoding data with JSON. The data will be stored in PostgreSQL (object-relational database system). The data objects are maintained and access in terms of four operations, often described with the acronym CRUD (Create, Read, Update, Delete). For the security and integrity of the store data the functionality will be limited to the user role.
A regular user will be able to perform the following tasks in the server:
Authenticate a customer account.
Create\Read\Update a customer account. 
Read products by category.
Read the details of a product.
Read\Update a shopping cart.
Create an order for items in the shopping cart.
Create\Read\Email an invoice of an order that has been placed.
Read a Review of a product, only logged user will Create\Update\Delete a review.
An administrator of the CoquiGames will be able to:
Authenticate an administrator account.
Create\Read\Update\Delete customer and administrator accounts.
Read sales data.
The signup process will be handled by way of a script configured for the application, which connects to the application server, handles the verification process and creates a session in the application server (Flask Server). User sensitive information such as credit numbers must be encrypted, for safety and protection of all the clients. Our front-end (which will be Angular) is going to request the back-end (Flask Server) for an encryption key. The front end will then encrypt the credit card information and then return it to the back end. Finally, the back end will decrypt information and the it will be stored in the database, which will once again encrypt the information.  


Planned Tables:
Table
Description
User:
Stores the user personal information.
User Account:
Holds the information to access and account.
User Role:
Has the account role and if its active.
Address:
Keeps all of the corresponding fields for an address.
Order:
Retains the order customer, date amount, tax.
Order Details
Stores the products in an order their quantity and price.
Order Status
Holds order status information such as open, cancelled, in transit etc.
Wish List
Has the products a user wishes to buy in the near future.
Shopping Cart
Keeps the selected products by a customer.
Reviews
Retains user reviews.
Platform
Stores additional information regarding a platform   
Game
Holds additional information regarding a game   
Accessories
Has additional information regarding an accessory.
Product Details
Keeps contain the general information of a product such as name, price, type, quantity, etc. 
Photos
Stores the photo name and location in the server.

#4. Division of Labor
Team Member
Tasks
Heriberto Bourdon
Products Reviews.
View the details of a product
Jesmarie Hernandez 
Browse for products
Shopping Cart
Abisai Ramos 
Account Sign up 
Export sales data.
Order creation and Invoice

