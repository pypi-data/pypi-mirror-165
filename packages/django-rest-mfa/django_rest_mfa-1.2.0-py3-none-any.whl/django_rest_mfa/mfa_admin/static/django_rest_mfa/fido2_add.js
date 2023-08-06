const form = document.getElementById('fido2_form');
form.onsubmit = function(event) {
  registerMFA(event.target.elements.name.value);
  return false;
}
