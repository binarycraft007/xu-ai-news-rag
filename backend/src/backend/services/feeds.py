from ..models import db, RssFeed

def get_user_feeds(user_id):
    feeds = RssFeed.query.filter_by(user_id=user_id).all()
    return [{"id": feed.id, "url": feed.url} for feed in feeds]

def add_feed(user_id, url):
    if RssFeed.query.filter_by(user_id=user_id, url=url).first():
        return None # Feed already exists
    feed = RssFeed(user_id=user_id, url=url)
    db.session.add(feed)
    db.session.commit()
    return feed

def delete_feed(user_id, feed_id):
    feed = RssFeed.query.filter_by(id=feed_id, user_id=user_id).first()
    if feed:
        db.session.delete(feed)
        db.session.commit()
        return True
    return False
