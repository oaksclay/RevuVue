import os
import sqlite3
import streamlit as st
import openai


class ReviewApp:

  def __init__(self, db_name='reviews.db'):
    self.conn = sqlite3.connect(db_name)
    self.c = self.conn.cursor()

  def setup(self):
    # Set OpenAI API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if OPENAI_API_KEY is None:
      st.error("OPENAI_API_KEY environment variable is not set")
      return
    openai.api_key = OPENAI_API_KEY

    # Create customer reviews table
    try:
      self.c.execute('''
                CREATE TABLE IF NOT EXISTS reviews(
                    rating integer,
                    text text
                )
            ''')
      self.conn.commit()
    except Exception as e:
      st.error(f"Failed to set up database: {e}")

  def add_review(self, rating, review_text):
    try:
      self.c.execute("INSERT INTO reviews VALUES (?, ?)",
                     (rating, review_text))
      self.conn.commit()
    except Exception as e:
      st.error(f"Failed to add review: {e}")

  def compute_average_rating(self):
    try:
      self.c.execute("SELECT AVG(rating) from reviews")
      avg_rating = self.c.fetchone()[0]
      return round(avg_rating, 2) if avg_rating is not None else None
    except Exception as e:
      st.error(f"Failed to compute average rating: {e}")

  def get_all_reviews(self):
    try:
      self.c.execute("SELECT * FROM reviews")
      return self.c.fetchall()
    except Exception as e:
      st.error(f"Failed to fetch all reviews: {e}")
      return []

  def create_master_review_summary(self):
    all_reviews = self.get_all_reviews()
    review_texts = ' '.join([review[1] for review in all_reviews])
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{
        "role":
        "system",
        "content":
        "You are reading a summary of customer reviews. Provide the overall sentiment, and write a brief summary of the reviews. Keep the summary to less than 6 sentences."
      }, {
        "role": "user",
        "content": review_texts
      }],
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0)
    return response.choices[0].message['content']

  def clear_data(self):
    try:
      self.c.execute("DROP TABLE IF EXISTS reviews")
      self.conn.commit()
      print("Database cleared")
    except Exception as e:
      st.error(f"Failed to clear database: {e}")


def main():
  app = ReviewApp()
  app.setup()
  st.title("Customer Reviews for :bed:")
  if st.button('Clear Database'):
    app.clear_data()
  # Get the user input
  rating = st.number_input('Enter Rating (1-5)', min_value=1, max_value=5)
  review_text = st.text_input('Enter Review')
  # On the press of the button
  if st.button('Add Review'):
    app.add_review(rating, review_text)
  avg_rating = app.compute_average_rating()
  st.subheader(
    f'Average Rating: {avg_rating if avg_rating is not None else "No ratings yet."}'
  )
  master_summary = app.create_master_review_summary()
  st.subheader(f'Review Summary: {master_summary}')

  st.subheader("All Reviews")
  # Get all reviews from the database
  all_reviews = app.get_all_reviews()
  if all_reviews:
    for review in all_reviews:
      st.write(f"{'⭐' * review[0]}: {review[1]}")


if __name__ == '__main__':
  main()
