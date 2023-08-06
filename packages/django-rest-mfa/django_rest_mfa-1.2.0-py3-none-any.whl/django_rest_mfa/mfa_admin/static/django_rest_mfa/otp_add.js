registerTOTPStart();
const form = document.getElementById('otp_form');
form.onsubmit = function(event) {
  registerTOTPFinish(event.target.elements.answer.value, event.target.elements.secret_key.value);
  return false;
}