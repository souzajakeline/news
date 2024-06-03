import scrapy
from readability import Document
import lxml.html

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    
    # URL where the spider will start crawling
    start_urls = [
        'https://www.theguardian.com/au'
    ]

    # Method to handle the response from the initial request
    def parse(self, response):
       #  Extract article links 
        for article_url in response.css('a::attr(href)').extract():
            if 'article' in article_url:
                yield response.follow(article_url, self.parse_article)
                
                
    #  Method to handle the response from each article page
    def parse_article(self, response):
        # Use Readability to extract the main content
        doc = Document(response.text)
        article_html = doc.summary() # Get the summarized HTML of the article
        article_title = doc.title() # Get the title of the article
        
        # Clean the article HTML to extract text content
        tree = lxml.html.fromstring(article_html)
        article_text = tree.text_content()# Get the cleaned text content of the article
        
        # Extract description
        article_caption = response.css('meta[name="description"]::attr(content)').get()
        
        # Extract the author's name from the article
        author = response.css('a[rel="author"]::text').get()
        if not author:
            # Try to find the author again if the first try fail
            author = response.css('address[aria-label="Contributor info"] span::text').get()
            
        url = response.url

        # Yield a dictionary with the extracted data
        yield {
            'title': article_title,
            'caption': article_caption,
            'author': author,
            'url': url,
            'text': article_text,
        }
