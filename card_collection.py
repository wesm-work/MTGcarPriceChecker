import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

def show_large_image(card):
    large_image_url = card['image_uris']['normal']
    image_bytes = requests.get(large_image_url, verify=False).content
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)
    
    top = tk.Toplevel()
    top.title(card['name'])
    
    card_label = tk.Label(top, image=tk_image)
    card_label.image = tk_image
    card_label.pack(padx=5, pady=5)

def search_card(event=None):
    card_name = entry.get()
    response = requests.get(f"https://api.scryfall.com/cards/search?q={card_name}", verify=False)
    card_data = response.json()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    if 'data' in card_data:
        for i, card in enumerate(card_data['data']):
            if 'image_uris' in card:
                card_image_url = card['image_uris']['small']
                image_bytes = requests.get(card_image_url, verify=False).content
                data_stream = io.BytesIO(image_bytes)
                pil_image = Image.open(data_stream)
                tk_image = ImageTk.PhotoImage(pil_image)
                card_label = tk.Label(scrollable_frame, image=tk_image)
                card_label.image = tk_image
                card_label.grid(row=2*(i//5), column=i%5, padx=5, pady=5)
                card_label.bind("<Button-1>", lambda event, card=card: show_large_image(card))

                price_usd = card['prices']['usd']
                price_eur = card['prices']['eur']
                price_tix = card['prices']['tix']

                price_text = "Price data not available."
                if price_usd:
                    price_text = f"USD: ${price_usd}"
                if price_eur:
                    price_text += f"  EUR: €{price_eur}"
                if price_tix:
                    price_text += f"  TIX: {price_tix}"

                price_label = tk.Label(scrollable_frame, text=price_text)
                price_label.grid(row=2*(i//5) + 1, column=i%5, padx=5, pady=5)

root = tk.Tk()
root.title("Trading Card Collection")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{screen_width}x{screen_height}')

search_frame = tk.Frame(root)
search_frame.pack(padx=10, pady=10)

label = tk.Label(search_frame, text="Enter card name:")
label.pack(side=tk.LEFT, padx=5, pady=5)

entry = tk.Entry(search_frame, width=50)
entry.pack(side=tk.LEFT, padx=5, pady=5)
entry.bind('<Return>', search_card) # Bind the Enter key to the search_card function

search_button = tk.Button(search_frame, text="Search", command=search_card)
search_button.pack(side=tk.LEFT, padx=5, pady=5)

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()
