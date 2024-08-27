# InstaBooking

InstaBooking is a hotel booking platform built using Django, offering users the ability to search for, book, and manage hotel reservations. It also includes a recommendation system powered by machine learning to suggest the best rooms based on user preferences.

## Features

- **User Authentication**: Sign up, log in, and manage your bookings.
- **Search and Filter**: Find hotels based on location, price, rating, and room type.
- **Booking Management**: Book rooms, view existing bookings, and cancel reservations.
- **Recommendation System**: Personalized room suggestions based on search parameters.
- **Chatbot Integration**: Get booking assistance through an integrated Rasa chatbot.

## Installations

1. Clone the repository:
   ``` bash
   git clone https://github.com/mufeez7/Insta_Booking.git

2. Navigate to project directory:
   ``` bash
   cd Insta_Booking

3. Create virtual environment:
   ``` bash
   python -m venv venv
   venv\Scripts\activate

4. Install required packages:
   ``` bash
   pip install -r requirements.txt

5. Apply migrations
   ``` bash
   py manage.py makemigrations
   py manage.py migrate

6. Start the server
   ``` bash
   py manage.py runserver

## Running Rasa chatbot

- In a separate terminal window use the following command
  ``` bash 
  rasa run -m models --enable-api --cors "*" --debug

- For enabling custom actions use the following command in a separate terminal
  ``` bash
  rasa run actions

## Usage
- **Homepage**: View the homepage from where you can navigate to different pages.
- **Hotel Listings**: Browse through various hotels along with their descriptions and images.
- **My Bookings**:  Lists all of the bookings made by the currently logged in user.
- **Chatbot**: Use the integrated chatbot to assist with booking and availability related queries.
- **Recommendation**: Recommends the user a hotel name based on their preferences. 