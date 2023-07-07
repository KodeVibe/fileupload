// Get the CSRF token from the cookie
function getCSRFToken() {
    const cookieValue = document.cookie.match(/csrftoken=([\w-]+)/);
    return cookieValue ? cookieValue[1] : '';
  }
  
  function generateSignedURL(userInputId) {
    const csrftoken = getCSRFToken();
  
    $.ajax({
      url: '/generate-signed-url/',
      method: 'POST',
      headers: { 'X-CSRFToken': csrftoken }, // Include the CSRF token in the request headers
      data: { user_input_id: userInputId },
      dataType: 'json',
      success: function(response) {
        if (response.signed_url) {
          // Redirect the user to the signed URL to initiate file download
          window.location.href = response.signed_url;
        } else {
          // Handle the error response, e.g., display an error message
          console.log(response.error);
        }
      },
      error: function(xhr, status, error) {
        // Handle the AJAX error, e.g., display an error message
        console.log(error);
      }
    });
  }
  