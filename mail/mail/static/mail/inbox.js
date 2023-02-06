document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener("submit", send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mailtext-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// TODO: Make the emails to light up when you set the mouse on them
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#mailtext-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Send the request to the server to get the mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      // Create the table element
      let email_table = document.createElement('table');

      // For each email in the json object, insert a row on the table
      emails.forEach(function(email) {
        // Create the container for the email
        let email_element = email_table.insertRow();      

        // Set HTML text depending on the inbox
        console.log(email)
        if (mailbox == "sent") {
          email_element.innerHTML = `<td><strong>To:</strong> ${email.recipients[0]}</td>`;
        } else {
          email_element.innerHTML = `<td><strong>From:</strong> ${email.sender}</td>`;
        }
        email_element.innerHTML += `<td><strong>Subject:</strong> ${email.subject}</td>`;
        email_element.innerHTML += `<td style="text-align:right">${email.timestamp}</td>`;

        // Add the event to make the email clickable
        email_element.addEventListener('click', function() {
          // Mark email as read
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              console.log("The email was read");
          });

          // Show the email view
          show_mail(email);
        });

        // Add email to the emails-view
        document.querySelector('#emails-view').append(email_table);
      });
  });

}

function show_mail(email) {

  // Show mailtext view and hide the others
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#mailtext-view').style.display = 'block'
  document.querySelector('#compose-view').style.display = 'none';

  // Get the mailview element and create needed ones to be added
  let mailview = document.querySelector('#mailtext-view');
  let subject_element = document.createElement('h3');
  let from_element = document.createElement('p');
  let to_element = document.createElement('p');
  let timestamp_element = document.createElement('p');
  let body_element = document.createElement('p');

  // Clear view before adding anything
  mailview.innerHTML = '';

  // Fill each HTML element with the data
  subject_element.innerHTML = `${email.subject}`;
  from_element.innerHTML = `<strong>From:</strong> ${email.sender}`;
  to_element.innerHTML = `<strong>To:</strong> ${email.recipients[0]}`;
  timestamp_element.innerHTML = `<strong>Timestampt:</strong> ${email.timestamp}`;
  body_element.innerHTML = `${email.body}`;

  // Append to the view
  mailview.append(subject_element);
  mailview.append(from_element);
  mailview.append(to_element);
  mailview.append(timestamp_element);
  mailview.append(document.createElement('hr'));
  mailview.append(body_element);
}

function send_mail() {
  // Avoids the template from changing to the original one
  //event.preventDefault();

  // Get values from the form
  let recipients = document.querySelector("#compose-recipients").value;
  let subject = document.querySelector("#compose-subject").value;
  let body = document.querySelector("#compose-body").value;
  
  /*
    Send a post request to the /emails API implemented by the course.
    The body of the method is a conversion from JavaScript object to JSON
    of the variables got above
  */
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
      // Print result
      console.log(result);
  });
}