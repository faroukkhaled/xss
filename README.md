This project is a Python script designed to search for XSS vulnerabilities in websites. It collects links from the target site and tests them using specific payloads to check if they are vulnerable to XSS attacks. The script uses libraries like requests and BeautifulSoup to request and parse pages, and it utilizes threading to speed up the testing process across different parameters. In the end, it gathers the results and saves them to a text file for review.

Key Functions of the Script:

    Load Payloads: The script loads payloads from a given file to use them in the testing process.

    Extract Links: It collects all internal links from a page using BeautifulSoup.

    Test Payloads: It tests each link to see if it is vulnerable to XSS by modifying the parameters with the payloads.

    Parallel Testing: The script uses threading to speed up the testing process by running multiple threads simultaneously.

    Save Results: Finally, it collects the results and saves them to a file called xss_results.txt.

Script Setup:

    The user can enter the target site’s URL and the payload wordlist file.

    The script automatically finds links within the page, and if no links are found, it allows the user to either manually enter links or load them from a file.

    After testing, the results are saved in a text file.
