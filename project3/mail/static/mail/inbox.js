document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(rec='',sub='',bod='') {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = rec;
  document.querySelector('#compose-subject').value = sub;
  document.querySelector('#compose-body').value = bod;

  //When email is sent, POST to API
  document.querySelector('#compose-form').onsubmit = () => {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
      })
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
    });

    load_mailbox('sent');
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  ///////////Figure out better option for this
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><hr>`;

  // GET emails to list 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(format_email);
    console.log(emails);
  });

  function format_email(email) {
    const div = document.createElement('div');
    div.className = "email";
    div.innerHTML = `${email['sender']}  ${email['subject']}  ${email['timestamp']}`;
    div.addEventListener('click', function() {
      load_email(email['id'])
    });
    document.querySelector('#emails-view').append(div);
  }

}

function load_email(email_id) {

  //Show email hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  document.querySelector('#email-view').innerHTML = '';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })


    const div = document.createElement('div');
    const reply = document.createElement('button');
    reply.className = "btn btn-sm btn-outline-primary";
    reply.innerHTML = "Reply";
    reply.addEventListener('click', function() {
      console.log("REPLY")
      rec = email['sender']
      sub = `Re: ${email['subject']}`
      bod = `\n\n---------------\nOn ${email['timestamp']} ${email['sender']} wrote:\n${email['body']}`
      compose_email(rec,sub,bod)
    });

    const archive = document.createElement('button');
    archive.className = "btn btn-sm btn-outline-primary";
    const status = true//email['archived'];
    text = 'Archive'
    if (status) {
      text = 'Unarchive'
    } 
    archive.innerHTML = text;
    archive.addEventListener('click', function() {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !status
        })
      })
      console.log(!status)
      console.log("ARCHIVE")
      load_mailbox('archive')
    });

    const read = document.createElement('button');
    read.className = "btn btn-sm btn-outline-primary";
    read.innerHTML = "Mark Unread";
    read.addEventListener('click', function() {
      fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: false
        })
      })
      load_mailbox('inbox')
    });
    
    
    div.innerHTML += `<b>From: </b>${email['sender']}`;
    div.innerHTML += `<br><b>To: </b>${email['recipients']}`;
    div.innerHTML += `<br><b>Subject: </b>${email['subject']}`;
    div.innerHTML += `<br><b>Timestamp: </b>${email['timestamp']}<hr>`;
    div.innerHTML += `${email['body']}<hr>`;
    div.append(reply);
    div.append(archive);
    div.append(read);
    document.querySelector('#email-view').append(div);
  })

}