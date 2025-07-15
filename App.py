from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_price(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'lxml')
        title = soup.find(id='productTitle').get_text().strip()
        price = soup.find('span', {'class': 'a-price-whole'}).get_text().replace(',', '')
        return title, float(price)
    except:
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        target = float(request.form['target'])
        title, current_price = get_price(url)
        if title and current_price:
            status = "Price is below target!" if current_price <= target else "Price is above target."
            return render_template('result.html', title=title, price=current_price, status=status)
        else:
            return render_template('result.html', error="Could not fetch product.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
