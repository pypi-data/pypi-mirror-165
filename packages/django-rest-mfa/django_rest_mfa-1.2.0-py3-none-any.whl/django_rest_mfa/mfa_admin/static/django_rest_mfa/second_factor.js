authenticateFido2();

const form = document.getElementById('otp_form');
form.onsubmit = function(event) {
  authenticateTOTP(event.target.elements.otp.value);
  return false;
}
