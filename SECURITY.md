# Security Policy

## Supported Versions

This project is under active development. Security updates will be provided for the latest version.

## Reporting a Vulnerability

**Do not open public issues for security vulnerabilities.**

If you discover a security vulnerability, please email the project maintainers with:
- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact

## Security Considerations

### Usage Warnings

This tool is designed for legitimate web scraping purposes. Users are responsible for:

- Respecting website Terms of Service and robots.txt
- Complying with local laws and regulations
- Not using this tool for unauthorized access or illegal activities
- Handling scraped data responsibly and with respect to privacy laws (GDPR, CCPA, etc.)

### Known Limitations

- Cloudflare and similar anti-bot systems may block requests
- Some websites explicitly prohibit automated scraping
- Rate limiting should always be considered to avoid overloading target servers
- Playwright headless browser may use significant system resources

### Best Practices

1. **Always respect robots.txt** and website scraping policies
2. **Implement rate limiting** to avoid overwhelming servers
3. **Use User-Agent headers** appropriately
4. **Handle errors gracefully** and respect retry limits
5. **Store credentials securely** if authentication is required
6. **Monitor for changes** in target website structure
7. **Cache results** when possible to reduce requests

## Dependency Security

This project uses several third-party libraries. Regular updates are recommended to maintain security. Monitor:
- FastAPI security updates
- Playwright security patches
- cloudscraper version updates
- curl_cffi vulnerability reports

## Recommended Production

- Host locally or behind a secure proxy
- Consider CloudFlare Tunnels for production deployment


## License

This project is licensed under GPLv3. See LICENSE file for details.

## Communication

Email: info@yigitdev.net

Discord: epicboy_9000s (YiğitDEVVariable)

Discord server: https://discord.gg/qA7trgxdVD