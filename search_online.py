import webbrowser


def unknown(massage):
    print("Bot: I'm sorry, but I don't know about that. Let me search online for you.")

    query = '+'.join(massage)
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

    return "...";
