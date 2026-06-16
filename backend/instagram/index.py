import json
import re
import instaloader


CORS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
}


def _extract_shortcode(url: str):
    m = re.search(r'instagram\.com/(?:reel|reels|p|tv)/([A-Za-z0-9_-]+)', url)
    return m.group(1) if m else None


def _get_video_info(shortcode: str) -> dict:
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    if not post.is_video:
        raise ValueError('Этот пост не содержит видео')
    return {
        'video_url': post.video_url,
        'thumbnail': post.url,
    }


def handler(event: dict, context) -> dict:
    """
    Извлекает прямую ссылку на видео из Instagram через instaloader.
    POST body: {"url": "https://instagram.com/reel/..."}
    """
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS, 'body': ''}

    if event.get('httpMethod') != 'POST':
        return {'statusCode': 405, 'headers': CORS, 'body': json.dumps({'error': 'Method not allowed'})}

    try:
        body = json.loads(event.get('body') or '{}')
    except Exception:
        body = {}

    url = (body.get('url') or '').strip()
    if not url:
        return {'statusCode': 400, 'headers': CORS, 'body': json.dumps({'error': 'Укажите ссылку на видео'})}

    shortcode = _extract_shortcode(url)
    if not shortcode:
        return {'statusCode': 400, 'headers': CORS, 'body': json.dumps({'error': 'Это не похоже на ссылку Instagram'})}

    try:
        info = _get_video_info(shortcode)
    except instaloader.exceptions.LoginRequiredException:
        return {'statusCode': 403, 'headers': CORS, 'body': json.dumps({'error': 'Пост приватный или требует авторизации'})}
    except instaloader.exceptions.InstaloaderException as e:
        return {'statusCode': 422, 'headers': CORS, 'body': json.dumps({'error': f'Не удалось получить видео: {str(e)}'})}
    except ValueError as e:
        return {'statusCode': 422, 'headers': CORS, 'body': json.dumps({'error': str(e)})}
    except Exception:
        return {'statusCode': 500, 'headers': CORS, 'body': json.dumps({'error': 'Ошибка сервера, попробуйте позже'})}

    return {
        'statusCode': 200,
        'headers': CORS,
        'body': json.dumps({
            'video_url': info['video_url'],
            'thumbnail': info.get('thumbnail'),
        }),
    }