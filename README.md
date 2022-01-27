# url2kindle

A simple web application to send web articles (e.g. blog posts) to a Kindle device.

Given a URL, url2kindle will:

1. Use [mercury-parser](https://github.com/postlight/mercury-parser) to download a simplified (reader) view of the webpage.
2. Embed any image content as base64 (so that images can be viewed on the Kindle).
3. Send the content as an HTML file to an email address (i.e. the email address for the kindle).

## Environment Variables

| Name                | Required? | Value                                                                                    |
| ------------------- | --------- | ---------------------------------------------------------------------------------------- |
| KINDLE_APPRISE_URL  | Yes       | An [apprise](https://pypi.org/project/apprise/) URL to send an email to your Kindle. Email platform must support attachments. |
| ADMIN_APPRISE_URL   | Yes       | An [apprise](https://pypi.org/project/apprise/) URL to send error notifications to an admin.                                  |
| BASIC_AUTH_USERNAME | Yes       | Basic auth username.                                                                     |
| BASIC_AUTH_PASSWORD | Yes       | Basic auth password.                                                                     |
| PARSER_PATH         | No        | The path to mercury-parser. Defaults to "mercury-parser".                                |

## Example Post

POST /

```json
{
  "url": "https://en.wikipedia.org/wiki/Lorem_ipsum"
}
```
