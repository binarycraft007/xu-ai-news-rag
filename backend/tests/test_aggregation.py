from unittest.mock import patch, MagicMock
from io import BytesIO
from src.backend.models import db, User, RssFeed
from src.backend.services.aggregation import run_aggregation_for_all_users
import feedparser

def test_run_aggregation_for_all_users_fetches_full_article(app):
    """
    Tests that the RSS aggregation service attempts to fetch the full article
    content and uses it instead of the summary.
    """
    # Arrange: Create a mock feed from the provided rss.xml file
    with open('tests/testdata/rss.xml', 'rb') as f:
        rss_content = f.read()
    
    parsed_feed = feedparser.parse(rss_content)
    
    with app.app_context():
        db.session.query(RssFeed).delete()
        db.session.query(User).delete()
        db.session.commit()

        user = User(username='testuser')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        feed = RssFeed(user_id=user.id, url='http://example.com/rss.xml')
        db.session.add(feed)
        db.session.commit()
        user_id = user.id

    # Mock HTML content that is significantly longer than any summary
    mock_html = """
    <html>
        <head><title>A Long Article</title></head>
        <body>
            <article>
                <h1>This is a Detailed Article Title to Ensure Content Length</h1>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                <p>Curabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida.</p>
                <p>Duis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam. Maecenas fermentum consequat mi. Donec fermentum.</p>
            </article>
        </body>
    </html>
    """
    mock_response = MagicMock()
    mock_response.content = mock_html.encode('utf-8')
    mock_response.raise_for_status.return_value = None

    with patch('src.backend.services.aggregation.feedparser.parse', return_value=parsed_feed) as mock_parse, \
         patch('src.backend.services.aggregation.requests.get', return_value=mock_response) as mock_get, \
         patch('src.backend.services.aggregation.add_document') as mock_add_document:
        
        with app.app_context():
            run_aggregation_for_all_users()

        # Assert
        assert mock_get.call_count == len(parsed_feed.entries)
        first_get_call_args = mock_get.call_args_list[0][0]
        assert first_get_call_args[0] == parsed_feed.entries[0].link

        first_entry = parsed_feed.entries[0]
        # This is the text we expect to be parsed from the mock HTML
        expected_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\nDuis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\nCurabitur pretium tincidunt lacus. Nulla gravida orci a odio. Nullam varius, turpis et commodo pharetra, est eros bibendum elit, nec luctus magna felis sollicitudin mauris. Integer in mauris eu nibh euismod gravida.\nDuis ac tellus et risus vulputate vehicula. Donec lobortis risus a elit. Etiam tempor. Ut ullamcorper, ligula eu tempor congue, eros est euismod turpis, id tincidunt sapien risus a quam. Maecenas fermentum consequat mi. Donec fermentum."
        
        first_call_args, _ = mock_add_document.call_args_list[0]
        assert first_call_args[0] == user_id
        
        file_obj = first_call_args[1]
        file_content = file_obj.stream.read().decode('utf-8')
        
        # Check that the parsed text is present in the final content
        assert expected_text in file_content
        assert first_entry.title in file_content
