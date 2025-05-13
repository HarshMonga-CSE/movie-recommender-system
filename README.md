# 🎬 Content-Based Movie Recommender System

A web app that uses **Content-Based Filtering** to recommend movies based on their content. Users can input a **movie title** or **genre**, and the system suggests similar movies using **Bag of Words** and **Cosine Similarity**.

---

## 🔗 Live Demo

> [Click here to view the live app](https://movie-recommender-system-m8ow.onrender.com) 

---

## ✨ Features

- 🔍 Input a **movie title** or **genre** to get movie recommendations
- 🧠 **Content-Based Filtering** for personalized movie suggestions
- 📝 Uses **Bag of Words** and **Cosine Similarity** for text analysis
- 🎥 Discover new movies based on content similarity


---

## 🛠 Tech Stack

- Python
- **Streamlit** for UI
- **Natural Language Processing (NLP)**
- **Bag of Words**
- **Cosine Similarity**
- **pandas**, **scikit-learn**

---

## 💻 Setup

To run this project locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/HarshMonga-CSE/movie-recommender-system.git
    ```

2. Navigate into the project directory:
    ```bash
    cd movie-recommender-system
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:
    ```bash
    streamlit run app.py
    ```

5. Visit the app at `http://localhost:8501` in your browser.

---

## 📝 How It Works

1. **Input a Movie Title or Genre:** Type in a movie name or choose a genre.
2. **System Analysis:** The app uses **Bag of Words** to process movie descriptions.
3. **Recommendation:** The app compares the input with a database of movies using **Cosine Similarity** to suggest similar movies.

---

## 📸 Screenshots

### 🏠 Home Page
![Home Page](./screenshots/home.png)

### ✍️ Input Movie Title
![Input Movie](./screenshots/input.png)

### 🔠 Movie Recommendations
![Movie Recommendations](./screenshots/recommendations.png)
![](./screenshots/recommendations2.png)

---


