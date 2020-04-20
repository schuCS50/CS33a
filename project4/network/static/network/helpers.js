// Function to load all posts
function load_posts(type, user) {
    document.querySelector('#posts').innerHTML = '';
    // GET all posts
    fetch(`/posts?type=${type}&username=${user}`)
    .then(response => {
        return response.json();
    })
    .then(posts => {
        posts.forEach(post => create_post(post, type, user));
    });
}

// Function to create individual post div
function create_post(post, type, user) {
    const div = document.createElement('div');
    div.id = `post-${post['id']}`;
    document.querySelector('#posts').append(div);
    // Format the post
    format_post(post, type, user);
}

//Function to format a specific post and handle changes
function format_post(post, type, user) {
    //Get CSRF token from cookie
    const token = Cookies.get('csrftoken');

    //Get the post's div
    const div = document.querySelector(`#post-${post['id']}`);
    div.innerHTML = '';
    div.className = 'row';

    //Create basic elements of post
    const creator = document.createElement('a');
    const text = document.createElement('div');
    const likes = document.createElement('div');
    const props = document.createElement('div');

    creator.innerHTML = post['creator'];
    creator.href = `/profile/${post['creator']}`;
    props.append(creator);
    props.append(` on ${post['createdTimestamp']}:`);

    text.innerHTML = post['post'];
    likes.innerHTML = `Likes: ${post['likes']} `;

    props.className = 'col-4';
    text.className = 'col-4';
    likes.className = 'col-4';

    div.append(props);
    div.append(text);
    div.append(likes);

    //Logged in Options
    if (document.querySelector('#username') !== null) {
        username = document.querySelector('#username').innerHTML;

        // Like Button Logic
        const likeBtn = document.createElement('button');
        likeBtn.className = "btn btn-sm btn-outline-primary";
        // Determine like status
        const liked = post['like'];
        let btnText = 'Like';
        if (liked) {
            btnText = 'Unlike'
        }
        likeBtn.innerHTML = btnText;
        // Add action to button
        likeBtn.addEventListener('click', function() {
            //Use PUT to update likes
            fetch('/posts', {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': token
                },
                body: JSON.stringify({
                    post: post['id'],
                    liked: !liked
                })
            })
            .then(response => {
                console.log(response);
                //Reload the post with updated likes
                fetch(`/posts?type=single&username=&postId=${post['id']}`)
                .then(response => {
                    console.log(response);
                    return response.json();
                })
                .then(posts => {
                    posts.forEach(post => format_post(post, type, user));
                })
            })
        });

        //Edit Button Logic
        if (username == post['creator']) {
            const edit = document.createElement('button');
            edit.className = "btn btn-sm btn-outline-primary";
            edit.innerHTML = "Edit";
            //Edit logic
            edit.addEventListener('click', function() {
                //Edit elements
                const div = document.querySelector(`#post-${post['id']}`);
                div.innerHTML = '';
                const textarea = document.createElement('textarea');
                textarea.required;
                textarea.class = 'form-control';
                textarea.id = 'edit-text';
                textarea.innerHTML = post['post'];
                const save = document.createElement('button');
                save.className = "btn btn-primary";
                save.innerHTML = "Save";
                //When we save post, use POST with post id to update post
                save.addEventListener('click', function () {
                    const postText = document.querySelector('#edit-text').value;
                    fetch('/posts', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': token
                        },
                        body: JSON.stringify({
                            postType: 'new',
                            post: post['id'],
                            postText: postText
                        })
                    })
                    .then(response => {
                        console.log(response);
                        // Reload the post
                        fetch(`/posts?type=single&username=&postId=${post['id']}`)
                        .then(response => {
                            console.log(response);
                            return response.json();
                        })
                        .then(posts => {
                            posts.forEach(post => format_post(post, type, user));
                        })
                    })
                });

                div.append(textarea);
                div.append(save);
                console.log("append");
            });

            props.append(edit);
        }

        likes.append(likeBtn);
    }
}

