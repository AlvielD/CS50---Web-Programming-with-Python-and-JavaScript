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
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// TODO: Modify the HTML table so you can see "From" on received emails and "To" on sent ones
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Send the request to the server to get the mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

      // Create an HTML string for the table
      let tableHTML = "<table>";
      emails.forEach(function(email) {
          tableHTML += 
            "<tr><td><strong>From:</strong> " + email.recipients[0] + "</td><td><strong>Subject:</strong> " + email.subject + "</td></tr>" +
            "<tr><td colspan=\"2\">" + email.body + "</td></tr>";
      });
      tableHTML += "</table>";

      // Insert the HTML into the page
      document.querySelector("#emails-view").innerHTML = tableHTML;
  });

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