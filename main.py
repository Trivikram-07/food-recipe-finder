import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

# TheMealDB API endpoint for searching by name
API_URL_SEARCH = "https://www.themealdb.com/api/json/v1/1/search.php"

# TheMealDB API endpoint for fetching details by ID
API_URL_DETAILS = "https://www.themealdb.com/api/json/v1/1/lookup.php"         ####
                                                                                ##############important
def search_recipe():
    query = entry.get()
    if not query:
        return

    # Send a GET request to TheMealDB API to search for recipes
    params = {"s": query}
    
    try:
        response = requests.get(API_URL_SEARCH, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        recipes = data.get("meals")

        if recipes:
            display_recipe(recipes[0])
        else:
            result_label.config(text="No recipes found")
    
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {e}")
    except ValueError as e:
        result_label.config(text="Error: Unable to parse response")

def display_recipe(recipe):
    result_label.config(text="")  # Clear previous result

    # Extract recipe details
    recipe_name = recipe["strMeal"]
    recipe_id = recipe["idMeal"]
    instructions = recipe["strInstructions"]
    
    ingredients = []
    for i in range(1, 21):
        ingredient = recipe[f"strIngredient{i}"]
        measure = recipe[f"strMeasure{i}"]
        if ingredient:
            ingredients.append(f"{measure} {ingredient}")

    # Display recipe details in the GUI with text wrapping
    result_label.config(text=f"Name: {recipe_name}\n\nIngredients:\n{', '.join(ingredients)}\n\nInstructions:\n{instructions}", wraplength=1200)

    # Fetch and display the image of the dish
    image_url = recipe["strMealThumb"]
    display_image(image_url)

def display_image(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        img_data = Image.open(BytesIO(response.content))
        img_data.thumbnail((300, 300))  # Resize the image to fit the window
        img = ImageTk.PhotoImage(img_data)

        image_label.config(image=img)
        image_label.image = img
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error fetching image: {e}")
    except Exception as e:
        result_label.config(text=f"Error displaying image: {e}")

# Create the main application window
root = tk.Tk()
root.title("Food Recipe Finder")
root.configure(bg="#222831")

# Entry widget for entering the meal name
entry = tk.Entry(root, width=40,bg="#DBE2EF")
entry.pack(pady=10)

# Search button
search_button = tk.Button(root, text="Search", command=search_recipe)
search_button.pack()

# Label to display the result with text wrapping
result_label = tk.Label(root, text="",bg="#00ADB5")
result_label.pack()

# Label to display the image
image_label = tk.Label(root)
image_label.pack()

# Start the Tkinter main loop
root.mainloop()
