function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

let userKeysList = "/mfa/user_keys/";
let authenticateFIDO2URL = "/mfa/authenticate/fido2/";
let authenticateTOTPURL = "/mfa/authenticate/totp/";

const mfaURLProvider = document.getElementById('mfa-url-provider');
if (mfaURLProvider) {
  userKeysList = mfaURLProvider.dataset.user_keys_list;
  authenticateFIDO2URL = mfaURLProvider.dataset.authenticate_fido2;
  authenticateTOTPURL = mfaURLProvider.dataset.authenticate_totp;
}

function registerMFA(name) {
  fetch(userKeysList + "fido2/", {
    headers: { Accept: "application/octet-stream" },
  })
    .then((response) => {
      if (response.ok) {
        return response.arrayBuffer();
      }
      throw new Error("Error getting registration data!");
    })
    .then(CBOR.decode)
    .then((options) => {
      return navigator.credentials.create(options);
    })
    .then((attestation) => {
      return fetch(userKeysList + "fido2/", {
        method: "POST",
        headers: {
          "Content-Type": "application/cbor",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: CBOR.encode({
          attestationObject: new Uint8Array(
            attestation.response.attestationObject
          ),
          clientDataJSON: new Uint8Array(attestation.response.clientDataJSON),
          name,
        }),
      });
    })
    .then(() => {
      window.location.href = "../";
    })
    .catch((err) => {
      alert(err);
    });
}

function authenticateFido2() {
  fetch(authenticateFIDO2URL, {
    headers: { Accept: "application/octet-stream" },
  })
    .then((response) => {
      if (response.ok) {
        return response.arrayBuffer();
      }
      throw new Error("Error getting auth data!");
    })
    .then(CBOR.decode)
    .then((options) => {
      return navigator.credentials.get(options);
    })
    .then((assertion) => {
      return fetch(authenticateFIDO2URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/cbor",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: CBOR.encode({
          credentialId: new Uint8Array(assertion.rawId),
          authenticatorData: new Uint8Array(
            assertion.response.authenticatorData
          ),
          clientDataJSON: new Uint8Array(assertion.response.clientDataJSON),
          signature: new Uint8Array(assertion.response.signature),
        }),
      });
    })
    .then(() => checkForRemember())
    .then(() => redirectToNext());
}

function checkForRemember() {
  const remember = document.getElementById("remember").checked;
  if (remember) {
    const trustedDeviceURL = "/mfa/user_keys/trusted_device/";
    return fetch(trustedDeviceURL)
      .then((response) => response.json())
      .then((userKey) => {
        const expire = new Date();
        expire.setTime(expire.getTime() + 1000 * 86400 * 180); // 180 days
        document.cookie = `remember_device_key=${userKey.key}; expires=${expire}; path=/`;
        return fetch(trustedDeviceURL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify({key: userKey.key})
        })
    })
  }
  return new Promise();
}

function redirectToNext() {
  const urlParams = new URLSearchParams(window.location.search);
  const nextParam = urlParams.get("next");
  if (nextParam) {
    window.location = nextParam;
  } else {
    window.location = "../../";
  }
}

function registerTOTPStart() {
  fetch(userKeysList + "totp/")
    .then((response) => response.json())
    .then((data) => {
      const provisioningURI = data.provisioning_uri;
      QRCode.toCanvas(document.getElementById("canvas"), provisioningURI);
      document.getElementById("secret_key").value = data.secret_key;
    });
}

function registerTOTPFinish(answer, secret_key) {
  const data = { answer, secret_key };
  fetch(userKeysList + "totp/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      window.location = "../";
    });
}

function authenticateTOTP(otp) {
  data = { otp };
  fetch(authenticateTOTPURL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.ok) {
        checkForRemember().then(() => redirectToNext())
      } else {
        throw new Error("Invalid OTP")
      }
    })
    .catch((err) => {
      alert(err);
    });
}
