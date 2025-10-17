# AllScrape Backend - Open Source

AllScrape Backend is an open-source web scraping and LLM-ready content extraction API built with FastAPI.

## License

This project is licensed under the **GNU General Public License v3 (GPLv3)**.

### What This Means

- ✅ You can use, modify, and distribute this software freely
- ✅ You must provide source code access to your modifications
- ✅ Derivative works must use the same GPLv3 license
- ✅ You must include the original license and copyright notice
- ✅ No warranty is provided

For full license details, see [LICENSE](LICENSE) and [GPLv3 Legal Text](https://www.gnu.org/licenses/gpl-3.0.html)

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

All contributions are licensed under GPLv3.

## Security

Please report security vulnerabilities responsibly. See [SECURITY.md](SECURITY.md) for details.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Features

- 🔍 Single URL scraping with multiple output formats
- 🌐 Web search with automatic result scraping
- 🤖 LLM-ready output format
- 📊 Metadata extraction
- ⚡ Fast async processing
- 🧹 Clean text extraction

## Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium
python -m uvicorn app.main:app --reload
```

## Documentation

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Support

For issues, questions, or suggestions, please open a GitHub issue.

## Acknowledgments

Built with:
- FastAPI
- BeautifulSoup4
- Trafilatura
- Playwright
- curl_cffi
- cloudscraper
