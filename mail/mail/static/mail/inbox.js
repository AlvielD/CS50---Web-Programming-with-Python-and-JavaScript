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

/**
 * Show the compose view to send emails. Before, it removes the content
 * of the forms' fields.
 */
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
/**
 * Load the view of the mails list depending on which mailbox
 * we are requesting
 * @param {string} mailbox - the mailbox to be loaded 
 */
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

      // For each email in the json object, add it to the mails table
      emails.forEach(function(email) {
        // Load the mail on the mails list
        load_mail(mailbox, email_table, email);
      });
  });
}

/**
 * This function loads a single mail in the mails listing that
 * should be shown in the respective inbox.
 * @param {string} mailbox - mailbox in which we are adding the mail
 * @param {HTMLElement} email_table - the table that will contain all the emails
 * @param {HTMLElement} email - mail object to be added to the list
 */
function load_mail(mailbox, email_table, email) {

  // Create the container for the email
  let email_element = email_table.insertRow(); // Row element of the table (will contain the email)
  let arc_button = document.createElement('button');  // Button to archive or unarchive email

  // Set HTML text depending on the mailbox
  if (mailbox == "sent") {
    // If the mailbox is "sent" -> set the field to "To:"
    email_element.innerHTML = `<td><strong>To:</strong> ${email.recipients[0]}</td>`;
  } else {
    // If the mailbox is "inbox" or "archive" -> set to "From:"
    email_element.innerHTML = `<td><strong>From:</strong> ${email.sender}</td>`;
  }

  // Set background color depending if its read or not
  // by default is gray = read, so if its not read, set it to white
  if (!email.read) {
    email_element.style.backgroundColor = "white";
  }

  // Add the rest of the information to the inbox email (subject and timestamp)
  email_element.innerHTML += `<td><strong>Subject:</strong> ${email.subject}</td>`;
  email_element.innerHTML += `<td style="text-align:right">${email.timestamp}</td>`;

  // EVENT TO MAKE MAIL CLICKABLE
  email_element.addEventListener('click', function() {
    // Mark email as read
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })

    // Show email view
    show_mail(email);
  });

  // ADD AN EXTRA BUTTON IF WE ARE NOT IN THE "SENT" MAILBOX
  if (mailbox != "sent") {
    // Adjust some properties of the button and add it to the email
    // Set the button depending if you can archive it or not
    let cell_button = email_element.insertCell(); // Add new cell to the row
    let archived_mail = false;

    cell_button.style.textAlign = "center";       // Set button in the center of the cell
    arc_button.classList = "btn btn-sm btn-outline-primary";

    // Set the text of the button depending in which mailbox are we
    if (mailbox == "inbox") {
      arc_button.innerHTML = 'archive'; // Text displayed on button
      archived_mail = true              // If we want to archive it, set this to true
    } else {
      arc_button.innerHTML = 'unarchive';// Text displayed on the button
      // Here we don't set "archived_mail" since it is to false by default
    }
    cell_button.appendChild(arc_button);

    // EVENT TO MAKE ARCHIVE BUTTON FUNCTIONABLE
    arc_button.addEventListener('click', function(event) {
      event.stopPropagation();
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: archived_mail
        })
      })
      
      // Refresh the mailbox
      // Delay the refreshing for 5ms so it has time to update changes
      setTimeout(load_mailbox, 5, mailbox);
    });
  }

  // APPEND MAIL TO THE TABLE (FINALLY)
  document.querySelector('#emails-view').append(email_table);
}

/**
 * Shows a full view of the email with all its needed fields like
 * "From", "To", "Timestamp", ...
 * @param {HTMLElement} email - email to be shown in the view
 */
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

/**
 * Take the values from the form of the compose view and send a 
 * POST request to the server. 
 */
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