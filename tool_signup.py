import requests
from bs4 import BeautifulSoup
from loguru import logger

class TelegramBot:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message: str):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
        }
        try:
            response = requests.post(url, data=payload)
            response_data = response.json()
            if not response_data.get("ok"):
                logger.error(f"Failed to send message: {response_data}")
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {str(e)}")

# Function to crawl technology news from vnexpress.net
def crawl_news():
    url = "https://vnexpress.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_data = []
    for article in soup.find_all('article', class_='item-news', limit=10):  # Limit to 5 articles
        title_element = article.find('h3', class_='title-news')
        title = title_element.text.strip() if title_element else "No title"
        link = title_element.find('a')['href'] if title_element and title_element.find('a') else "#"
        summary_element = article.find('p', class_='description')
        summary = summary_element.text.strip() if summary_element else "No summary available"

        news_data.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return news_data

# def crawl_news():
#     url = "https://baomoi.com/"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     news_data = []
#     for article in soup.find_all('div', class_='group/card', limit=5):  # Limit to 5 articles
#         title_element = article.find('h3', class_='title-news')
#         title = title_element.text.strip() if title_element else "No title"
#         link = title_element.find('a')['href'] if title_element and title_element.find('a') else "#"
#         summary_element = article.find('p', class_='description')
#         summary = summary_element.text.strip() if summary_element else "No summary available"

#         news_data.append({
#             "title": title.encode('utf-8', errors='ignore').decode(),  # Ensure proper encoding
#             "link": link,
#             "summary": summary.encode('utf-8', errors='ignore').decode()  # Ensure proper encoding
#         })

#     return news_data


# Function to prepare and send news to Telegram
def send_news_to_telegram(news_data, bot_token, chat_id):
    bot = TelegramBot(bot_token, chat_id)

    # Use proper Unicode characters instead of surrogate pairs
    message = "📊 <b>Today's News Summary from VNExpress</b>\n\n"
    for i, news in enumerate(news_data, 1):
        message += f"{i}. <b>{news['title']}</b>\n{news['summary']}\n<a href=\"{news['link']}\">Read More</a>\n\n"

    bot.send_message(message)

# Main function to schedule the task
def main():
    def job():
        news_data = crawl_news()
        bot_token = "token"  # Replace with your bot token
        chat_id = "chat_ia"  # Replace with your chat ID
        send_news_to_telegram(news_data, bot_token, chat_id)
    job()
    print("News Crawler Bot is running... Press Ctrl+C to stop.")

if __name__ == "__main__":
    main()