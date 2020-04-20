document.addEventListener('DOMContentLoaded', function() {
    

    const profileUsername = document.querySelector('#profile-username').innerHTML;
    load_posts('profile', profileUsername)

    // Follow Logic
    if (document.querySelector('#follow') !== null) {
        document.querySelector('#follow').onsubmit = () => {
            
            const following = document.querySelector('#following');
            const profileUsername = document.querySelector('#profile-username').innerHTML;
            const token = Cookies.get('csrftoken');
        
            // Update follow status with PUT
            fetch(`/profile/${profileUsername}`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': token
                },
                body: JSON.stringify({
                    following: following.value
                })
            })
            .then(response => {
                console.log(response)
                //Update page with new follower count
                if (response.status == 204) {
                    const followers = document.querySelector('#followers');
                    if (following.value == 'False') {
                        document.querySelector('#follow-btn').value = "Unfollow";
                        followers.innerHTML++;
                        following.value = 'True';
                    } else {
                        document.querySelector('#follow-btn').value = "Follow"
                        followers.innerHTML--;
                        following.value = 'False';
                    }
                }
            })
            return false;
        }
    }  
  });
