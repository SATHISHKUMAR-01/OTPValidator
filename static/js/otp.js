function movetoNext(prevField, current, nextFieldID) {
  if (current.value.length >= current.maxLength) {
    document.getElementById(nextFieldID).focus();
  } else {
    document.getElementById(prevField).focus();
  }
}

function changeBorder(id, current) {
  if (current.value.length < 1) {
    document.getElementById(id).style.border = "3px solid red";
  } else {
    document.getElementById(id).style.border = "3px solid darkgreen";
  }
}

var attemptsVal = document.getElementById("attempts").innerHTML;
var attempts = document.getElementById("attempts");

if (attemptsVal === "3") {
  attempts.style.color = "green";
  attempts.style.fontWeight = "bold";
} else if (attemptsVal === "2") {
  attempts.style.color = "orange";
  attempts.style.fontWeight = "bold";
} else if (attemptsVal == "1") {
  attempts.style.color = "red";
  attempts.style.fontWeight = "bold";
}
