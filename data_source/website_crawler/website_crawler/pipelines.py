# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import csv
import os
import re
from urllib.parse import urlparse


class WebsiteCrawlerPipeline:
    def open_spider(self, spider):
        # Create base directory for output
        domain = urlparse(spider.start_urls[0]).netloc
        self.base_dir = f"data/{domain}"
        self.markdown_dir = f"{self.base_dir}/markdown"

        # Create directories
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.markdown_dir, exist_ok=True)

        # Init data stores
        self.items = []
        self.file = open(f"{self.base_dir}/website_data.json", "w", encoding="utf-8")

        # Create CSV for summary data
        self.csv_file = open(
            f"{self.base_dir}/website_summary.csv", "w", newline="", encoding="utf-8"
        )
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(["URL", "Title", "Links Count", "Markdown File"])

    def close_spider(self, spider):
        # Save all data to JSON
        json.dump(self.items, self.file, indent=4, ensure_ascii=False)
        self.file.close()
        self.csv_file.close()

        # Create main index file
        with open(f"{self.base_dir}/index.md", "w", encoding="utf-8") as index_file:
            index_file.write(
                f"# Website Content Index: {spider.allowed_domains[0]}\n\n"
            )
            index_file.write(f"Total pages scraped: {len(self.items)}\n\n")

            # Sort pages alphabetically by URL
            sorted_items = sorted(self.items, key=lambda x: x["url"])

            # Group by URL path
            path_groups = {}
            for item in sorted_items:
                path = urlparse(item["url"]).path.split("/")
                if len(path) > 1:
                    main_path = path[1] if path[1] else "root"
                else:
                    main_path = "root"

                if main_path not in path_groups:
                    path_groups[main_path] = []

                path_groups[main_path].append(item)

            # Write index by group
            for group, pages in sorted(path_groups.items()):
                index_file.write(f"## {group}\n\n")
                for page in pages:
                    file_path = f"markdown/{self.get_filename(page['url'])}"
                    index_file.write(
                        f"- [{page['title']}]({file_path}) - {page['url']}\n"
                    )
                index_file.write("\n")

        print(f"Crawling completed. Saved {len(self.items)} pages.")
        print(f"Results saved in {self.base_dir}/")

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.items.append(item_dict)

        # Generate filename
        filename = self.get_filename(item_dict["url"])
        markdown_path = f"{self.markdown_dir}/{filename}"

        # Save as markdown file
        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(item_dict["markdown_content"])

        # Add to CSV summary
        self.csv_writer.writerow(
            [
                item_dict["url"],
                item_dict["title"],
                item_dict["links_count"],
                markdown_path,
            ]
        )

        return item

    def get_filename(self, url):
        """Generate a filename from URL"""
        parsed = urlparse(url)
        path = parsed.path

        # Handle the homepage and URLs with no path
        if not path or path == "/":
            return "index.md"

        # Remove the leading slash and any file extension
        path = path.lstrip("/")
        path = re.sub(r"\.\w+$", "", path)

        # Convert to slug
        path = re.sub(r"[^a-zA-Z0-9/]", "_", path)

        # Replace slashes with dashes for the filename
        filename = path.replace("/", "-")

        # Add .md extension
        if not filename.endswith(".md"):
            filename += ".md"

        return filename
