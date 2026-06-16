import json
import re
import urllib.request
import urllib.error


def _extract_shortcode(url: str):
    m = re.search(r'instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)', url)
    return m.group(1) if m else None


def _fetch_via_graphql(shortcode: str):
    api_url = f'https://www.instagram.com/api/v1/media/{shortcode}/info/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
        'X-IG-App-ID': '936619743392459',
        'Accept': '*/*',
    }
    embed_url = f'https://www.instagram.com/p/{shortcode}/embed/captioned/'
    req = urllib.request.Request(embed_url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
    })
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode('utf-8', errors='ignore')

    candidates = re.findall(r'"video_url":"([^"]+)"', html)
    if not candidates:
        candidates = re.findall(r'<meta property="og:video" content="([^"]+)"', html)
    if not candidates:
        candidates = re.findall(r'property="og:video:secure_url" content="([^"]+)"', html)

    if candidates:
        video_url = candidates[0].encode().decode('unicode_escape').replace('\\/', '/')
        thumb = re.findall(r'"display_url":"([^"]+)"', html)
        thumb_url = thumb[0].encode().decode('unicode_escape').replace('\\/', '/') if thumb else None
        return {'video_url': video_url, 'thumbnail': thumb_url}
    return None


def handler(event: dict, context) -> dict:
    '''
    Извлекает прямую ссылку на видео из Instagram по ссылке на пост или Reels.
    Args: event с httpMethod, body (JSON со ссылкой url)
    Returns: HTTP-ответ с прямой ссылкой на видео для скачивания
    '''
    method = event.get('httpMethod', 'GET')
    cors = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json',
    }

    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': cors, 'body': ''}

    if method != 'POST':
        return {'statusCode': 405, 'headers': cors, 'body': json.dumps({'error': 'Method not allowed'})}

    try:
        body = json.loads(event.get('body') or '{}')
    except Exception:
        body = {}

    url = (body.get('url') or '').strip()
    if not url:
        return {'statusCode': 400, 'headers': cors, 'body': json.dumps({'error': 'Укажите ссылку на видео'})}

    shortcode = _extract_shortcode(url)
    if not shortcode:
        return {'statusCode': 400, 'headers': cors, 'body': json.dumps({'error': 'Это не похоже на ссылку Instagram'})}

    try:
        result = _fetch_via_graphql(shortcode)
    except urllib.error.URLError:
        result = None
    except Exception:
        result = None

    if not result or not result.get('video_url'):
        return {
            'statusCode': 422,
            'headers': cors,
            'body': json.dumps({'error': 'Не удалось получить видео. Возможно, пост приватный или Instagram временно заблокировал доступ.'}),
        }

    return {
        'statusCode': 200,
        'headers': cors,
        'body': json.dumps({
            'video_url': result['video_url'],
            'thumbnail': result.get('thumbnail'),
            'shortcode': shortcode,
        }),
    }
