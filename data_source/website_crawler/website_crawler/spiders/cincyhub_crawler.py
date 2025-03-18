import scrapy
import re
import html2text
from urllib.parse import urlparse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CincyHubSpider(CrawlSpider):
    name = "cincyhub_crawler"

    # Override the default constructor to accept a URL
    def __init__(self, url=None, *args, **kwargs):
        super(CincyHubSpider, self).__init__(*args, **kwargs)

        # Set the start URL
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = ["https://www.cincinnatirecyclingandreusehub.org"]

        # Extract the domain from the starting URL
        parsed_url = urlparse(self.start_urls[0])
        self.allowed_domains = [parsed_url.netloc]

        # Define the rules for following links
        self.rules = (
            # Extract links and follow them, calling parse_item on each
            Rule(
                LinkExtractor(allow=(), allow_domains=self.allowed_domains),
                callback="parse_item",
                follow=True,
            ),
        )

        # Initialize HTML to Markdown converter
        self.html2md = html2text.HTML2Text()
        self.html2md.ignore_links = True
        self.html2md.ignore_images = True
        self.html2md.ignore_tables = False
        self.html2md.body_width = 0  # Don't wrap text

        # Set up the crawler
        super(CincyHubSpider, self)._compile_rules()

    def parse_item(self, response):
        """Parse each page that the crawler visits"""
        self.logger.info(f"Scraping: {response.url}")

        # Convert HTML to Markdown
        # Extract the main content area if possible
        main_content = (
            response.css("section").getall()
            or response.css("article").getall()
            or response.css("div::site-wrapper").getall()
        )

        # print("MAIN CONTENT before body: {}".format(main_content))

        # If no main content area is found, use the whole body
        if not main_content:
            main_content = response.css("body").get()
            # print("MAIN CONTENT from body: {} \n\nResponse: {}".format(main_content, response))

        # Convert HTML to Markdown
        markdown_content = ""
        if isinstance(main_content, list):
            for content in main_content:
                markdown_content += self.html2md.handle(content)
        else:
            markdown_content = self.html2md.handle(main_content) if main_content else ""

        # Clean up the markdown
        markdown_content = self.clean_markdown(markdown_content)

        # Extract metadata for document structure
        title = response.css("title::text").get("").strip()
        h1_tags = response.css("h1::text").getall()
        h1 = h1_tags[0].strip() if h1_tags else title

        # Create a structured markdown document
        structured_markdown = f"# {h1}\n"

        # Add metadata section
        structured_markdown += "\n## Metadata\n"
        structured_markdown += f"- **URL**: {response.url}\n"
        structured_markdown += f"- **Title**: {title}\n"

        meta_description = response.css('meta[name="description"]::attr(content)').get(
            ""
        )
        if meta_description:
            structured_markdown += f"- **Description**: {meta_description}\n"

        meta_keywords = response.css('meta[name="keywords"]::attr(content)').get("")
        if meta_keywords:
            structured_markdown += f"- **Keywords**: {meta_keywords}\n"

        # Add the main content
        structured_markdown += "\n## Content\n"
        structured_markdown += markdown_content + "\n"

        # Get all links on the page
        page_links = LinkExtractor(allow_domains=self.allowed_domains).extract_links(
            response
        )

        """
        if page_links:
            structured_markdown += "\n\n## Links on this page\n"
            for link in page_links:
                structured_markdown += f"- [{link.text.strip()}]({link.url})\n"
        """

        # Return the scraped data
        return {
            "url": response.url,
            "title": title,
            "h1": h1_tags,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "markdown_content": structured_markdown,
            "links_count": len(page_links),
        }

    def clean_markdown(self, markdown_text):
        """Clean up the generated markdown text"""
        # Remove excessive blank lines
        cleaned = re.sub(r"\n{3,}", "\n\n", markdown_text)
        # Fix spacing after headings
        cleaned = re.sub(r"(#+.*)\n(?!\n)", r"\1\n\n", cleaned)
        # Remove any weird characters that html2text might leave
        cleaned = re.sub(r"[^\x00-\x7F]+", " ", cleaned)
        # Normalize whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        cleaned = re.sub(r"##", "\n##", cleaned)
        cleaned = re.sub(r"\*\*\*\*", "**\n**", cleaned)
        # Restore paragraphs
        cleaned = re.sub(r"(\. |\? |! )(?=[A-Z])", r"\1\n", cleaned)
        return cleaned
