document.addEventListener('DOMContentLoaded', function() {
    load_posts('all');

    // Add New Post
    if (document.querySelector('#new-post') !== null) {
        document.querySelector('#new-post').onsubmit = () => {

            const postText = document.querySelector('#post-body').value;
            const token = Cookies.get('csrftoken');

            // Use POST method to create new post
            fetch('/posts', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': token
                },
                body: JSON.stringify({
                    postType: 'new',
                    postText: postText
                })
            })
            .then(response => {
                console.log(response)
                // Reload posts
                document.querySelector('#post-body').value = '';
                document.querySelector('#posts').innerHTML = '';
                load_posts('all');
            })
            return false;
        }
    }
});

